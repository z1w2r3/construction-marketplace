---
name: citation-manager
description: "引用管理技能 - 自动追踪和格式化文档引用。支持 APA、MLA、Chicago、GB7714 等多种引用格式,自动生成内联引用和参考文献列表"
---

# Citation Manager Skill
引用管理技能 - 自动追踪和格式化文档引用

## 技能说明
自动追踪报告中使用的所有信息来源,生成标准格式的引用。

## 输入参数
- `content`: 报告内容(包含需要引用的信息)
- `source_documents`: 源文档列表(从其他 Skills 获取)
- `citation_style`: 引用格式(APA/MLA/Chicago/GB7714)

---

## 执行逻辑

### 1. 识别需要引用的内容

扫描报告内容,识别:
- 直接引用(引号内的文字)
- 数据引用(数字、统计数据)
- 观点引用(特定论述)

### 2. 匹配源文档

对每个需要引用的内容:
- 在源文档中定位原始位置
- 提取元数据(作者、日期、页码)
- 生成唯一引用 ID

### 3. 插入内联引用

根据引用格式插入:

**APA 格式**:
```
...根据研究报告(Smith, 2024, p. 15),项目成功率达到 87%...
```

**GB 7714(中文)**:
```
...根据研究报告[1],项目成功率达到 87%...
```

### 4. 生成参考文献列表

在报告末尾生成完整的参考文献:

**APA 格式**:
```
References

Smith, J. (2024). Project Analysis Report. Company Name.
  Retrieved from: /path/to/document.pdf
```

**GB 7714 格式**:
```
参考文献

[1] 张三. 项目分析报告[R]. 公司名称, 2024.
```

### 5. 返回增强后的内容

```json
{
  "content_with_citations": "...",
  "references": [
    {
      "id": 1,
      "source": "document.pdf",
      "page": 15,
      "formatted_citation": "Smith, J. (2024)..."
    }
  ]
}
```

---

## 使用示例

```markdown
使用 /skill custom/citation-manager:
- content: [报告章节内容]
- source_documents: [已使用的文档列表]
- citation_style: "GB7714"

返回: 带引用的内容 + 参考文献列表
```
