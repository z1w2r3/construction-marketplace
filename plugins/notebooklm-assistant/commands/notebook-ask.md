# NotebookLM 智能问答

基于知识库智能回答用户问题(利用预览索引加速检索)。

---

**用户问题**: $ARGUMENTS

---

## 核心原则 ⭐ 新增

在整个执行过程中,我将遵循以下原则:
1. **透明化思考**: 每个决策都说明理由
2. **真实优先**: 绝不编造数据,所有信息必须有来源
3. **用户确认**: 重要决策前等待用户确认
4. **信息溯源**: 所有引用必须标注文档来源

---

## 执行流程

### 步骤 0: 任务分类与路由 ⭐ 新增

#### 0.1 判断任务类型

💭 **我的思考过程**:

分析用户问题,判断属于哪种类型:

**Type A: 简单事实查询(fact-finding)**
- 示例: "项目经理是谁?"、"预算是多少?"、"截止日期是什么时候?"
- 特征: 单一事实,答案明确,通常在1-2个文档中
- 检索策略: 快速检索(文件名匹配 + 关键词搜索)
- 预计阅读文档数: 1-3 个

**Type B: 深度分析(analysis)**
- 示例: "项目的主要风险?"、"技术选型的优劣?"、"为什么选择XX方案?"
- 特征: 需要综合多个文档,深度思考,分析原因和影响
- 检索策略: 深度检索(全文分析 + 跨文档综合)
- 预计阅读文档数: 5-10 个

**Type C: 对比分析(comparison)**
- 示例: "方案A和方案B哪个更好?"、"Redis和Memcached的区别?"
- 特征: 需要对比多个维度,提取对比点
- 检索策略: 结构化对比(提取对比维度 + 逐项对比)
- 预计阅读文档数: 3-8 个

**Type D: 时间线追溯(timeline)**
- 示例: "项目是如何演进的?"、"XX功能的开发历程?"
- 特征: 需要按时间顺序整理信息
- 检索策略: 时间序列检索(按修改时间排序)
- 预计阅读文档数: 5-15 个

#### 0.2 输出任务分类结果

基于用户问题 **"$ARGUMENTS"**,我判断这是:

```
📋 任务类型: [Type A/B/C/D]
🎯 检索策略: [说明]
📊 预计阅读文档数: [数量]
⏱️  预计耗时: [时间估计]

💭 判断理由:
- [理由1]
- [理由2]
```

#### 0.3 确认执行策略(重要问题才需要)

如果是 Type B/C/D(复杂问题),询问用户:

```
我的理解是 [复述问题意图]。
我计划 [检索策略描述]。

如果您想调整检索范围或方式,请告诉我。否则我将继续执行。
```

---

### 步骤 1: 理解问题意图

💭 **提取关键信息**:
- 核心关键词: [列表]
- 问题焦点: [说明]
- 期望答案形式: [事实/分析/对比/时间线]

### 步骤 2: 第一轮筛选(基于索引预览)

💭 **我的检索策略**:
- 优先匹配: [文件名/内容预览/目录/标题]
- 关键词组合: [AND/OR 逻辑]
- 时间范围: [最近30天/全部/特定时期]

从 `.notebooklm/index/metadata.json` 读取索引,利用预览数据快速筛选相关文档:

