---
name: format-analyzer
description: "Word文档格式深度分析器 - 解析OOXML结构,提取样式、字体、段落格式、页面设置等完整格式信息,用于精确复制文档排版。"
---

# Format Analyzer - Word文档格式分析器

## 技能说明

这是一个专业的Word文档格式分析工具,能够深度解析OOXML(Office Open XML)结构,提取文档的完整格式信息,包括样式、字体、段落格式、页面设置等,用于实现文档格式的精确复制。

**核心能力**:
- 📐 页面设置分析(纸张大小、页边距、方向)
- 🎨 样式定义提取(标题、正文、表格等样式)
- 🔤 字体信息分析(字体名称、字号、颜色、效果)
- 📏 段落格式提取(对齐、缩进、间距、行距)
- 📊 表格格式分析(边框、填充、单元格样式)
- 📄 节属性提取(分栏、页眉页脚)

**应用场景**:
- 文档格式克隆
- 模板格式提取
- 格式标准化检查
- 文档格式对比

---

## 输入参数

| 参数名 | 类型 | 必需 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `document_path` | string | ✅ | - | Word文档路径(.docx) |
| `extract_styles` | boolean | ⚠️ | true | 是否提取样式定义 |
| `extract_page_settings` | boolean | ⚠️ | true | 是否提取页面设置 |
| `extract_paragraph_formats` | boolean | ⚠️ | true | 是否提取段落格式 |
| `extract_font_details` | boolean | ⚠️ | true | 是否提取字体详情 |
| `extract_table_formats` | boolean | ⚠️ | false | 是否提取表格格式 |

---

## 执行逻辑

### 前提条件

在执行分析前,需要解压Word文档:

```bash
# 使用docx skill中的解压工具
python skills/docx/ooxml/scripts/unpack.py <document_path> /tmp/unpacked_doc
```

解压后的目录结构:
```
/tmp/unpacked_doc/
├── word/
│   ├── document.xml         # 主文档内容
│   ├── styles.xml           # 样式定义
│   ├── numbering.xml        # 编号定义
│   ├── settings.xml         # 文档设置
│   └── fontTable.xml        # 字体表
├── docProps/
│   ├── core.xml             # 核心属性
│   └── app.xml              # 应用属性
└── _rels/
    └── .rels                # 关系文件
```

---

### 阶段 1: 页面设置分析

#### 步骤 1.1: 解析节属性(sectPr)

Word文档的页面设置存储在 `<w:sectPr>` 元素中,位于 `document.xml` 的文档末尾或每个节的末尾。

