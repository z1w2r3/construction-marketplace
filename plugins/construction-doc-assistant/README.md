# 建筑施工文档助手 Claude Code 插件

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/z1w2r3/construction-marketplace)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

专为建筑施工行业设计的智能文档管理工具,帮助项目团队高效管理、分析和整理项目文档。

## ✨ 特性

- 🔒 **非侵入式设计** - 只读访问原文档,零风险
- 🤖 **智能化分析** - AI 驱动的文档理解和分析
- 📊 **标准化输出** - 符合建筑行业规范的报告格式
- 🚀 **易于使用** - 简单的命令行接口
- 🐍 **Python 集成** - 支持 Word/Excel/PDF 文档解析

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
- `/construction-summary [范围]` - 生成项目总结
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