```python
import json
import re
from pathlib import Path

# 读取索引
with open('.notebooklm/index/metadata.json', 'r', encoding='utf-8') as f:
    index_data = json.load(f)

files = index_data['index']
query = "$ARGUMENTS"  # 用户问题

# 提取问题关键词
def extract_keywords(text):
    """简单的关键词提取"""
    # 移除标点和停用词
    stopwords = {'的', '是', '在', '有', '和', '与', '或', '及', '等', '了', '吗', '呢', '什么', '如何', '为什么'}
    words = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]+', text)
    return [w for w in words if w not in stopwords and len(w) > 1]

query_keywords = extract_keywords(query)
print(f"🔍 问题关键词: {', '.join(query_keywords)}")

# 计算相关度得分
def calculate_relevance(file, keywords):
    """基于预览数据计算相关度"""
    score = 0
    reasons = []

    # 文件名匹配(权重 2)
    for kw in keywords:
        if kw.lower() in file['name'].lower():
            score += 2
            reasons.append(f"文件名包含'{kw}'")

    # 预览内容匹配(权重 3)
    preview_text = file.get('preview', '')
    for kw in keywords:
        if kw in preview_text:
            count = preview_text.count(kw)
            score += min(count * 3, 9)  # 单个关键词最多加9分
            reasons.append(f"内容包含'{kw}'({count}次)")

    # PDF 目录匹配(权重 2)
    if file.get('has_toc'):
        toc_text = ' '.join(file.get('toc', []))
        for kw in keywords:
            if kw in toc_text:
                score += 2
                reasons.append(f"目录包含'{kw}'")

    # Word 标题匹配(权重 2)
    if file.get('headings'):
        headings_text = ' '.join([h['text'] for h in file['headings']])
        for kw in keywords:
            if kw in headings_text:
                score += 2
                reasons.append(f"标题包含'{kw}'")

    # Excel Sheet 名称匹配(权重 1)
    if file.get('sheet_names'):
        sheets_text = ' '.join(file['sheet_names'])
        for kw in keywords:
            if kw in sheets_text:
                score += 1
                reasons.append(f"Sheet名包含'{kw}'")

    # 最新文档加分(权重 1)
    import time
    days_old = (time.time() - file['modified']) / (24 * 3600)
    if days_old < 30:
        score += 1
        reasons.append("最近30天内的文档")

    return score, reasons

# 对所有文档计算相关度
scored_files = []
for file in files:
    score, reasons = calculate_relevance(file, query_keywords)
    if score > 0:  # 只保留有相关性的
        file_with_score = file.copy()
        file_with_score['relevance_score'] = score
        file_with_score['relevance_reasons'] = reasons
        scored_files.append(file_with_score)

# 按相关度排序
scored_files_sorted = sorted(scored_files, key=lambda f: f['relevance_score'], reverse=True)

# 筛选 top 10 候选文档
top_candidates = scored_files_sorted[:10]

print(f"\n📊 初筛结果: 从 {len(files)} 个文档中筛选出 {len(top_candidates)} 个候选文档")
for i, f in enumerate(top_candidates[:5], 1):
    print(f"   {i}. {f['name']} (得分: {f['relevance_score']}, 原因: {', '.join(f['relevance_reasons'][:2])})")
```

### 步骤 3: 第二轮精准匹配(深度解析)

💭 **筛选结果分析**:
```
📊 找到 [N] 个候选文档:
   🔴 高相关 (得分 > 10): [数量] 个
   🟡 中相关 (得分 5-10): [数量] 个
   🟢 低相关 (得分 < 5): [数量] 个

📖 我将深度解析前 [N] 个文档,因为 [理由]
```

对 top 10 候选文档进行完整解析,使用对应的 **pdf/docx/xlsx Skills**:

```python
import pdfplumber
from docx import Document
from openpyxl import load_workbook

def parse_pdf_full(pdf_path):
    """完整解析 PDF"""
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() or ""
        return full_text

def parse_docx_full(docx_path):
    """完整解析 Word"""
    doc = Document(docx_path)
    full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return full_text

def parse_xlsx_full(xlsx_path):
    """完整解析 Excel(主要 sheet)"""
    wb = load_workbook(xlsx_path, read_only=True, data_only=True)
    full_text = ""

    for sheet_name in wb.sheetnames[:3]:  # 只解析前3个sheet
        ws = wb[sheet_name]
        full_text += f"\n=== Sheet: {sheet_name} ===\n"

        for row in ws.iter_rows(values_only=True, max_row=100):  # 每个sheet最多100行
            row_text = '\t'.join([str(cell) if cell else '' for cell in row])
            full_text += row_text + "\n"

    wb.close()
    return full_text

# 对候选文档进行完整解析
parsed_docs = []
for file in top_candidates:
    try:
        if file['extension'] == '.pdf':
            content = parse_pdf_full(file['path'])
        elif file['extension'] in ['.docx', '.doc']:
            content = parse_docx_full(file['path'])
        elif file['extension'] in ['.xlsx', '.xls']:
            content = parse_xlsx_full(file['path'])
        else:
            content = file.get('preview', '')

        parsed_docs.append({
            "file": file,
            "content": content[:50000]  # 限制长度,避免超token
        })

        print(f"✅ 已解析: {file['name']} ({len(content)} 字符)")

    except Exception as e:
        print(f"⚠️  解析失败: {file['name']} - {e}")
        continue
```

