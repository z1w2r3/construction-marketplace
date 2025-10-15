# 更新日志

## v1.3.0 (2025-10-16)

### 新增功能: 双模式解析

为所有文档解析工具添加了 `parse_mode` 参数,支持两种解析深度:

#### ✨ 主要改进

1. **新增 `parse_mode` 参数**
   - `summary` 模式(默认): 快速扫描,返回摘要内容,控制 token 消耗
   - `full` 模式: 深度解析,返回完整内容,不限制长度

2. **影响的工具**
   - `parse_word_document`: 支持 summary(前100段) / full(所有段落)
   - `parse_excel_document`: 支持 summary(每表100行) / full(所有行)
   - `parse_powerpoint_document`: 支持 summary(前50张) / full(所有幻灯片)
   - `parse_pdf_document`: 支持 summary(前50页) / full(所有页)

3. **智能限制调整**
   - `summary` 模式: 自动应用默认限制(max_paragraphs, max_rows 等)
   - `full` 模式: 自动移除所有限制,提取完整内容

4. **用户友好提示**
   - 解析结果中显示使用的模式
   - `summary` 模式提示可切换到 `full` 模式
   - `full` 模式警告可能消耗大量 token

#### 📝 使用示例

```python
# 摘要模式 - 快速扫描
parse_word_document(
    file_path="report.docx",
    parse_mode="summary"  # 默认值,可省略
)

# 完整模式 - 深度解析
parse_word_document(
    file_path="report.docx",
    parse_mode="full"
)
```

#### 🎯 推荐使用策略

**两阶段读取策略**:
1. **阶段1**: 使用 `summary` 模式批量扫描,识别关键文档
2. **阶段2**: 对关键文档使用 `full` 模式深度解析

#### 🔄 向后兼容性

- ✅ **完全向后兼容**: 默认使用 `summary` 模式
- ✅ **现有调用无需修改**: 所有现有代码继续正常工作
- ✅ **可选升级**: 需要完整内容时添加 `parse_mode="full"`

#### 📊 测试结果

**Word 文档测试**:
- 摘要模式: 5 段落 (限制生效)
- 完整模式: 15 段落 (提取全部) ✅

**Excel 文档测试**:
- 摘要模式: 10 行 (限制生效)
- 完整模式: 37 行 (提取全部) ✅

#### 📚 文档更新

- 更新 [README.md](README.md) - 添加双模式使用说明和最佳实践
- 新增使用示例和 token 消耗估算
- 添加两阶段读取策略指南

---

## v1.2.0

### 新增功能
- Markdown 转 Word 文档生成
- 支持多种报告模板类型
- 自动格式化和样式应用

---

## v1.1.0

### 新增功能
- PowerPoint 文档解析
- 批量文档处理
- 智能摘要提取

---

## v1.0.0

### 初始版本
- Word 文档解析
- Excel 文档解析
- PDF 文档解析
- 文档元数据提取
