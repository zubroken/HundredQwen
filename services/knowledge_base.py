"""
知识库 RAG 服务 —— PDF 教材提取 + 分块 + 关键词索引 + 检索
"""
from __future__ import annotations
import json
import os
import re
import hashlib
import logging
from typing import List, Dict, Optional
from settings import KNOWLEDGE_DIR

logger = logging.getLogger(__name__)

PAPERS_DIR = KNOWLEDGE_DIR / "papers"
CHUNKS_DIR = KNOWLEDGE_DIR / "chunks"
TOC_DIR = KNOWLEDGE_DIR / "toc"


class KnowledgeBase:
    """PDF 教材 + JSON 知识条目的 RAG 检索服务"""

    def __init__(self):
        self.documents: List[dict] = []       # 文档元数据
        self.chunks: List[dict] = []          # 所有分块 [{id, doc_id, doc_title, text, keywords, page}]
        self._keyword_index: Dict[str, List[int]] = {}  # 关键词 → chunk 索引
        self._page_sections: Dict[str, dict] = {}  # doc_id → {page: section_info}
        self._loaded = False

    # ---- 生命周期 ----

    def _load_toc(self, doc_id: str) -> dict:
        """加载教材目录，返回 {page_number: section_info} 映射"""
        toc_file = os.path.join(TOC_DIR, f"{doc_id}.json")
        if not os.path.exists(toc_file):
            return {}
        try:
            with open(toc_file, "r", encoding="utf-8") as f:
                toc = json.load(f)
        except Exception as exc:
            logger.warning(f"加载目录文件 {doc_id} 失败: {exc}")
            return {}

        page_map = {}
        for ch in toc.get("chapters", []):
            for section in ch.get("sections", []):
                # section 里没有独立页码，用章的页码范围
                page_map[str(ch["page_start"])] = {
                    "chapter_num": ch["num"],
                    "chapter_title": ch["title"],
                    "section": section
                }
            # 为章节内每个可能页面粗略映射到章
            for p in range(ch["page_start"], ch["page_end"] + 1):
                if str(p) not in page_map:
                    page_map[str(p)] = {
                        "chapter_num": ch["num"],
                        "chapter_title": ch["title"]
                    }
        # 最后一章之后 → 附录/参考资料（惰性：不预生成，检索时按需返回）
        if toc.get("chapters"):
            page_map["_last_chapter_end"] = toc["chapters"][-1]["page_end"]
        return page_map

    def scan_and_index(self) -> int:
        """启动时调用：扫描 knowledge 目录，提取新 PDF 并索引"""
        os.makedirs(PAPERS_DIR, exist_ok=True)
        os.makedirs(CHUNKS_DIR, exist_ok=True)
        os.makedirs(TOC_DIR, exist_ok=True)

        count = 0
        # 1. 加载 JSON 概念文件
        json_files = [f for f in os.listdir(KNOWLEDGE_DIR) if f.endswith(".json") and f not in ("papers_cache.json",)]
        for fname in json_files:
            fpath = os.path.join(KNOWLEDGE_DIR, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    self._index_json_entries(data, fname)
                    count += len(data)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"加载 {fname} 失败: {e}")

        # 2. 扫描 PDF
        if os.path.isdir(PAPERS_DIR):
            for fname in os.listdir(PAPERS_DIR):
                if fname.lower().endswith(".pdf"):
                    doc_id = self._doc_id(fname)
                    if doc_id not in self._page_sections:
                        self._page_sections[doc_id] = self._load_toc(doc_id)
                    chunk_file = os.path.join(CHUNKS_DIR, f"{doc_id}.json")
                    if os.path.exists(chunk_file):
                        # 已有分块，直接加载
                        try:
                            with open(chunk_file, "r", encoding="utf-8") as f:
                                saved = json.load(f)
                            page_sections = self._page_sections.get(doc_id, {})
                            for ch in saved:
                                ch["doc_title"] = fname
                                ch["doc_id"] = doc_id
                                # 打章节标签
                                pg = ch.get("page", "")
                                if pg and pg in page_sections:
                                    ch["chapter"] = page_sections[pg]
                                idx = len(self.chunks)
                                self.chunks.append(ch)
                                self._add_to_index(idx, ch.get("text", ""))
                            self.documents.append({
                                "id": doc_id, "title": fname, "type": "pdf",
                                "chunks": len(saved), "path": os.path.join(PAPERS_DIR, fname)
                            })
                            logger.info(f"加载已分块 PDF: {fname} ({len(saved)} chunks)")
                            continue
                        except (json.JSONDecodeError, IOError):
                            pass  # 文件损坏，重新提取

                    # 新 PDF → 提取文本
                    try:
                        text = self._extract_pdf(os.path.join(PAPERS_DIR, fname))
                        if not text or len(text.strip()) < 100:
                            logger.warning(f"PDF '{fname}' 提取文本过短（可能为扫描版），跳过")
                            continue
                        chunks = self._chunk_text(text, fname)
                        page_sections = self._page_sections.get(doc_id, {})
                        for ch in chunks:
                            ch["doc_title"] = fname
                            ch["doc_id"] = doc_id
                            pg = ch.get("page", "")
                            if pg and pg in page_sections:
                                ch["chapter"] = page_sections[pg]
                            idx = len(self.chunks)
                            self.chunks.append(ch)
                            self._add_to_index(idx, ch.get("text", ""))
                        # 持久化分块
                        with open(chunk_file, "w", encoding="utf-8") as f:
                            json.dump(chunks, f, ensure_ascii=False)
                        self.documents.append({
                            "id": doc_id, "title": fname, "type": "pdf",
                            "chunks": len(chunks), "path": os.path.join(PAPERS_DIR, fname)
                        })
                        count += len(chunks)
                        logger.info(f"已索引 PDF: {fname} ({len(chunks)} chunks)")
                    except Exception as e:
                        logger.error(f"处理 PDF '{fname}' 失败: {e}")
                        continue

        self._loaded = True
        logger.info(f"知识库就绪：{len(self.documents)} 个文档, {len(self.chunks)} 个分块, {len(self._keyword_index)} 个索引词")
        return count

    # ---- PDF 文本提取 ----

    def _extract_pdf(self, filepath: str) -> str:
        try:
            import pdfplumber
        except ImportError:
            logger.error("pdfplumber 未安装，请执行: pip install pdfplumber")
            return ""
        text_parts = []
        with pdfplumber.open(filepath) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(f"[第{i+1}页]\n{page_text}")
        return "\n\n".join(text_parts)

    # ---- 文本分块 ----

    def _chunk_text(self, text: str, doc_title: str = "", size: int = 600, overlap: int = 150) -> List[dict]:
        chunks = []
        # 按段落分割
        paragraphs = re.split(r'\n{2,}', text)
        current = ""
        current_page = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            # 提取页码标记
            page_match = re.match(r'\[第(\d+)页\]', para)
            if page_match:
                current_page = page_match.group(1)

            if len(current) + len(para) > size and current:
                # 提取关键词
                keywords = self._extract_keywords(current)
                chunks.append({
                    "id": hashlib.md5(current.encode()).hexdigest()[:12],
                    "doc_title": doc_title,
                    "text": current.strip(),
                    "keywords": keywords,
                    "page": current_page
                })
                # 保留重叠部分
                overlap_text = current[-overlap:] if len(current) > overlap else ""
                current = overlap_text + para
            else:
                current += ("\n" if current else "") + para

        # 最后一个 chunk
        if current.strip():
            keywords = self._extract_keywords(current)
            chunks.append({
                "id": hashlib.md5(current.encode()).hexdigest()[:12],
                "doc_title": doc_title,
                "text": current.strip(),
                "keywords": keywords,
                "page": current_page
            })
        return chunks

    # ---- 关键词提取 ----

    def _extract_keywords(self, text: str) -> List[str]:
        try:
            import jieba
        except ImportError:
            # 无 jieba 时回退到简单分词
            words = re.findall(r'[一-鿿\w]{2,}', text.lower())
            stop = {'可以', '使用', '一个', '这个', '其中', '通过', '进行', '以及', '不是',
                    '就是', '但是', '如果', '因为', '所以', '因此', '没有', '这些', '那些',
                    '我们', '它们', '他们', '什么', '怎样', '如何', 'this', 'that', 'the',
                    'and', 'for', 'with', 'from', 'are', 'was', 'has', 'its', 'not', 'but'}
            return list(set(w for w in words if w not in stop))[:20]

        stop = {'可以', '使用', '一个', '这个', '其中', '通过', '进行', '以及', '不是',
                '就是', '但是', '如果', '因为', '所以', '因此', '没有', '这些', '那些',
                '我们', '它们', '他们', '什么', '怎样', '如何', 'this', 'that', 'the',
                'and', 'for', 'with', 'from', 'are', 'was', 'has', 'its', 'not', 'but', '了', '的', '是', '在', '有'}
        words = jieba.cut(text.lower())
        filtered = [w.strip() for w in words if len(w.strip()) >= 2 and w.strip() not in stop]
        # 返回频次最高的 20 个词
        from collections import Counter
        return [w for w, _ in Counter(filtered).most_common(20)]

    # ---- 索引 ----

    def _index_json_entries(self, entries: List[dict], source: str):
        for entry in entries:
            doc_id = entry.get("id", hashlib.md5(entry.get("title","").encode()).hexdigest()[:12])
            text = entry.get("content", "")
            keywords = entry.get("keywords", []) + self._extract_keywords(text)
            ch = {
                "id": doc_id,
                "doc_title": entry.get("title", ""),
                "text": text,
                "keywords": list(set(keywords)),
                "page": "",
                "type": entry.get("type", "concept"),
                "difficulty": entry.get("difficulty", "easy"),
            }
            idx = len(self.chunks)
            self.chunks.append(ch)
            for kw in ch["keywords"]:
                kw = kw.strip().lower()
                if kw not in self._keyword_index:
                    self._keyword_index[kw] = []
                self._keyword_index[kw].append(idx)
            self.documents.append({
                "id": doc_id, "title": entry.get("title", ""), "type": entry.get("type", "concept"),
                "chunks": 1
            })

    def _add_to_index(self, chunk_idx: int, text: str):
        keywords = self._extract_keywords(text)
        self.chunks[chunk_idx]["keywords"] = keywords
        for kw in keywords:
            kw = kw.strip().lower()
            if kw not in self._keyword_index:
                self._keyword_index[kw] = []
            self._keyword_index[kw].append(chunk_idx)

    # ---- 检索 ----

    def retrieve(self, query: str, top_k: int = 5, doc_id: str = "") -> List[dict]:
        """检索最相关的 chunks（供 RAG 注入用），可选按文档ID筛选"""
        if not self._loaded:
            self.scan_and_index()
        if not self.chunks:
            return []

        # 先按文档筛选
        source_chunks = self.chunks
        if doc_id:
            source_chunks = [c for c in self.chunks if self._doc_id(c.get("doc_title", "")) == doc_id]
            if not source_chunks:
                return []

        query_words = self._extract_keywords(query)
        if not query_words:
            return []

        scores: Dict[int, int] = {}
        for w in query_words:
            for idx in self._keyword_index.get(w, []):
                if idx >= len(self.chunks):
                    continue
                ch = self.chunks[idx]
                if doc_id and self._doc_id(ch.get("doc_title", "")) != doc_id:
                    continue
                scores[idx] = scores.get(idx, 0) + 1

        sorted_idxs = sorted(scores.items(), key=lambda x: -x[1])[:top_k]
        results = []
        for idx, score in sorted_idxs:
            ch = dict(self.chunks[idx])
            ch["score"] = score
            results.append(ch)
        return results

    def search(self, query: str, type_filter: str = "all", doc_id: str = "", top_k: int = 10) -> dict:
        """前端搜索接口：返回 chunks，支持按文档ID筛选"""
        chunks = self.retrieve(query, top_k, doc_id=doc_id)
        if type_filter != "all":
            chunks = [c for c in chunks if c.get("type", "pdf") == type_filter]

        return {
            "query": query,
            "total": len(chunks),
            "results": [{
                "id": c["id"],
                "title": c.get("doc_title", ""),
                "text": c.get("text", "")[:300],
                "full_text": c.get("text", ""),
                "keywords": c.get("keywords", [])[:8],
                "type": c.get("type", "pdf"),
                "difficulty": c.get("difficulty", ""),
                "page": c.get("page", ""),
                "score": c.get("score", 0),
                "chapter": c.get("chapter", {}).get("chapter_num", ""),
                "chapter_title": c.get("chapter", {}).get("chapter_title", ""),
                "section": c.get("chapter", {}).get("section", ""),
            } for c in chunks],
        }

    # ---- Prompt 格式化 ----

    def format_context(self, chunks: List[dict]) -> str:
        """将检索结果拼接为 LLM prompt 可用的上下文文本（含章节信息）"""
        if not chunks:
            return ""
        lines = []
        for i, c in enumerate(chunks, 1):
            source = c.get("doc_title", "知识库")
            page = f"第{c['page']}页" if c.get("page") else ""
            ch_info = c.get("chapter") if isinstance(c.get("chapter"), dict) else {}
            ch_num = ch_info.get("chapter_num", "")
            ch_title = ch_info.get("chapter_title", "")
            chapter_str = f"第{ch_num}章 {ch_title} > " if ch_num and ch_title else ""
            lines.append(f"[{i}] 来源：《{source}》{chapter_str}{page}\n{c.get('text', '')[:600]}\n")
        return "\n".join(lines)

    # ---- 统计 ----

    def get_stats(self) -> dict:
        if not self._loaded:
            self.scan_and_index()
        types = {}
        for doc in self.documents:
            t = doc.get("type", "unknown")
            types[t] = types.get(t, 0) + 1
        return {
            "documents": len(self.documents),
            "chunks": len(self.chunks),
            "index_terms": len(self._keyword_index),
            "types": types,
        }

    def list_documents(self) -> List[dict]:
        if not self._loaded:
            self.scan_and_index()
        return self.documents

    def _doc_id(self, filename: str) -> str:
        return hashlib.md5(filename.encode()).hexdigest()[:12]
