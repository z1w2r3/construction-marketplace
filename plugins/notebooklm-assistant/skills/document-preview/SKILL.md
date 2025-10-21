---
name: document-preview
description: "智能提取文档预览内容,用于索引增强和快速相关性判断。支持 PDF 目录提取、Word 标题提取、Excel sheet 概览"
---

# 文档预览提取指南

## 概述

本指南提供高效的文档预览提取方法,用于构建智能索引。预览数据帮助快速判断文档相关性,避免完整解析大文件。

**支持格式**: PDF, Word (.docx), Excel (.xlsx), PowerPoint (.pptx)

## PDF 预览提取

### 策略优先级

1. **首选**: 提取文档目录(TOC/Outline)
2. **次选**: 提取前 2 页文本
3. **补充**: 提取页数等元数据

### 完整实现

```python
import pdfplumber
import sys

def extract_pdf_preview(pdf_path, max_chars=500):
    """
    提取 PDF 预览:优先目录,其次前2页

    参数:
        pdf_path: PDF 文件路径
        max_chars: 最大预览字符数

    返回:
        包含预览数据的字典
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            preview_data = {
                "page_count": len(pdf.pages),
                "has_toc": False,
                "toc": [],
                "preview": "",
                "preview_error": None
            }

            # 1. 尝试提取目录
            if hasattr(pdf, 'outline') and pdf.outline:
                preview_data["has_toc"] = True
                # 提取前 10 个目录项
                for item in pdf.outline[:10]:
                    if isinstance(item, dict) and 'title' in item:
                        preview_data["toc"].append(item['title'])
                    elif hasattr(item, 'get'):
                        preview_data["toc"].append(item.get('title', ''))

            # 2. 提取前 2 页文本作为预览
            pages_to_read = min(2, len(pdf.pages))
            for i in range(pages_to_read):
                try:
                    page = pdf.pages[i]
                    text = page.extract_text() or ""
                    preview_data["preview"] += text

                    # 达到最大长度后停止
                    if len(preview_data["preview"]) >= max_chars:
                        break
                except Exception as e:
                    print(f"⚠️  PDF 页面 {i+1} 提取失败: {e}", file=sys.stderr)
                    continue

            # 截断到最大长度
            preview_data["preview"] = preview_data["preview"][:max_chars]

            return preview_data

    except Exception as e:
        return {
            "page_count": 0,
            "has_toc": False,
            "toc": [],
            "preview": "",
            "preview_error": str(e)
        }
```

### 优化:大文件处理

```python
def extract_pdf_preview_smart(pdf_path, max_pages=100):
    """针对大 PDF 文件的优化版本"""
    with pdfplumber.open(pdf_path) as pdf:
        page_count = len(pdf.pages)

        # 大文件(>100页)只提取目录,不提取内容
        if page_count > max_pages:
            preview_data = {
                "page_count": page_count,
                "has_toc": False,
                "toc": [],
                "preview": f"[大文件: {page_count} 页,仅提取目录]"
            }

            if hasattr(pdf, 'outline') and pdf.outline:
                preview_data["has_toc"] = True
                preview_data["toc"] = [
                    item.get('title', '') for item in pdf.outline[:10]
                ]

            return preview_data

        # 正常大小文件,完整提取
        return extract_pdf_preview(pdf_path)
```

## Word 文档预览提取

### 策略优先级

1. **首选**: 提取标题结构(Heading 1-6)
2. **次选**: 提取前 3 段正文
3. **补充**: 统计段落数

### 完整实现

