# Smart Retrieval Skill
智能文档检索技能 - 根据查询意图动态确定需要读取的文档

---

## 技能说明
这是一个可复用的检索技能，用于从大量文档中智能筛选相关内容。

## 输入参数
- `query`: 用户查询/问题
- `knowledge_base_path`: 知识库根路径（从配置文件读取）
- `top_k`: 返回的文档数量（默认 5）

---

## 执行逻辑

### 1. 读取轻量级索引

从 `.notebooklm/index/metadata.json` 读取:
- 文档路径列表
- 文件元数据（文件名、类型、大小、修改时间）
- 预提取的关键词（如果有）

### 2. 关键词提取

从用户查询中提取关键词:
- 识别重要名词（使用简单的空格分词或正则）
- 识别专业术语
- 识别时间范围（如"2023年"、"最近"）

示例:
```
查询: "项目的主要风险是什么？"
关键词: ["项目", "风险", "主要"]
```

### 3. 文件名匹配（第一轮过滤）

在索引中搜索包含关键词的文档:
- 匹配文件名
- 匹配相对路径
- 不区分大小写

示例:
```python
matches = [
  doc for doc in index
  if any(keyword in doc["name"].lower() or keyword in doc["relative_path"].lower()
         for keyword in keywords)
]
```

### 4. 元数据匹配（第二轮过滤）

基于文件类型、修改时间等元数据进一步筛选:
- 如果查询涉及"最新"：优先选择最近修改的文件
- 如果查询涉及特定格式（如"图表"）：优先选择 Excel/PPT
- 如果查询涉及"数据"：优先选择 Excel

示例:
```python
if "最新" in query or "近期" in query:
    matches.sort(key=lambda x: x["modified"], reverse=True)
elif "图表" in query or "数据" in query:
    matches = [doc for doc in matches if doc["extension"] in [".xlsx", ".pptx"]]
```

### 5. 内容预览（第三轮精排）

对候选文档（前 10 个）调用 MCP 工具读取预览:

```
mcp_tool: preview_document
params: {
  file_path: "文档路径",
  preview_length: 500
}
```

### 6. 相关度评分

基于以下因素评分:
- **文件名匹配度**（权重 30%）：完全匹配 > 部分匹配
- **元数据相关性**（权重 20%）：时间匹配、类型匹配
- **内容预览匹配度**（权重 50%）：关键词在预览中出现次数

评分公式:
```python
score = (
    filename_match_score * 0.3 +
    metadata_match_score * 0.2 +
    content_match_score * 0.5
)
```

### 7. 返回结果

返回 top_k 个文档，JSON 格式:

```json
[
  {
    "path": "/absolute/path/to/document.pdf",
    "name": "document.pdf",
    "score": 0.95,
    "reason": "包含关键词'风险'、'项目'，且是最新文档（2025-10-15修改）",
    "preview": "前500字符预览内容..."
  },
  {
    "path": "/absolute/path/to/another.docx",
    "score": 0.87,
    "reason": "包含关键词'风险'，文档类型匹配",
    "preview": "前500字符预览内容..."
  },
  ...
]
```

---

## 使用示例

在 Commands 中调用:

```markdown
使用 /skill custom/smart-retrieval:
- query: "项目预算分配情况"
- knowledge_base_path: /path/to/docs
- top_k: 5

返回: [相关文档列表]
```

---

## 性能优化

- 索引读取: O(1) - 一次性读取 JSON
- 第一轮过滤: O(n) - 遍历所有文档
- 第二轮过滤: O(m) - 遍历匹配文档（m < n）
- 第三轮预览: O(k) - 只预览前 k 个（k=10）

预计耗时: < 3 秒（1000 个文档）

---

## 错误处理

- 索引文件不存在: 提示运行 `/notebook-index`
- 无匹配文档: 返回空列表，提示"未找到相关文档"
- 文档无法读取: 跳过并记录警告，继续处理其他文档

---

## 扩展功能（TODO）

- 语义搜索（使用 embedding）
- 缓存最近检索结果
- 支持模糊匹配（拼音、同义词）