```python
#!/usr/bin/env python3
"""页面设置分析脚本"""
from lxml import etree
from pathlib import Path

def extract_page_settings(unpacked_dir):
    """提取页面设置"""

    doc_xml = Path(unpacked_dir) / "word" / "document.xml"
    tree = etree.parse(str(doc_xml))
    root = tree.getroot()

    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    }

    page_settings = {
        "page_size": {},
        "margins": {},
        "orientation": "",
        "columns": {},
        "headers_footers": {}
    }

    # 查找最后一个节属性(通常是全文档设置)
    sect_pr = root.findall('.//w:sectPr', ns)[-1] if root.findall('.//w:sectPr', ns) else None

    if sect_pr is None:
        return page_settings

    # 1. 页面尺寸
    pg_sz = sect_pr.find('.//w:pgSz', ns)
    if pg_sz is not None:
        width = pg_sz.get('{%s}w' % ns['w'])
        height = pg_sz.get('{%s}h' % ns['w'])
        orient = pg_sz.get('{%s}orient' % ns['w'])

        page_settings["page_size"] = {
            "width_twips": int(width) if width else 11906,  # A4默认宽度
            "height_twips": int(height) if height else 16838,  # A4默认高度
            "width_cm": round(int(width) / 567, 2) if width else 21.0,  # 1cm = 567 twips
            "height_cm": round(int(height) / 567, 2) if height else 29.7,
            "paper_type": detect_paper_type(int(width) if width else 11906,
                                           int(height) if height else 16838)
        }
        page_settings["orientation"] = orient or "portrait"

    # 2. 页边距
    pg_mar = sect_pr.find('.//w:pgMar', ns)
    if pg_mar is not None:
        page_settings["margins"] = {
            "top_twips": int(pg_mar.get('{%s}top' % ns['w']) or 1440),
            "bottom_twips": int(pg_mar.get('{%s}bottom' % ns['w']) or 1440),
            "left_twips": int(pg_mar.get('{%s}left' % ns['w']) or 1800),
            "right_twips": int(pg_mar.get('{%s}right' % ns['w']) or 1800),
            "header_twips": int(pg_mar.get('{%s}header' % ns['w']) or 720),
            "footer_twips": int(pg_mar.get('{%s}footer' % ns['w']) or 720),
            # 转换为厘米
            "top_cm": round(int(pg_mar.get('{%s}top' % ns['w']) or 1440) / 567, 2),
            "bottom_cm": round(int(pg_mar.get('{%s}bottom' % ns['w']) or 1440) / 567, 2),
            "left_cm": round(int(pg_mar.get('{%s}left' % ns['w']) or 1800) / 567, 2),
            "right_cm": round(int(pg_mar.get('{%s}right' % ns['w']) or 1800) / 567, 2)
        }

    # 3. 分栏设置
    cols = sect_pr.find('.//w:cols', ns)
    if cols is not None:
        num_cols = cols.get('{%s}num' % ns['w'])
        space = cols.get('{%s}space' % ns['w'])

        page_settings["columns"] = {
            "num_columns": int(num_cols) if num_cols else 1,
            "space_twips": int(space) if space else 720,
            "equal_width": cols.get('{%s}equalWidth' % ns['w']) != "0"
        }

    return page_settings

def detect_paper_type(width_twips, height_twips):
    """检测纸张类型"""

    paper_types = {
        "A4": (11906, 16838),
        "A3": (16838, 23811),
        "Letter": (12240, 15840),
        "Legal": (12240, 20160),
        "B5": (9920, 14032)
    }

    # 允许一定误差(100 twips)
    tolerance = 100

    for paper_name, (std_width, std_height) in paper_types.items():
        if (abs(width_twips - std_width) < tolerance and
            abs(height_twips - std_height) < tolerance):
            return paper_name

    return "Custom"
```

**输出示例**:
```json
{
  "page_size": {
    "width_twips": 11906,
    "height_twips": 16838,
    "width_cm": 21.0,
    "height_cm": 29.7,
    "paper_type": "A4"
  },
  "margins": {
    "top_twips": 1440,
    "bottom_twips": 1440,
    "left_twips": 1800,
    "right_twips": 1800,
    "top_cm": 2.54,
    "bottom_cm": 2.54,
    "left_cm": 3.18,
    "right_cm": 3.18
  },
  "orientation": "portrait",
  "columns": {
    "num_columns": 1,
    "space_twips": 720,
    "equal_width": true
  }
}
```

---

### 阶段 2: 样式定义提取

#### 步骤 2.1: 解析styles.xml

```python
def extract_styles(unpacked_dir):
    """提取样式定义"""

    styles_xml = Path(unpacked_dir) / "word" / "styles.xml"
    if not styles_xml.exists():
        return {}

    tree = etree.parse(str(styles_xml))
    root = tree.getroot()

    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    }

    styles = {}

    # 遍历所有样式
    for style in root.findall('.//w:style', ns):
        style_id = style.get('{%s}styleId' % ns['w'])
        style_type = style.get('{%s}type' % ns['w'])

        if not style_id:
            continue

        # 样式名称
        name_elem = style.find('.//w:name', ns)
        style_name = name_elem.get('{%s}val' % ns['w']) if name_elem is not None else style_id

        # 提取样式详情
        style_detail = {
            "id": style_id,
            "name": style_name,
            "type": style_type,  # paragraph, character, table, numbering
            "base_on": None,
            "font": {},
            "paragraph": {}
        }

        # 基于的样式
        based_on = style.find('.//w:basedOn', ns)
        if based_on is not None:
            style_detail["base_on"] = based_on.get('{%s}val' % ns['w'])

        # 字体属性
        r_pr = style.find('.//w:rPr', ns)
        if r_pr is not None:
            style_detail["font"] = extract_font_properties(r_pr, ns)

        # 段落属性
        p_pr = style.find('.//w:pPr', ns)
        if p_pr is not None:
            style_detail["paragraph"] = extract_paragraph_properties(p_pr, ns)

        styles[style_id] = style_detail

    return styles
```

