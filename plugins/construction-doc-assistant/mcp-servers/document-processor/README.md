# 建筑施工文档处理 MCP 服务器

这是一个用于建筑施工文档助手的 MCP (Model Context Protocol) 服务器,提供 Word、Excel、PDF 文档的解析和分析功能。

## 功能

### 核心特性: 双模式解析

所有文档解析工具都支持 **`parse_mode`** 参数,提供两种解析深度:

- **`summary` 模式**(默认): 快速扫描,返回摘要内容,控制 token 消耗
- **`full` 模式**: 深度解析,返回完整内容,不限制长度

### 1. parse_word_document
解析 Word 文档,提取文本、表格和元数据。

**参数**:
- `file_path` (必需): Word 文档的绝对路径
- `parse_mode` (可选): 解析模式,`summary`(默认) 或 `full`
- `extract_tables` (可选): 是否提取表格,默认 true
- `max_paragraphs` (可选): 最大段落数,仅在 `summary` 模式生效

**返回**: 文档内容包括段落、表格信息

**示例**:
```python
# 摘要模式 - 快速扫描(提取前100段)
parse_word_document(file_path="report.docx", parse_mode="summary")

# 完整模式 - 深度解析(提取所有段落)
parse_word_document(file_path="report.docx", parse_mode="full")
```

### 2. parse_excel_document
解析 Excel 文档,提取工作表和单元格数据。

**参数**:
- `file_path` (必需): Excel 文档的绝对路径
- `parse_mode` (可选): 解析模式,`summary`(默认) 或 `full`
- `sheet_name` (可选): 工作表名称,默认读取所有工作表
- `max_rows` (可选): 每个工作表最大行数,仅在 `summary` 模式生效,默认 100

**返回**: 工作表列表和数据

**示例**:
```python
# 摘要模式 - 每个工作表最多100行
parse_excel_document(file_path="data.xlsx", parse_mode="summary")

# 完整模式 - 提取所有行
parse_excel_document(file_path="data.xlsx", parse_mode="full")
```

### 3. parse_powerpoint_document
解析 PowerPoint 文档,提取幻灯片内容、标题和备注。

**参数**:
- `file_path` (必需): PowerPoint 文档的绝对路径
- `parse_mode` (可选): 解析模式,`summary`(默认) 或 `full`
- `max_slides` (可选): 最大幻灯片数,仅在 `summary` 模式生效,默认 50
- `extract_notes` (可选): 是否提取备注,默认 true

**返回**: 幻灯片内容和备注

### 4. parse_pdf_document
解析 PDF 文档,提取文本和元数据。

**参数**:
- `file_path` (必需): PDF 文档的绝对路径
- `parse_mode` (可选): 解析模式,`summary`(默认) 或 `full`
- `max_pages` (可选): 最大页数,仅在 `summary` 模式生效,默认 50
- `extract_tables` (可选): 是否提取表格,默认 false

**返回**: 页面文本

### 5. extract_document_summary
智能提取文档摘要,支持关键词过滤。

**参数**:
- `file_path` (必需): 文档的绝对路径
- `focus_keywords` (可选): 关注的关键词列表
- `max_length` (可选): 摘要最大字符数,默认 2000

**返回**: 智能摘要和关键信息

### 6. get_document_metadata
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

## 最佳实践

### 两阶段文档读取策略

推荐使用以下策略来平衡性能和完整性:

**阶段 1: 快速扫描 (使用 `summary` 模式)**
```python
# 批量扫描文档,识别关键文档
parse_word_document(file_path="方案1.docx", parse_mode="summary")
parse_word_document(file_path="方案2.docx", parse_mode="summary")
parse_word_document(file_path="方案3.docx", parse_mode="summary")

# 根据摘要判断哪些文档需要深度分析
```

**阶段 2: 深度解析 (使用 `full` 模式)**
```python
# 只对关键文档使用 full 模式
parse_word_document(file_path="重要方案.docx", parse_mode="full")
```

### 何时使用哪种模式

| 场景 | 推荐模式 | 原因 |
|------|---------|------|
| 批量文档索引 | `summary` | 快速扫描,节省 token |
| 文档搜索定位 | `summary` | 找到相关文档即可 |
| 生成详细报告 | `full` | 需要完整信息 |
| 提取表格数据 | `full` | 确保数据完整 |
| 项目总结分析 | 先 `summary` 后 `full` | 两阶段策略 |

### Token 消耗估算

- **`summary` 模式**: 每个文档约 1000-5000 tokens
- **`full` 模式**: 每个文档约 5000-50000 tokens (取决于文档大小)

## 开发注意事项

1. **日志输出**: 只能写到 stderr,不能写到 stdout
2. **错误处理**: 捕获所有异常,返回清晰的错误信息
3. **性能**: 大文件只提取关键信息,避免超时
4. **安全**: 验证文件路径,防止访问敏感目录
5. **模式选择**: 优先使用 `summary` 模式,仅在必要时使用 `full` 模式
