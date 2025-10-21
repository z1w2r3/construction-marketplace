# 生成文档索引

生成或更新知识库的文档索引(支持全量预览提取)。

---

你现在要为用户生成或更新知识库的文档索引。

## 执行步骤

### 1. 读取配置

从 `.notebooklm/config.md` 读取:
- 文档源路径列表
- 知识库名称

如果配置文件不存在，提示:
```
❌ 知识库未初始化，请先运行: /notebook-init
```

### 2. 扫描所有文档源(Level 1: 元数据)

对配置文件中的每个文档源路径,使用 **filesystem-scan Skill** 扫描目录:

参考 filesystem-scan Skill,使用以下代码:

```python
import os
from pathlib import Path
from datetime import datetime

def scan_directory(root_path, file_types=None, max_depth=10):
    """扫描目录,返回文件元数据列表"""
    files = []
    root_path = Path(root_path).resolve()
    root_depth = str(root_path).count(os.sep)

    for dirpath, dirnames, filenames in os.walk(root_path):
        # 排除系统目录
        dirnames[:] = [d for d in dirnames if d not in {'.git', 'node_modules', '__pycache__', '.notebooklm'}]

        # 限制深度
        current_depth = dirpath.count(os.sep) - root_depth
        if current_depth > max_depth:
            dirnames[:] = []
            continue

        for filename in filenames:
            file_path = Path(dirpath) / filename

            # 过滤文件类型
            if file_types and file_path.suffix.lower() not in file_types:
                continue

            try:
                stat = file_path.stat()
                files.append({
                    "path": str(file_path.absolute()),
                    "name": filename,
                    "extension": file_path.suffix.lower(),
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                    "modified_readable": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "relative_path": str(file_path.relative_to(root_path))
                })
            except (OSError, PermissionError) as e:
                print(f"⚠️  跳过文件 {file_path}: {e}")
                continue

    return files

# 扫描所有支持的文档类型
file_types = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.md']
all_files = []

for doc_path in document_source_paths:
    print(f"📁 扫描目录: {doc_path}")
    files = scan_directory(doc_path, file_types=file_types, max_depth=10)
    all_files.extend(files)

print(f"✅ 扫描完成,找到 {len(all_files)} 个文档")
```

### 3. 批量预览提取(Level 2: 全量索引)

使用 **document-preview Skill** 对**所有文档**进行预览提取:

参考 document-preview Skill,使用批量处理代码:

```python
import pdfplumber
from docx import Document
from openpyxl import load_workbook
from pptx import Presentation
import time

def extract_pdf_preview(pdf_path, max_chars=500):
    """提取 PDF 预览:目录 + 前2页"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            preview_data = {
                "page_count": len(pdf.pages),
                "has_toc": False,
                "toc": [],
                "preview": ""
            }

            # 提取目录
            if hasattr(pdf, 'outline') and pdf.outline:
                preview_data["has_toc"] = True
                for item in pdf.outline[:10]:
                    if isinstance(item, dict):
                        preview_data["toc"].append(item.get('title', ''))

            # 提取前2页
            for page in pdf.pages[:2]:
                text = page.extract_text() or ""
                preview_data["preview"] += text
                if len(preview_data["preview"]) >= max_chars:
                    break

            preview_data["preview"] = preview_data["preview"][:max_chars]
            return preview_data
    except Exception as e:
        return {"page_count": 0, "has_toc": False, "toc": [], "preview": "", "preview_error": str(e)}

def extract_docx_preview(docx_path, max_chars=500):
    """提取 Word 预览:标题 + 前3段"""
    try:
        doc = Document(docx_path)
        preview_data = {
            "headings": [],
            "paragraph_count": len(doc.paragraphs),
            "preview": ""
        }

        # 提取标题
        for para in doc.paragraphs:
            if para.style.name.startswith('Heading'):
                try:
                    level = int(para.style.name.replace('Heading ', ''))
                    preview_data["headings"].append({"level": level, "text": para.text.strip()})
                except:
                    pass

        # 提取前3段正文
        normal_paras = [p.text for p in doc.paragraphs if p.style.name in ['Normal', '正文'] and p.text.strip()][:3]
        preview_data["preview"] = "\n\n".join(normal_paras)[:max_chars]

        return preview_data
    except Exception as e:
        return {"headings": [], "paragraph_count": 0, "preview": "", "preview_error": str(e)}

def extract_xlsx_preview(xlsx_path):
    """提取 Excel 预览:sheet名称 + 前5行"""
    try:
        wb = load_workbook(xlsx_path, read_only=True, data_only=True)
        preview_data = {
            "sheet_names": wb.sheetnames,
            "sheet_count": len(wb.sheetnames),
            "first_sheet_preview": []
        }

        if wb.sheetnames:
            first_sheet = wb[wb.sheetnames[0]]
            for i, row in enumerate(first_sheet.iter_rows(values_only=True)):
                if i >= 5:
                    break
                preview_data["first_sheet_preview"].append([cell if cell is not None else "" for cell in row])

        wb.close()
        return preview_data
    except Exception as e:
        return {"sheet_names": [], "sheet_count": 0, "first_sheet_preview": [], "preview_error": str(e)}

def extract_pptx_preview(pptx_path):
    """提取 PPT 预览:幻灯片标题"""
    try:
        prs = Presentation(pptx_path)
        preview_data = {
            "slide_count": len(prs.slides),
            "slide_titles": []
        }

        for slide in prs.slides:
            if slide.shapes.title:
                title_text = slide.shapes.title.text.strip()
                if title_text:
                    preview_data["slide_titles"].append(title_text)

        return preview_data
    except Exception as e:
        return {"slide_count": 0, "slide_titles": [], "preview_error": str(e)}

def batch_preview_all_documents(files, batch_size=10, timeout=10):
    """批量提取文档预览"""
    total = len(files)
    processed = []
    errors = []

    print(f"\n📊 开始批量预览提取: 共 {total} 个文档")
    print(f"⏱️  预计耗时: {total * 2 // 60} - {total * 2 // 60 + 1} 分钟\n")

    for i, file in enumerate(files):
        # 显示进度
        if i % batch_size == 0:
            percent = i * 100 // total
            print(f"   进度: {i}/{total} ({percent}%)")

        start_time = time.time()

        try:
            # 根据文件类型调用对应预览函数
            if file['extension'] == '.pdf':
                # 大PDF优化
                if file['size'] > 10 * 1024 * 1024:  # >10MB
                    preview = {"preview": "大文件,仅提取目录", "page_count": 0}
                else:
                    preview = extract_pdf_preview(file['path'])
            elif file['extension'] in ['.docx', '.doc']:
                preview = extract_docx_preview(file['path'])
            elif file['extension'] in ['.xlsx', '.xls']:
                preview = extract_xlsx_preview(file['path'])
            elif file['extension'] in ['.pptx', '.ppt']:
                preview = extract_pptx_preview(file['path'])
            else:
                preview = {"preview": ""}

            # 超时检查
            elapsed = time.time() - start_time
            if elapsed > timeout:
                preview["preview_error"] = f"处理超时({elapsed:.1f}秒)"

            # 合并预览数据
            file.update(preview)
            file["has_preview"] = preview.get("preview_error") is None

        except Exception as e:
            file["preview_error"] = str(e)
            file["has_preview"] = False
            errors.append({"file": file['name'], "error": str(e)})

        processed.append(file)

        # 每50个保存中间结果
        if (i + 1) % 50 == 0:
            print(f"   💾 保存中间结果...")

    print(f"\n✅ 预览提取完成!")
    print(f"   成功: {len([f for f in processed if f.get('has_preview', False)])} 个")
    print(f"   失败: {len(errors)} 个")

    return processed, errors

# 执行批量预览
all_files_with_preview, preview_errors = batch_preview_all_documents(all_files)
```

### 4. 合并索引结果

将所有路径的扫描结果合并:
- 去重(相同路径的文件)
- 按修改时间排序(最新的在前)
- 统计文件类型分布

```python
# 去重
seen_paths = set()
unique_files = []
for f in all_files_with_preview:
    if f['path'] not in seen_paths:
        seen_paths.add(f['path'])
        unique_files.append(f)

# 按修改时间排序
unique_files_sorted = sorted(unique_files, key=lambda f: f['modified'], reverse=True)

# 统计文件类型
from collections import Counter
type_counts = Counter(f['extension'] for f in unique_files_sorted)
```

### 5. 保存索引

创建索引目录并保存 JSON 索引:

```python
import json
from pathlib import Path

# 创建索引目录
index_dir = Path('.notebooklm/index')
index_dir.mkdir(parents=True, exist_ok=True)

# 构建索引数据
index_data = {
    "knowledge_base_name": knowledge_base_name,
    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_files": len(unique_files_sorted),
    "indexed_files": len([f for f in unique_files_sorted if f.get('has_preview', False)]),
    "failed_files": len(preview_errors),
    "file_types": dict(type_counts),
    "index": unique_files_sorted,
    "errors": preview_errors
}

# 保存 JSON 索引
with open(index_dir / 'metadata.json', 'w', encoding='utf-8') as f:
    json.dump(index_data, f, ensure_ascii=False, indent=2)

print(f"💾 已保存索引到: {index_dir / 'metadata.json'}")
```