### 4. 使用 Context Builder Skill 构建上下文

使用 Skill tool 调用 context-builder:

```python
# 调用 context-builder skill 构建上下文
# 注意:这里应该使用 Skill tool,而不是直接调用代码

# 伪代码示意:
# context = Skill("notebooklm-assistant:context-builder", {
#     "documents": parsed_docs,
#     "query": query,
#     "max_tokens": 10000
# })

# 手动实现简化版上下文构建:
def build_context(docs, query, max_tokens=10000):
    """简化的上下文构建"""
    context_parts = []
    total_tokens = 0

    for doc in docs:
        # 提取包含关键词的段落
        content = doc['content']
        relevant_paragraphs = []

        for paragraph in content.split('\n'):
            if any(kw in paragraph for kw in query_keywords):
                relevant_paragraphs.append(paragraph)

        # 构建文档上下文
        if relevant_paragraphs:
            doc_context = f"\n## 文档: {doc['file']['name']}\n"
            doc_context += '\n'.join(relevant_paragraphs[:5])  # 最多5段

            # 估算token(粗略:1字符≈0.5token)
            estimated_tokens = len(doc_context) // 2
            if total_tokens + estimated_tokens < max_tokens:
                context_parts.append(doc_context)
                total_tokens += estimated_tokens

    return '\n'.join(context_parts)

context = build_context(parsed_docs, query)
print(f"\n📝 已构建上下文: {len(context)} 字符 (约 {len(context)//2} tokens)")
```

### 步骤 5: 生成答案

💭 **答案构建策略**:
```
📝 我将基于以下文档生成答案:
1. [文档1] - 提供 [信息类型]
2. [文档2] - 提供 [信息类型]
3. [文档3] - 提供 [信息类型]

⚠️  如果文档中没有明确答案,我将:
   - 明确告知"文档库中未找到相关信息"
   - 不编造或猜测
   - 建议用户补充文档或调整问题
```

基于构建的上下文,Claude 综合分析并回答问题:

**核心原则(绝不妥协)**:
- ❌ **绝不编造数据或信息**
- ❌ **绝不使用模型训练数据中的知识(除非明确标注"来自AI知识库")**
- ✅ **直接引用原文(带文件名和页码/位置)**
- ✅ **综合多个来源时,列出所有来源**
- ✅ **突出重点,客观陈述**
- ✅ **不确定时明确标注"需要人工确认"或"文档库中未找到"**
- ✅ **多个来源有矛盾时,列出所有观点,不擅自判断**

参考上下文,生成结构化答案:

```markdown
## 🤔 您的问题
[复述用户问题]

## ✅ 答案
[基于文档的回答,段落形式]

根据文档分析,[核心答案]...

具体来说:
1. [要点1]
   > "[原文引用]"
   > 📄 来源: 文档名.pdf

2. [要点2]
   > "[原文引用]"
   > 📄 来源: 文档名.docx

### 📊 关键数据(如果有)
| 指标 | 数值 | 来源 |
|------|------|------|
| XX | YY | 文档A |

### 📄 信息来源
1. [文档名1](路径) - 相关度: 95%
2. [文档名2](路径) - 相关度: 87%
3. ...

## 💡 您可能还想了解
- [相关问题1]
- [相关问题2]
- [相关问题3]

## 🔍 深入探索
- 深度研究: `/notebook-research [主题]`
- 生成报告: `/notebook-report analysis "[主题]"`
```

### 6. 智能缓存(可选优化)

将解析结果缓存到 `.notebooklm/cache/` 避免重复解析:

