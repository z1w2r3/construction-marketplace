# NotebookLM 助手帮助文档

显示所有可用命令和使用说明。

---

# 📚 NotebookLM 智能文档助手

类似 Google NotebookLM 的知识库问答、深度研究和专业报告生成工具。

## 🚀 快速开始

### 1. 初始化知识库
```
/notebook-init
```
首次使用时运行此命令，设置文档源路径和知识库配置。

### 2. 生成文档索引
```
/notebook-index
```
扫描并索引所有文档（初始化时会自动执行）。

### 3. 开始提问
```
/notebook-ask 项目的主要风险是什么？
```
基于知识库进行智能问答。

---

## 📖 所有命令

### 基础命令

#### `/notebook-init`
**初始化知识库**
- 设置文档源路径
- 创建配置和输出目录
- 自动生成初始索引

**使用场景**: 首次使用或重新配置知识库

---

#### `/notebook-index`
**生成/更新文档索引**
- 扫描所有文档源
- 提取元数据（文件名、大小、修改时间）
- 提取关键词（可选）

**使用场景**: 添加新文档后更新索引

---

#### `/notebook-help`
**显示帮助文档**

**使用场景**: 查看所有命令和使用说明

---

### 分析命令

#### `/notebook-ask <问题>`
**智能问答**

基于知识库回答您的问题，自动检索相关文档并综合分析。

**示例**:
```
/notebook-ask 项目预算是多少？
/notebook-ask 有哪些主要风险？
/notebook-ask A方案和B方案的区别？
```

**特点**:
- 自动检索相关文档
- 综合多个来源
- 标注信息来源（文件名+位置）
- 提供后续探索建议

---

#### `/notebook-research <主题>`
**深度研究**

对特定主题进行深入研究，使用 Anthropic 官方 `research-documents` Skill。

**示例**:
```
/notebook-research 项目技术架构
/notebook-research 市场竞争分析
```

**特点**:
- 全面分析相关文档
- 构建知识图谱
- 提取深层洞察
- 生成结构化报告

---

#### `/notebook-summarize [范围]`
**生成摘要**

对文档或主题生成摘要，使用官方 `summarize-documents` Skill。

**示例**:
```
/notebook-summarize                    # 整体摘要
/notebook-summarize 技术方案           # 主题摘要
```

**特点**:
- 可配置摘要长度
- 提取关键要点
- 支持多种风格

---

#### `/notebook-compare <对象A> <对象B>`
**文档对比**

对比两个方案、版本或文档，使用官方 `compare-documents` Skill。

**示例**:
```
/notebook-compare 方案A 方案B
/notebook-compare v1.0 v2.0
```

**特点**:
- 识别差异和共同点
- 生成对比表格
- 追踪版本变化

---

### 报告生成命令

#### `/notebook-clone-format <参考文档路径>`
**智能文档格式克隆**（🌟 新功能）

基于参考文档的格式模板,从知识库智能提取数据并生成排版一致、内容不同的新文档。

**适用场景**:
- 智能建造实施方案生成
- 智能建造申报资料编制
- 技术方案文档生成
- 标准化报告文档制作

**示例**:
```
/notebook-clone-format ./templates/智能建造实施方案-模板.docx
/notebook-clone-format ~/Documents/申报资料模板.docx
```

**核心特点**:
- ✅ 格式精确复制（样式、字体、段落格式）
- ✅ 内容智能生成（从知识库提取）
- ✅ 多样化改写（查重率<20%）
- ✅ 人机协同（关键信息用户提供）

**工作流程**:
1. **解析参考文档** - 深度分析文档结构和格式
2. **识别数据需求** - AI智能识别需要的字段和数据
3. **智能检索数据** - 从知识库检索相关内容
4. **多样化改写** - 5种改写策略降低查重率
5. **按格式生成** - 生成格式一致的Word文档

**输出文件**:
- Word文档: `notebooklm-outputs/项目名称-实施方案-YYYYMMDD.docx`
- Markdown预览: `notebooklm-outputs/项目名称-实施方案-YYYYMMDD.md`
- 审阅报告: `notebooklm-outputs/项目名称-实施方案-审阅报告.md`

**查重率控制**:
- 预估查重率: 15-20%
- 多样化改写技术: 同义替换、句式重组、段落重构
- 保护专业术语: BIM、智慧工地等术语不改写
- 保持数值准确: 面积、金额等数据保持原值

**注意事项**:
- ⚠️ 生成文档需人工审阅后使用
- ⚠️ 技术参数和数值数据需确认准确性
- ⚠️ 查重率为预估值,建议使用专业工具检测

---

#### `/notebook-report <类型> <主题>`
**生成专业报告**（🌟 核心功能）

生成专业排版的 Word 报告,支持多种报告类型。

**报告类型**:
- `research` - 研究报告（学术风格，深度分析）
- `summary` - 总结报告（简明扼要，突出要点）
- `comparison` - 对比报告（多方案对比）
- `analysis` - 分析报告（数据驱动，图表支持）

**示例**:
```
/notebook-report research "2024年项目执行情况研究"
/notebook-report analysis "预算执行分析"
/notebook-report comparison "技术方案对比"
```

**报告特点**:
- ✅ 专业 Word 排版（支持多级标题、表格、图表）
- ✅ 自动生成大纲
- ✅ 智能提取数据
- ✅ 引用标注
- ✅ 图表建议（数据已准备，可手动插入）
- ✅ 可选 PDF 导出