```python
from docx import Document
import sys

def extract_docx_preview(docx_path, max_chars=500):
    """
    提取 Word 文档预览:标题列表 + 前3段

    参数:
        docx_path: Word 文档路径
        max_chars: 最大预览字符数

    返回:
        包含预览数据的字典
    """
    try:
        doc = Document(docx_path)

        preview_data = {
            "headings": [],
            "paragraph_count": len(doc.paragraphs),
            "preview": "",
            "preview_error": None
        }

        # 1. 提取所有标题
        for para in doc.paragraphs:
            style_name = para.style.name
            if style_name.startswith('Heading'):
                try:
                    # 提取标题级别(Heading 1 -> 1)
                    level = int(style_name.replace('Heading ', '').replace('标题 ', ''))
                    preview_data["headings"].append({
                        "level": level,
                        "text": para.text.strip()
                    })
                except ValueError:
                    # 处理非标准标题样式
                    preview_data["headings"].append({
                        "level": 0,
                        "text": para.text.strip()
                    })

        # 2. 提取前 3 段正文
        normal_paras = []
        for para in doc.paragraphs:
            if para.style.name in ['Normal', '正文']:
                text = para.text.strip()
                if text:  # 跳过空段落
                    normal_paras.append(text)
                    if len(normal_paras) >= 3:
                        break

        preview_data["preview"] = "\n\n".join(normal_paras)[:max_chars]

        return preview_data

    except Exception as e:
        return {
            "headings": [],
            "paragraph_count": 0,
            "preview": "",
            "preview_error": str(e)
        }
```

### 优化:大文件处理

```python
def extract_docx_preview_smart(docx_path, max_size_mb=10):
    """针对大 Word 文档的优化版本"""
    import os

    file_size_mb = os.path.getsize(docx_path) / (1024 * 1024)

    # 大文件(>10MB)只提取标题,不提取正文
    if file_size_mb > max_size_mb:
        doc = Document(docx_path)
        preview_data = {
            "headings": [],
            "paragraph_count": len(doc.paragraphs),
            "preview": f"[大文件: {file_size_mb:.1f} MB,仅提取标题]"
        }

        for para in doc.paragraphs:
            if para.style.name.startswith('Heading'):
                try:
                    level = int(para.style.name.replace('Heading ', ''))
                    preview_data["headings"].append({
                        "level": level,
                        "text": para.text.strip()
                    })
                except:
                    pass

        return preview_data

    # 正常大小文件,完整提取
    return extract_docx_preview(docx_path)
```

## Excel 表格预览提取

### 策略

1. **提取所有 sheet 名称**
2. **提取第一个 sheet 的前 5 行**
3. **统计 sheet 数量和行列信息**

### 完整实现

```python
from openpyxl import load_workbook
import sys

def extract_xlsx_preview(xlsx_path, max_rows=5):
    """
    提取 Excel 预览:sheet 名称 + 第一个 sheet 的前5行

    参数:
        xlsx_path: Excel 文件路径
        max_rows: 最大预览行数

    返回:
        包含预览数据的字典
    """
    try:
        # 使用 read_only 和 data_only 提高性能
        wb = load_workbook(xlsx_path, read_only=True, data_only=True)

        preview_data = {
            "sheet_names": wb.sheetnames,
            "sheet_count": len(wb.sheetnames),
            "first_sheet_preview": [],
            "preview_error": None
        }

        # 提取第一个 sheet 的前 N 行
        if wb.sheetnames:
            first_sheet = wb[wb.sheetnames[0]]

            # 获取实际行列数
            preview_data["first_sheet_rows"] = first_sheet.max_row
            preview_data["first_sheet_cols"] = first_sheet.max_column

            # 提取前 N 行数据
            for i, row in enumerate(first_sheet.iter_rows(values_only=True)):
                if i >= max_rows:
                    break
                # 转换为列表,处理 None 值
                row_data = [cell if cell is not None else "" for cell in row]
                preview_data["first_sheet_preview"].append(row_data)

        wb.close()
        return preview_data

    except Exception as e:
        return {
            "sheet_names": [],
            "sheet_count": 0,
            "first_sheet_preview": [],
            "preview_error": str(e)
        }
```

### 优化:大文件处理