```python
import hashlib
from pathlib import Path

# 缓存目录
cache_dir = Path('.notebooklm/cache')
cache_dir.mkdir(parents=True, exist_ok=True)

# 生成文件哈希作为缓存key
def get_file_hash(file_path, modified_time):
    """基于路径和修改时间生成哈希"""
    key = f"{file_path}_{modified_time}"
    return hashlib.md5(key.encode()).hexdigest()

# 保存缓存
for doc in parsed_docs:
    file = doc['file']
    cache_key = get_file_hash(file['path'], file['modified'])
    cache_file = cache_dir / f"{cache_key}.json"

    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump({
            "file_path": file['path'],
            "file_name": file['name'],
            "modified": file['modified'],
            "content": doc['content']
        }, f, ensure_ascii=False)

print(f"💾 已缓存 {len(parsed_docs)} 个文档到 .notebooklm/cache/")
```

---

## 智能检索原理(优化后)

### 第一轮: 基于索引预览的快速筛选
- 从 metadata.json 读取所有文档的预览数据
- 匹配文件名、预览内容、目录、标题、Sheet名称
- 计算综合相关度得分
- **优势**: 无需打开文件,极快速(毫秒级)

### 第二轮: 深度解析 top 候选文档
- 只对相关度最高的 10 个文档进行完整解析
- 使用对应的 pdf/docx/xlsx Skills
- 提取包含关键词的段落
- **优势**: Token 消耗可控,准确度高

### 第三轮: 上下文构建和答案生成
- 使用 context-builder skill 整合信息
- Claude 基于上下文生成答案
- 引用来源,保证可追溯

---

## 性能优化

- **两轮检索**: 先索引筛选(快),再深度解析(准)
- **Token 节省**: 只读取相关文档,避免全量加载
- **智能缓存**: 已解析文档缓存复用
- **超时保护**: 单个文档解析超时跳过

---

## 示例

**用户**: `/notebook-ask 项目的主要风险是什么?`

**输出**:
```
🔍 问题关键词: 项目, 主要, 风险

📊 初筛结果: 从 100 个文档中筛选出 8 个候选文档
   1. risk-assessment.pdf (得分: 15, 原因: 文件名包含'风险', 内容包含'风险'(5次))
   2. project-plan.docx (得分: 8, 原因: 内容包含'项目'(3次), 内容包含'风险'(2次))
   3. meeting-notes-2024.txt (得分: 5, 原因: 内容包含'风险'(1次), 最近30天内的文档)
   ...

✅ 已解析: risk-assessment.pdf (15234 字符)
✅ 已解析: project-plan.docx (8567 字符)
✅ 已解析: meeting-notes-2024.txt (3421 字符)

📝 已构建上下文: 5680 字符 (约 2840 tokens)

---

## 🤔 您的问题
项目的主要风险是什么?

## ✅ 答案
根据文档分析,项目面临三大主要风险:

1. **预算超支风险**(高优先级)
   > "当前预算储备仅 5%,低于行业标准 10-15%"
   > 📄 来源: risk-assessment.pdf

2. **进度延期风险**(中优先级)
   > "关键路径上的模块 B 依赖外部供应商,交付存在不确定性"
   > 📄 来源: project-plan.docx

3. **技术债务风险**(中优先级)
   > "团队在会议中提到现有架构难以扩展"
   > 📄 来源: meeting-notes-2024.txt

### 📊 风险评估汇总
| 风险类型 | 优先级 | 提及频率 | 缓解措施 |
|---------|--------|---------|---------|
| 预算超支 | 高 | 3次 | 增加储备金 |
| 进度延期 | 中 | 2次 | 寻找备选供应商 |
| 技术债务 | 中 | 1次 | 架构重构计划 |

### 📄 信息来源
1. [risk-assessment.pdf](path) - 相关度: 98%
2. [project-plan.docx](path) - 相关度: 85%
3. [meeting-notes-2024.txt](path) - 相关度: 72%

## 💡 您可能还想了解
- 这些风险的具体缓解措施是什么?
- 历史项目中类似风险是如何解决的?
- 是否有应急预案文档?

## 🔍 深入探索
- 深度研究: `/notebook-research 项目风险管理`
- 生成报告: `/notebook-report analysis "项目风险评估报告"`
```

---

## 注意事项

- ✅ 所有答案基于文档,不编造信息
- ✅ 不确定时明确标注"需要人工确认"
- ✅ 多个来源有矛盾时,列出所有观点
- ✅ 重要数据必须标注来源
- ✅ 利用预览索引大幅提升检索速度
- ✅ 只深度解析高相关文档,节省 Token