#### 步骤 2.2: 提取字体属性

```python
def extract_font_properties(r_pr, ns):
    """提取字体属性"""

    font_props = {
        "font_name": None,
        "font_name_ascii": None,
        "font_name_east_asia": None,
        "font_size": None,  # 半磅为单位
        "font_size_pt": None,  # 磅为单位
        "bold": False,
        "italic": False,
        "underline": None,
        "color": None,
        "highlight": None,
        "strike": False
    }

    # 字体名称
    r_fonts = r_pr.find('.//w:rFonts', ns)
    if r_fonts is not None:
        font_props["font_name_ascii"] = r_fonts.get('{%s}ascii' % ns['w'])
        font_props["font_name_east_asia"] = r_fonts.get('{%s}eastAsia' % ns['w'])
        font_props["font_name"] = font_props["font_name_east_asia"] or font_props["font_name_ascii"]

    # 字号
    sz = r_pr.find('.//w:sz', ns)
    if sz is not None:
        size_half_pt = sz.get('{%s}val' % ns['w'])
        if size_half_pt:
            font_props["font_size"] = int(size_half_pt)
            font_props["font_size_pt"] = int(size_half_pt) / 2

    # 粗体
    b = r_pr.find('.//w:b', ns)
    if b is not None:
        font_props["bold"] = b.get('{%s}val' % ns['w']) != "0"

    # 斜体
    i = r_pr.find('.//w:i', ns)
    if i is not None:
        font_props["italic"] = i.get('{%s}val' % ns['w']) != "0"

    # 下划线
    u = r_pr.find('.//w:u', ns)
    if u is not None:
        font_props["underline"] = u.get('{%s}val' % ns['w'])

    # 颜色
    color = r_pr.find('.//w:color', ns)
    if color is not None:
        font_props["color"] = color.get('{%s}val' % ns['w'])

    # 高亮
    highlight = r_pr.find('.//w:highlight', ns)
    if highlight is not None:
        font_props["highlight"] = highlight.get('{%s}val' % ns['w'])

    # 删除线
    strike = r_pr.find('.//w:strike', ns)
    if strike is not None:
        font_props["strike"] = True

    return font_props
```

#### 步骤 2.3: 提取段落属性

```python
def extract_paragraph_properties(p_pr, ns):
    """提取段落属性"""

    para_props = {
        "alignment": None,
        "indent": {},
        "spacing": {},
        "line_spacing": {},
        "outline_level": None,
        "numbering": {}
    }

    # 对齐方式
    jc = p_pr.find('.//w:jc', ns)
    if jc is not None:
        para_props["alignment"] = jc.get('{%s}val' % ns['w'])  # left, right, center, both

    # 缩进
    ind = p_pr.find('.//w:ind', ns)
    if ind is not None:
        para_props["indent"] = {
            "left_twips": int(ind.get('{%s}left' % ns['w']) or 0),
            "right_twips": int(ind.get('{%s}right' % ns['w']) or 0),
            "first_line_twips": int(ind.get('{%s}firstLine' % ns['w']) or 0),
            "hanging_twips": int(ind.get('{%s}hanging' % ns['w']) or 0),
            # 转换为字符(1字符 = 420 twips, 假设中文字符)
            "left_chars": round(int(ind.get('{%s}left' % ns['w']) or 0) / 420, 1),
            "first_line_chars": round(int(ind.get('{%s}firstLine' % ns['w']) or 0) / 420, 1)
        }

    # 段落间距
    spacing = p_pr.find('.//w:spacing', ns)
    if spacing is not None:
        para_props["spacing"] = {
            "before_twips": int(spacing.get('{%s}before' % ns['w']) or 0),
            "after_twips": int(spacing.get('{%s}after' % ns['w']) or 0),
            "line_twips": spacing.get('{%s}line' % ns['w']),
            "line_rule": spacing.get('{%s}lineRule' % ns['w'])  # auto, exact, atLeast
        }

        # 计算行距倍数
        if spacing.get('{%s}lineRule' % ns['w']) == "auto":
            line_val = spacing.get('{%s}line' % ns['w'])
            if line_val:
                # auto模式下,line值为240的倍数,240 = 1倍行距
                para_props["line_spacing"]["multiplier"] = int(line_val) / 240
        elif spacing.get('{%s}lineRule' % ns['w']) == "exact":
            line_val = spacing.get('{%s}line' % ns['w'])
            if line_val:
                para_props["line_spacing"]["exact_twips"] = int(line_val)

    # 大纲级别(用于标题)
    outline_lvl = p_pr.find('.//w:outlineLvl', ns)
    if outline_lvl is not None:
        para_props["outline_level"] = int(outline_lvl.get('{%s}val' % ns['w']))

    # 编号
    num_pr = p_pr.find('.//w:numPr', ns)
    if num_pr is not None:
        num_id = num_pr.find('.//w:numId', ns)
        ilvl = num_pr.find('.//w:ilvl', ns)

        para_props["numbering"] = {
            "num_id": int(num_id.get('{%s}val' % ns['w'])) if num_id is not None else None,
            "level": int(ilvl.get('{%s}val' % ns['w'])) if ilvl is not None else 0
        }

    return para_props
```

