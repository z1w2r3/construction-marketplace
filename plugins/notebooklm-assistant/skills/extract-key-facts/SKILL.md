---
name: extract-key-facts
description: "从文档中提取结构化的关键事实,用于后续报告引用。确保所有信息可追溯,避免AI编造内容"
---

# Extract Key Facts Skill
从文档中提取关键事实并建立事实索引

## 技能说明
这是一个核心技能,用于从文档中提取结构化的事实信息,构建"事实索引",确保报告生成时所有信息都有明确来源,避免AI编造内容。

**核心价值** (来自文章启发):
- ✅ 真实 > 编造:所有事实都来自真实文档
- ✅ 可追溯:每个事实都标注来源文档和位置
- ✅ 结构化:便于后续查询和引用

---

## 输入参数

- `document_path`: 文档绝对路径
- `extraction_type`: 提取类型
  - `project_info` - 项目基本信息
  - `decision_records` - 决策记录
  - `risk_events` - 风险事件
  - `success_cases` - 成功案例
  - `key_data` - 关键数据
  - `all` - 全部提取(默认)
- `output_path`: 输出路径(可选,默认返回JSON)

---

## 执行逻辑

### 步骤 1: 读取文档内容

根据文档类型调用对应的 document skill:

```markdown
如果是 PDF:
  使用 Skill tool 调用 pdf skill

如果是 Word:
  使用 Skill tool 调用 docx skill

如果是 Excel:
  使用 Skill tool 调用 xlsx skill

如果是 PowerPoint:
  使用 Skill tool 调用 pptx skill
```

---

### 步骤 2: 识别事实类型

根据文档内容和结构,识别包含的事实类型:

**项目基本信息** (project_info):
- 项目名称
- 项目时间
- 参与人员/团队
- 项目目标
- 预算规模

识别规则:
- 通常在文档开头
- 包含"项目名称"、"项目经理"、"开始时间"等关键词
- Word文档的第一页或首节
- PPT的首页

**决策记录** (decision_records):
- 技术选型决策
- 方案选择决策
- 重要变更决策

识别规则:
- 包含"决定"、"选择"、"采用"、"变更为"等关键词
- 会议纪要中的决策事项
- 通常有理由说明

**风险事件** (risk_events):
- 已发生的风险
- 风险影响
- 应对措施

识别规则:
- 包含"风险"、"问题"、"延期"、"超预算"等关键词
- 风险评估报告
- 问题跟踪文档

**成功案例** (success_cases):
- 成功完成的里程碑
- 创新实践
- 优秀成果

识别规则:
- 包含"完成"、"达成"、"超额"、"优秀"等关键词
- 验收文档
- 总结报告中的亮点部分

**关键数据** (key_data):
- 性能指标
- 统计数据
- 量化结果

识别规则:
- 包含数字和单位
- Excel中的数据表格
- 报告中的数据章节

---

### 步骤 3: 提取结构化事实

对每个识别到的事实,提取以下信息:

```json
{
  "fact_id": "唯一标识符",
  "type": "事实类型",
  "content": "事实内容(原文摘录或概括)",
  "source": {
    "document_path": "文档绝对路径",
    "document_name": "文档文件名",
    "location": "具体位置(页码/段落/单元格)",
    "timestamp": "文档修改时间"
  },
  "metadata": {
    "confidence": "置信度(high/medium/low)",
    "keywords": ["关键词列表"],
    "related_facts": ["相关事实ID"]
  },
  "extracted_at": "提取时间(ISO格式)"
}
```

**示例 1 - 项目信息**:
```json
{
  "fact_id": "fact_001",
  "type": "project_info",
  "content": "项目名称: XX系统开发项目, 项目经理: 张三, 开始时间: 2024-01-15",
  "source": {
    "document_path": "/path/to/project-overview.docx",
    "document_name": "项目概述.docx",
    "location": "第1页, 第2段",
    "timestamp": "2024-01-15T10:30:00"
  },
  "metadata": {
    "confidence": "high",
    "keywords": ["项目名称", "项目经理", "开始时间"],
    "related_facts": []
  },
  "extracted_at": "2025-10-27T14:30:00"
}
```

**示例 2 - 决策记录**:
```json
{
  "fact_id": "fact_005",
  "type": "decision_records",
  "content": "技术选型: 选择Redis作为缓存方案, 原因: 支持数据持久化, 性能优于Memcached, 团队熟悉度高",
  "source": {
    "document_path": "/path/to/tech-design.pdf",
    "document_name": "技术方案设计.pdf",
    "location": "第5页, 3.2节",
    "timestamp": "2024-02-10T16:20:00"
  },
  "metadata": {
    "confidence": "high",
    "keywords": ["技术选型", "Redis", "缓存"],
    "related_facts": []
  },
  "extracted_at": "2025-10-27T14:32:00"
}
```

