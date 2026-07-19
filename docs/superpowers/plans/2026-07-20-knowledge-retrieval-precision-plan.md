# Knowledge Retrieval Precision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an offline, explainable hybrid ranker that prioritizes course-relevant knowledge-base evidence.

**Architecture:** Extend `KnowledgeBase` with query expansion, deterministic candidate scoring, deduplication and evidence thresholds. Keep existing retrieval and search contracts compatible while adding explanation fields.

**Tech Stack:** Python 3, existing JSON/PDF chunks, FastAPI, pytest; no external service or new package.

---

### Task 1: Add retrieval-quality regression tests

**Files:**
- Create: `tests/test_knowledge_retrieval_precision.py`

- [ ] **Step 1: Write failing ranking, alias, deduplication and insufficient-evidence tests**

```python
def test_phrase_and_title_match_outrank_generic_keyword_match(): ...
def test_alias_expansion_finds_qkv_content(): ...
def test_same_document_page_is_deduplicated(): ...
def test_unknown_query_returns_insufficient_evidence(): ...
```

- [ ] **Step 2: Run the tests and confirm they fail because scoring fields do not exist**

Run: `python -m pytest -q tests/test_knowledge_retrieval_precision.py`

- [ ] **Step 3: Commit the regression tests**

```powershell
git add tests/test_knowledge_retrieval_precision.py
git commit -m "test: define knowledge retrieval precision"
```

### Task 2: Implement deterministic hybrid retrieval

**Files:**
- Modify: `services/knowledge_base.py`
- Test: `tests/test_knowledge_retrieval_precision.py`

- [ ] **Step 1: Add configurable aliases and metadata-preserving indexing**

Add `DEFAULT_QUERY_ALIASES`, preserve `course`, `topic`, `source_quality` and `difficulty` from JSON entries, and infer source quality from existing type values.

- [ ] **Step 2: Add query normalization, alias expansion and scoring helpers**

Implement `_expand_query_terms`, `_char_bigram_similarity`, `_score_chunk`, `_dedupe_ranked_chunks`. `_score_chunk` returns total score plus named components and human-readable match reasons.

- [ ] **Step 3: Replace hit-count-only ordering in `retrieve()`**

Use the existing keyword index only for candidate recall; rank candidates with the helpers, attach `score_details`, `match_reasons` and `evidence_level`, and return no result below the evidence threshold.

- [ ] **Step 4: Run focused tests and commit**

Run: `python -m pytest -q tests/test_knowledge_retrieval_precision.py tests/test_knowledge_service.py`

```powershell
git add services/knowledge_base.py tests/test_knowledge_retrieval_precision.py
git commit -m "feat: add explainable hybrid knowledge retrieval"
```

### Task 3: Expose evidence status without breaking the API

**Files:**
- Modify: `services/knowledge_base.py`
- Modify: `tests/test_knowledge_service.py`

- [ ] **Step 1: Write a failing API/service assertion for `evidence_level`, `warnings` and match explanations**

- [ ] **Step 2: Add top-level evidence status to `search()` and include per-result explanation fields**

- [ ] **Step 3: Run focused regression tests and commit**

Run: `python -m pytest -q tests/test_knowledge_service.py tests/test_knowledge_retrieval_precision.py`

### Task 4: Verify the course evidence path and publish

**Files:**
- Modify: `docs/知识库与测试数据说明.md`

- [ ] **Step 1: Update documentation with ranking signals and evidence-level semantics**

- [ ] **Step 2: Run full test suite, restart service, and query the Transformer topic**

Run: `python -m pytest -q`

Run: `python check_server.py`

Run: `Invoke-RestMethod http://127.0.0.1:9010/api/knowledge/stats`

- [ ] **Step 3: Commit and push `Kira2026`**

```powershell
git add docs/知识库与测试数据说明.md
git commit -m "docs: describe knowledge retrieval evidence"
git push gitee Kira2026
```