**报告结构** (以 research 为例):
1. 封面（标题、作者、日期）
2. 摘要
3. 目录（占位符，需在 Word 中手动更新）
4. 正文章节
5. 参考文献

**输出文件**:
- Word: `notebooklm-outputs/reports/报告标题-YYYYMMDD.docx`
- Markdown 预览: `notebooklm-outputs/reports/报告标题-YYYYMMDD.md`

---

## 🎯 使用场景示例

### 场景 1: 快速了解项目

```bash
# 1. 初始化
/notebook-init

# 2. 提问
/notebook-ask 项目的主要目标是什么？
/notebook-ask 当前进展如何？
```

---

### 场景 2: 深度研究

```bash
# 深度研究技术架构
/notebook-research 微服务架构设计

# 生成研究报告
/notebook-report research "微服务架构深度分析"
```

---

### 场景 3: 对比分析

```bash
# 对比两个方案
/notebook-compare 云部署方案 本地部署方案

# 生成对比报告
/notebook-report comparison "部署方案对比分析"
```

---

### 场景 4: 项目总结

```bash
# 整体摘要
/notebook-summarize

# 生成总结报告
/notebook-report summary "2024年项目总结"
```

---

### 场景 5: 智能建造方案生成（🌟 新功能）

```bash
# 1. 初始化知识库（添加相关技术文档）
/notebook-init

# 2. 使用参考模板生成实施方案
/notebook-clone-format ./templates/智能建造实施方案-模板.docx

# 3. 提供项目信息（交互式）
项目名称: 苏州工业园区智能建造示范项目
建设地点: 江苏省苏州市工业园区星湖街
建设单位: 苏州一建集团有限公司

# 4. AI自动从知识库提取内容并生成文档
# 输出: 格式一致、内容不同、查重率<20%的方案文档

# 5. 如需生成不同版本（进一步降低查重）
/notebook-clone-format ./templates/智能建造实施方案-模板.docx
```

**特点**:
- 每次生成内容都不同
- 自动从知识库提取BIM、智慧工地等技术内容
- 保持参考文档的排版格式
- 适用于申报资料、实施方案、技术文档等场景

---

## ⚙️ 技术特性

### 轻量级索引 + 按需加载
- 📍 只索引元数据（文件名、大小、修改时间）
- 🎯 根据问题动态决定读取哪些文档
- ⚡ 快速响应，节省 token

### 基于 Anthropic 官方 Document Skills
- 📄 DOCX - Word 文档处理
- 📊 XLSX - Excel 数据分析
- 🖼️ PPTX - PowerPoint 演示文稿
- 📑 PDF - PDF 文档解析

### 智能检索
- 🔍 三轮过滤: 文件名 → 元数据 → 内容预览
- 🧠 关键词匹配和相关度评分
- 📚 上下文构建和 token 预算管理

### 专业报告生成
- 📝 使用 python-docx 生成 Word 文档
- 🎨 三种风格: academic / business / technical
- 📊 自动表格和图表占位符
- 📖 完整引用管理

---

## 🔧 配置文件

### `.notebooklm/config.md`
知识库配置文件，包含:
- 知识库名称和描述
- 文档源路径列表
- 输出目录配置

### `.notebooklm/index/metadata.json`
文档索引文件（JSON 格式），包含:
- 所有文档的元数据
- 文件类型统计
- 关键词索引（可选）

---

## 📁 目录结构

```
项目根目录/
├── .notebooklm/              # 知识库配置
│   ├── config.md            # 配置文件
│   ├── index/               # 索引文件
│   │   ├── metadata.json   # JSON 索引
│   │   └── index.md        # 可读索引
│   ├── cache/               # 缓存
│   └── sessions/            # 会话记录
├── notebooklm-outputs/       # 输出文件
│   ├── summaries/           # 摘要
│   ├── insights/            # 洞察
│   ├── reports/             # 报告
│   └── chat-history/        # 对话历史
└── [您的文档目录]/           # 原始文档（只读）
```

---

## ❓ 常见问题

### Q: 如何添加新文档？
A: 将文档放到文档源目录，然后运行 `/notebook-index` 更新索引。

### Q: 支持哪些文档格式？
A: PDF、Word (.docx)、Excel (.xlsx)、PowerPoint (.pptx)、Markdown (.md)、纯文本 (.txt)。

### Q: 原始文档会被修改吗？
A: 不会！所有操作都是只读的，绝不修改您的原始文档。

### Q: 如何导出 PDF 报告？
A: 生成 Word 报告后，可以使用 `soffice --headless --convert-to pdf` 命令转换（需要安装 LibreOffice）。

### Q: 索引需要多久更新一次？
A: 添加新文档后手动运行 `/notebook-index`，未来会支持自动检测。

---

## 💡 最佳实践

1. **定期更新索引** - 添加新文档后运行 `/notebook-index`
2. **具体提问** - 问题越具体，答案越准确
3. **验证引用** - 重要信息请查看原始文档确认
4. **合理组织文档** - 使用有意义的文件名和目录结构
5. **保存重要对话** - 使用 `/notebook-chat` 的会话保存功能

---

## 🆘 获取支持

遇到问题？
- 查看配置文件: `.notebooklm/config.md`
- 查看索引状态: `.notebooklm/index/index.md`
- 重新初始化: `/notebook-init`

---

*NotebookLM Assistant v1.0.0*
*基于 Anthropic Claude Code 插件系统和官方 Document Skills*
