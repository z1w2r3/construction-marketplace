# NotebookLM Assistant - 安装指南

完整的安装和配置说明。

---

## 📋 系统要求

### 必需
- **Claude Code**: 最新版本
- **Python**: 3.8 或更高版本
- **操作系统**: macOS / Linux / Windows (WSL)

### 推荐
- **LibreOffice**: 用于 PDF 导出功能（可选）
- **磁盘空间**: 至少 100MB

---

## 🚀 快速安装

### 方式一：从 Marketplace 安装（推荐）

```bash
# 1. 添加 marketplace
claude marketplace add z1w2r3/construction-marketplace

# 2. 安装插件
claude marketplace install notebooklm-assistant

# 3. 验证安装
claude
> /notebook-help
```

### 方式二：本地开发安装

```bash
# 1. Clone 仓库
git clone https://github.com/z1w2r3/construction-marketplace.git
cd construction-marketplace/plugins/notebooklm-assistant

# 2. 安装 Python 依赖
cd mcp-servers/filesystem-indexer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd ../report-generator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 配置 Claude Code
# 将插件目录添加到 Claude Code
```

---

## 🔧 详细安装步骤

### 步骤 1: 安装 Python 依赖

#### Filesystem Indexer

```bash
cd mcp-servers/filesystem-indexer

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\\Scripts\\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

**依赖包**:
- `mcp>=1.0.0` - MCP SDK
- `python-docx>=1.1.0` - Word 文档处理
- `openpyxl>=3.1.0` - Excel 文档处理
- `PyPDF2>=3.0.0` - PDF 文档处理
- `pdfplumber>=0.10.0` - PDF 高级处理
- `chardet>=5.0.0` - 字符编码检测

#### Report Generator

```bash
cd mcp-servers/report-generator

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

**依赖包**:
- `mcp>=1.0.0` - MCP SDK
- `python-docx>=1.1.0` - Word 文档生成
- `reportlab>=4.0.0` - PDF 生成（可选）
- `Pillow>=10.0.0` - 图像处理（可选）

### 步骤 2: 配置 MCP 服务器

插件的 `.mcp.json` 文件已预配置，无需手动修改。

验证配置:
```bash
cat mcp-servers/.mcp.json
```

应该看到两个 MCP 服务器:
- `notebooklm-filesystem`
- `notebooklm-report-generator`

### 步骤 3: 测试 MCP 服务器

#### 测试 Filesystem Indexer

```bash
cd mcp-servers/filesystem-indexer
source venv/bin/activate
python server.py
```

如果正常启动，按 `Ctrl+C` 退出。

#### 测试 Report Generator

```bash
cd mcp-servers/report-generator
source venv/bin/activate
python server.py
```

如果正常启动，按 `Ctrl+C` 退出。

### 步骤 4: 安装可选依赖（LibreOffice）

用于 PDF 导出功能:

**macOS**:
```bash
brew install libreoffice
```

**Ubuntu/Debian**:
```bash
sudo apt-get install libreoffice
```

**验证安装**:
```bash
soffice --version
```

---

## ✅ 验证安装

### 1. 启动 Claude Code

```bash
claude
```

### 2. 测试插件命令

```bash
# 显示帮助
> /notebook-help

# 应该看到完整的命令列表
```

### 3. 初始化测试知识库

```bash
> /notebook-init

# 按提示输入测试路径
```

### 4. 验证 MCP 工具

```bash
# 在 Claude Code 中运行
> 请列出所有可用的 MCP 工具

# 应该看到:
# - scan_directory
# - preview_document
# - parse_document_smart
# - extract_keywords
# - generate_word_report
# - insert_table
# - list_templates
# - convert_to_pdf
```

---

## 🐛 故障排除

### 问题 1: MCP 服务器无法启动

**错误信息**: `command not found: python3`

**解决方案**:
```bash
# 检查 Python 版本
python3 --version

# 如果未安装，安装 Python 3
# macOS
brew install python3

# Ubuntu/Debian
sudo apt-get install python3 python3-pip
```

---

### 问题 2: 依赖安装失败

**错误信息**: `No module named 'mcp'`

**解决方案**:
```bash
# 确保在虚拟环境中
source venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 重新安装依赖
pip install -r requirements.txt
```

---

### 问题 3: run.sh 权限错误

**错误信息**: `Permission denied: run.sh`

**解决方案**:
```bash
# 添加执行权限
chmod +x mcp-servers/filesystem-indexer/run.sh
chmod +x mcp-servers/report-generator/run.sh
```

---

### 问题 4: Word 文档生成失败

**错误信息**: `No module named 'docx'`

**解决方案**:
```bash
cd mcp-servers/report-generator
source venv/bin/activate
pip install python-docx
```

---

### 问题 5: PDF 转换失败

**错误信息**: `LibreOffice not found`

**解决方案**:
```bash
# 安装 LibreOffice
brew install libreoffice  # macOS

# 或手动下载安装
# https://www.libreoffice.org/download/download/
```

---

## 🔍 日志和调试

### 查看 MCP 服务器日志

日志输出到 `stderr`，在 Claude Code 中可以看到。

### 启用调试模式

编辑 `.mcp.json`:
```json
{
  "mcpServers": {
    "notebooklm-filesystem": {
      "env": {
        "LOG_LEVEL": "DEBUG"  # 改为 DEBUG
      }
    }
  }
}
```

---

## 📦 卸载

### 完全卸载

```bash
# 1. 卸载插件
claude marketplace uninstall notebooklm-assistant

# 2. 删除虚拟环境（可选）
cd mcp-servers/filesystem-indexer
rm -rf venv

cd ../report-generator
rm -rf venv

# 3. 删除用户数据（可选）
# 在您的项目中
rm -rf .notebooklm
rm -rf notebooklm-outputs
```

---

## 🔄 更新插件

### 从 Marketplace 更新

```bash
# 检查更新
claude marketplace list --updates

# 更新插件
claude marketplace upgrade notebooklm-assistant
```

### 本地开发更新

```bash
# Pull 最新代码
cd construction-marketplace
git pull

# 重新安装依赖（如果有更新）
cd plugins/notebooklm-assistant/mcp-servers/filesystem-indexer
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

---

## 📞 获取帮助

遇到问题？

1. **查看文档**: 运行 `/notebook-help`
2. **查看日志**: 检查 MCP 服务器输出
3. **搜索 Issues**: [GitHub Issues](https://github.com/z1w2r3/construction-marketplace/issues)
4. **提交 Bug**: 创建新的 Issue 并提供:
   - 错误信息
   - 系统环境（OS、Python 版本）
   - 复现步骤

---

## ✨ 下一步

安装完成后:

1. 运行 `/notebook-help` 查看所有命令
2. 运行 `/notebook-init` 初始化您的知识库
3. 尝试提问: `/notebook-ask 你的问题`
4. 生成报告: `/notebook-report analysis "主题"`

**祝您使用愉快！** 🎉