**示例 3 - 关键数据**:
```json
{
  "fact_id": "fact_012",
  "type": "key_data",
  "content": "系统性能: QPS达到10000, 平均响应时间50ms, P99延迟200ms",
  "source": {
    "document_path": "/path/to/performance-test.xlsx",
    "document_name": "性能测试报告.xlsx",
    "location": "Sheet: 测试结果, 单元格 A10:C10",
    "timestamp": "2024-03-20T09:15:00"
  },
  "metadata": {
    "confidence": "high",
    "keywords": ["QPS", "响应时间", "P99延迟"],
    "related_facts": []
  },
  "extracted_at": "2025-10-27T14:35:00"
}
```

---

### 步骤 4: 去重和关联

检查已有的事实索引,避免重复提取:

```python
# 伪代码
existing_facts = load_facts_index()

for new_fact in extracted_facts:
    # 检查是否已存在相同内容
    if is_duplicate(new_fact, existing_facts):
        skip_or_merge(new_fact)
    else:
        # 检查是否与已有事实相关
        related = find_related_facts(new_fact, existing_facts)
        new_fact["metadata"]["related_facts"] = related

        # 添加到索引
        existing_facts.append(new_fact)
```

---

### 步骤 5: 保存事实索引

将提取的事实保存到索引文件:

**文件路径**: `.notebooklm/index/facts-index.json`

**格式**:
```json
{
  "version": "1.0",
  "created_at": "2025-10-27T14:00:00",
  "updated_at": "2025-10-27T14:35:00",
  "total_facts": 25,
  "facts_by_type": {
    "project_info": 3,
    "decision_records": 8,
    "risk_events": 5,
    "success_cases": 4,
    "key_data": 5
  },
  "facts": [
    {/* 事实1 */},
    {/* 事实2 */},
    ...
  ]
}
```

---

### 步骤 6: 返回结果

返回提取的事实列表(JSON格式),并输出摘要:

```
✅ 事实提取完成

📊 提取统计:
- 文档: 技术方案设计.pdf
- 提取事实数: 8 个
  - 项目信息: 1 个
  - 决策记录: 3 个
  - 关键数据: 4 个

💾 已保存到: .notebooklm/index/facts-index.json
```

---

## 输出格式

**返回值**: JSON 数组

```json
[
  {
    "fact_id": "fact_001",
    "type": "project_info",
    "content": "...",
    "source": {...},
    "metadata": {...},
    "extracted_at": "..."
  },
  ...
]
```

---

## 使用场景

### 场景 1: 初始化时批量提取
```markdown
对知识库中的所有核心文档执行事实提取:
- 项目概述文档 → 提取项目信息
- 技术方案文档 → 提取决策记录
- 测试报告文档 → 提取关键数据
```

### 场景 2: 报告生成前强制引用
```markdown
在生成报告时,优先查询事实索引:
- 需要项目信息 → 查询 facts-index.json 中的 project_info
- 需要决策理由 → 查询 decision_records
- 需要性能数据 → 查询 key_data

如果索引中没有,才去读取原文档。
```

### 场景 3: 新增文档时增量提取
```markdown
当用户添加新文档到知识库:
- 运行 /notebook-index (更新文档索引)
- 自动调用 extract-key-facts 提取新文档的事实
- 更新 facts-index.json
```

---

## 核心原则 (绝不妥协)

1. **绝不编造**: 所有事实必须来自真实文档,不能猜测或补充
2. **完整溯源**: 每个事实必须标注文档来源和具体位置
3. **原文优先**: 尽量摘录原文,避免过度概括导致失真
4. **去重严格**: 相同内容只保留一份,避免索引膨胀
5. **置信度标注**: 不确定的事实标注为 low confidence

---

## 错误处理

- 文档无法读取: 跳过并记录警告
- 无法识别事实类型: 标注为 "unknown" 类型
- 提取失败: 返回空数组,不影响整体流程

---

## 性能优化

- 批量处理: 一次调用处理多个文档
- 增量更新: 只处理新增或修改的文档
- 缓存机制: 文档未修改时复用已提取的事实
- 并发处理: 对多个文档并行提取(可选)

---

## TODO 扩展功能

- [ ] 支持自定义事实类型
- [ ] 支持事实验证(多文档交叉验证)
- [ ] 支持事实演进追踪(同一事实的多个版本)
- [ ] 支持事实关系图谱可视化
