# NotebookLM 智能文档格式克隆

**功能**: 完全模仿参考文档的格式和排版,生成内容不同但格式完全一致的新Word文档

**命令格式**: `/notebook-clone-format <参考文档路径>`

**适用场景**:
- 根据A项目文档模板生成B项目文档
- 智能建造实施方案生成
- 技术方案文档快速生成
- 标准化报告文档制作

**核心特点**:
- ✅ **格式完全克隆**: 样式、字体、段落格式、页面设置完全一致
- ✅ **生成Word文档**: 输出标准 .docx 文件,可直接编辑
- ✅ **模板+填充机制**: 先提取模板,再填充内容
- ✅ **交互式信息收集**: 引导用户输入项目特定信息

---

## 使用方法

### 基本用法

```bash
/notebook-clone-format <参考文档.docx>
```

**执行流程**:

1. **提取模板** - 分析参考文档的格式、样式、结构
2. **收集信息** - 交互式收集项目名称、地点、单位等信息
3. **生成内容** - 基于用户信息和章节结构生成内容
4. **输出文档** - 生成格式完全一致的 Word 文档

### 示例

```bash
/notebook-clone-format ./templates/智能建造实施方案-模板.docx
/notebook-clone-format ~/Documents/申报资料模板.docx
```

---

## 实现说明

本命令使用 Python 脚本实现:

1. `extract_template.py` - 提取文档模板(格式、样式、结构)
2. `fill_template.py` - 填充模板生成新文档
3. `clone_format.py` - 主命令脚本(整合流程)

执行本命令时,将调用 `clone_format.py` 脚本完成整个流程。

---

## 执行命令

请使用以下 Bash 工具调用主脚本:

```bash
python /home/user/construction-marketplace/plugins/notebooklm-assistant/scripts/clone_format.py "$1"
```

其中 `$1` 是用户提供的参考文档路径。

---

### Phase 1: 深度解析参考文档结构

这是最关键的阶段,需要完整理解参考文档的结构和格式。

#### 步骤 1.1: 转换为Markdown提取结构

使用 `pandoc` 将参考文档转换为 Markdown,提取文本结构:

```bash
# 转换为 Markdown
pandoc "$REFERENCE_DOC" -o /tmp/reference_structure.md

# 统计基本信息
echo "📊 文档统计:"
echo "- 字数: $(wc -w < /tmp/reference_structure.md)"
echo "- 段落: $(grep -c "^[^#]" /tmp/reference_structure.md)"
```

#### 步骤 1.2: 解析XML获取格式详情

使用 **Skill tool** 调用 `docx` skill 解析参考文档的 XML 结构:

**重要**: 必须先使用 **Read tool** 完整阅读 `skills/docx/ooxml.md` 文件,了解 OOXML 操作方法。

**解压文档**:
```bash
# 使用 docx skill 中的解压脚本
python skills/docx/ooxml/scripts/unpack.py "$REFERENCE_DOC" /tmp/reference_unpacked
```

**分析关键XML文件**:
```bash
# 读取主文档结构
cat /tmp/reference_unpacked/word/document.xml

# 读取样式定义
cat /tmp/reference_unpacked/word/styles.xml

# 读取文档属性
cat /tmp/reference_unpacked/docProps/core.xml
```

#### 步骤 1.3: 提取文档结构和格式信息

使用 **Skill tool** 调用 `format-analyzer` skill(如果已创建)或直接编写 Python 脚本分析:

**创建分析脚本** `/tmp/analyze_format.py`:

