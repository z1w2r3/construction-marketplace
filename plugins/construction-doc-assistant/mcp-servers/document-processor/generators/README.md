# Word文档生成器模块

## 📋 模块概述

这个模块提供将Markdown报告转换为专业排版Word文档的功能,专为建筑施工行业设计。

**当前版本**: Phase 1 - 纯文字排版(图片功能预留在Phase 2)

## 📁 文件结构

```
generators/
├── __init__.py                  # 模块导出
├── base_generator.py            # 生成器基类(4.4KB)
├── construction_styles.py       # 建筑行业样式库(12KB)
├── markdown_parser.py           # Markdown解析器(10KB)
├── word_generator.py            # Word生成器(19KB)
└── README.md                    # 本文件
```

## 🚀 快速使用

### 在命令中调用

```markdown
使用 MCP 工具生成Word文档:

mcp__construction_doc_processor__generate_word_report:
  markdown_file: "生成文件/项目总结/项目总结-整体-20251015-143022.md"
  output_file: "生成文件/项目总结/项目总结-整体-20251015-143022.docx"
  template_type: "project_summary"
  project_info:
    project_name: "XX建设项目"
    report_type: "项目总结报告"
    generate_date: "2025-10-15"
```

### Python代码调用

```python
from generators import WordGenerator

# 创建生成器
generator = WordGenerator(template_type="project_summary")

# 生成Word文档
result = generator.generate(
    markdown_file="report.md",
    output_file="report.docx",
    options={
        "project_info": {
            "project_name": "XX建设项目",
            "report_type": "项目总结报告",
            "generate_date": "2025-10-15"
        }
    }
)

# 检查结果
if result["status"] == "success":
    print(f"✅ 生成成功: {result['output_file']}")
    print(f"文件大小: {result['file_size']} bytes")
else:
    print(f"❌ 生成失败: {result['error']}")
```

## 📝 支持的Markdown语法

### ✅ Phase 1已支持

| 元素 | Markdown语法 | Word效果 |
|------|-------------|---------|
| **一级标题** | `# 标题` | 黑体22pt,居中,加粗 |
| **二级标题** | `## 标题` | 黑体16pt,左对齐,加粗 |
| **三级标题** | `### 标题` | 黑体14pt,左对齐,加粗 |
| **段落** | 普通文本 | 宋体12pt,1.5倍行距 |
| **表格** | `\| 列1 \| 列2 \|` | 三线表,表头蓝色背景 |
| **无序列表** | `- 项目` | 带圆点列表 |
| **有序列表** | `1. 项目` | 带数字列表 |
| **引用块** | `> 引用` | 楷体,斜体,左缩进 |
| **代码块** | ` ```code``` ` | Consolas字体,灰色背景 |
| **水平线** | `---` | 下划线分隔符 |

### 🔲 Phase 1占位符

| 元素 | Markdown语法 | Word效果 |
|------|-------------|---------|
| **图片** | `![说明](path)` | 显示`[图片: 说明]`占位符 |

### 🚧 Phase 2计划支持

- ✅ 图片插入和自动调整大小
- ✅ 图片题注
- ✅ 图片对齐(居中/左对齐)
- ✅ 图片压缩优化
- ⚠️ 超链接(可选)
- ⚠️ 文字颜色/高亮(可选)

## 🎨 样式模板

### 1. project_summary (项目总结报告)

**适用于**: 项目总结、阶段总结、时期总结

**特点**:
- 一级标题:黑体22pt,居中
- 二级标题:黑体16pt,左对齐
- 正文:宋体12pt,1.5倍行距
- 表格:三线表样式,表头蓝色背景

### 2. inspection_report (完整性检查报告)

**适用于**: 资料完整性检查、专项检查

**特点**:
- 与项目总结类似,但标题稍小
- 强调数据表格展示

### 3. progress_analysis (进度分析报告)

**适用于**: 进度分析、进度对比

**特点**:
- 紧凑的排版
- 适合数据密集型报告

### 4. organize_plan (整理方案)

**适用于**: 资料整理方案、归档方案

**特点**:
- 清晰的层级结构
- 适合流程说明

## 🔧 技术细节

### Markdown解析

使用正则表达式解析Markdown,支持:
- 标题:`^(#{1,6})\s+(.+)$`
- 表格:`^\|(.+)\|$`
- 列表:`^(\s*)([-*+]|\d+\.)\s+(.+)$`
- 引用:`^>\s+(.+)$`
- 代码块:` ```language\n...\n``` `

### Word样式应用

```python
# 标题样式
heading.runs[0].font.name = "黑体"
heading.runs[0].font.size = Pt(16)
heading.runs[0].font.bold = True

# 表格样式
table.style = "Light Grid Accent 1"
header_cell.shading.fill = RGBColor(217, 226, 243)  # 浅蓝色

# 段落样式
paragraph.paragraph_format.line_spacing = 1.5
paragraph.paragraph_format.space_after = Pt(6)
```

## ⚠️ 注意事项

### 文件路径

- 所有路径必须是**绝对路径**
- Windows用户注意路径分隔符(`\`需要转义或使用`/`)

### 文件权限

- 输出目录必须可写
- 如果输出文件已存在,会被覆盖

### 性能

- 小文件(<100KB): <2秒
- 中文件(100KB-1MB): 2-5秒
- 大文件(>1MB): 5-10秒

### 错误处理

生成器会捕获所有错误并返回友好提示:
- Markdown文件不存在
- 输出目录无权限
- Markdown语法解析失败

## 📊 输出示例

**输入Markdown**:
```markdown
# 项目总结报告

## 一、项目概况

项目名称:XX建设项目

## 二、进度情况

| 工程阶段 | 计划 | 实际 |
|---------|------|------|
| 基础施工 | 100% | 100% |
| 主体结构 | 80% | 75% |
```

**输出Word效果**:
- 页眉:"XX建设项目 - 项目总结报告"
- 页脚:"第 1 页"
- "项目总结报告":黑体22pt,居中
- "一、项目概况":黑体16pt,左对齐
- "项目名称:XX建设项目":宋体12pt
- 表格:三线表,表头蓝色背景,数据居中对齐

## 🐛 已知限制

1. **图片**: Phase 1仅显示占位符,不插入实际图片
2. **超链接**: 当前不保留超链接,仅显示文字
3. **嵌套列表**: 仅支持单层列表
4. **表格合并**: 不支持单元格合并
5. **行内样式**: 粗体/斜体标记会被移除(文字保留)

## 🔮 未来规划

### Phase 2: 图片支持(下一版本)

- [ ] 插入本地图片
- [ ] 下载网络图片
- [ ] 图片自动缩放
- [ ] 图片压缩优化
- [ ] 图片题注

### Phase 3: 高级排版

- [ ] 目录自动生成
- [ ] 图表交叉引用
- [ ] 页码样式自定义
- [ ] 多列布局

## 📞 支持

如有问题,请查看:
- 主项目文档:[CLAUDE.md](../../CLAUDE.md)
- MCP服务器日志:stderr输出
- 测试示例:[../tests/](../tests/)

---

**版本**: v1.2.0
**更新日期**: 2025-10-15
**作者**: Construction Team
