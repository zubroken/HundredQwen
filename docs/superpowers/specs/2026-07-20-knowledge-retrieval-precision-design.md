# 内置知识库精准检索设计

## 目标

在不引入向量数据库、外部 Embedding 服务或网络依赖的前提下，把当前纯关键词检索升级为可解释的本地混合检索；优先返回与课程主题直接相关、可引用的教材片段，并在证据不足时明确降级。

## 现状与问题

- `KnowledgeBase.retrieve()` 仅按关键词命中次数排序，标题、章节、来源质量和同义表达均不参与排序。
- 同一页或重叠 chunk 可重复占据前列，弱化真正相关内容。
- 返回值只有整数 `score`，无法解释为何被选中，也没有低相关结果的可靠性边界。

## 范围

### 包含

- 基于可配置同义词的查询扩展。
- 关键词、标题/章节、短语和二元字符 n-gram 的混合召回与重排序。
- 课程/难度/来源质量元数据的保留与排序。
- 页级去重、可解释分数、证据等级与低证据警告。
- `POST /api/knowledge/search` 对现有字段保持兼容，新增说明字段。

### 不包含

- 外部向量数据库、在线 Embedding 或重新抓取网络论文。
- 改写现有资源生成 Agent 的 prompt 结构。
- 重新制作 PDF 或新增大规模课程语料。

## 架构

`KnowledgeBase` 仍是唯一的检索入口。它在加载 JSON、PDF chunk 时保留标准化元数据；查询时先提取词项并展开别名，然后用倒排索引召回候选，最后以纯函数计算混合分数并过滤/去重。`KnowledgeService.search()` 仅透传增强后的结果，因此现有 API 调用方不受影响。

```text
查询 -> 分词/别名扩展 -> 倒排候选
     -> 标题/章节/短语/n-gram/来源重排序
     -> 页级去重与可信阈值 -> 可解释结果与引用
```

## 评分规则

每个候选的 `score_details` 固定包含：

- `keyword`: 原始查询词精确命中数 × 3。
- `alias`: 同义扩展词命中数 × 2。
- `title`: 标题或章节名命中时 + 4。
- `phrase`: 归一化查询短语出现在文本或标题中时 + 5。
- `ngram`: 二元字符 Jaccard 相似度 × 3（0–3）。
- `source_quality`: `textbook=3`、`pdf=3`、`concept=2`、`paper=1`。
- `difficulty`: 请求难度与条目难度一致时 + 1；未请求时为 0。

按总分倒序、标题/教材优先顺序和稳定的 chunk ID 作为并列排序。相同文档且相同页码只保留得分最高的一条；无页码的 JSON 条目按 `doc_id` 去重。

## 可信度与接口

- `score >= 5`：`evidence_level="supported"`。
- `0 < score < 5`：`evidence_level="weak"`，附带 `请核验低相关依据`。
- 无候选：返回空列表、`evidence_level="insufficient"` 和 `知识库未找到充分依据，请核验`。

`retrieve()` 继续返回 chunk 列表，新增 `score_details`、`match_reasons`、`evidence_level`；原有 `id/title/text/page/score/chapter` 字段不变。`search()` 新增顶层 `evidence_level`、`warnings`，每条 `results` 新增 `match_reasons`、`score_details`。

## 验收与测试

1. “Transformer 注意力机制”优先命中标题或正文直接包含该主题的教材 chunk，而非仅含“机制”的条目。
2. “QKV 机制”可通过别名命中“查询、键、值”相关内容。
3. 同一文档同一页的多个重叠 chunk 只返回一个。
4. 无关查询不伪造引用，返回 `insufficient`。
5. 现有知识库、引用服务、资源生成与 API 回归测试全部通过。