```python
def extract_xlsx_preview_smart(xlsx_path, max_sheets=50):
    """针对大 Excel 文件的优化版本"""
    wb = load_workbook(xlsx_path, read_only=True, data_only=True)
    sheet_count = len(wb.sheetnames)

    # 大文件(>50 sheets)只扫描前 10 个 sheet
    if sheet_count > max_sheets:
        preview_data = {
            "sheet_names": wb.sheetnames[:10],
            "sheet_count": sheet_count,
            "first_sheet_preview": [],
            "note": f"大文件: {sheet_count} sheets,仅显示前10个"
        }

        # 只读第一个 sheet 的前 5 行
        if wb.sheetnames:
            first_sheet = wb[wb.sheetnames[0]]
            for i, row in enumerate(first_sheet.iter_rows(values_only=True)):
                if i >= 5:
                    break
                preview_data["first_sheet_preview"].append(list(row))

        wb.close()
        return preview_data

    # 正常大小文件,完整提取
    return extract_xlsx_preview(xlsx_path)
```

## PowerPoint 预览提取

### 策略

1. **提取幻灯片数量**
2. **提取每页标题**
3. **提取第一页文本预览**

### 完整实现

```python
from pptx import Presentation
import sys

def extract_pptx_preview(pptx_path, max_chars=500):
    """
    提取 PowerPoint 预览:幻灯片标题列表

    参数:
        pptx_path: PPT 文件路径
        max_chars: 最大预览字符数

    返回:
        包含预览数据的字典
    """
    try:
        prs = Presentation(pptx_path)

        preview_data = {
            "slide_count": len(prs.slides),
            "slide_titles": [],
            "preview": "",
            "preview_error": None
        }

        # 提取每页标题
        for slide in prs.slides:
            if slide.shapes.title:
                title_text = slide.shapes.title.text.strip()
                if title_text:
                    preview_data["slide_titles"].append(title_text)

        # 提取第一页的所有文本作为预览
        if prs.slides:
            first_slide = prs.slides[0]
            text_parts = []

            for shape in first_slide.shapes:
                if hasattr(shape, "text"):
                    text = shape.text.strip()
                    if text:
                        text_parts.append(text)

            preview_data["preview"] = "\n".join(text_parts)[:max_chars]

        return preview_data

    except Exception as e:
        return {
            "slide_count": 0,
            "slide_titles": [],
            "preview": "",
            "preview_error": str(e)
        }
```

## 批量预览提取

### 完整的批量处理实现

```python
import time

def batch_preview_documents(files, batch_size=10, timeout=10):
    """
    批量提取文档预览,包含进度显示和错误处理

    参数:
        files: 文件元数据列表(来自 filesystem-scan)
        batch_size: 显示进度的批次大小
        timeout: 单个文件处理超时(秒)

    返回:
        增强后的文件列表(包含预览数据)
    """
    total = len(files)
    processed = []
    errors = []

    print(f"📊 开始批量预览提取: 共 {total} 个文档")

    for i, file in enumerate(files):
        # 显示进度
        if i % batch_size == 0:
            print(f"   进度: {i}/{total} ({i*100//total}%)")

        # 设置超时保护
        start_time = time.time()

        try:
            # 根据文件类型调用对应的预览函数
            if file['extension'] == '.pdf':
                preview = extract_pdf_preview(file['path'])
            elif file['extension'] in ['.docx', '.doc']:
                preview = extract_docx_preview(file['path'])
            elif file['extension'] in ['.xlsx', '.xls']:
                preview = extract_xlsx_preview(file['path'])
            elif file['extension'] in ['.pptx', '.ppt']:
                preview = extract_pptx_preview(file['path'])
            else:
                preview = {"preview_error": "不支持的文件类型"}

            # 检查超时
            elapsed = time.time() - start_time
            if elapsed > timeout:
                preview["preview_error"] = f"处理超时({elapsed:.1f}秒)"

            # 合并预览数据到文件元数据
            file.update(preview)
            file["has_preview"] = preview.get("preview_error") is None

        except Exception as e:
            file["preview_error"] = str(e)
            file["has_preview"] = False
            errors.append({"file": file['path'], "error": str(e)})

        processed.append(file)

        # 每 50 个保存一次中间结果(可选)
        if (i + 1) % 50 == 0:
            save_intermediate_index(processed)

    print(f"✅ 预览提取完成: {total} 个文档")
    print(f"   成功: {len([f for f in processed if f.get('has_preview', False)])} 个")
    print(f"   失败: {len(errors)} 个")

    return processed, errors


def save_intermediate_index(files):
    """保存中间结果(可选实现)"""
    import json
    with open(".notebooklm/index/index_intermediate.json", "w", encoding="utf-8") as f:
        json.dump({"files": files}, f, ensure_ascii=False, indent=2)
```

