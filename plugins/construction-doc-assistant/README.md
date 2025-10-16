# 建筑施工文档助手 Claude Code 插件

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/z1w2r3/construction-marketplace)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

专为建筑施工行业设计的智能文档管理工具,帮助项目团队高效管理、分析和整理项目文档。

## ✨ 特性

- 🔒 **非侵入式设计** - 只读访问原文档,零风险
- 🤖 **智能化分析** - AI 驱动的文档理解和分析
- 📊 **标准化输出** - 符合建筑行业规范的报告格式
- 🚀 **易于使用** - 简单的命令行接口
- 🐍 **Python 集成** - 支持 Word/Excel/PDF 文档解析
- 🎨 **自定义模板** - 支持使用Word文档创建自定义报告模板
- 🔄 **模板复用** - 保存常用模板,随时调用

## 🎯 目标用户

- **项目经理** - 快速了解项目状态,生成汇报材料
- **资料员** - 检查资料完整性,整理归档
- **技术负责人** - 技术文档管理,方案编制
- **监理工程师** - 验收资料审核

## 📦 安装

### 系统要求

- **Python**: 3.8 或更高版本
- **Claude Code**: 最新版本
- **操作系统**: macOS / Linux / Windows

### 方式 1: 从 GitHub Marketplace 安装(推荐)

#### macOS / Linux 用户

```bash
# 1. 添加 marketplace
/plugin marketplace add z1w2r3/construction-marketplace

# 2. 安装插件
/plugin install construction-doc-assistant@construction-marketplace

# 3. 安装 Python 依赖(必需!)
cd ~/.claude/plugins/marketplaces/construction-marketplace/plugins/construction-doc-assistant/mcp-servers/document-processor
./install.sh
```

#### Windows 用户

```powershell
# 1. 在 Claude Code 中添加 marketplace
/plugin marketplace add z1w2r3/construction-marketplace

# 2. 安装插件
/plugin install construction-doc-assistant@construction-marketplace

# 3. 安装 Python 依赖(必需!)
cd %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers\document-processor
install.bat

# 4. 配置 MCP 服务器(Windows 专用步骤)
cd %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers
setup-windows.bat

# 5. 重启 VSCode
# Ctrl + Shift + P → 输入 "Reload Window" → 回车
```

**📖 Windows 详细安装指南**: [WINDOWS-SETUP.md](mcp-servers/WINDOWS-SETUP.md)

**⚠️ 重要**:
- 必须运行安装脚本安装 Python 依赖,否则文档解析功能无法工作!
- Windows 用户必须运行 `setup-windows.bat` 配置 MCP 服务器

### 方式 2: 本地开发安装

#### macOS / Linux

```bash
# 1. 克隆仓库
git clone https://github.com/z1w2r3/construction-marketplace.git
cd construction-marketplace/plugins/construction-doc-assistant

# 2. 安装 Python 依赖
cd mcp-servers/document-processor
./install.sh
```

#### Windows

```powershell
# 1. 克隆仓库
git clone https://github.com/z1w2r3/construction-marketplace.git
cd construction-marketplace\plugins\construction-doc-assistant

# 2. 安装 Python 依赖
cd mcp-servers\document-processor
install.bat

# 3. 配置 MCP
cd ..\
setup-windows.bat
```

### 安装验证

#### macOS / Linux

```bash
# 验证所有依赖已正确安装
python3 -c "
import mcp, docx, openpyxl, PyPDF2, pptx
print('✅ 所有依赖已正确安装')
"
```

#### Windows

```powershell
# 验证 MCP 服务器状态
# 在 Claude Code 中运行
/debug mcp

# 应显示: ✓ construction-doc-processor: running
```

### 常见安装问题

#### macOS / Linux

- **问题**: `./install.sh: Permission denied`
  - **解决**: `chmod +x install.sh && ./install.sh`

- **问题**: `python3: command not found`
  - **解决**: 安装 Python 3.8+: https://www.python.org/downloads/

#### Windows

- **问题**: `未找到 Python`
  - **解决**: 安装 Python 并勾选 "Add Python to PATH"

- **问题**: MCP 服务器显示 `failed`
  - **解决**: 确保已运行 `setup-windows.bat` 配置脚本

- **问题**: `找不到 PowerShell`
  - **解决**: 参考 [WINDOWS-SETUP.md](mcp-servers/WINDOWS-SETUP.md) 手动修改配置文件

## 🚀 快速开始

### 1. 初始化项目

在您的施工项目目录下运行:

```bash
claude

# 在 Claude Code 中执行
/construction-init
```

按提示输入项目信息和原文档目录路径。

### 2. 生成文档索引

```bash
/construction-index
```

扫描原文档目录,生成结构化索引。

### 3. 检查资料完整性

```bash
# 全面检查
/construction-check

# 专项检查
/construction-check 主体结构验收资料
```

### 4. 查看帮助

```bash
/construction-help
```

## 📖 命令列表

### 初始化配置
- `/construction-init` - 初始化项目配置