**输出示例**:
```json
{
  "Heading1": {
    "id": "Heading1",
    "name": "标题 1",
    "type": "paragraph",
    "base_on": "Normal",
    "font": {
      "font_name": "黑体",
      "font_name_ascii": "Arial",
      "font_name_east_asia": "黑体",
      "font_size": 36,
      "font_size_pt": 18,
      "bold": true,
      "italic": false,
      "color": "000000"
    },
    "paragraph": {
      "alignment": "left",
      "indent": {
        "left_twips": 0,
        "first_line_twips": 0
      },
      "spacing": {
        "before_twips": 340,
        "after_twips": 200,
        "line_twips": "360",
        "line_rule": "auto"
      },
      "line_spacing": {
        "multiplier": 1.5
      },
      "outline_level": 0
    }
  },
  "Normal": {
    "id": "Normal",
    "name": "正文",
    "type": "paragraph",
    "font": {
      "font_name": "仿宋_GB2312",
      "font_size": 32,
      "font_size_pt": 16
    },
    "paragraph": {
      "alignment": "both",
      "indent": {
        "first_line_twips": 480,
        "first_line_chars": 1.14
      },
      "spacing": {
        "line_twips": "360",
        "line_rule": "auto"
      },
      "line_spacing": {
        "multiplier": 1.5
      }
    }
  }
}
```

---

### 阶段 3: 文档结构分析

#### 步骤 3.1: 提取章节结构

```python
def extract_document_structure(unpacked_dir):
    """提取文档章节结构"""

    doc_xml = Path(unpacked_dir) / "word" / "document.xml"
    tree = etree.parse(str(doc_xml))
    root = tree.getroot()

    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    }

    structure = {
        "chapters": [],
        "paragraph_count": 0,
        "table_count": 0
    }

    # 遍历所有段落
    for para in root.findall('.//w:p', ns):
        # 提取段落样式
        p_style = para.find('.//w:pStyle', ns)
        style_id = p_style.get('{%s}val' % ns['w']) if p_style is not None else None

        # 提取段落文本
        text_elements = para.findall('.//w:t', ns)
        text = ''.join([t.text for t in text_elements if t.text])

        # 判断是否为标题
        if style_id and ('Heading' in style_id or '标题' in style_id):
            # 确定标题级别
            level = 1
            if '1' in style_id:
                level = 1
            elif '2' in style_id:
                level = 2
            elif '3' in style_id:
                level = 3

            structure["chapters"].append({
                "level": level,
                "title": text,
                "style_id": style_id
            })

        structure["paragraph_count"] += 1

    # 统计表格
    tables = root.findall('.//w:tbl', ns)
    structure["table_count"] = len(tables)

    return structure
```

---

### 阶段 4: 表格格式分析(可选)

#### 步骤 4.1: 提取表格格式

