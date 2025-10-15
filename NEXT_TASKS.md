# 🚀 建筑文档助手 - 未完成工作清单

**最后更新**: 2025-10-15
**当前版本**: v1.2.0
**Git提交**: `4c6d1ea` - Phase 1 Word生成功能已完成

---

## ✅ 已完成工作(本次会话)

### Phase 1: Markdown转Word文档生成

- ✅ 创建generators模块(5个核心文件,~45KB代码)
- ✅ 实现Markdown解析器(支持标题/段落/表格/列表/引用/代码块)
- ✅ 实现Word生成器(4种专业模板)
- ✅ 集成到MCP服务器(新增generate_word_report工具)
- ✅ 更新construction-summary命令(添加Word生成步骤)
- ✅ 编写使用文档(generators/README.md)

**提交信息**:
```bash
git log --oneline -1
# 4c6d1ea feat: 实现Markdown转Word文档生成功能(Phase 1)
```

---

## 🔴 高优先级 - 必须完成的任务

### 任务1: 测试Word生成功能 ⭐⭐⭐⭐⭐

**目标**: 验证Word生成功能是否正常工作

**步骤**:
1. 重启MCP服务器(确保新代码加载)
2. 创建测试Markdown文件
3. 运行construction-summary命令
4. 检查生成的Word文档

**测试用例**:

```markdown
# 测试Markdown文件内容

创建文件: test-report.md

---
# 项目总结报告

## 一、项目概况

项目名称:测试项目
建设地点:测试地点

## 二、进度情况

| 工程阶段 | 计划完成 | 实际完成 | 状态 |
|---------|---------|---------|------|
| 基础施工 | 100% | 100% | ✅ |
| 主体结构 | 80% | 75% | ⚠️ |

## 三、列表测试

### 无序列表
- 项目1
- 项目2
- 项目3

### 有序列表
1. 第一项
2. 第二项
3. 第三项

## 四、引用测试

> 这是一段引用文字,用于测试引用块的样式。

## 五、代码块测试

```bash
echo "测试代码块"
ls -la
```

## 六、图片测试

![测试图片](./test.jpg)

---

生成时间: 2025-10-15
```

**手动测试命令**:
```bash
# 1. 进入项目目录
cd /Users/zhengwr/workspace/baogao1/construction-marketplace/plugins/construction-doc-assistant

# 2. 测试MCP工具(使用Python直接调用)
cd mcp-servers/document-processor
python -c "
from generators import WordGenerator

generator = WordGenerator('project_summary')
result = generator.generate(
    markdown_file='/path/to/test-report.md',
    output_file='/path/to/test-report.docx',
    options={'project_info': {
        'project_name': '测试项目',
        'report_type': '测试报告',
        'generate_date': '2025-10-15'
    }}
)
print(result)
"
```

**预期结果**:
- ✅ Word文档生成成功
- ✅ 文件大小: 50-100KB
- ✅ 页眉显示项目名称和报告类型
- ✅ 页脚显示页码
- ✅ 表格显示三线表样式
- ✅ 图片显示占位符

**如果失败**:
- 检查Python依赖: `pip list | grep docx`
- 查看MCP服务器日志(stderr输出)
- 检查文件路径是否为绝对路径

---

### 任务2: 完善其他命令的Word生成功能 ⭐⭐⭐⭐

**需要修改的命令文件**:

#### 2.1 construction-check.md (完整性检查报告)

**位置**: `commands/construction-check.md`

**修改内容**: 在保存报告步骤后添加Word生成步骤

```markdown
### [最后一步+1]. 生成Word文档

使用 MCP 工具生成Word文档:

mcp__construction_doc_processor__generate_word_report:
  markdown_file: [步骤X保存的Markdown文件路径]
  output_file: [同目录下,将.md替换为.docx]
  template_type: "inspection_report"  # 使用完整性检查模板
  project_info:
    project_name: [从配置文件读取]
    report_type: "资料完整性检查报告"
    generate_date: [当前日期]
```

**模板类型**: `inspection_report`

---

#### 2.2 construction-progress.md (进度分析报告)

**位置**: `commands/construction-progress.md`

**修改内容**: 添加Word生成步骤

```markdown
### [最后一步+1]. 生成Word文档

mcp__construction_doc_processor__generate_word_report:
  markdown_file: [Markdown文件路径]
  output_file: [Word文件路径]
  template_type: "progress_analysis"  # 使用进度分析模板
  project_info:
    project_name: [从配置文件读取]
    report_type: "进度分析报告"
    generate_date: [当前日期]
```

**模板类型**: `progress_analysis`

---

#### 2.3 construction-organize.md (整理方案)

**位置**: `commands/construction-organize.md`

