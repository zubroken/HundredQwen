"""
讯飞大模型中文语音识别（流式版）WebSocket 服务
基于官方 Demo: 大模型中文语音识别.py
参考接口文档: 接口要求与更多.md
"""
from __future__ import annotations
import os
import sys
import json
import base64
import hashlib
import hmac
import time
import logging
import tempfile
import subprocess
import threading
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

logger = logging.getLogger(__name__)

STATUS_FIRST_FRAME = 0
STATUS_CONTINUE_FRAME = 1
STATUS_LAST_FRAME = 2

# 讯飞语音听写 WebSocket 地址
IAT_URL = "wss://iat.xf-yun.com/v1"


class SpeechService:
    """讯飞大模型中文语音识别（流式版）"""

    def __init__(self, app_id: str, api_key: str, api_secret: str):
        self.APP_ID = app_id
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.ffmpeg_path = self._detect_ffmpeg()

    @property
    def configured(self) -> bool:
        return bool(self.APP_ID and self.API_KEY and self.API_SECRET and self.ffmpeg_path)

    def _detect_ffmpeg(self) -> str:
        """自动探测 ffmpeg 路径"""
        candidates = [
            "ffmpeg",
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
            r"C:\ffmpeg\bin\ffmpeg.exe",
            "/usr/bin/ffmpeg",
            "/usr/local/bin/ffmpeg",
        ]
        for c in candidates:
            try:
                subprocess.run([c, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return c
            except (FileNotFoundError, subprocess.SubprocessError):
                continue
        return ""

    def _build_url(self) -> str:
        """HMAC-SHA256 签名鉴权，返回完整 wss URL
        完全复用官方 Demo 的 create_url() 逻辑"""
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = "host: " + "iat.xf-yun.com" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v1 " + "HTTP/1.1"

        signature_sha = hmac.new(
            self.API_SECRET.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode('utf-8')

        authorization_origin = (
            f'api_key="{self.API_KEY}", algorithm="hmac-sha256", '
            f'headers="host date request-line", signature="{signature_sha}"'
        )
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')

        v = {
            "authorization": authorization,
            "date": date,
            "host": "iat.xf-yun.com"
        }
        return IAT_URL + '?' + urlencode(v)

    def _convert_to_pcm(self, audio_bytes: bytes) -> str:
        """用 ffmpeg 将浏览器 webm/opus 转为 16kHz mono PCM WAV，返回临时文件路径"""
        tmp_in = tempfile.NamedTemporaryFile(suffix=".webm", delete=False)
        tmp_in.write(audio_bytes)
        tmp_in.close()

        tmp_out = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp_out.close()

        subprocess.run([
            self.ffmpeg_path, "-y",
            "-i", tmp_in.name,
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            "-f", "wav",
            tmp_out.name
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        os.unlink(tmp_in.name)
        return tmp_out.name

    def _extract_pcm_data(self, wav_path: str) -> bytes:
        """从 WAV 文件中提取原始 PCM 数据（跳过 44 字节 WAV 头）"""
        with open(wav_path, "rb") as f:
            data = f.read()
        # WAV 头 44 字节，之后全是 PCM raw data
        if len(data) > 44 and data[:4] == b'RIFF':
            return data[44:]
        return data

    def recognize(self, audio_bytes: bytes) -> str:
        """
        对外暴露的主方法：接收浏览器音频 Blob → 返回识别文本
        """
        if not self.configured:
            raise RuntimeError("SpeechService 未正确配置：请检查 .env 中 SPARK_APP_ID/API_KEY/API_SECRET 和 ffmpeg 安装")

        wav_path = self._convert_to_pcm(audio_bytes)
        try:
            pcm_data = self._extract_pcm_data(wav_path)
            return self._run_websocket_recognition(pcm_data)
        finally:
            try:
                os.unlink(wav_path)
            except OSError:
                pass

    def _run_websocket_recognition(self, pcm_data: bytes) -> str:
        """连接讯飞 WebSocket，发送 PCM 数据，收集识别结果"""
        import websocket
        import ssl

        current_text = [""]  # 用 list 包装以便在闭包中修改
        error_msg = []
        done_event = threading.Event()

        def on_message(ws, message):
            try:
                msg = json.loads(message)
                code = msg["header"]["code"]
                if code != 0:
                    error_msg.append(f"讯飞错误码: {code}")
                    ws.close()
                    return
                payload = msg.get("payload")
                if payload and "result" in payload:
                    text_b64 = payload["result"]["text"]
                    decoded = base64.b64decode(text_b64)
                    data = json.loads(decoded)
                    # 拼出本次消息的文本
                    parts = []
                    for word_group in data.get("ws", []):
                        for char_item in word_group.get("cw", []):
                            parts.append(char_item.get("w", ""))
                    this_text = "".join(parts)
                    # 取最长文本（wpgs 模式下后续消息是修正和扩展版本）
                    if this_text and len(this_text) > len(current_text[0]):
                        current_text[0] = this_text
                if msg["header"].get("status") == 2:
                    ws.close()
            except Exception as e:
                error_msg.append(str(e))

        def on_error(ws, error):
            error_msg.append(str(error))

        def on_close(ws, close_code, close_msg):
            done_event.set()

        def on_open(ws):
            def run():
                frame_size = 1280  # 官方规范：1280 字节/帧
                interval = 0.04    # 40ms/帧
                status = STATUS_FIRST_FRAME
                offset = 0

                params = {
                    "domain": "slm",
                    "language": "zh_cn",
                    "accent": "mandarin",
                    "dwa": "wpgs",
                    "result": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "plain"
                    }
                }

                while True:
                    buf = pcm_data[offset:offset + frame_size]
                    offset += frame_size
                    audio_b64 = base64.b64encode(buf).decode('utf-8')

                    if not buf or len(buf) < frame_size:
                        status = STATUS_LAST_FRAME

                    if status == STATUS_FIRST_FRAME:
                        d = {
                            "header": {"status": 0, "app_id": self.APP_ID},
                            "parameter": {"iat": params},
                            "payload": {
                                "audio": {
                                    "audio": audio_b64,
                                    "sample_rate": 16000,
                                    "encoding": "raw"
                                }
                            }
                        }
                        ws.send(json.dumps(d))
                        status = STATUS_CONTINUE_FRAME

                    elif status == STATUS_CONTINUE_FRAME:
                        d = {
                            "header": {"status": 1, "app_id": self.APP_ID},
                            "payload": {
                                "audio": {
                                    "audio": audio_b64,
                                    "sample_rate": 16000,
                                    "encoding": "raw"
                                }
                            }
                        }
                        ws.send(json.dumps(d))

                    elif status == STATUS_LAST_FRAME:
                        d = {
                            "header": {"status": 2, "app_id": self.APP_ID},
                            "payload": {
                                "audio": {
                                    "audio": "",
                                    "sample_rate": 16000,
                                    "encoding": "raw"
                                }
                            }
                        }
                        ws.send(json.dumps(d))
                        break

                    time.sleep(interval)

            threading.Thread(target=run, daemon=True).start()

        try:
            ws_url = self._build_url()
            ws = websocket.WebSocketApp(
                ws_url,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            ws.on_open = on_open

            # 在子线程中运行 WebSocket
            def run_ws():
                ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

            t = threading.Thread(target=run_ws, daemon=True)
            t.start()

            # 等待完成或超时 (65秒，讯飞限制60秒+5秒余量)
            if not done_event.wait(timeout=65):
                ws.close()
                raise TimeoutError("语音识别超时（超过60秒）")

            if error_msg:
                raise RuntimeError("; ".join(error_msg))

            return current_text[0]

        except ImportError:
            raise RuntimeError("请安装 websocket-client: pip install websocket-client")