```python
def extract_table_formats(unpacked_dir):
    """提取表格格式"""

    doc_xml = Path(unpacked_dir) / "word" / "document.xml"
    tree = etree.parse(str(doc_xml))
    root = tree.getroot()

    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    }

    table_formats = []

    # 遍历所有表格
    for table_idx, table in enumerate(root.findall('.//w:tbl', ns)):
        table_format = {
            "table_index": table_idx,
            "width": {},
            "borders": {},
            "cell_spacing": None,
            "alignment": None
        }

        # 表格属性
        tbl_pr = table.find('.//w:tblPr', ns)
        if tbl_pr is not None:
            # 表格宽度
            tbl_w = tbl_pr.find('.//w:tblW', ns)
            if tbl_w is not None:
                table_format["width"] = {
                    "value": tbl_w.get('{%s}w' % ns['w']),
                    "type": tbl_w.get('{%s}type' % ns['w'])  # auto, dxa, pct
                }

            # 表格边框
            tbl_borders = tbl_pr.find('.//w:tblBorders', ns)
            if tbl_borders is not None:
                for border_type in ['top', 'bottom', 'left', 'right', 'insideH', 'insideV']:
                    border = tbl_borders.find(f'.//w:{border_type}', ns)
                    if border is not None:
                        table_format["borders"][border_type] = {
                            "style": border.get('{%s}val' % ns['w']),
                            "size": border.get('{%s}sz' % ns['w']),
                            "color": border.get('{%s}color' % ns['w'])
                        }

            # 单元格间距
            tbl_cell_spacing = tbl_pr.find('.//w:tblCellSpacing', ns)
            if tbl_cell_spacing is not None:
                table_format["cell_spacing"] = tbl_cell_spacing.get('{%s}w' % ns['w'])

            # 表格对齐
            jc = tbl_pr.find('.//w:jc', ns)
            if jc is not None:
                table_format["alignment"] = jc.get('{%s}val' % ns['w'])

        table_formats.append(table_format)

    return table_formats
```

---

## 完整分析脚本

### 主函数

```python
def analyze_document_format(document_path, extract_styles=True,
                           extract_page_settings=True,
                           extract_paragraph_formats=True,
                           extract_font_details=True,
                           extract_table_formats=False):
    """
    完整的文档格式分析

    Args:
        document_path: Word文档路径
        extract_styles: 是否提取样式
        extract_page_settings: 是否提取页面设置
        extract_paragraph_formats: 是否提取段落格式
        extract_font_details: 是否提取字体详情
        extract_table_formats: 是否提取表格格式

    Returns:
        dict: 完整的格式分析结果
    """
    import tempfile
    import shutil
    import subprocess

    # 创建临时目录
    unpacked_dir = tempfile.mkdtemp(prefix='format_analyzer_')

    try:
        # 解压文档
        subprocess.run([
            'python',
            'skills/docx/ooxml/scripts/unpack.py',
            document_path,
            unpacked_dir
        ], check=True)

        result = {
            "document_path": document_path,
            "page_settings": {},
            "styles": {},
            "structure": {},
            "table_formats": []
        }

        # 提取页面设置
        if extract_page_settings:
            result["page_settings"] = extract_page_settings(unpacked_dir)

        # 提取样式
        if extract_styles:
            result["styles"] = extract_styles(unpacked_dir)

        # 提取文档结构
        result["structure"] = extract_document_structure(unpacked_dir)

        # 提取表格格式
        if extract_table_formats:
            result["table_formats"] = extract_table_formats(unpacked_dir)

        return result

    finally:
        # 清理临时目录
        shutil.rmtree(unpacked_dir)
```

---

## 使用示例

### 示例 1: 完整分析

```python
result = analyze_document_format(
    document_path="/path/to/智能建造实施方案-模板.docx",
    extract_styles=True,
    extract_page_settings=True,
    extract_paragraph_formats=True,
    extract_font_details=True,
    extract_table_formats=False
)

print("页面设置:")
print(f"纸张类型: {result['page_settings']['page_size']['paper_type']}")
print(f"页边距(上): {result['page_settings']['margins']['top_cm']} cm")

print("\n样式:")
for style_id, style in result['styles'].items():
    if 'Heading' in style_id:
        print(f"{style['name']}: {style['font']['font_name']} {style['font']['font_size_pt']}号")

print("\n文档结构:")
print(f"章节数: {len(result['structure']['chapters'])}")
print(f"段落数: {result['structure']['paragraph_count']}")
```