**修改内容**: 添加Word生成步骤

```markdown
### [最后一步+1]. 生成Word文档

mcp__construction_doc_processor__generate_word_report:
  markdown_file: [Markdown文件路径]
  output_file: [Word文件路径]
  template_type: "organize_plan"  # 使用整理方案模板
  project_info:
    project_name: [从配置文件读取]
    report_type: "资料整理方案"
    generate_date: [当前日期]
```

**模板类型**: `organize_plan`

---

**工作量估算**: 每个命令约15分钟,总计1小时

---

## 🟡 中优先级 - 重要但不紧急

### 任务3: 索引优先读取优化 ⭐⭐⭐⭐

**目标**: 实现从索引文件读取文档信息,避免重复扫描文件系统

#### 3.1 实现索引读取工具

**新增文件**: `mcp-servers/document-processor/utils/index_reader.py`

```python
"""
索引文件读取工具

从索引文件中提取JSON元数据
"""
import os
import re
import json
from typing import Dict, Optional

def read_index_file(index_file: str) -> Dict:
    """
    读取索引文件的JSON元数据

    Args:
        index_file: 索引文件路径

    Returns:
        索引数据字典或错误信息
    """
    if not os.path.exists(index_file):
        return {
            "status": "error",
            "error": f"索引文件不存在: {index_file}"
        }

    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取JSON代码块
        json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)

        if json_match:
            index_data = json.loads(json_match.group(1))
            return {
                "status": "success",
                "index_data": index_data,
                "index_file": index_file
            }
        else:
            return {
                "status": "error",
                "error": "索引文件中未找到JSON元数据块"
            }

    except Exception as e:
        return {
            "status": "error",
            "error": f"读取索引失败: {str(e)}"
        }

def find_latest_index(index_dir: str) -> Optional[str]:
    """
    查找最新的索引文件

    Args:
        index_dir: 索引目录路径

    Returns:
        最新索引文件路径或None
    """
    if not os.path.exists(index_dir):
        return None

    index_files = [
        f for f in os.listdir(index_dir)
        if f.startswith("文档索引-") and f.endswith(".md")
    ]

    if not index_files:
        return None

    # 按文件名排序(包含时间戳)
    index_files.sort(reverse=True)
    return os.path.join(index_dir, index_files[0])
```

**工作量估算**: 1-2小时

---

#### 3.2 在server.py中添加MCP工具

**位置**: `mcp-servers/document-processor/server.py`

**在list_tools()中添加**:

```python
# 10. 读取文档索引(新增)
Tool(
    name="read_document_index",
    description="读取文档索引的JSON元数据",
    inputSchema={
        "type": "object",
        "properties": {
            "index_file": {
                "type": "string",
                "description": "索引文件路径"
            }
        },
        "required": ["index_file"]
    }
)
```

**在call_tool()中添加**:

```python
elif name == "read_document_index":
    from utils.index_reader import read_index_file

    result = read_index_file(arguments["index_file"])

    return [TextContent(
        type="text",
        text=_format_index_result(result)
    )]
```

**添加格式化函数**:

```python
def _format_index_result(result: dict) -> str:
    """格式化索引读取结果"""
    if result.get("status") == "error":
        return f"❌ 索引读取失败: {result.get('error')}"

    index_data = result.get("index_data", {})

    output = f"""✅ 索引读取成功

📄 索引文件: {result.get('index_file')}
📊 索引版本: {index_data.get('index_version', 'Unknown')}
📅 生成时间: {index_data.get('generated_at', 'Unknown')}
📦 文档总数: {index_data.get('total_documents', 0)}

📁 文档类型分布:
"""

    doc_types = index_data.get('document_types', {})
    for doc_type, count in doc_types.items():
        output += f"  - {doc_type}: {count} 个\n"

    # 关键词索引
    keyword_index = index_data.get('keyword_index', {})
    if keyword_index:
        output += f"\n🔍 关键词索引 ({len(keyword_index)} 个关键词):\n"
        for keyword in list(keyword_index.keys())[:5]:
            count = len(keyword_index[keyword])
            output += f"  - {keyword}: {count} 个文档\n"
        if len(keyword_index) > 5:
            output += f"  ... 还有 {len(keyword_index) - 5} 个关键词\n"

    return output
```

**工作量估算**: 1小时

---

#### 3.3 修改construction-index.md生成JSON元数据

**位置**: `commands/construction-index.md`

**在生成索引文件时添加JSON代码块**:

