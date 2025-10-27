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

## 核心原则 ⭐ 新增

在整个执行过程中,我将遵循以下原则:
1. **透明化思考**: 每个决策都说明理由
2. **真实优先**: 绝不编造数据,所有信息必须有来源
3. **用户确认**: 重要决策前等待用户确认
4. **信息溯源**: 所有引用必须标注文档来源

---

## 执行流程

### Phase 0: 需求理解 ⭐ 新增

💭 **我的理解**:
```
📋 报告主题: [从 $ARGUMENTS 提取]
📊 报告类型: [research/summary/comparison/analysis]
🎯 目标读者: [需要询问]
📄 报告长度: [需要询问]

💭 基于主题,我初步判断应该:
- 重点关注: [维度1, 维度2]
- 可能需要的数据: [数据类型]
- 预计复杂度: [简单/中等/复杂]
```

---

### Phase 1: 报告规划

#### 步骤 1.1: 理解需求

如果用户未提供完整信息,交互式询问:
- **报告主题**: $ARGUMENTS 中的主题部分
- **目标读者**: 管理层 / 技术团队 / 客户(默认:管理层)
- **报告长度**: 简明 / 标准 / 详细(默认:标准)
- **特殊要求**: 是否需要特定章节、图表等

#### 步骤 1.2: 生成多种报告结构方案 ⭐ 修改 (来自文章启发)

**重要**: 不要直接生成报告!先提供 2-3 种报告结构方案供用户选择。

使用 **Skill tool** 调用 `report-structure` skill 生成**多种**报告大纲方案:

**输入**:
- topic: $ARGUMENTS 中的主题
- report_type: $ARGUMENTS 中的类型
- audience: 目标读者
- knowledge_base_path: 从 `.notebooklm/config.md` 读取
- generate_alternatives: true  # ⭐ 新增参数

**输出**: 2-3 种备选方案（JSON 格式）

---

展示所有方案给用户选择:

```
📋 为您规划了 3 种报告结构:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**方案 A: 时间线分析报告** （推荐用于: 展现发展历程）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**预估页数**: 10-12 页
**预估时间**: 4 分钟
**工作量**: ⭐⭐ (中等)

### 章节结构:
1. 概述 (1页)
2. 第一阶段分析 (2025 Q1)  (2页)
   - 数据来源: 需读取 3 份月报
3. 第二阶段分析 (2025 Q2)  (2页)
   - 数据来源: 需读取 3 份月报
4. 第三阶段分析 (2025 Q3)  (2页)
   - 数据来源: 需读取 3 份月报
5. 演进趋势与展望 (2页)

**优势**:
- ✅ 清晰展现进度演进
- ✅ 时间脉络清晰

**劣势**:
- ⚠️  可能忽略跨时期的关联
- ⚠️  重复性描述较多

**需要的文档**: 12 份月报 + 4 份季度总结

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**方案 B: 维度分析报告** （推荐用于: 全面深入分析）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**预估页数**: 15-18 页
**预估时间**: 6-7 分钟
**工作量**: ⭐⭐⭐ (高)

### 章节结构:
1. 概述 (1页)
2. 技术架构分析 (4页)
   - 数据来源: 需读取 8 份技术文档
3. 团队协作分析 (3页)
   - 数据来源: 需读取 5 份会议纪要
4. 风险与挑战 (3页)
   - 数据来源: 需读取 4 份风险评估文档
5. 成果与亮点 (3页)
   - 数据来源: 需读取 6 份验收文档
6. 改进建议 (2页)

**优势**:
- ✅ 全面深入,覆盖多个维度
- ✅ 结构清晰,便于理解

**劣势**:
- ⚠️  耗时较长
- ⚠️  需要读取大量文档

**需要的文档**: 30+ 份各类文档

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**方案 C: 问题导向分析报告** （推荐用于: 快速聚焦核心）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**预估页数**: 8-10 页
**预估时间**: 3 分钟
**工作量**: ⭐ (低)

### 章节结构:
1. 概述 (1页)
2. 主要问题识别 (2页)
   - 数据来源: 需读取 3 份问题清单
3. 原因分析 (2页)
   - 数据来源: 需读取 2 份根因分析文档
4. 解决方案 (2页)
   - 数据来源: 需读取 3 份改进方案
5. 效果评估与建议 (2页)

**优势**:
- ✅ 快速聚焦核心问题
- ✅ 工作量小,产出快

**劣势**:
- ⚠️  缺少全貌信息
- ⚠️  可能遗漏潜在问题

**需要的文档**: 8 份核心文档

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 **请选择方案**:
- 回复 A/B/C 选择对应方案
- 回复 "自定义" 并描述您想要的报告结构
- 回复 "修改X" 对某个方案进行调整

💭 **我的建议**:
如果您 [条件], 建议选择方案 [X],因为 [理由]。
```