## 使用建议

### 1. 索引时的最佳实践

```python
# 对所有文档进行预览提取
files = scan_directory("/path/to/docs")
files_with_preview, errors = batch_preview_documents(files)

# 保存索引
save_index(files_with_preview)

# 记录错误
if errors:
    save_error_log(errors)
```

### 2. 性能优化策略

```python
def extract_preview_adaptive(file):
    """根据文件大小自适应选择提取策略"""
    size_mb = file['size'] / (1024 * 1024)

    if size_mb > 10:
        # 大文件使用优化版本
        if file['extension'] == '.pdf':
            return extract_pdf_preview_smart(file['path'])
        elif file['extension'] == '.docx':
            return extract_docx_preview_smart(file['path'])
    else:
        # 小文件完整提取
        if file['extension'] == '.pdf':
            return extract_pdf_preview(file['path'])
        elif file['extension'] == '.docx':
            return extract_docx_preview(file['path'])
```

### 3. 错误容忍

- 单个文档提取失败不应中断整个批处理
- 使用 `preview_error` 字段记录错误原因
- 继续处理后续文档

## 预览数据格式

### PDF 预览数据

```python
{
    "page_count": 42,
    "has_toc": True,
    "toc": ["第一章 引言", "第二章 方法", "第三章 结论"],
    "preview": "这是文档的前500字符...",
    "preview_error": None  # 或错误信息
}
```

### Word 预览数据

```python
{
    "headings": [
        {"level": 1, "text": "项目概述"},
        {"level": 2, "text": "背景介绍"}
    ],
    "paragraph_count": 150,
    "preview": "这是前3段正文...",
    "preview_error": None
}
```

### Excel 预览数据

```python
{
    "sheet_names": ["销售数据", "统计分析", "图表"],
    "sheet_count": 3,
    "first_sheet_rows": 1000,
    "first_sheet_cols": 15,
    "first_sheet_preview": [
        ["姓名", "部门", "销售额"],
        ["张三", "华东", 125000],
        ["李四", "华北", 98000]
    ],
    "preview_error": None
}
```

## 常见问题

### Q: 如何处理加密的 PDF/Word 文档?

A: 捕获异常并标记:

```python
try:
    preview = extract_pdf_preview(pdf_path)
except Exception as e:
    if "password" in str(e).lower() or "encrypted" in str(e).lower():
        preview = {"preview_error": "文档已加密,无法预览"}
    else:
        preview = {"preview_error": str(e)}
```

### Q: 提取目录时遇到格式问题怎么办?

A: 使用容错处理:

```python
toc_items = []
for item in pdf.outline[:10]:
    try:
        if isinstance(item, dict):
            toc_items.append(item.get('title', '未命名'))
        else:
            toc_items.append(str(item))
    except:
        continue  # 跳过格式异常的项
```

### Q: 如何避免内存溢出?

A:
1. 使用 `read_only=True` 打开大文件
2. 只读取前 N 页/行,不全量加载
3. 及时关闭文件句柄

## 相关 Skills

- [filesystem-scan](../filesystem-scan/SKILL.md) - 文件系统扫描
- [pdf](../pdf/SKILL.md) - PDF 完整处理
- [docx](../docx/SKILL.md) - Word 完整处理
- [xlsx](../xlsx/SKILL.md) - Excel 完整处理
- [pptx](../pptx/SKILL.md) - PowerPoint 完整处理