```markdown
在索引文件末尾添加JSON元数据:

```json
{
  "index_version": "1.2.0",
  "generated_at": "[ISO 8601格式时间]",
  "project_name": "[从配置读取]",
  "source_directory": "[原文档路径]",
  "total_documents": [文档总数],
  "document_types": {
    "pdf": [PDF数量],
    "docx": [Word数量],
    "xlsx": [Excel数量],
    "pptx": [PowerPoint数量]
  },
  "keyword_index": {
    "进度": ["路径1", "路径2"],
    "质量": ["路径3", "路径4"],
    "安全": ["路径5"],
    "概况": ["路径6"]
  },
  "important_documents": [
    {
      "name": "文件名",
      "path": "绝对路径",
      "category": "分类",
      "size": 字节数,
      "modified": "修改时间"
    }
  ]
}
```
```

**关键词分类规则**:
- 文件名包含"进度"、"计划" → keyword_index["进度"]
- 文件名包含"质量"、"验收" → keyword_index["质量"]
- 文件名包含"安全"、"检查" → keyword_index["安全"]
- 文件名包含"概况"、"介绍" → keyword_index["概况"]

**工作量估算**: 2小时

---

#### 3.4 优化命令使用索引优先读取

**需要修改的命令**:
- construction-summary.md
- construction-check.md
- construction-search.md
- construction-organize.md

**修改模式**(以construction-summary为例):

```markdown
### 3. 识别关键文档

#### 3.1 检查索引文件是否存在

使用 Bash 查找最新索引:
```bash
find "生成文件/索引" -name "文档索引-*.md" -type f | sort -r | head -1
```

#### 3.2 优先从索引读取(如果索引存在)

使用 MCP 工具读取索引:
```
mcp__construction_doc_processor__read_document_index:
  index_file: [步骤3.1找到的索引文件路径]
```

从返回的 index_data 中提取:
- 概况文档: index_data["keyword_index"]["概况"]
- 进度文档: index_data["keyword_index"]["进度"]
- 质量文档: index_data["keyword_index"]["质量"]

如果索引读取成功 → 使用索引文档列表,跳过文件系统扫描
如果索引不存在或失败 → 继续文件系统扫描

#### 3.3 回退到文件系统扫描

[保持原有的find命令扫描逻辑]
```

**工作量估算**: 每个命令30分钟,总计2小时

---

**任务3总工作量**: 5-6小时

---

## 🟢 低优先级 - 功能增强

### 任务4: Phase 2 - 图片插入功能 ⭐⭐⭐

**目标**: 实现图片从Markdown到Word的插入

**依赖**: 需要安装Pillow库

```bash
cd mcp-servers/document-processor
echo "Pillow>=10.0.0" >> requirements.txt
source venv/bin/activate
pip install Pillow
```

**修改文件**: `generators/word_generator.py`

**在_add_image_placeholder方法中实现图片插入**:

```python
def _add_image_placeholder(self, section: Dict):
    """添加图片(Phase 2实现)"""
    from PIL import Image
    import io

    alt_text = section.get("alt", "图片")
    image_url = section.get("url", "")

    # 1. 解析图片路径
    if image_url.startswith('http'):
        # TODO: 下载网络图片
        self._add_placeholder_text(alt_text, image_url, "网络图片暂不支持")
        return

    # 相对路径转绝对路径
    if not os.path.isabs(image_url):
        markdown_dir = os.path.dirname(self.markdown_file)
        image_path = os.path.join(markdown_dir, image_url)
    else:
        image_path = image_url

    # 2. 验证图片存在
    if not os.path.exists(image_path):
        self._add_placeholder_text(alt_text, image_url, "文件不存在")
        return

    try:
        # 3. 打开并预处理图片
        img = Image.open(image_path)

        # 转换为RGB
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')

        # 调整大小(如果过大)
        max_width = 1200
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

        # 保存到内存(压缩)
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG', quality=85, optimize=True)
        img_buffer.seek(0)

        # 4. 插入Word
        paragraph = self.doc.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

        run = paragraph.add_run()

        # 计算显示宽度
        max_width_inch = 6.0  # Word页面宽度
        width_inch = img.width / 96
        if width_inch > max_width_inch:
            width_inch = max_width_inch

        run.add_picture(img_buffer, width=Inches(width_inch))

        # 5. 添加题注
        caption = self.doc.add_paragraph()
        caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        caption_run = caption.add_run(alt_text)
        caption_run.font.size = Pt(10)
        caption_run.font.italic = True
        caption_run.font.color.rgb = ConstructionStyles.COLORS["secondary"]

        caption.paragraph_format.space_after = Pt(12)

        self.logger.info(f"✅ 图片插入成功: {alt_text}")

    except Exception as e:
        self.logger.error(f"图片插入失败: {e}")
        self._add_placeholder_text(alt_text, image_url, f"插入失败: {str(e)}")
```

**工作量估算**: 2-3小时

---

### 任务5: 更新README和文档 ⭐⭐