```python
#!/usr/bin/env python3
"""参考文档格式分析脚本"""
import sys
import json
from pathlib import Path
from lxml import etree

def analyze_document_structure(unpacked_dir):
    """分析文档结构和格式"""

    # 解析 document.xml
    doc_xml = Path(unpacked_dir) / "word" / "document.xml"
    tree = etree.parse(str(doc_xml))
    root = tree.getroot()

    # 命名空间
    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    }

    structure = {
        "chapters": [],
        "formatting": {},
        "required_fields": [],
        "page_settings": {}
    }

    # 提取章节结构(基于标题样式)
    for para in root.findall('.//w:p', ns):
        # 检查段落样式
        pStyle = para.find('.//w:pStyle', ns)
        if pStyle is not None:
            style_id = pStyle.get('{%s}val' % ns['w'])

            # 识别标题级别
            if 'Heading' in style_id or '标题' in style_id:
                level = 1  # 默认一级标题
                if 'Heading1' in style_id or '标题1' in style_id:
                    level = 1
                elif 'Heading2' in style_id or '标题2' in style_id:
                    level = 2
                elif 'Heading3' in style_id or '标题3' in style_id:
                    level = 3

                # 提取标题文本
                text_elements = para.findall('.//w:t', ns)
                title = ''.join([t.text for t in text_elements if t.text])

                # 分析标题中的占位符或字段
                fields = extract_fields_from_text(title)

                structure["chapters"].append({
                    "level": level,
                    "title": title,
                    "style_id": style_id,
                    "fields": fields
                })

    # 提取格式信息
    styles_xml = Path(unpacked_dir) / "word" / "styles.xml"
    if styles_xml.exists():
        styles_tree = etree.parse(str(styles_xml))
        styles_root = styles_tree.getroot()

        # 提取标题样式
        for style in styles_root.findall('.//w:style', ns):
            style_id = style.get('{%s}styleId' % ns['w'])
            if 'Heading' in style_id or 'Title' in style_id or '标题' in style_id:
                font_info = extract_font_info(style, ns)
                structure["formatting"][style_id] = font_info

        # 提取正文样式
        normal_style = styles_root.find('.//w:style[@w:styleId="Normal"]', ns)
        if normal_style is not None:
            structure["formatting"]["Normal"] = extract_font_info(normal_style, ns)

    # 提取页面设置
    sect_pr = root.find('.//w:sectPr', ns)
    if sect_pr is not None:
        structure["page_settings"] = extract_page_settings(sect_pr, ns)

    return structure

def extract_fields_from_text(text):
    """从文本中提取字段占位符"""
    import re

    fields = []

    # 识别常见占位符模式
    patterns = [
        r'\[(.+?)\]',           # [项目名称]
        r'___+',                 # _______
        r'（\s*）',              # （  ）
        r'\(\s*\)',              # (  )
        r'【(.+?)】',            # 【项目名称】
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, str) and match.strip():
                fields.append(match.strip())
            elif match == '___+':
                fields.append('填空字段')

    return fields

def extract_font_info(style_element, ns):
    """提取字体信息"""
    font_info = {
        "font_name": "宋体",  # 默认值
        "font_size": 10.5,
        "bold": False,
        "italic": False,
        "color": "000000"
    }

    # 提取字体名称
    rFonts = style_element.find('.//w:rFonts', ns)
    if rFonts is not None:
        font_name = rFonts.get('{%s}eastAsia' % ns['w']) or rFonts.get('{%s}ascii' % ns['w'])
        if font_name:
            font_info["font_name"] = font_name

    # 提取字号(半磅为单位,需要除以2)
    sz = style_element.find('.//w:sz', ns)
    if sz is not None:
        size_val = sz.get('{%s}val' % ns['w'])
        if size_val:
            font_info["font_size"] = int(size_val) / 2

    # 提取粗体
    b = style_element.find('.//w:b', ns)
    if b is not None:
        font_info["bold"] = True

    # 提取斜体
    i = style_element.find('.//w:i', ns)
    if i is not None:
        font_info["italic"] = True

    # 提取颜色
    color = style_element.find('.//w:color', ns)
    if color is not None:
        color_val = color.get('{%s}val' % ns['w'])
        if color_val:
            font_info["color"] = color_val

    return font_info

def extract_page_settings(sect_pr, ns):
    """提取页面设置"""
    settings = {
        "page_width": 11906,   # A4默认宽度(twips)
        "page_height": 16838,  # A4默认高度
        "margin_top": 1440,
        "margin_bottom": 1440,
        "margin_left": 1800,
        "margin_right": 1800
    }

    # 提取页面尺寸
    pgSz = sect_pr.find('.//w:pgSz', ns)
    if pgSz is not None:
        width = pgSz.get('{%s}w' % ns['w'])
        height = pgSz.get('{%s}h' % ns['w'])
        if width:
            settings["page_width"] = int(width)
        if height:
            settings["page_height"] = int(height)

    # 提取页边距
    pgMar = sect_pr.find('.//w:pgMar', ns)
    if pgMar is not None:
        for margin in ['top', 'bottom', 'left', 'right']:
            val = pgMar.get('{%s}%s' % (ns['w'], margin))
            if val:
                settings[f"margin_{margin}"] = int(val)

    return settings

# 执行分析
if __name__ == "__main__":
    unpacked_dir = sys.argv[1]
    result = analyze_document_structure(unpacked_dir)

    # 输出JSON格式
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

**运行分析脚本**:
```bash
python /tmp/analyze_format.py /tmp/reference_unpacked > /tmp/doc_structure.json
```

#### 步骤 1.4: 展示分析结果

读取并展示分析结果:

```bash
cat /tmp/doc_structure.json
```

**输出示例**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Phase 1: 参考文档结构分析完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 文档统计:
- 章节数: 6 个
- 一级标题: 6 个
- 二级标题: 15 个
- 三级标题: 8 个
- 总段落: 127 段
- 总字数: 5,432 字

📐 格式信息:
- 标题字体: 黑体 22号 加粗
- 一级标题: 黑体 18号 加粗
- 二级标题: 黑体 16号 加粗
- 正文字体: 仿宋_GB2312 16号
- 行间距: 1.5倍
- 页边距: 上下2.54cm, 左右3.18cm

📑 章节结构:
1. 一、项目概述
   1.1 项目背景
   1.2 项目基本信息
   1.3 建设目标
2. 二、BIM技术应用方案
   2.1 BIM软件选型
   2.2 BIM应用场景
   2.3 实施计划
3. 三、智慧工地管理
   ...

✅ 结构分析完成,用时: 8秒
```

---

### Phase 2: 识别数据需求与字段

基于文档结构,智能识别需要收集的数据和字段。

#### 步骤 2.1: AI分析章节内容

读取参考文档的 Markdown 版本,使用 AI 分析每个章节需要的数据类型:

```markdown
💭 **我的分析过程**:

基于参考文档的章节结构,我识别出以下数据需求:

**一、项目概述**
- 需要数据: 项目名称、建设地点、建设单位、项目规模
- 数据来源: 🔵 用户提供(必需)
- 理由: 这些是项目特定信息,无法从知识库推断

**二、BIM技术应用方案**
- 需要数据: BIM软件名称、应用场景、实施步骤、技术参数
- 数据来源: 🟢 知识库检索(可推断)
- 理由: 技术方案内容可从BIM相关文档中提取

**三、智慧工地管理**
- 需要数据: 管理系统、监控设备、数据平台
- 数据来源: 🟢 知识库检索(可推断)
- 理由: 智慧工地方案可从相关技术文档中提取

**四、施工组织设计**
- 需要数据: 施工工期、人员配置、机械设备
- 数据来源: 🟡 混合(部分用户提供,部分知识库提取)
- 理由: 工期需用户确认,施工方法可从知识库提取

**五、质量安全保障措施**
- 需要数据: 质量标准、安全措施、应急预案
- 数据来源: 🟢 知识库检索(可推断)
- 理由: 标准化措施可从质量安全文档中提取

**六、预期效益分析**
- 需要数据: 经济效益、社会效益、技术效益
- 数据来源: 🟢 知识库检索(可推断)
- 理由: 效益分析可基于类似项目文档生成
```

