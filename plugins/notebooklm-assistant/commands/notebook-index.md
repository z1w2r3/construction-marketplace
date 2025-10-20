# 生成文档索引

生成或更新知识库的文档索引。

---

你现在要为用户生成或更新知识库的文档索引。

## 执行步骤

### 1. 读取配置

从 `.notebooklm/config.md` 读取:
- 文档源路径列表
- 知识库名称

如果配置文件不存在，提示:
```
❌ 知识库未初始化，请先运行: /notebook-init
```

### 2. 扫描所有文档源

对配置文件中的每个文档源路径:

使用 MCP 工具 `scan_directory`:
```
mcp_tool: scan_directory
params: {
  directory: "文档源路径",
  file_types: [],  # 空数组表示所有支持的类型
  max_depth: 10
}
```

### 3. 合并索引结果

将所有路径的扫描结果合并:
- 去重（相同路径的文件）
- 按修改时间排序（最新的在前）
- 统计文件类型分布

### 4. 增强索引（可选）

对重要文档提取关键词（限前 20 个文档，避免过长时间）:

使用 MCP 工具 `extract_keywords`:
```
mcp_tool: extract_keywords
params: {
  file_path: "文档路径",
  top_k: 10
}
```

将关键词添加到索引中，用于后续检索优化。

### 5. 保存索引

使用 Write 工具保存索引到 `.notebooklm/index/metadata.json`:

```json
{
  "knowledge_base_name": "知识库名称",
  "last_updated": "2025-10-18 13:30:00",
  "total_files": 47,
  "file_types": {
    ".pdf": 12,
    ".docx": 20,
    ".xlsx": 10,
    ".pptx": 5
  },
  "index": [
    {
      "path": "/absolute/path/to/file.pdf",
      "name": "file.pdf",
      "extension": ".pdf",
      "size": 1048576,
      "modified": 1729241234.56,
      "modified_readable": "2025-10-15 10:30:00",
      "relative_path": "docs/file.pdf",
      "keywords": ["关键词1", "关键词2"]  // 可选
    },
    ...
  ]
}
```

### 6. 生成可读索引

同时生成 Markdown 格式的可读索引 `.notebooklm/index/index.md`:

```markdown
# 文档索引

**知识库**: [名称]
**最后更新**: [时间]
**总文档数**: [N]

## 文件类型分布
| 类型 | 数量 |
|------|------|
| PDF | 12 |
| Word | 20 |
| Excel | 10 |
| PowerPoint | 5 |

## 文档列表（按修改时间排序）

### PDF 文档
1. [file1.pdf](path/to/file1.pdf) - 修改时间: 2025-10-15 10:30
   - 关键词: keyword1, keyword2
2. ...

### Word 文档
1. [doc1.docx](path/to/doc1.docx) - 修改时间: 2025-10-14 09:20
   ...

...
```

### 7. 输出结果

显示索引生成结果:
```
✅ 文档索引已更新！

📊 统计信息:
- 总文档数: [N]
- 新增文档: [X]
- 更新文档: [Y]

📁 文件类型分布:
- PDF: [N1] 个
- Word: [N2] 个
- Excel: [N3] 个
- PowerPoint: [N4] 个
- 其他: [N5] 个

📝 索引文件:
- JSON 索引: .notebooklm/index/metadata.json
- 可读索引: .notebooklm/index/index.md

⏱️ 索引耗时: [X] 秒

💡 现在可以使用:
- /notebook-ask [问题] - 智能问答
- /notebook-research [主题] - 深度研究
- /notebook-report [类型] [主题] - 生成报告
```

## 性能优化

- 只扫描元数据，不读取文件内容（快速）
- 关键词提取限制在前 20 个重要文档
- 使用缓存避免重复扫描未修改的文件（TODO）

## 错误处理

- 路径不存在: 跳过并警告
- 无权限访问: 跳过并记录
- 文件损坏: 跳过并记录到错误日志
