# NotebookLM Assistant

> 智能文档助手 - 类似 Google NotebookLM 的知识库问答、深度研究和专业报告生成工具

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/z1w2r3/construction-marketplace)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🌟 核心特性

### 🎯 智能问答
基于您的文档库回答问题，自动检索相关内容并综合分析。

### 🔬 深度研究
对特定主题进行全面研究，构建知识图谱，发现隐藏洞察。

### 📊 专业报告生成
自动生成专业排版的 Word 报告（研究报告/分析报告/对比报告/总结报告）。

### 📚 基于 Anthropic 官方 Document Skills
完整支持 DOCX、PDF、XLSX、PPTX 等文档格式的专业处理。

---

## 🚀 快速开始

### 1. 安装插件

```bash
# 方式一：从 Marketplace 安装（推荐）
claude marketplace add z1w2r3/construction-marketplace
claude marketplace install notebooklm-assistant

# 方式二：本地安装
git clone https://github.com/z1w2r3/construction-marketplace.git
cd construction-marketplace/plugins/notebooklm-assistant
# 按照 INSTALL.md 的步骤操作
```

### 2. 初始化知识库

```bash
claude
> /notebook-init
```

按提示输入：
- 知识库名称（可选）
- 文档源路径（必需，如 `/Users/you/Documents/ProjectDocs`）
- 用途描述（可选）

### 3. 开始使用

```bash
# 智能问答
> /notebook-ask 项目的主要风险是什么？

# 深度研究
> /notebook-research 技术架构设计

# 生成报告
> /notebook-report analysis "2024年项目执行情况分析"
```

---

## 📖 主要命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `/notebook-init` | 初始化知识库 | `/notebook-init` |
| `/notebook-index` | 更新文档索引 | `/notebook-index` |
| `/notebook-ask` | 智能问答 | `/notebook-ask 预算是多少？` |
| `/notebook-research` | 深度研究 | `/notebook-research 微服务架构` |
| `/notebook-summarize` | 生成摘要 | `/notebook-summarize` |
| `/notebook-compare` | 文档对比 | `/notebook-compare 方案A 方案B` |
| `/notebook-report` | 生成报告 | `/notebook-report research "主题"` |
| `/notebook-help` | 帮助文档 | `/notebook-help` |

详细说明请运行 `/notebook-help`

---

## 🎨 核心设计理念

### 轻量级索引 + 按需加载

```
传统方法：一次性读取所有文档 → 慢、占用大量 tokens
我们的方法：只索引元数据 → 快速、按需加载
```

**索引内容**（轻量）:
- 文件名、路径、大小
- 修改时间
- 文件类型
- 关键词（可选）

**按需加载**（智能）:
Claude 根据问题决定读取哪些文档。

### 三轮智能检索

1. **文件名匹配** - 快速过滤（< 1秒）
2. **元数据筛选** - 精准定位（考虑时间、类型）
3. **内容预览** - 相关度评分（读取前 500 字符）

---

## 📊 报告类型

### Research Report（研究报告）
**适用**: 深度分析、学术研究、技术调研
**风格**: Academic
**特点**: 完整的方法论、详细的发现、深入的讨论

### Analysis Report（分析报告）
**适用**: 数据分析、绩效分析、市场分析
**风格**: Business
**特点**: 数据驱动、图表支持、洞察建议

### Comparison Report（对比报告）
**适用**: 方案对比、版本对比、竞品分析
**风格**: Technical
**特点**: 逐项对比、对比矩阵、客观结论

### Summary Report（总结报告）
**适用**: 项目总结、季度报告、简报
**风格**: Business
**特点**: 简明扼要、突出要点、行动导向

---

## 🔧 技术架构