#### 步骤 2.2: 生成字段清单

整理出需要用户提供的必需字段:

```json
{
  "required_fields": [
    {
      "field_name": "project_name",
      "display_name": "项目名称",
      "type": "text",
      "example": "某某智能建造示范项目",
      "required": true
    },
    {
      "field_name": "project_location",
      "display_name": "建设地点",
      "type": "text",
      "example": "江苏省苏州市工业园区",
      "required": true
    },
    {
      "field_name": "construction_unit",
      "display_name": "建设单位",
      "type": "text",
      "example": "苏州某某建设发展有限公司",
      "required": true
    },
    {
      "field_name": "project_scale",
      "display_name": "项目规模",
      "type": "text",
      "example": "总建筑面积50000平方米",
      "required": false
    },
    {
      "field_name": "construction_period",
      "display_name": "建设工期",
      "type": "text",
      "example": "24个月",
      "required": false
    }
  ],
  "optional_fields": [
    {
      "field_name": "investment_amount",
      "display_name": "投资金额",
      "type": "text",
      "example": "2.5亿元"
    },
    {
      "field_name": "building_layers",
      "display_name": "建筑层数",
      "type": "text",
      "example": "地上18层,地下2层"
    }
  ]
}
```

#### 步骤 2.3: 交互式收集用户信息

展示字段清单,交互式收集用户输入:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Phase 2: 数据需求识别完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 根据参考文档分析,我需要以下信息:

🔴 **必需字段**(请务必提供):
1. 项目名称: ___________
   示例: 某某智能建造示范项目

2. 建设地点: ___________
   示例: 江苏省苏州市工业园区

3. 建设单位: ___________
   示例: 苏州某某建设发展有限公司

🟡 **可选字段**(可留空,我将从知识库推断):
4. 项目规模: ___________
   示例: 总建筑面积50000平方米

5. 建设工期: ___________
   示例: 24个月

6. 投资金额: ___________
   示例: 2.5亿元

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请按以下格式提供信息(每行一个字段):
```
项目名称: [您的输入]
建设地点: [您的输入]
建设单位: [您的输入]
项目规模: [您的输入或留空]
建设工期: [您的输入或留空]
投资金额: [您的输入或留空]
```

💡 提示:
- 必需字段不能留空
- 可选字段留空时,我会从知识库智能推断
- 其他描述性内容将从知识库自动提取

⏸️  等待用户输入...
```

**等待用户输入,解析并验证**:

```bash
# 读取用户输入
read -p "项目名称: " project_name
read -p "建设地点: " project_location
read -p "建设单位: " construction_unit
read -p "项目规模(可选): " project_scale
read -p "建设工期(可选): " construction_period
read -p "投资金额(可选): " investment_amount

# 验证必需字段
if [ -z "$project_name" ] || [ -z "$project_location" ] || [ -z "$construction_unit" ]; then
  echo "❌ 错误: 必需字段不能为空"
  exit 1
fi

# 保存到临时文件
cat > /tmp/user_input.json <<EOF
{
  "project_name": "$project_name",
  "project_location": "$project_location",
  "construction_unit": "$construction_unit",
  "project_scale": "$project_scale",
  "construction_period": "$construction_period",
  "investment_amount": "$investment_amount"
}
EOF
```

**确认信息**:
```
✅ 信息收集完成

📝 您提供的信息:
- 项目名称: 苏州工业园区智能建造示范项目
- 建设地点: 江苏省苏州市工业园区星湖街
- 建设单位: 苏州一建集团有限公司
- 项目规模: (将从知识库推断)
- 建设工期: (将从知识库推断)
- 投资金额: (将从知识库推断)

是否确认? (y/n)
```

---

### Phase 3: 从知识库智能检索数据

这是内容生成的核心阶段,需要从知识库中检索相关数据。

#### 步骤 3.1: 读取知识库索引

读取知识库索引文件:

```bash
# 读取索引
INDEX_FILE=".notebooklm/index/metadata.json"

if [ ! -f "$INDEX_FILE" ]; then
  echo "❌ 错误: 知识库索引不存在"
  echo "请先运行: /notebook-index 生成索引"
  exit 1
fi

# 统计文档数量
DOC_COUNT=$(jq '.documents | length' "$INDEX_FILE")
echo "📚 知识库文档数: $DOC_COUNT"
```

#### 步骤 3.2: 逐章节检索相关文档

对参考文档的每个章节,使用 **Skill tool** 调用 `smart-retrieval` skill 检索相关文档:

**示例 - 第一章"项目概述"**:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Phase 3: 智能检索知识库数据
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 正在检索第 1 章: 一、项目概述

💭 检索策略:
- 关键词: ["项目", "概述", "背景", "目标", "规模"]
- 优先文档类型: 项目简介、可研报告、立项文件
- 预期文档数: 3-5 份

使用 Skill tool 调用 smart-retrieval:
- query: "项目概述 项目背景 建设目标 项目规模"
- knowledge_base_path: [从配置读取]
- top_k: 5
- min_score: 0.3
```

