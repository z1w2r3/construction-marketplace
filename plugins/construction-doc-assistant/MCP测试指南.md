# MCP 文档读取测试指南

> **目的**: 验证 docxtpl MCP 服务器的文档读取功能是否正常工作
> **测试时间**: 预计 15-30 分钟
> **前置条件**: 已安装 docxtpl MCP 服务器

---

## 📋 测试前准备

### 1. 确认 MCP 服务器状态

检查 docxtpl MCP 服务器是否已配置:

```bash
# 查看 MCP 配置
cat ~/.claude/config.json | grep -A 5 "docxtpl"
```

如果没有配置,参考 docxtpl 的官方文档进行安装配置。

### 2. 准备测试文档

创建测试文档目录:

```bash
mkdir -p ~/test-docs/
cd ~/test-docs/
```

准备以下测试文档:
- ✅ **Word 文档** (.docx) - 包含文本和表格
- ✅ **Excel 文档** (.xlsx) - 包含数据表
- ✅ **PDF 文档** (.pdf) - 包含文本内容

**快速创建测试文档**:

```bash
# 如果您有现成的建筑项目文档,可以复制几个过来
cp /Volumes/MOVESPEED/projectDocs2/苏州一建0518项目/*.docx ~/test-docs/
cp /Volumes/MOVESPEED/projectDocs2/苏州一建0518项目/*.xlsx ~/test-docs/
```

---

## 🧪 测试步骤

### 测试 1: 验证文档可读性 ⭐

**目的**: 测试 `validate_document` 工具

**步骤**:

1. 在 Claude Code 中打开一个对话
2. 运行以下测试命令:

```
请使用 mcp__docxtpl__validate_document 工具验证以下文档:
- file_path: ~/test-docs/test.docx

如果文档有效,返回 valid: true 和文档信息。
```

**预期结果**:
```
✅ 成功返回:
- valid: true
- file_name: test.docx
- file_size: XXX bytes
- file_type: docx
```

**如果失败**:
- ❌ 检查文件路径是否正确
- ❌ 检查文件是否存在
- ❌ 检查 MCP 服务器是否运行

---

### 测试 2: 解析 Word 文档 ⭐⭐

**目的**: 测试 `parse_docx_document` 工具

**步骤**:

```
请使用 mcp__docxtpl__parse_docx_document 工具解析文档:
- file_path: ~/test-docs/test.docx
- include_tables: true

返回文档的段落和表格内容。
```

**预期结果**:
```json
{
  "status": "success",
  "paragraphs": [
    "第一段内容...",
    "第二段内容..."
  ],
  "tables": [
    {
      "headers": ["列1", "列2"],
      "rows": [[...], [...]]
    }
  ],
  "metadata": {
    "author": "...",
    "created": "..."
  }
}
```

**验证点**:
- ✅ 能正确提取段落文本
- ✅ 能正确提取表格数据
- ✅ 中文内容显示正常
- ✅ 返回文档元数据

---

### 测试 3: 解析 Excel 文档 ⭐⭐

**目的**: 测试 `parse_excel_document` 工具

**步骤**:

```
请使用 mcp__docxtpl__parse_excel_document 工具解析文档:
- file_path: ~/test-docs/test.xlsx
- include_formulas: false

返回工作表数据。
```

**预期结果**:
```json
{
  "status": "success",
  "sheets": [
    {
      "name": "Sheet1",
      "rows": 100,
      "cols": 5,
      "data": [[...], [...]]
    }
  ]
}
```

**验证点**:
- ✅ 能读取所有工作表
- ✅ 能正确提取单元格数据
- ✅ 数字、日期格式正确
- ✅ 中文内容显示正常

---

### 测试 4: 解析 PDF 文档 ⭐

**目的**: 测试 `parse_pdf_document` 工具

**步骤**:

```
请使用 mcp__docxtpl__parse_pdf_document 工具解析文档:
- file_path: ~/test-docs/test.pdf
- include_tables: true
- pages: "all"

返回PDF文档内容。
```

**预期结果**:
```json
{
  "status": "success",
  "page_count": 5,
  "pages": [
    {
      "page_number": 1,
      "text": "页面文本内容..."
    }
  ]
}
```

**验证点**:
- ✅ 能读取PDF文本
- ✅ 能识别页数
- ✅ 文本提取基本准确

---

### 测试 5: 获取文档元数据 ⭐

**目的**: 测试 `get_document_metadata` 工具

**步骤**:

```
请使用 mcp__docxtpl__get_document_metadata 工具:
- file_path: ~/test-docs/test.docx

返回文档元数据信息。
```

**预期结果**:
```json
{
  "file_name": "test.docx",
  "file_size": 12345,
  "created_time": "2024-01-01T00:00:00",
  "modified_time": "2024-01-01T00:00:00",
  "file_extension": ".docx"
}
```

**验证点**:
- ✅ 返回文件基本信息
- ✅ 时间格式正确
- ✅ 文件大小准确

---

### 测试 6: 集成测试 - 在命令中使用 ⭐⭐⭐

**目的**: 在实际命令中测试MCP工具

**步骤 1**: 初始化测试项目

```
/construction-init
```

按提示输入:
- 项目名称: 测试项目
- 项目类型: 1 (通用)
- 原文档目录: ~/test-docs/

**步骤 2**: 运行项目总结命令

```
/construction-summary
```