### 示例 2: 只提取页面设置

```python
result = analyze_document_format(
    document_path="/path/to/document.docx",
    extract_styles=False,
    extract_page_settings=True,
    extract_paragraph_formats=False,
    extract_font_details=False
)

print(result["page_settings"])
```

### 示例 3: 格式对比

```python
def compare_formats(doc1_path, doc2_path):
    """对比两个文档的格式"""

    format1 = analyze_document_format(doc1_path)
    format2 = analyze_document_format(doc2_path)

    differences = []

    # 对比页面设置
    if format1["page_settings"] != format2["page_settings"]:
        differences.append("页面设置不同")

    # 对比样式数量
    if len(format1["styles"]) != len(format2["styles"]):
        differences.append(f"样式数量不同: {len(format1['styles'])} vs {len(format2['styles'])}")

    return differences
```

---

## 输出格式

完整的输出JSON结构:

```json
{
  "document_path": "/path/to/document.docx",
  "page_settings": {
    "page_size": {
      "width_twips": 11906,
      "height_twips": 16838,
      "width_cm": 21.0,
      "height_cm": 29.7,
      "paper_type": "A4"
    },
    "margins": {
      "top_twips": 1440,
      "bottom_twips": 1440,
      "left_twips": 1800,
      "right_twips": 1800,
      "top_cm": 2.54,
      "bottom_cm": 2.54,
      "left_cm": 3.18,
      "right_cm": 3.18
    },
    "orientation": "portrait",
    "columns": {
      "num_columns": 1,
      "space_twips": 720,
      "equal_width": true
    }
  },
  "styles": {
    "Heading1": {
      "id": "Heading1",
      "name": "标题 1",
      "type": "paragraph",
      "font": {
        "font_name": "黑体",
        "font_size_pt": 18,
        "bold": true
      },
      "paragraph": {
        "alignment": "left",
        "line_spacing": {
          "multiplier": 1.5
        }
      }
    },
    "Normal": {
      "id": "Normal",
      "name": "正文",
      "type": "paragraph",
      "font": {
        "font_name": "仿宋_GB2312",
        "font_size_pt": 16
      },
      "paragraph": {
        "alignment": "both",
        "indent": {
          "first_line_chars": 1.14
        }
      }
    }
  },
  "structure": {
    "chapters": [
      {"level": 1, "title": "一、项目概述", "style_id": "Heading1"},
      {"level": 2, "title": "1.1 项目背景", "style_id": "Heading2"}
    ],
    "paragraph_count": 127,
    "table_count": 3
  },
  "table_formats": []
}
```

---

## 注意事项

### ⚠️  重要提醒

1. **XML命名空间**
   - 必须正确处理OOXML命名空间
   - 不同版本的Word可能使用不同的命名空间

2. **单位转换**
   - Twips(缇): 1英寸 = 1440 twips
   - 磅(Point): 字号单位,半磅存储
   - 厘米: 1cm = 567 twips

3. **样式继承**
   - 样式可以基于其他样式(`basedOn`)
   - 需要递归解析完整样式

4. **兼容性**
   - 仅支持.docx格式(Office 2007+)
   - 不支持.doc格式

5. **性能**
   - 大文档分析可能较慢
   - 建议只提取需要的格式信息

### 📚 相关资源

- [Office Open XML规范](http://officeopenxml.com/)
- [WordprocessingML参考](https://docs.microsoft.com/en-us/office/open-xml/word/)

### 🔧 故障排除

**问题1: 解压失败**
```
原因: 文档损坏或格式不正确
解决: 用Word打开并另存为新文件
```

**问题2: 样式提取不完整**
```
原因: styles.xml不存在或损坏
解决: 检查文档是否包含自定义样式
```

**问题3: 中文字体名称乱码**
```
原因: 编码问题
解决: 确保使用UTF-8编码读取XML
```

---

**版本**: v1.0
**最后更新**: 2025-11-06
**作者**: NotebookLM Assistant Team