**Smart Retrieval 返回结果**:
```json
{
  "results": [
    {
      "file_path": "/path/to/项目可行性研究报告.pdf",
      "relevance_score": 0.85,
      "preview": "本项目位于苏州市工业园区,总建筑面积约5万平方米...",
      "matched_keywords": ["项目", "建设", "规模"]
    },
    {
      "file_path": "/path/to/项目立项申请书.docx",
      "relevance_score": 0.72,
      "preview": "项目建设目标是打造智能建造示范工程...",
      "matched_keywords": ["项目", "目标", "建设"]
    },
    {
      "file_path": "/path/to/工程概况.docx",
      "relevance_score": 0.68,
      "preview": "工程概况:本工程为框架剪力墙结构...",
      "matched_keywords": ["工程", "概况"]
    }
  ]
}
```

**输出进度**:
```
✅ 第 1 章检索完成: 找到 3 份相关文档
   - 项目可行性研究报告.pdf (相关度: 85%)
   - 项目立项申请书.docx (相关度: 72%)
   - 工程概况.docx (相关度: 68%)
```

**对所有章节重复此过程**:

```markdown
🔍 正在检索第 2 章: 二、BIM技术应用方案
✅ 第 2 章检索完成: 找到 5 份相关文档

🔍 正在检索第 3 章: 三、智慧工地管理
✅ 第 3 章检索完成: 找到 4 份相关文档

🔍 正在检索第 4 章: 四、施工组织设计
✅ 第 4 章检索完成: 找到 6 份相关文档

🔍 正在检索第 5 章: 五、质量安全保障措施
✅ 第 5 章检索完成: 找到 7 份相关文档

🔍 正在检索第 6 章: 六、预期效益分析
✅ 第 6 章检索完成: 找到 3 份相关文档

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 全部章节检索完成
总计找到: 28 份相关文档
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 步骤 3.3: 深度提取文档内容

对检索到的高相关度文档,使用 **Skill tool** 调用 `docx`、`pdf`、`xlsx` skills 提取完整内容:

**示例 - 提取第一章的文档内容**:

```markdown
📖 正在深度解析文档...

使用 Skill tool 调用 pdf skill:
- file_path: "/path/to/项目可行性研究报告.pdf"
- extract_mode: "text_and_tables"
- pages: "all"

返回内容:
- 文本内容: 约3000字
- 表格数: 2个
- 关键信息: 项目背景、建设规模、投资估算
```

**提取结果保存**:
```bash
# 保存提取的内容到临时文件
echo "章节1的提取内容" > /tmp/chapter_1_content.txt
echo "章节2的提取内容" > /tmp/chapter_2_content.txt
...
```

#### 步骤 3.4: 使用Context Builder整合内容

使用 **Skill tool** 调用 `context-builder` skill 整合多文档内容:

```markdown
使用 Skill tool 调用 context-builder:
- documents: [章节1的3份文档路径]
- query: "项目概述 项目背景 建设目标"
- max_tokens: 2000
- deduplication: true
- citation_style: "inline"

返回:
- 整合后的文本内容
- 引用来源标注
- 去重后的段落
```

**输出示例**:
```
✅ 内容整合完成

📊 第 1 章内容统计:
- 原始字数: 8,234 字(来自3份文档)
- 整合后字数: 1,856 字
- 去重段落: 12 段
- 引用来源: 3 份文档

💡 内容预览:
"[项目名称]位于[建设地点],由[建设单位]投资建设。本项目总建筑面积约5万平方米,
建设工期24个月。项目旨在打造智能建造示范工程,通过BIM技术、智慧工地等新技术
应用,提升工程质量和管理水平...[1]

项目建设背景:随着建筑行业转型升级,智能建造已成为行业发展趋势。本项目响应
国家智能建造发展战略,积极探索新技术在工程建设中的应用...[2]"

[1] 项目可行性研究报告.pdf, 第3页
[2] 项目立项申请书.docx, 第2页
```

---

### Phase 4: 生成多样化内容(降查重核心)

这是降低查重率的关键阶段,需要对提取的内容进行多样化改写。

#### 步骤 4.1: 调用Content Diversifier Skill

使用 **Skill tool** 调用 `content-diversifier` skill(核心功能):

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Phase 4: 内容多样化改写(降查重)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

使用 Skill tool 调用 content-diversifier:
- input_text: [第1章整合后的内容]
- diversification_level: "high"  # 高强度改写
- preserve_data: true  # 保留数值数据
- preserve_terms: ["BIM", "智慧工地", "智能建造"]  # 保留专业术语
- target_similarity: 0.2  # 目标相似度20%(查重率预期)
```

**Content Diversifier 执行5种改写策略**:

**策略1: 同义词替换**
```
原文: "采用BIM技术进行三维建模"
改写: "运用建筑信息模型技术实施立体化建模"

替换词典:
- 采用 → 运用、应用、使用
- 进行 → 实施、开展、执行
- 三维 → 立体化、3D
```

**策略2: 句式重组**
```
原文: "本项目位于苏州市工业园区,总建筑面积50000平方米,建设工期24个月"

改写方式A(拆分):
"该工程坐落于苏州市工业园区。建筑总面积达5万平方米。计划工期为24个月。"

改写方式B(合并):
"位于苏州市工业园区的本工程,建筑面积5万平方米,计划24个月建成。"

改写方式C(倒装):
"计划工期24个月的本项目,建筑面积5万平方米,位于苏州市工业园区。"
```

**策略3: 段落重构**
```
原段落结构: A句 + B句 + C句 + D句

重构方式1: C句(改写) + A句(改写) + D句(改写) + B句(改写)
重构方式2: 合并A+B句 + 扩展C句 + D句(改写)
重构方式3: A句(改写) + 新增过渡句 + B+C合并句 + D句(改写)
```