```
┌─────────────────────────────────────────────┐
│          Commands (用户命令层)                │
│  notebook-ask, notebook-report, etc.        │
└───────────────┬─────────────────────────────┘
                │
                ├─────────────────────┐
                │                     │
┌───────────────▼───────┐  ┌──────────▼──────────────┐
│  Custom Skills        │  │ Official Document Skills│
│  - smart-retrieval    │  │ - docx (Word)           │
│  - context-builder    │  │ - pdf (PDF)             │
│  - report-structure   │  │ - xlsx (Excel)          │
│  - citation-manager   │  │ - pptx (PowerPoint)     │
└───────────┬───────────┘  └──────────┬──────────────┘
            │                         │
            └────────┬────────────────┘
                     │
┌────────────────────▼──────────────────────────┐
│          新增 Skills (辅助层)                   │
│  - filesystem-scan (文件系统扫描)              │
│  - document-preview (文档预览提取)             │
└───────────────────────────────────────────────┘
```

---

## 📁 目录结构

初始化后的项目结构:

```
您的项目/
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

## 💡 使用场景

### 场景 1: 快速了解新项目

```bash
/notebook-init
/notebook-ask 项目的主要目标是什么？
/notebook-ask 当前进展如何？
/notebook-summarize
```

### 场景 2: 深度技术研究

```bash
/notebook-research 微服务架构设计
/notebook-report research "微服务架构深度分析"
```

### 场景 3: 方案对比决策

```bash
/notebook-compare 云部署方案 本地部署方案
/notebook-report comparison "部署方案对比分析"
```

### 场景 4: 定期项目总结

```bash
/notebook-summarize
/notebook-report summary "2024Q3 项目总结"
```

---

## ⚙️ 配置

### 文档源路径

编辑 `.notebooklm/config.md`:

```markdown
## 文档源路径
- /Users/you/Documents/ProjectDocs
- /Users/you/Dropbox/Research
```

---

## 🔒 安全与隐私

- ✅ **只读访问**: 绝不修改您的原始文档
- ✅ **本地运行**: 所有处理在本地完成
- ✅ **数据隐私**: 文档内容不离开您的设备
- ✅ **开源透明**: 完整源代码可审查

---

## 📝 支持的文档格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| PDF | `.pdf` | 完整支持（包括表格提取） |
| Word | `.docx`, `.doc` | 完整支持（包括样式、表格） |
| Excel | `.xlsx`, `.xls` | 完整支持（包括公式） |
| PowerPoint | `.pptx`, `.ppt` | 完整支持（包括备注） |
| Markdown | `.md` | 完整支持 |
| 纯文本 | `.txt` | 完整支持 |

---

## 🆘 故障排除

### 问题：索引生成失败

**解决方案**:
1. 检查文档路径是否正确
2. 检查文件权限
3. 查看日志: `.notebooklm/logs/`

### 问题：报告生成错误

**解决方案**:
1. 确保安装了 `python-docx`: `pip install python-docx`
2. 检查输出目录权限
3. 重新初始化: `/notebook-init`

---

## 🚧 开发路线图

### v1.0.0（当前版本）
- [x] 核心问答功能
- [x] 文档索引
- [x] 专业报告生成
- [x] 基于官方 Document Skills

### v1.1.0（计划中）
- [ ] 对话模式（持续会话）
- [ ] 语义搜索（embedding）
- [ ] 图表自动插入（Word 图表）
- [ ] 多语言支持

### v2.0.0（远期）
- [ ] 知识图谱可视化
- [ ] 协作功能（团队知识库）
- [ ] API 接口
- [ ] Web 界面

---

## 🤝 贡献

欢迎贡献代码、报告 Bug 或提出功能建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [Anthropic](https://anthropic.com) - Claude AI 和官方 Document Skills
- [Claude Code](https://claude.com/claude-code) - 插件系统
- 所有贡献者

---

## 📧 联系方式

- GitHub: [z1w2r3/construction-marketplace](https://github.com/z1w2r3/construction-marketplace)
- Issues: [GitHub Issues](https://github.com/z1w2r3/construction-marketplace/issues)

---

**享受智能文档分析的乐趣！** 🎉
