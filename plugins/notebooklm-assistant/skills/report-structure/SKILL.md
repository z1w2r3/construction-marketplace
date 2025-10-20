---
name: report-structure
description: "报告结构规划技能 - 根据主题和类型生成专业报告大纲。支持研究报告、总结报告、对比报告、分析报告等多种类型,自动分配数据源"
---

# Report Structure Skill
报告结构规划技能 - 根据主题和类型生成专业报告大纲

## 技能说明
根据报告主题和类型,自动生成专业的报告大纲结构。

## 输入参数
- `topic`: 报告主题
- `report_type`: 报告类型(research/summary/comparison/analysis)
- `audience`: 目标读者(executive/technical/general)
- `knowledge_base_path`: 知识库路径

---

## 执行逻辑

### 1. 分析主题和知识库
- 读取知识库索引文件
- 识别与主题相关的文档类别
- 确定可用的数据类型(文本/表格/图表)

### 2. 根据报告类型生成大纲框架

#### Research Report(研究报告)
```markdown
1. 摘要(Executive Summary)
2. 背景与目的(Background & Objectives)
3. 方法论(Methodology)
4. 主要发现(Key Findings)
   - 4.1 数据分析
   - 4.2 趋势识别
5. 讨论(Discussion)
6. 结论与建议(Conclusions & Recommendations)
7. 参考文献(References)
```

#### Summary Report(总结报告)
```markdown
1. 概述(Overview)
2. 关键要点(Key Points)
3. 重要数据(Critical Data)
4. 下一步行动(Next Steps)
```

#### Comparison Report(对比报告)
```markdown
1. 对比目标介绍
2. 方法论
3. 逐项对比
   - 3.1 维度1
   - 3.2 维度2
4. 综合对比矩阵
5. 结论
```

#### Analysis Report(分析报告)
```markdown
1. 问题陈述
2. 数据来源
3. 分析方法
4. 结果
   - 4.1 定量分析
   - 4.2 定性分析
5. 洞察与建议
```

### 3. 为每个章节分配数据源

对大纲中的每个章节:
- 使用 `smart-retrieval` Skill 找到相关文档
- 标注需要使用的 Skill(官方或自定义)
- 预估所需内容长度

示例:
```json
{
  "chapter": 1,
  "title": "摘要",
  "sections": [
    {
      "title": "1.1 背景",
      "required_skill": "summarize-documents",
      "source_documents": ["doc1.pdf", "doc2.docx"],
      "target_length": 200
    }
  ]
}
```

### 4. 输出结构化大纲

返回 JSON 格式:
```json
{
  "report_title": "...",
  "report_type": "research",
  "outline": [
    {
      "chapter": 1,
      "title": "摘要",
      "sections": [...]
    }
  ],
  "estimated_pages": 12,
  "estimated_time": "5 minutes"
}
```

---

## 使用示例

```markdown
使用 /skill custom/report-structure:
- topic: "2024年项目执行情况分析"
- report_type: "analysis"
- audience: "executive"
- knowledge_base_path: /path/to/docs

返回: 报告大纲(JSON)
```