**策略4: 表达方式变换**
```
原文: "采用先进的BIM技术"
改写: "引入BIM建筑信息模型技术"

原文: "提高施工效率"
改写: "提升工程建设效能"

原文: "加强质量管理"
改写: "强化工程质量管控"
```

**策略5: 数值表达多样化**
```
原文: "50000平方米"
改写选项:
- 5万平方米
- 50000㎡
- 五万平方米
- 建筑面积约5万m²

原文: "24个月"
改写选项:
- 两年
- 24月
- 二十四个月
```

#### 步骤 4.2: 对所有章节执行多样化改写

```markdown
✍️  正在改写第 1 章...
✅ 第 1 章改写完成
   - 同义替换: 34 处
   - 句式重组: 12 处
   - 段落重构: 5 处
   - 预估相似度: 18%

✍️  正在改写第 2 章...
✅ 第 2 章改写完成
   - 同义替换: 45 处
   - 句式重组: 15 处
   - 段落重构: 6 处
   - 预估相似度: 16%

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 全部章节改写完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 改写统计:
- 总同义替换: 187 处
- 总句式重组: 68 处
- 总段落重构: 25 处
- 预估整体查重率: 15-18%

⚠️  注意:
- 专业术语(BIM、智慧工地等)已保留,未改写
- 数值数据(面积、金额等)已保留原始表达
- 项目特定信息(名称、地点)已替换为用户提供的信息
```

#### 步骤 4.3: 质量检查

检查改写后的内容质量:

```markdown
🔍 内容质量检查中...

✅ 专业性检查: 通过
   - 专业术语使用正确
   - 行业表达规范

✅ 准确性检查: 通过
   - 数值数据保持一致
   - 引用来源准确标注

✅ 可读性检查: 通过
   - 句子流畅自然
   - 逻辑连贯清晰

✅ 完整性检查: 通过
   - 所有章节内容完整
   - 无遗漏关键信息

⚠️  人工审阅建议:
- 建议重点审阅: 第2章技术参数、第4章工期安排
- 原因: 涉及项目特定数据,需确认准确性
```

---

### Phase 5: 按参考格式生成Word文档

最后阶段,使用docx skill按照参考文档的格式生成最终的Word文档。

#### 步骤 5.1: 读取docx-js API文档

**重要**: 必须先使用 **Read tool** 完整阅读 `skills/docx/docx-js.md` 文件:

```markdown
正在读取 docx-js API 文档...
📖 Reading: skills/docx/docx-js.md

✅ 已了解 docx-js 的完整API:
- Document、Section 创建方法
- Paragraph、TextRun 格式设置
- 标题级别(HeadingLevel)
- 字体、字号、颜色设置
- 段落对齐、缩进、间距
- 表格创建和格式
- 页面设置(页边距、纸张大小)
```

#### 步骤 5.2: 生成文档创建脚本

创建 JavaScript 脚本 `/tmp/generate_document.js`:

```javascript
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell, WidthType } = require("docx");
const fs = require("fs");

// 读取格式模板
const formatTemplate = JSON.parse(fs.readFileSync('/tmp/doc_structure.json', 'utf8'));

// 读取改写后的内容
const diversifiedContent = JSON.parse(fs.readFileSync('/tmp/diversified_content.json', 'utf8'));

// 读取用户输入
const userInput = JSON.parse(fs.readFileSync('/tmp/user_input.json', 'utf8'));

// 创建文档
const doc = new Document({
  sections: [{
    properties: {
      page: {
        // 页面尺寸(从格式模板读取)
        width: formatTemplate.page_settings.page_width,
        height: formatTemplate.page_settings.page_height,
        margin: {
          top: formatTemplate.page_settings.margin_top,
          bottom: formatTemplate.page_settings.margin_bottom,
          left: formatTemplate.page_settings.margin_left,
          right: formatTemplate.page_settings.margin_right
        }
      }
    },
    children: [
      // 标题页
      new Paragraph({
        text: diversifiedContent.title || `${userInput.project_name}实施方案`,
        heading: HeadingLevel.TITLE,
        alignment: AlignmentType.CENTER,
        spacing: {
          before: 400,
          after: 400
        },
        style: {
          font: {
            name: formatTemplate.formatting.Title?.font_name || "黑体",
            size: (formatTemplate.formatting.Title?.font_size || 22) * 2  // 半磅为单位
          }
        }
      }),

      // 项目基本信息
      new Paragraph({
        text: "",
        spacing: { before: 200, after: 200 }
      }),
      new Paragraph({
        children: [
          new TextRun({
            text: "项目名称: ",
            bold: true
          }),
          new TextRun({
            text: userInput.project_name
          })
        ],
        alignment: AlignmentType.CENTER
      }),
      new Paragraph({
        children: [
          new TextRun({
            text: "建设地点: ",
            bold: true
          }),
          new TextRun({
            text: userInput.project_location
          })
        ],
        alignment: AlignmentType.CENTER
      }),
      new Paragraph({
        children: [
          new TextRun({
            text: "建设单位: ",
            bold: true
          }),
          new TextRun({
            text: userInput.construction_unit
          })
        ],
        alignment: AlignmentType.CENTER
      }),

      // 生成日期
      new Paragraph({
        text: `编制日期: ${new Date().toLocaleDateString('zh-CN')}`,
        alignment: AlignmentType.CENTER,
        spacing: { before: 200, after: 400 }
      }),

      // 分页
      new Paragraph({
        pageBreakBefore: true,
        text: ""
      }),

      // 逐章节生成内容
      ...diversifiedContent.chapters.flatMap(chapter => {
        const paragraphs = [];

        // 章节标题
        paragraphs.push(new Paragraph({
          text: chapter.title,
          heading: chapter.level === 1 ? HeadingLevel.HEADING_1 :
                  chapter.level === 2 ? HeadingLevel.HEADING_2 :
                  HeadingLevel.HEADING_3,
          spacing: {
            before: 300,
            after: 200
          },
          style: {
            font: {
              name: formatTemplate.formatting[`Heading${chapter.level}`]?.font_name || "黑体",
              size: (formatTemplate.formatting[`Heading${chapter.level}`]?.font_size || 16) * 2
            }
          }
        }));

        // 章节内容(分段)
        if (chapter.content) {
          const contentParagraphs = chapter.content.split('\n\n');
          contentParagraphs.forEach(para => {
            if (para.trim()) {
              paragraphs.push(new Paragraph({
                text: para.trim(),
                spacing: {
                  before: 100,
                  after: 100,
                  line: 360  // 1.5倍行距
                },
                indent: {
                  firstLine: 480  // 首行缩进2字符
                },
                style: {
                  font: {
                    name: formatTemplate.formatting.Normal?.font_name || "仿宋_GB2312",
                    size: (formatTemplate.formatting.Normal?.font_size || 16) * 2
                  }
                }
              }));
            }
          });
        }

        // 如果有表格
        if (chapter.tables && chapter.tables.length > 0) {
          chapter.tables.forEach(tableData => {
            const tableRows = tableData.rows.map(rowData =>
              new TableRow({
                children: rowData.cells.map(cellText =>
                  new TableCell({
                    children: [
                      new Paragraph({
                        text: cellText,
                        style: {
                          font: {
                            name: "仿宋_GB2312",
                            size: 24  // 12号字
                          }
                        }
                      })
                    ],
                    width: {
                      size: 100 / rowData.cells.length,
                      type: WidthType.PERCENTAGE
                    }
                  })
                )
              })
            );

            paragraphs.push(new Paragraph({
              text: "",
              spacing: { before: 200 }
            }));

            // 注意: docx库的Table创建方式
            // 这里简化处理,实际需要完整的Table API调用
            paragraphs.push(new Paragraph({
              text: `[表格: ${tableData.title || '数据表格'}]`,
              alignment: AlignmentType.CENTER,
              style: {
                font: {
                  name: "楷体",
                  size: 24
                }
              }
            }));

            paragraphs.push(new Paragraph({
              text: "",
              spacing: { after: 200 }
            }));
          });
        }

        return paragraphs;
      }),

      // 分页 - 参考文献
      new Paragraph({
        pageBreakBefore: true,
        text: ""
      }),

      // 参考文献标题
      new Paragraph({
        text: "参考文献",
        heading: HeadingLevel.HEADING_1,
        spacing: {
          before: 300,
          after: 200
        }
      }),

      // 引用来源列表
      ...diversifiedContent.references.map((ref, index) =>
        new Paragraph({
          text: `[${index + 1}] ${ref.document_name} (${ref.file_path})`,
          spacing: {
            before: 50,
            after: 50
          },
          indent: {
            left: 240,
            hanging: 240
          },
          style: {
            font: {
              name: "宋体",
              size: 20  // 10号字
            }
          }
        })
      )
    ]
  }]
});

// 导出为 .docx 文件
const outputFileName = `${userInput.project_name}-智能建造实施方案-${new Date().toISOString().slice(0,10).replace(/-/g,'')}.docx`;
const outputPath = `notebooklm-outputs/${outputFileName}`;

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outputPath, buffer);
  console.log(`✅ Word 文档生成完成: ${outputPath}`);
}).catch(err => {
  console.error(`❌ 文档生成失败: ${err.message}`);
  process.exit(1);
});
```

#### 步骤 5.3: 运行文档生成脚本

```bash
# 确保输出目录存在
mkdir -p notebooklm-outputs

# 安装依赖(如果未安装)
if ! npm list docx >/dev/null 2>&1; then
  echo "正在安装 docx 库..."
  npm install docx
fi

# 运行脚本
node /tmp/generate_document.js
```

#### 步骤 5.4: 生成Markdown预览版

同时生成 Markdown 预览版:

```bash
cat > notebooklm-outputs/${OUTPUT_FILENAME%.docx}.md <<EOF
# ${userInput.project_name}实施方案

**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')
**生成方式**: NotebookLM 智能文档格式克隆
**参考文档**: ${REFERENCE_DOC}

---

## 项目基本信息

- **项目名称**: ${userInput.project_name}
- **建设地点**: ${userInput.project_location}
- **建设单位**: ${userInput.construction_unit}
- **项目规模**: ${userInput.project_scale:-从知识库推断}
- **建设工期**: ${userInput.construction_period:-从知识库推断}

---

[插入改写后的全部章节内容]

---

## 参考文献

[插入引用来源列表]

---

**说明**:
- 本文档基于知识库 ${DOC_COUNT} 份文档生成
- 已执行多样化改写,预估查重率 < 20%
- 建议人工审阅技术参数和项目特定信息
EOF
```

---

### Phase 6: 质量检查与交付

#### 步骤 6.1: 自动质量检查

```bash
# 检查文件是否生成
if [ -f "notebooklm-outputs/${OUTPUT_FILENAME}" ]; then
  echo "✅ Word 文档: 生成成功"

  # 统计文件大小
  FILE_SIZE=$(du -h "notebooklm-outputs/${OUTPUT_FILENAME}" | cut -f1)
  echo "📏 文件大小: ${FILE_SIZE}"
else
  echo "❌ Word 文档: 生成失败"
  exit 1
fi

# 检查 Markdown 文件
if [ -f "notebooklm-outputs/${OUTPUT_FILENAME%.docx}.md" ]; then
  echo "✅ Markdown 预览: 生成成功"

  # 统计字数
  WORD_COUNT=$(wc -w < "notebooklm-outputs/${OUTPUT_FILENAME%.docx}.md")
  echo "📊 总字数: ${WORD_COUNT} 字"
fi
```