---

### Phase 2: 数据收集

对大纲中的每个章节，根据指定的 Skill 和数据源收集内容。

#### 2.1 调用 Smart Retrieval Skill

使用 **Skill tool** 调用 `smart-retrieval` skill 找到相关文档:

**示例**（第一章 - 背景介绍）:
```
使用 Skill tool 调用 smart-retrieval:
- query: "背景 + 目的 + 项目介绍"
- knowledge_base_path: [从配置读取]
- top_k: 5
```

**返回**: 相关文档列表（按相关度排序）

#### 2.2 调用官方 Document Skills

根据章节需求使用 **Skill tool** 调用相应的 Skill:

**示例 1** - 深度研究（第一章）:
```
使用 Skill tool 调用 docx 或 pdf skill:
- 读取背景文档
- 提取关键信息
- 综合多个来源
```

**示例 2** - 数据提取（第二章）:
```
使用 Skill tool 调用 xlsx skill:
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

使用 **Skill tool** 调用 `citation-manager` skill 管理引用:
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

#### 3.2 识别需要图表的数据

分析提取的结构化数据,识别适合可视化的内容:

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

#### 4.2 使用 DOCX Skill 生成 Word 报告

调用 **Skill tool** 使用 `docx` skill:

**步骤**:
1. 使用 Skill tool 调用 `docx` skill
2. 读取 [`docx-js.md`](../skills/docx/docx-js.md) 获取完整的 docx-js API 文档
3. 编写 JavaScript/TypeScript 代码生成 Word 文档:

```javascript
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell } = require("docx");
const fs = require("fs");

// 根据 Report Content 对象构建 Word 文档
const doc = new Document({
  sections: [{
    properties: {},
    children: [
      // 标题页
      new Paragraph({
        text: reportContent.title,
        heading: HeadingLevel.TITLE,
        alignment: "center"
      }),
      new Paragraph({
        text: `作者: ${reportContent.author}`,
        alignment: "center"
      }),
      new Paragraph({
        text: `日期: ${reportContent.date}`,
        alignment: "center"
      }),

      // 摘要
      new Paragraph({
        text: "摘要",
        heading: HeadingLevel.HEADING_1
      }),
      new Paragraph({
        text: reportContent.abstract
      }),

      // 逐章节生成
      ...reportContent.chapters.flatMap(chapter => [
        new Paragraph({
          text: chapter.title,
          heading: HeadingLevel.HEADING_1
        }),
        ...chapter.sections.flatMap(section => [
          new Paragraph({
            text: section.title,
            heading: HeadingLevel.HEADING_2
          }),
          new Paragraph({
            text: section.content
          }),
          // 如果有表格
          ...(section.table ? [createTable(section.table)] : [])
        ])
      ]),

      // 参考文献
      new Paragraph({
        text: "参考文献",
        heading: HeadingLevel.HEADING_1
      }),
      ...reportContent.references.map((ref, index) =>
        new Paragraph({
          text: ref.formatted_citation,
          numbering: {
            reference: "references",
            level: 0
          }
        })
      )
    ]
  }]
});

// 导出为 .docx 文件
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("notebooklm-outputs/reports/报告标题-YYYYMMDD.docx", buffer);
  console.log("✅ Word 报告生成完成");
});
```

**注意**:
- 根据 `style` 参数调整字体、颜色、间距等格式
- 图表生成占位符段落,提示用户手动插入
- 确保所有依赖已安装 (`npm install docx`)

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
5. 导出 PDF: 使用 `soffice --headless --convert-to pdf` 命令

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
```bash
# 使用 LibreOffice 将 Word 文档转换为 PDF
soffice --headless --convert-to pdf "报告路径.docx" --outdir "notebooklm-outputs/reports/"
```

**注意**: 确保已安装 LibreOffice (`sudo apt-get install libreoffice`)

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
