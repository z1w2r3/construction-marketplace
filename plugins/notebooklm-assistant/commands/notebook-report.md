# NotebookLM 专业报告生成

基于知识库生成专业排版的 Word/PDF 报告。

---

**命令格式**: `/notebook-report <类型> <主题>`

**报告类型**:
- `research` - 研究报告（深度分析型）
- `summary` - 总结报告（简明概括型）
- `comparison` - 对比报告（多方案对比）
- `analysis` - 分析报告（数据驱动型）

---

## 执行流程

### Phase 1: 报告规划

#### 1.1 理解需求

如果用户未提供完整信息，交互式询问:
- **报告主题**: $ARGUMENTS 中的主题部分
- **目标读者**: 管理层 / 技术团队 / 客户（默认：管理层）
- **报告长度**: 简明 / 标准 / 详细（默认：标准）
- **特殊要求**: 是否需要特定章节、图表等

#### 1.2 调用 Custom Skill: report-structure

使用 `/skill custom/report-structure` 生成报告大纲:

**输入**:
- topic: $ARGUMENTS 中的主题
- report_type: $ARGUMENTS 中的类型
- audience: 目标读者
- knowledge_base_path: 从 `.notebooklm/config.md` 读取

**输出**: 结构化大纲（JSON 格式），包含:
- 章节列表
- 每个章节需要使用的 Skill
- 需要的源文档列表
- 预估页数和时间

展示大纲给用户确认:
```
## 📋 报告大纲

**报告类型**: Research Report
**预估页数**: 12 页
**预估时间**: 5 分钟

### 第一章：概述
- 1.1 背景介绍（来源: 3 个文档）
- 1.2 研究目的

### 第二章：主要发现
- 2.1 关键数据（将提取 2 个表格）
- 2.2 趋势分析

### 第三章：结论与建议
...

是否继续生成？(继续/修改)
```

---

### Phase 2: 数据收集

对大纲中的每个章节，根据指定的 Skill 和数据源收集内容。

#### 2.1 调用 Smart Retrieval Skill

使用 `/skill custom/smart-retrieval` 找到相关文档:

**示例**（第一章 - 背景介绍）:
```
使用 /skill custom/smart-retrieval:
- query: "背景 + 目的 + 项目介绍"
- knowledge_base_path: [从配置读取]
- top_k: 5
```

**返回**: 相关文档列表（按相关度排序）

#### 2.2 调用官方 Document Skills

根据章节需求调用相应的 Skill:

**示例 1** - 深度研究（第一章）:
```
使用 /skill official/docx/SKILL 或 official/pdf/SKILL:
- 读取背景文档
- 提取关键信息
- 综合多个来源
```

**示例 2** - 数据提取（第二章）:
```
使用 /skill official/xlsx/SKILL:
- 提取 Excel 表格数据
- 统计关键指标
- 生成汇总表
```

**示例 3** - 文档摘要（第三章）:
```
调用 summarize 功能:
- 对已分析文档生成摘要
- 提取行动建议
```

#### 2.3 调用 Citation Manager Skill

使用 `/skill custom/citation-manager` 管理引用:
- 追踪所有信息来源
- 生成内联引用
- 准备参考文献列表

---

### Phase 3: 内容生成

#### 3.1 逐章节撰写

基于收集的数据，由 Claude 撰写每个章节的内容:

- 开头段落（引入主题）
- 正文段落（详细阐述，引用数据）
- 小结段落（承上启下）

**格式要求**:
- 使用专业术语和行业规范
- 数据必须标注来源
- 逻辑清晰，层次分明

#### 3.2 调用 Data Visualization Skill

使用 `/skill custom/data-visualization` 识别需要图表的数据:

**输入**: 提取的结构化数据
**输出**: 图表建议（类型、数据、描述）

**示例输出**:
```json
{
  "chart_type": "line",
  "title": "项目进度趋势",
  "data": {
    "labels": ["1月", "2月", "3月", "4月"],
    "datasets": [
      {"label": "计划进度", "data": [20, 40, 60, 80]},
      {"label": "实际进度", "data": [15, 35, 55, 75]}
    ]
  },
  "suggested_placement": "第 2 章第 1 节之后"
}
```

#### 3.3 构建 Report Content 对象

组织所有章节内容为结构化数据:

```json
{
  "title": "报告标题",
  "author": "NotebookLM Assistant",
  "date": "2025-10-18",
  "abstract": "摘要内容（200-300字）",
  "chapters": [
    {
      "title": "第一章：概述",
      "sections": [
        {
          "title": "1.1 背景介绍",
          "content": "段落内容...",
          "table": {...},  // 可选
          "chart": {...}   // 可选
        }
      ]
    }
  ],
  "references": [
    {
      "formatted_citation": "[1] 文档名. 路径. 2025-10-15."
    }
  ]
}
```

---

### Phase 4: 专业排版

#### 4.1 选择模板和风格