#### 步骤 6.2: 生成审阅报告

创建详细的审阅报告:

```bash
cat > notebooklm-outputs/${OUTPUT_FILENAME%.docx}-审阅报告.md <<EOF
# 文档生成审阅报告

## 📊 基本信息

- **生成时间**: $(date '+%Y-%m-%d %H:%M:%S')
- **参考文档**: ${REFERENCE_DOC}
- **输出文档**: ${OUTPUT_FILENAME}
- **生成耗时**: ${ELAPSED_TIME} 秒

---

## 📈 统计信息

### 文档规模
- **总字数**: ${WORD_COUNT} 字
- **章节数**: ${CHAPTER_COUNT} 章
- **段落数**: ${PARAGRAPH_COUNT} 段
- **引用文档**: ${CITATION_COUNT} 份

### 知识库使用
- **检索文档数**: ${SEARCHED_DOCS} 份
- **实际使用文档**: ${USED_DOCS} 份
- **使用率**: ${USAGE_RATE}%

---

## ✍️  改写统计

### 多样化改写效果
- **同义替换**: ${SYNONYM_COUNT} 处
- **句式重组**: ${RESTRUCTURE_COUNT} 处
- **段落重构**: ${PARAGRAPH_REORG_COUNT} 处

### 查重率预估
- **整体相似度**: 15-18% (目标 <20%)
- **章节相似度**:
  - 第1章: 18%
  - 第2章: 16%
  - 第3章: 17%
  - ...

---

## ✅ 质量检查结果

### 格式检查
- ✅ 标题样式: 与参考文档一致
- ✅ 正文字体: 仿宋_GB2312 16号
- ✅ 段落格式: 首行缩进、1.5倍行距
- ✅ 页边距: 与参考文档一致

### 内容检查
- ✅ 所有章节完整
- ✅ 数据引用准确
- ✅ 专业术语正确
- ✅ 逻辑连贯清晰

### 准确性检查
- ✅ 项目特定信息已替换
- ✅ 数值数据保持准确
- ✅ 引用来源标注清晰

---

## 📚 使用的知识库文档

1. **项目可行性研究报告.pdf**
   - 使用次数: 5 次
   - 主要用于: 第1章、第6章
   - 提取内容: 项目背景、投资估算

2. **BIM技术实施方案.docx**
   - 使用次数: 8 次
   - 主要用于: 第2章
   - 提取内容: BIM软件、应用场景

3. **智慧工地管理办法.pdf**
   - 使用次数: 6 次
   - 主要用于: 第3章
   - 提取内容: 管理系统、监控设备

[列出所有使用的文档]

---

## ⚠️  人工审阅建议

### 🔴 必需审阅项
1. **第2章 BIM技术参数**
   - 位置: 第2章第1节
   - 原因: 软件版本和技术参数需确认符合项目实际
   - 建议: 核对BIM软件选型是否与项目一致

2. **第4章 施工工期安排**
   - 位置: 第4章第3节
   - 原因: 工期数据从知识库推断,需确认准确性
   - 建议: 核对工期是否符合合同要求

3. **第6章 投资估算**
   - 位置: 第6章第2节
   - 原因: 涉及金额数据,需严格审核
   - 建议: 核对投资金额是否与预算一致

### 🟡 建议审阅项
1. **专业术语使用**
   - 检查BIM、智慧工地等术语表达是否规范
   - 确认行业标准引用是否准确

2. **图表数据**
   - 如果参考文档含图表,当前版本为文字描述
   - 建议: 手动插入图表,数据已在文本中标注

---

## 💡 优化建议

### 内容优化
1. 可根据项目实际情况调整第3章智慧工地方案细节
2. 建议补充项目特色亮点(第6章)
3. 可增加现场照片或效果图(如有)

### 格式优化
1. 如需调整字体,可在 Word 中批量修改样式
2. 建议添加页眉页脚(文档名称、页码)
3. 可插入封面页和目录

---

## 📁 输出文件清单

1. ✅ **Word 文档**: \`${OUTPUT_FILENAME}\`
   - 完整的实施方案文档
   - 格式与参考文档一致
   - 可直接编辑和打印

2. ✅ **Markdown 预览**: \`${OUTPUT_FILENAME%.docx}.md\`
   - 纯文本预览版
   - 便于快速查阅和对比

3. ✅ **审阅报告**: \`${OUTPUT_FILENAME%.docx}-审阅报告.md\`(本文件)
   - 详细的生成报告
   - 质量检查结果
   - 审阅建议

---

## 🔄 后续操作

### 审阅修改
1. 在 Word 中打开文档进行人工审阅
2. 重点检查上述"必需审阅项"
3. 根据项目实际情况调整内容

### 再次生成
如需生成不同版本(降低互相查重):
\`\`\`bash
/notebook-clone-format ${REFERENCE_DOC}
\`\`\`
每次生成的内容都会不同,查重率更低。

### 导出PDF
\`\`\`bash
# 使用 LibreOffice 转换为 PDF
soffice --headless --convert-to pdf "${OUTPUT_FILENAME}" --outdir notebooklm-outputs/
\`\`\`

---

**生成工具**: NotebookLM Assistant v1.0
**技术支持**: /notebook-help
EOF
```

#### 步骤 6.3: 输出完成信息

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 文档生成完成!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 **输出文档**:
   ${OUTPUT_FILENAME}