### 文档分析
- `/construction-index` - 生成文档索引
- `/construction-check [范围]` - 检查资料完整性
- `/construction-search <关键词>` - 搜索文档内容

### 方案生成
- `/construction-organize <资料类型>` - 生成整理方案
- `/construction-summary [范围] [选项]` - 生成项目总结报告
  - `--template <类型>` - 指定报告模板
  - `--custom-template <Word文件>` - 使用自定义Word模板
  - `--save-template` - 保存自定义模板
  - `--list-templates` - 列出所有可用模板
- `/construction-progress` - 分析项目进度

### 帮助支持
- `/construction-help` - 显示帮助信息

## 📁 目录结构

项目初始化后会创建以下结构:

```
项目目录/
├── .claude/
│   └── CLAUDE-construction.md      # 项目配置文件
├── 生成文件/                        # 所有输出内容
│   ├── 索引/                        # 文档索引
│   ├── 分析报告/                    # 完整性检查、进度分析
│   ├── 整理方案/                    # 整理方案
│   └── 项目总结/                    # 项目总结报告
└── 建筑施工文档助手使用说明.md
```

## 🐍 Python MCP 服务器

插件包含一个 Python MCP 服务器,提供文档解析功能:

- **parse_word_document** - 解析 Word 文档
- **parse_excel_document** - 解析 Excel 文档
- **parse_pdf_document** - 解析 PDF 文档
- **get_document_metadata** - 获取文档元数据

### 安装依赖

```bash
pip install mcp python-docx openpyxl PyPDF2
```

## 🎨 自定义模板功能 (v1.1.0新增)

### 功能概述

从v1.1.0开始,插件支持使用您自己的Word文档作为报告模板,实现完全自定义的报告结构。

### 使用场景

- **月度总结** - 使用公司固定的月度总结模板
- **专项汇报** - 创建特定技术专项的汇报模板
- **验收材料** - 按照业主要求的格式生成验收文档
- **内部报告** - 使用团队约定的报告格式

### 快速开始

#### 1. 查看可用模板

```bash
/construction-summary --list-templates
```

查看所有内置模板和已保存的自定义模板。

#### 2. 使用自定义Word模板(临时使用)

```bash
/construction-summary --custom-template ~/Documents/月度总结模板.docx
```

系统会:
- 自动提取Word文档的章节结构(标题1/2/3)
- 根据章节结构生成报告
- 本次使用后不保存模板

#### 3. 保存自定义模板(长期复用)

```bash
/construction-summary --custom-template ~/Documents/月度总结模板.docx --save-template
```

系统会询问:
- 模板名称(如: `custom_monthly_report`)
- 适用场景描述
- 保存后可以通过 `--template` 参数随时调用

#### 4. 使用已保存的模板

```bash
/construction-summary --template custom_monthly_report
```

### Word模板要求

**✅ 必须使用标题样式**:
- 在Word中使用"标题1"、"标题2"、"标题3"样式
- 不要只是手动加粗文字

**✅ 支持自动清理序号**:
- "一、项目概况" → "项目概况"
- "1. 基本信息" → "基本信息"
- "(1) 建设规模" → "建设规模"
- 系统会自动清理常见序号格式

**示例模板结构**:
```
一、项目概况            (标题1)
  1.1 基本信息          (标题2)
  1.2 参建单位          (标题2)
二、本月完成情况        (标题1)
  2.1 施工进度          (标题2)
  2.2 质量管理          (标题2)
三、存在问题及建议      (标题1)
```

### 模板管理

**查看所有模板**:
```bash
/construction-summary --list-templates
```

**删除自定义模板**:
1. 打开 `~/.claude/plugins/.../templates/report_templates.json`
2. 删除对应的模板对象
3. 保存文件

**修改模板**:
直接编辑 `report_templates.json` 文件

详细文档: [templates/template_matcher.md - 第六章](templates/template_matcher.md)

---

## 💡 使用示例

### 检查主体结构验收资料

```bash
/construction-check 主体结构验收资料
```

### 生成质量验收资料整理方案

```bash
/construction-organize 质量验收资料
```

### 搜索混凝土相关信息

```bash
/construction-search 混凝土强度
```

### 生成第一季度项目总结

```bash
/construction-summary 第一季度
```

## ⚠️ 重要提示

- ✅ 插件只会**只读访问**原文档目录
- ✅ **不会修改、移动或删除**任何原始文件
- ⚠️ 生成的报告和建议**仅供参考**
- ⚠️ 关键信息请人工验证

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🔗 相关链接

- [GitHub 仓库](https://github.com/z1w2r3/construction-marketplace)
- [Claude Code 文档](https://docs.claude.com/en/docs/claude-code)
- [MCP 协议](https://modelcontextprotocol.io)

## 📮 联系方式

- 项目仓库: https://github.com/z1w2r3/construction-marketplace
- Issue 反馈: https://github.com/z1w2r3/construction-marketplace/issues

---

**版本**: 1.0.2
**更新日期**: 2025-10-15
**支持平台**: macOS / Linux / Windows