根据报告类型自动选择:
- `research` → academic 风格
- `analysis` → business 风格
- `summary` → business 风格
- `comparison` → technical 风格

#### 4.2 调用 MCP Report Generator

使用 MCP 工具 `generate_word_report`:

```
mcp_tool: generate_word_report
params: {
  template: "default",
  content: {上面构建的 Report Content 对象},
  style: "academic",
  output_path: "notebooklm-outputs/reports/报告标题-YYYYMMDD.docx"
}
```

#### 4.3 生成 Markdown 预览版

同时生成 Markdown 版本供快速审阅:
```markdown
# [报告标题]

**生成时间**: 2025-10-18
**文档数**: Word 版本 + Markdown 版本

## 摘要
[摘要内容]

## 第一章：概述
### 1.1 背景介绍
...

## 参考文献
[1] ...
```

---

### Phase 5: 质量检查与交付

#### 5.1 自动检查

验证报告完整性:
- ✅ 所有章节是否完整
- ✅ 引用是否正确标注
- ✅ 表格是否插入
- ✅ 图表占位符是否添加

#### 5.2 生成审阅报告

创建审阅版本 `报告标题-审阅.md`:

```markdown
# 报告生成完成

## 📊 统计信息
- 总字数: 5,432
- 章节数: 5
- 表格数: 3
- 图表数: 4
- 引用文档: 12

## 📖 内容大纲
[完整大纲，带页码估算]

## 💾 生成的文件
- **Word 版本**: `notebooklm-outputs/reports/报告标题-20251018.docx`
- **Markdown 预览**: `notebooklm-outputs/reports/报告标题-20251018.md`
- **审阅报告**: `notebooklm-outputs/reports/报告标题-审阅.md`

## 📝 下一步操作
1. 在 Word 中打开报告查看
2. 更新目录（引用 → 更新目录）
3. 根据数据表手动插入图表（或保留占位符）
4. 如需修改，使用: `/notebook-report-revise [章节号] [修改说明]`
5. 导出 PDF: 使用 MCP 工具 `convert_to_pdf`

## 🔍 质量检查结果
✅ 所有章节完整
✅ 引用格式正确（12 条引用）
✅ 表格已插入（3 个）
⚠️ 图表需手动插入（4 个占位符）

## 📚 使用的文档
1. [文档1](路径) - 引用 3 次
2. [文档2](路径) - 引用 2 次
...
```

#### 5.3 输出完成信息

```
🎉 报告生成完成！

📄 **报告标题**: [标题]
📅 **生成时间**: 2025-10-18 13:45:30
📏 **总页数**: ~12 页
📊 **总字数**: 5,432 字

📁 **输出文件**:
- Word: notebooklm-outputs/reports/报告标题-20251018.docx
- Markdown: notebooklm-outputs/reports/报告标题-20251018.md
- 审阅报告: notebooklm-outputs/reports/报告标题-审阅.md

✅ **质量检查**: 通过
- 章节: 5/5 完整
- 表格: 3 个已插入
- 图表: 4 个占位符（需手动插入）
- 引用: 12 条（格式正确）

💡 **下一步**:
1. 打开 Word 文档查看
2. 更新目录（引用 → 目录 → 更新）
3. 插入图表（数据已在表格中）
4. 导出 PDF（可选）

🔧 **修改报告**: `/notebook-report-revise [章节号] [修改说明]`
```

---

## 高级功能（可选）

### 修订报告章节
```
/notebook-report-revise 2.1 "增加更多数据对比"
```

### 导出 PDF
```
使用 MCP 工具 convert_to_pdf:
- docx_path: "报告路径.docx"
- pdf_path: "报告路径.pdf"
```

---

## 注意事项

⚠️ **首次生成可能需要 3-10 分钟**（取决于文档数量和复杂度）

✅ **支持中断恢复**: 如果生成过程中断，可以重新运行命令

🔒 **只读原则**: 不修改任何原始文档

📊 **图表处理**: 目前生成占位符和数据表，用户可手动插入 Word 图表

---

## 报告类型详解

### Research Report（研究报告）
**适用**: 深度分析、学术研究、技术调研
**风格**: Academic
**结构**:
1. 摘要
2. 背景与目的
3. 方法论
4. 主要发现
5. 讨论
6. 结论与建议
7. 参考文献

### Summary Report（总结报告）
**适用**: 项目总结、季度报告、简报
**风格**: Business
**结构**:
1. 概述
2. 关键要点
3. 重要数据
4. 下一步行动

### Comparison Report（对比报告）
**适用**: 方案对比、版本对比、竞品分析
**风格**: Technical
**结构**:
1. 对比目标介绍
2. 方法论
3. 逐项对比
4. 综合对比矩阵
5. 结论

### Analysis Report（分析报告）
**适用**: 数据分析、绩效分析、市场分析
**风格**: Business
**结构**:
1. 问题陈述
2. 数据来源
3. 分析方法
4. 结果（定量+定性）
5. 洞察与建议
