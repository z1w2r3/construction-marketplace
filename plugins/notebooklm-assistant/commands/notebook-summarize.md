# NotebookLM 文档摘要

生成文档或主题的智能摘要。

---

**摘要范围**: $ARGUMENTS（可选，默认整体摘要）

---

## 执行流程

### 1. 确定摘要范围

- 如果 $ARGUMENTS 为空：生成整体知识库摘要
- 如果提供主题：生成该主题的摘要

### 2. 检索文档

使用 `/skill custom/smart-retrieval`（如果有主题）

### 3. 调用官方 Summarize Skill

参考 `/skill official/docx/SKILL` 中的摘要方法:
- 提取关键要点
- 压缩冗余信息
- 保持核心观点

### 4. 生成摘要

输出格式:
```markdown
# [主题] 摘要

## 核心要点
1. [要点1]
2. [要点2]
3. [要点3]

## 关键数据
- [数据1]
- [数据2]

## 主要来源
- [文档1]
- [文档2]

---
**摘要长度**: [N] 字
**原文长度**: [M] 字
**压缩比**: [X]%
```

保存到: `notebooklm-outputs/summaries/摘要-YYYYMMDD.md`

---

## 示例

```
/notebook-summarize 技术方案

→ 检索技术方案相关文档
→ 提取核心要点
→ 生成 500 字摘要
```