**预期行为**:
1. ✅ 扫描 ~/test-docs/ 目录
2. ✅ 找到 Word、Excel、PDF 文档
3. ✅ 验证每个文档 (validate_document)
4. ✅ 解析每个文档 (parse_xxx_document)
5. ✅ 生成文档读取状态表
6. ✅ 生成项目总结报告

**检查生成的报告**:

```bash
cat 生成文件/项目总结/项目总结-整体-*.md
```

应该包含:
- ✅ 文档读取情况表格
- ✅ 提取的文档内容
- ✅ 数据来源标注
- ✅ 状态标识 (✅/⚠️/❌)

---

## 🔍 故障排查

### 问题 1: MCP 服务器未响应

**症状**: 调用 MCP 工具时没有响应或超时

**解决方案**:
```bash
# 1. 检查 MCP 服务器是否在配置中
cat ~/.claude/config.json

# 2. 重启 Claude Code
# 3. 检查日志
tail -f ~/.claude/logs/mcp-*.log
```

### 问题 2: 文档解析失败

**症状**: 返回 status: "error" 或 valid: false

**可能原因**:
- ❌ 文件路径不正确
- ❌ 文件损坏
- ❌ 文件格式不支持 (.doc 旧格式)
- ❌ 文件权限不足

**解决方案**:
```bash
# 检查文件是否存在
ls -la ~/test-docs/test.docx

# 检查文件权限
chmod 644 ~/test-docs/test.docx

# 尝试转换文件格式 (如果是 .doc)
# 使用 LibreOffice 或 Microsoft Word 转换为 .docx
```

### 问题 3: 中文内容乱码

**症状**: 返回的中文内容显示为乱码

**解决方案**:
- ✅ 确认文档保存为 UTF-8 编码
- ✅ 检查 MCP 服务器日志
- ✅ 重新保存文档

### 问题 4: 表格数据不完整

**症状**: 表格只提取了部分数据

**原因**:
- 可能设置了行数限制
- 表格结构复杂 (合并单元格)

**解决方案**:
- 检查返回结果的行数限制
- 简化表格结构测试

---

## ✅ 测试检查清单

完成以下测试后打勾:

### 基础功能测试
- [ ] validate_document - 验证 Word 文档
- [ ] validate_document - 验证 Excel 文档
- [ ] validate_document - 验证 PDF 文档
- [ ] parse_docx_document - 解析 Word 文档
- [ ] parse_excel_document - 解析 Excel 文档
- [ ] parse_pdf_document - 解析 PDF 文档
- [ ] get_document_metadata - 获取元数据

### 边界测试
- [ ] 空文档处理
- [ ] 大文件处理 (>50MB)
- [ ] 中文文件名和内容
- [ ] 损坏文档处理

### 集成测试
- [ ] /construction-init 命令
- [ ] /construction-summary 命令
- [ ] /construction-check 命令
- [ ] 查看生成的报告质量

### 性能测试
- [ ] 单文档解析时间 < 5秒
- [ ] 批量处理 (5个文档) < 30秒

---

## 📊 测试结果记录

### 测试环境
- 操作系统: macOS / Linux / Windows
- Claude Code 版本:
- MCP docxtpl 版本:
- 测试时间: YYYY-MM-DD

### 测试结果

| 测试项 | 状态 | 备注 |
|--------|------|------|
| validate_document (Word) | ✅/❌ | |
| validate_document (Excel) | ✅/❌ | |
| parse_docx_document | ✅/❌ | |
| parse_excel_document | ✅/❌ | |
| parse_pdf_document | ✅/❌ | |
| get_document_metadata | ✅/❌ | |
| /construction-summary | ✅/❌ | |
| 中文内容处理 | ✅/❌ | |
| 性能测试 | ✅/❌ | |

### 发现的问题

1. 问题描述:
   - 解决方案:

2. 问题描述:
   - 解决方案:

---

## 🎯 测试通过标准

所有测试通过的标准:

1. ✅ **基础功能** (8/8)
   - 所有 MCP 工具能正常调用
   - 返回正确的数据格式
   - 错误处理友好

2. ✅ **中文支持** (3/3)
   - 中文文件名正常
   - 中文内容正常显示
   - 不出现乱码

3. ✅ **集成测试** (3/3)
   - 命令能正常使用 MCP 工具
   - 生成的报告质量良好
   - 包含完整的文档读取状态

4. ✅ **性能测试** (2/2)
   - 单文档处理时间合理
   - 批量处理不卡顿

---

## 📚 参考资料

### MCP docxtpl 工具文档
- [docxtpl GitHub](https://github.com/elapouya/python-docx-template)
- [MCP Protocol](https://modelcontextprotocol.io/)

### 项目文档
- [README.md](./README.md)
- [CHANGELOG.md](./CHANGELOG.md)
- [CLAUDE.md](../../CLAUDE.md)

---

## 💡 测试完成后

### 如果测试全部通过 ✅
1. 记录测试结果
2. 开始使用真实项目文档
3. 持续监控性能和稳定性

### 如果有测试失败 ❌
1. 查看故障排查章节
2. 检查 MCP 服务器日志
3. 提交 Issue 到项目仓库

### 反馈和改进
发现问题或有改进建议,请联系:
- GitHub Issues: https://github.com/z1w2r3/construction-marketplace/issues

---

**测试愉快!** 🚀
