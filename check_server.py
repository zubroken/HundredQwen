"""
百问即查 服务状态诊断脚本
用法: python check_server.py
"""
import os
import sys
import subprocess
import time
import json
import csv

PORT = 9010
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
WATCH_DIRS = ["api", "services", "agents", "models", "main.py"]


def windows_netstat_path(env=None):
    system_root = (env or os.environ).get("SystemRoot", r"C:\Windows")
    return os.path.join(system_root, "System32", "netstat.exe")


def parse_windows_listener_pid(output, port):
    target = f":{port}"
    for line in output.splitlines():
        parts = line.split()
        if len(parts) < 5:
            continue
        protocol, local_address, _, state, pid = parts[:5]
        if protocol.upper() == "TCP" and state.upper() == "LISTENING" and local_address.endswith(target):
            return int(pid)
    return None


def parse_tasklist_process_info(output):
    rows = list(csv.reader(output.splitlines()))
    if not rows or len(rows[0]) < 2:
        return None
    return {"name": rows[0][0], "start_time": None}


def get_server_pid():
    """查端口占用"""
    try:
        import platform
        if platform.system() == "Windows":
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex(('127.0.0.1', PORT))
            s.close()
            if result != 0:
                return None
            # 端口被占用，找 PID
            out = subprocess.check_output(
                [windows_netstat_path(), "-ano"],
                text=True,
            )
            return parse_windows_listener_pid(out, PORT)
        else:
            out = subprocess.check_output(f"lsof -ti:{PORT}", shell=True, text=True)
            if out.strip():
                return int(out.strip())
    except Exception:
        pass
    return None


def get_process_info(pid):
    """获取进程信息"""
    try:
        if sys.platform.startswith("win"):
            tasklist = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "tasklist.exe")
            out = subprocess.check_output(
                [tasklist, "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                text=True,
                stderr=subprocess.DEVNULL,
            )
            return parse_tasklist_process_info(out)
    except Exception:
        pass
    return None


def get_file_mtimes(root, dirnames):
    """收集关键文件的修改时间"""
    files = []
    for entry in dirnames:
        path = os.path.join(root, entry)
        if os.path.isfile(path):
            files.append((entry, os.path.getmtime(path)))
        elif os.path.isdir(path):
            for dirpath, _, filenames in os.walk(path):
                for fn in filenames:
                    if fn.endswith(".py"):
                        full = os.path.join(dirpath, fn)
                        rel = os.path.relpath(full, root)
                        files.append((rel, os.path.getmtime(full)))
    return files


def format_time(ts):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


def print_status():
    print("=" * 60)
    print("  百问即查 服务状态诊断")
    print("=" * 60)

    # 1. 检查服务是否在跑
    pid = get_server_pid()
    if not pid:
        print(f"\n  状态 : 未运行 ")
        print(f"  端口 {PORT} 无 LISTEN")
        print("\n  建议: python main.py")
        return

    proc = get_process_info(pid)
    if proc:
        print(f"\n  状态  : 运行中")
        print(f"  端口  : {PORT}")
        print(f"  PID   : {pid}")
        if proc.get("start_time"):
            print(f"  启动  : {format_time(proc['start_time'])}")
    else:
        print(f"\n  状态  : 端口 {PORT} 被占用 (PID {pid})")

    # 2. 检查文件是否在进程启动后被修改过
    if proc and proc.get("start_time"):
        start_ts = proc["start_time"]
        modified_after = []
        for path, mtime in get_file_mtimes(PROJECT_ROOT, WATCH_DIRS):
            if mtime > start_ts:
                modified_after.append((path, mtime))

        if modified_after:
            print(f"\n    [注意] 以下 {len(modified_after)} 个文件在服务启动后被修改:")
            for path, mtime in sorted(modified_after, key=lambda x: -x[1])[:10]:
                print(f"    {format_time(mtime)}  {path}")
            if len(modified_after) > 10:
                print(f"    ... 共 {len(modified_after)} 个文件")
            print(f"\n    当前运行的是 旧版本代码! 需要重启!")
        else:
            print(f"\n    所有文件未在启动后修改 — 运行的是最新代码")

    # 3. HTTP 响应测试
    print(f"\n  HTTP 测试:")
    try:
        import urllib.request
        resp = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/api/config/llm/status", timeout=3)
        data = json.loads(resp.read())
        print(f"    /api/config/llm/status 200 OK")
        print(f"    默认模型: {data.get('default_backend', '?')}")
        backends = data.get("backends", {})
        for name, info in backends.items():
            mark = " ← 默认" if info.get("is_default") else ""
            status = "可用" if info.get("available") else "不可用"
            print(f"      {name}: {status}{mark}")
    except Exception as e:
        print(f"    HTTP 请求失败: {e}")

    print("=" * 60)


if __name__ == "__main__":
    print_status()
