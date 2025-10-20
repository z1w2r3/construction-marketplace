# NotebookLM Assistant - 5分钟快速上手

> 最快速度体验智能文档助手

---

## ⚡ 3步开始使用

### 第1步: 安装依赖（仅首次）

```bash
# 进入插件目录
cd construction-marketplace/plugins/notebooklm-assistant

# 安装 Filesystem Indexer 依赖
cd mcp-servers/filesystem-indexer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 安装 Report Generator 依赖
cd ../report-generator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 第2步: 初始化知识库

```bash
# 启动 Claude Code
claude

# 初始化
> /notebook-init
```

按提示输入：
- 知识库名称: **我的文档库**（回车使用默认）
- 文档路径: `/Users/you/Documents`（您的文档目录）
- 用途描述: **个人文档管理**（可选）

### 第3步: 开始提问

```bash
> /notebook-ask 这个目录里有什么重要文档？
```

🎉 **完成！开始享受智能文档助手**

---

## 🎯 5个必试功能

### 1. 智能问答
```bash
> /notebook-ask 项目的主要目标是什么？
> /notebook-ask 有哪些风险？
> /notebook-ask 预算分配情况如何？
```

**特点**: 自动找相关文档，综合多个来源，标注信息来源

---

### 2. 深度研究
```bash
> /notebook-research 技术架构设计
```

**输出**: Markdown 研究报告（保存到 `notebooklm-outputs/insights/`）

---

### 3. 生成专业报告
```bash
> /notebook-report analysis "2024年项目分析"
```

**输出**:
- Word 文档（专业排版）: `notebooklm-outputs/reports/项目分析-YYYYMMDD.docx`
- Markdown 预览: `notebooklm-outputs/reports/项目分析-YYYYMMDD.md`

---

### 4. 文档对比
```bash
> /notebook-compare 方案A 方案B
```

**输出**: 对比分析报告（表格 + 文字）

---

### 5. 更新索引
```bash
# 添加新文档后
> /notebook-index
```

**作用**: 扫描新文档，更新索引

---

## 💡 实用技巧

### 技巧 1: 具体提问
❌ **不好**: "告诉我关于项目的信息"
✅ **更好**: "项目的预算是多少？分配到哪些部分？"

### 技巧 2: 使用关键词
✅ "关于**风险评估**的最新文档"
✅ "**2024年Q3**的进度报告"

### 技巧 3: 验证重要信息
📄 报告中的引用会标注来源，点击查看原文确认

### 技巧 4: 定期更新索引
添加新文档后运行 `/notebook-index`

### 技巧 5: 查看帮助
忘记命令？运行 `/notebook-help`

---

## 📊 报告类型选择

### Research Report - 研究报告
**适用**: 需要深入分析的主题
```bash
/notebook-report research "微服务架构研究"
```
**特点**: 完整的方法论、详细分析、学术风格

---

### Analysis Report - 分析报告
**适用**: 数据驱动的分析
```bash
/notebook-report analysis "项目预算执行分析"
```
**特点**: 数据图表、商业风格、洞察建议

---

### Comparison Report - 对比报告
**适用**: 多个方案对比
```bash
/notebook-report comparison "云部署vs本地部署"
```
**特点**: 对比矩阵、逐项分析、技术风格

---

### Summary Report - 总结报告
**适用**: 项目总结、季度报告
```bash
/notebook-report summary "2024Q3项目总结"
```
**特点**: 简明扼要、突出要点、商业风格

---

## 🔍 查看输出文件

### 索引文件
```bash
# 可读索引（Markdown）
cat .notebooklm/index/index.md

# JSON 索引（程序用）
cat .notebooklm/index/metadata.json
```

### 报告文件
```bash
# 列出所有报告
ls -la notebooklm-outputs/reports/

# 打开最新的 Word 报告
open notebooklm-outputs/reports/[最新文件].docx
```

---

## 🆘 快速故障排除

### 问题: MCP 工具不可用
```bash
# 检查虚拟环境是否激活
which python3
# 应该显示虚拟环境路径

# 重新安装依赖
cd mcp-servers/filesystem-indexer
source venv/bin/activate
pip install -r requirements.txt
```

### 问题: 找不到文档
```bash
# 检查配置
cat .notebooklm/config.md

# 重新初始化
/notebook-init
```

### 问题: 报告生成失败
```bash
# 检查 python-docx 是否安装
cd mcp-servers/report-generator
source venv/bin/activate
pip show python-docx

# 如果未安装
pip install python-docx
```

---

## 🎓 进阶使用

### 1. 多文档源
编辑 `.notebooklm/config.md`:
```markdown
## 文档源路径
- /Users/you/Documents/Work
- /Users/you/Dropbox/Research
- /Users/you/Downloads/PDFs
```

然后运行 `/notebook-index` 重新扫描。

### 2. 导出 PDF
生成 Word 报告后:
```bash
# 在 Claude Code 中
> 请使用 convert_to_pdf 工具将报告转为 PDF
```

（需要安装 LibreOffice）

### 3. 查看使用统计
```bash
# 文档数量
cat .notebooklm/index/metadata.json | grep "total_files"

# 报告数量
ls notebooklm-outputs/reports/ | wc -l
```

---

## 📚 更多资源

- **完整文档**: [README.md](README.md)
- **安装指南**: [INSTALL.md](INSTALL.md)
- **待完善功能**: [TODO.md](TODO.md)
- **在线帮助**: `/notebook-help`

---

## ⏱️ 5分钟速查表

| 操作 | 命令 | 耗时 |
|------|------|------|
| 初始化 | `/notebook-init` | 30秒 |
| 更新索引 | `/notebook-index` | 10秒 |
| 智能问答 | `/notebook-ask [问题]` | 5秒 |
| 深度研究 | `/notebook-research [主题]` | 30秒 |
| 生成报告 | `/notebook-report [类型] [主题]` | 2-5分钟 |

---

**开始您的智能文档之旅！** 🚀

有问题？运行 `/notebook-help` 或查看 [INSTALL.md](INSTALL.md)
