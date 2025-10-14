# 建筑施工文档处理 MCP 服务器

这是一个用于建筑施工文档助手的 MCP (Model Context Protocol) 服务器,提供 Word、Excel、PDF 文档的解析和分析功能。

## 功能

### 1. parse_word_document
解析 Word 文档,提取文本、表格和元数据。

**参数**:
- `file_path` (必需): Word 文档的绝对路径
- `extract_tables` (可选): 是否提取表格,默认 true

**返回**: 文档内容包括段落、表格信息

### 2. parse_excel_document
解析 Excel 文档,提取工作表和单元格数据。

**参数**:
- `file_path` (必需): Excel 文档的绝对路径
- `sheet_name` (可选): 工作表名称,默认读取所有工作表

**返回**: 工作表列表和数据预览

### 3. parse_pdf_document
解析 PDF 文档,提取文本和元数据。

**参数**:
- `file_path` (必需): PDF 文档的绝对路径

**返回**: 页面文本预览

### 4. get_document_metadata
获取文档元数据。

**参数**:
- `file_path` (必需): 文档的绝对路径

**返回**: 文件名、大小、创建时间、修改时间等

## 安装

⚠️ **重要**: MCP 服务器的 Python 依赖需要单独安装,Claude Code 不会自动安装。

### 方式1: 使用自动安装脚本(推荐)

```bash
cd mcp-servers/document-processor
./install.sh
```

安装脚本会:
1. 检测 Python 版本(需要 3.8+)
2. 创建虚拟环境(可选但推荐)
3. 安装所有 Python 依赖
4. 安装系统依赖(macOS: libmagic)
5. 验证安装是否成功

### 方式2: 手动安装

```bash
cd mcp-servers/document-processor

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# macOS 用户需要安装 libmagic
brew install libmagic
```

## 配置说明

插件的 `.mcp.json` 配置文件会自动使用虚拟环境中的 Python:

```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/mcp-servers/document-processor/venv/bin/python",
  "args": ["${CLAUDE_PLUGIN_ROOT}/mcp-servers/document-processor/server.py"]
}
```

`${CLAUDE_PLUGIN_ROOT}` 会自动解析为插件安装目录。

## 验证安装

### 测试 Python 依赖

```bash
cd mcp-servers/document-processor
source venv/bin/activate
python -c "import mcp, docx, openpyxl, pptx, PyPDF2; print('✓ 所有依赖已安装')"
```

### 测试 MCP 服务器

```bash
cd mcp-servers/document-processor
source venv/bin/activate
python server.py
```

如果看到类似输出表示服务器可以正常启动:
```
INFO:mcp.server.stdio:Server running
```

## 使用

此 MCP 服务器通过 Claude Code 插件自动启动和管理。

安装插件后:
1. ✅ MCP 服务器配置自动加载
2. ✅ 插件启用时服务器自动启动
3. ✅ 在命令文件中可以直接调用工具

**重启后生效**: 修改 MCP 配置后需要重启 Claude Code/VSCode。

## 开发注意事项

1. **日志输出**: 只能写到 stderr,不能写到 stdout
2. **错误处理**: 捕获所有异常,返回清晰的错误信息
3. **性能**: 大文件只提取关键信息,避免超时
4. **安全**: 验证文件路径,防止访问敏感目录