**需要更新的文件**:

1. **主README.md** - 更新版本号和功能列表
2. **plugin.json** - 更新版本到1.2.0
3. **marketplace.json** - 更新版本和描述
4. **CHANGELOG.md** - 添加版本更新日志

**CHANGELOG.md示例**:

```markdown
# 更新日志

## [1.2.0] - 2025-10-15

### 新增
- ✨ Markdown转Word文档生成功能(Phase 1)
- ✨ 4种专业报告模板
- ✨ 自动页眉页脚和页码
- ✨ 建筑行业标准排版样式

### 修改
- 🔧 MCP服务器升级到v1.2.0
- 🔧 construction-summary命令增加Word生成步骤

### 待完成
- 🚧 图片插入功能(Phase 2)
- 🚧 索引优先读取优化
- 🚧 其他命令的Word生成集成

## [1.0.2] - 2025-10-14

### 新增
- ✨ 完整的文档解析功能
- ✨ 批量文档处理
- ✨ 智能摘要提取

### 修复
- 🐛 修复Windows路径问题
- 🐛 修复MCP服务器配置

## [1.0.0] - 2025-10-10

### 新增
- 🎉 初始版本发布
- ✨ 8个核心命令
- ✨ MCP文档处理服务器
```

**工作量估算**: 1小时

---

## 📋 工作优先级建议

### 第一天(4-5小时)
1. ✅ **测试Word生成功能** (1小时) - 确保基础功能正常
2. ✅ **完善其他3个命令** (1小时) - check/progress/organize
3. ✅ **修复发现的问题** (1-2小时) - 根据测试结果修复bug
4. ✅ **更新文档** (1小时) - README和CHANGELOG

### 第二天(5-6小时)
1. ✅ **索引读取工具** (2小时) - index_reader.py
2. ✅ **MCP工具集成** (1小时) - server.py
3. ✅ **修改index命令** (2小时) - 生成JSON元数据
4. ✅ **优化4个命令** (2小时) - 使用索引优先读取

### 第三天(可选,Phase 2)
1. ✅ **图片插入功能** (2-3小时)
2. ✅ **测试和调试** (2小时)
3. ✅ **文档完善** (1小时)

---

## 🔍 测试检查清单

### Word生成功能测试

- [ ] 标题层级正确(H1-H6)
- [ ] 段落样式正确(宋体12pt,1.5倍行距)
- [ ] 表格显示三线表样式
- [ ] 表头背景色为浅蓝色
- [ ] 列表格式正确
- [ ] 引用块样式正确
- [ ] 代码块使用等宽字体
- [ ] 页眉显示项目名称
- [ ] 页脚显示页码
- [ ] 图片占位符显示正确
- [ ] 文件大小合理(50-200KB)
- [ ] 各种模板样式正确

### 索引功能测试

- [ ] 索引文件包含JSON元数据
- [ ] JSON格式正确(可用jq验证)
- [ ] 关键词索引分类正确
- [ ] 命令能成功读取索引
- [ ] 从索引读取比扫描快70%+
- [ ] 索引失败时能回退到扫描

---

## 📞 遇到问题时的排查步骤

### 问题1: Word生成失败

**排查**:
1. 检查python-docx是否安装: `pip list | grep docx`
2. 查看MCP服务器日志(stderr)
3. 确认Markdown文件路径是绝对路径
4. 检查输出目录是否有写权限

### 问题2: MCP工具不可用

**排查**:
1. 重启Claude Code
2. 检查.mcp.json配置
3. 运行`claude --debug`查看日志
4. 手动测试MCP服务器: `python server.py`

### 问题3: 样式不正确

**排查**:
1. 检查construction_styles.py配置
2. 在Word中检查"设计"选项卡样式
3. 手动调整Word模板
4. 重新生成文档

---

## 📚 相关文档链接

- **Word生成器文档**: [generators/README.md](plugins/construction-doc-assistant/mcp-servers/document-processor/generators/README.md)
- **MCP服务器**: [mcp-servers/document-processor/server.py](plugins/construction-doc-assistant/mcp-servers/document-processor/server.py)
- **主项目文档**: [CLAUDE.md](plugins/construction-doc-assistant/CLAUDE.md)
- **Git提交历史**: `git log --oneline`

---

## 🎯 下次会话开始时的操作

```bash
# 1. 查看代码状态
cd /Users/zhengwr/workspace/baogao1/construction-marketplace
git status
git log --oneline -5

# 2. 查看未完成任务
cat NEXT_TASKS.md

# 3. 继续开发
# 从"高优先级任务"开始执行
```

---

**生成时间**: 2025-10-15
**文档维护者**: Claude + Human
**联系方式**: 参考主项目README