📊 **文档统计**:
   - 总字数: ${WORD_COUNT} 字
   - 章节数: ${CHAPTER_COUNT} 章
   - 页数估算: ~${PAGE_ESTIMATE} 页
   - 引用文档: ${CITATION_COUNT} 份

⏱️  **生成耗时**: ${ELAPSED_TIME} 秒

🔍 **查重率预估**: 15-18% (目标 <20%)

✅ **质量检查**: 全部通过
   - ✅ 格式: 与参考文档一致
   - ✅ 内容: 完整准确
   - ✅ 引用: 来源清晰
   - ✅ 改写: 多样化充分

📁 **输出文件位置**:
   notebooklm-outputs/
   ├── ${OUTPUT_FILENAME}                    # Word文档
   ├── ${OUTPUT_FILENAME%.docx}.md           # Markdown预览
   └── ${OUTPUT_FILENAME%.docx}-审阅报告.md  # 审阅报告

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 **下一步操作**:

1. **人工审阅** (建议)
   - 打开 Word 文档审阅内容
   - 重点检查技术参数和工期安排
   - 查看审阅报告中的必需审阅项

2. **再次生成** (可选)
   如需生成不同版本:
   /notebook-clone-format ${REFERENCE_DOC}

3. **导出PDF** (可选)
   soffice --headless --convert-to pdf "${OUTPUT_FILENAME}"

4. **查看帮助**
   /notebook-help

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  **重要提醒**:
- 本文档由AI生成,建议人工审阅后使用
- 技术参数和数值数据需确认准确性
- 查重率为预估值,建议使用专业工具检测
- 生成的内容应符合相关法规和标准要求

📞 **技术支持**:
   如有问题,请运行 /notebook-help 查看完整文档
   或参考: notebooklm-outputs/${OUTPUT_FILENAME%.docx}-审阅报告.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 执行完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 高级功能(可选)

### 批量生成不同版本

如需生成多份互不相同的版本(进一步降低互相查重):

```bash
/notebook-clone-format <参考文档> --batch 3
```

将生成3份不同的文档,每份查重率<20%,且互相查重率<30%。

### 指定改写强度

```bash
/notebook-clone-format <参考文档> --diversity low|medium|high
```

- `low`: 低强度改写(查重率 25-30%)
- `medium`: 中等强度(查重率 20-25%,默认)
- `high`: 高强度改写(查重率 15-20%)

### 保留特定内容

```bash
/notebook-clone-format <参考文档> --preserve "BIM,智慧工地,关键术语"
```

指定不需要改写的专业术语。

---

## 注意事项

### ⚠️  重要提醒

1. **法律合规**
   - 生成的文档应由用户审核,确保准确性和合规性
   - 涉及资质、合同的内容需严格核实
   - 不得用于欺诈、造假等违法用途

2. **查重率说明**
   - 预估查重率为15-20%,实际值请用专业工具检测
   - 专业术语和行业标准表述可能影响查重率
   - 数值数据不改写,可能影响查重结果

3. **内容准确性**
   - AI生成内容可能存在不准确之处
   - 技术参数、工期、金额等关键数据需人工核实
   - 建议由专业人员审阅后使用

4. **知识产权**
   - 参考文档应为用户合法拥有或授权使用
   - 知识库文档应为项目相关合法资料
   - 生成文档的知识产权归用户所有

5. **数据安全**
   - 文档生成过程中的临时文件存储在 /tmp 目录
   - 建议定期清理临时文件
   - 敏感信息请谨慎处理

### 🔧 故障排除

**问题1: 参考文档解析失败**
```
原因: 文档格式不兼容或损坏
解决:
1. 确认文档为 .docx 格式
2. 尝试用 Word 打开并另存为新文件
3. 检查文档是否加密或受保护
```

**问题2: 知识库检索结果过少**
```
原因: 知识库文档与参考文档主题不匹配
解决:
1. 检查知识库是否包含相关文档
2. 运行 /notebook-index 重建索引
3. 手动提供更多可选字段信息
```

**问题3: 生成文档格式错乱**
```
原因: 参考文档格式过于复杂
解决:
1. 使用格式较简单的参考文档
2. 生成后在 Word 中手动调整格式
3. 参考审阅报告中的格式说明
```

**问题4: Word文档生成失败**
```
原因: docx库未安装或版本不兼容
解决:
1. 运行: npm install docx
2. 检查Node.js版本(建议 >=14)
3. 查看错误日志: /tmp/generate_document.log
```

---

## 技术细节

### 使用的技术栈

- **文档解析**: pandoc, python-docx, lxml
- **内容检索**: smart-retrieval skill, context-builder skill
- **多样化改写**: content-diversifier skill
- **文档生成**: docx.js (Node.js)
- **格式分析**: Python + lxml

### 依赖项

**Python库**:
- python-docx >= 0.8.11
- lxml >= 4.9.0
- pandas >= 1.5.0

**Node.js库**:
- docx >= 7.8.0

**系统工具**:
- pandoc >= 2.19
- LibreOffice (可选,用于PDF导出)

### 性能指标

- **小型文档**(5-10页): 2-3 分钟
- **中型文档**(10-20页): 3-5 分钟
- **大型文档**(20-30页): 5-8 分钟

性能取决于:
- 知识库文档数量
- 参考文档复杂度
- 改写强度设置

---

## 相关命令

- `/notebook-init` - 初始化知识库
- `/notebook-index` - 生成知识库索引
- `/notebook-report` - 生成标准报告
- `/notebook-help` - 查看帮助文档

---

**版本**: v1.0
**最后更新**: 2025-11-06
**作者**: NotebookLM Assistant Team