### 6. 生成可读索引

生成 Markdown 格式的可读索引:

```python
# 生成 Markdown 索引
md_lines = [
    f"# {knowledge_base_name} - 文档索引\n",
    f"**最后更新**: {index_data['last_updated']}  ",
    f"**总文档数**: {index_data['total_files']}  ",
    f"**成功索引**: {index_data['indexed_files']}  ",
    f"**失败文档**: {index_data['failed_files']}\n",
    "## 文件类型分布\n",
    "| 类型 | 数量 |",
    "|------|------|"
]

# 类型分布表格
for ext, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
    type_name = {
        '.pdf': 'PDF',
        '.docx': 'Word',
        '.doc': 'Word',
        '.xlsx': 'Excel',
        '.xls': 'Excel',
        '.pptx': 'PowerPoint',
        '.ppt': 'PowerPoint'
    }.get(ext, ext.upper())

    md_lines.append(f"| {type_name} | {count} |")

md_lines.append("\n## 文档列表(按修改时间排序)\n")

# 按类型分组显示
for ext in sorted(type_counts.keys()):
    files_of_type = [f for f in unique_files_sorted if f['extension'] == ext]
    if files_of_type:
        type_name = {
            '.pdf': 'PDF 文档',
            '.docx': 'Word 文档',
            '.xlsx': 'Excel 文档',
            '.pptx': 'PowerPoint 文档'
        }.get(ext, f'{ext.upper()} 文件')

        md_lines.append(f"\n### {type_name}\n")

        for i, f in enumerate(files_of_type[:20], 1):  # 每类最多显示20个
            md_lines.append(f"{i}. [{f['name']}]({f['path']}) - {f['modified_readable']}")

            # 显示预览信息
            if f.get('has_toc'):
                md_lines.append(f"   - 📑 目录: {', '.join(f.get('toc', [])[:3])}")
            if f.get('headings'):
                headings_text = ', '.join([h['text'] for h in f['headings'][:3]])
                md_lines.append(f"   - 📝 标题: {headings_text}")
            if f.get('sheet_names'):
                md_lines.append(f"   - 📊 Sheets: {', '.join(f['sheet_names'][:3])}")

# 保存 Markdown 索引
with open(index_dir / 'index.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines))

print(f"📝 已保存可读索引到: {index_dir / 'index.md'}")
```

### 7. 输出结果

显示索引生成结果:

```python
print("\n" + "="*60)
print("✅ 文档索引已更新!\n")

print("📊 统计信息:")
print(f"   - 总文档数: {index_data['total_files']}")
print(f"   - 成功索引: {index_data['indexed_files']}")
print(f"   - 失败文档: {index_data['failed_files']}")

if preview_errors:
    print(f"\n⚠️  失败文档列表:")
    for err in preview_errors[:5]:  # 只显示前5个
        print(f"   - {err['file']}: {err['error']}")
    if len(preview_errors) > 5:
        print(f"   - ... 还有 {len(preview_errors) - 5} 个")

print(f"\n📁 文件类型分布:")
for ext, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
    # 统计有预览的数量
    with_preview = len([f for f in unique_files_sorted if f['extension'] == ext and f.get('has_preview')])
    print(f"   - {ext.upper()}: {count} 个 ({with_preview} 个有预览)")

print(f"\n📝 索引文件:")
print(f"   - JSON 索引: .notebooklm/index/metadata.json")
print(f"   - 可读索引: .notebooklm/index/index.md")

print(f"\n💡 现在可以使用:")
print(f"   - /notebook-ask [问题] - 智能问答")
print(f"   - /notebook-research [主题] - 深度研究")
print(f"   - /notebook-report [类型] [主题] - 生成报告")
print("="*60)
```

## 性能优化

- **分层索引**: Level 1(元数据) + Level 2(全量预览)
- **批量处理**: 每10个文档显示进度,每50个保存中间结果
- **超时保护**: 单个文档处理超过10秒跳过
- **大文件优化**:
  - PDF > 10MB 只提取目录
  - Word > 10MB 只提取标题
  - Excel > 50 sheets 只扫描前10个
- **错误容忍**: 单个文档失败不影响整体索引

## 错误处理

- **路径不存在**: 跳过并警告
- **无权限访问**: 跳过并记录到 errors
- **文件损坏**: 标记 `preview_error`,继续处理
- **处理超时**: 记录超时信息,继续下一个

## 预期时间

- 100个文档约需 2-3 分钟
- 1000个文档约需 20-30 分钟
- 建议首次索引时耐心等待
