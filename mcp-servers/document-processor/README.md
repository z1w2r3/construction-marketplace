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

```bash
# 安装依赖
cd mcp-servers/document-processor
pip install -r requirements.txt
```

## 测试

```bash
# 测试服务器是否可以启动
python3 server.py
```

## 使用

此 MCP 服务器通过 Claude Code 插件自动启动和管理。在命令文件中可以直接调用工具。

## 开发注意事项

1. **日志输出**: 只能写到 stderr,不能写到 stdout
2. **错误处理**: 捕获所有异常,返回清晰的错误信息
3. **性能**: 大文件只提取关键信息,避免超时
4. **安全**: 验证文件路径,防止访问敏感目录
