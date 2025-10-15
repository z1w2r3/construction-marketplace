"""
建筑施工行业文档样式定义

定义符合建筑行业规范的文档样式,包括字体、颜色、排版等
"""
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH


class ConstructionStyles:
    """建筑施工行业文档样式库"""

    # 字体定义
    FONTS = {
        "title": "黑体",          # 大标题
        "heading": "黑体",        # 章节标题
        "body": "宋体",           # 正文
        "table": "宋体",          # 表格
        "code": "Consolas",       # 代码
        "caption": "楷体",        # 图表说明
    }

    # 颜色定义(RGB)
    COLORS = {
        "primary": RGBColor(0, 0, 0),           # 主文本:黑色
        "secondary": RGBColor(102, 102, 102),   # 次要文本:深灰
        "heading": RGBColor(51, 51, 51),        # 标题:深灰黑
        "table_header_bg": "D9E2F3",            # 表头背景:浅蓝
        "table_header_text": RGBColor(0, 0, 0), # 表头文字:黑色
        "quote_bg": "F5F5F5",                   # 引用块背景:浅灰
        "code_bg": "F0F0F0",                    # 代码块背景:灰色
        "placeholder": RGBColor(128, 128, 128), # 占位符:灰色
    }

    # 对齐方式映射
    ALIGNMENT_MAP = {
        "left": WD_ALIGN_PARAGRAPH.LEFT,
        "center": WD_ALIGN_PARAGRAPH.CENTER,
        "right": WD_ALIGN_PARAGRAPH.RIGHT,
        "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
    }

    # 文档模板定义
    TEMPLATES = {
        # 项目总结报告模板
        "project_summary": {
            "name": "项目总结报告",
            "description": "用于项目总结、阶段总结、时期总结",

            # 一级标题(报告名称)
            "h1": {
                "font_name": "黑体",
                "font_size": 22,
                "bold": True,
                "color": "primary",
                "alignment": "center",
                "space_before": 0,
                "space_after": 18,
            },

            # 二级标题(一、二、三)
            "h2": {
                "font_name": "黑体",
                "font_size": 16,
                "bold": True,
                "color": "heading",
                "alignment": "left",
                "space_before": 12,
                "space_after": 6,
            },

            # 三级标题((一)(二))
            "h3": {
                "font_name": "黑体",
                "font_size": 14,
                "bold": True,
                "color": "heading",
                "alignment": "left",
                "space_before": 6,
                "space_after": 3,
            },

            # 四级标题
            "h4": {
                "font_name": "黑体",
                "font_size": 13,
                "bold": True,
                "color": "heading",
                "alignment": "left",
                "space_before": 6,
                "space_after": 3,
            },

            # 五级标题
            "h5": {
                "font_name": "黑体",
                "font_size": 12,
                "bold": True,
                "color": "heading",
                "alignment": "left",
                "space_before": 3,
                "space_after": 3,
            },

            # 六级标题
            "h6": {
                "font_name": "黑体",
                "font_size": 12,
                "bold": True,
                "color": "secondary",
                "alignment": "left",
                "space_before": 3,
                "space_after": 3,
            },

            # 正文
            "body": {
                "font_name": "宋体",
                "font_size": 12,
                "color": "primary",
                "line_spacing": 1.5,
                "first_line_indent": 0,  # 建筑文档通常不缩进
                "alignment": "left",
                "space_after": 6,
            },

            # 表格
            "table": {
                "style": "Light Grid Accent 1",
                "header_bg": "table_header_bg",
                "header_font_name": "黑体",
                "header_font_size": 11,
                "header_bold": True,
                "header_alignment": "center",
                "cell_font_name": "宋体",
                "cell_font_size": 11,
                "cell_alignment": "center",
            },

            # 列表
            "list": {
                "font_name": "宋体",
                "font_size": 12,
                "color": "primary",
                "line_spacing": 1.3,
            },

            # 引用块
            "quote": {
                "font_name": "楷体",
                "font_size": 11,
                "color": "secondary",
                "italic": True,
                "left_indent": Inches(0.5),
                "space_after": 6,
            },

            # 代码块
            "code": {
                "font_name": "Consolas",
                "font_size": 10,
                "color": "primary",
                "line_spacing": 1.2,
                "left_indent": Inches(0.3),
            },
        },

        # 资料完整性检查报告模板
        "inspection_report": {
            "name": "资料完整性检查报告",
            "description": "用于资料完整性检查、专项检查",

            "h1": {
                "font_name": "黑体",
                "font_size": 22,
                "bold": True,
                "color": "primary",
                "alignment": "center",
                "space_before": 0,
                "space_after": 18,
            },

            "h2": {
                "font_name": "黑体",
                "font_size": 15,
                "bold": True,
                "color": "heading",
                "alignment": "left",
                "space_before": 12,
                "space_after": 6,
            },

            "h3": {
                "font_name": "黑体",
                "font_size": 13,
                "bold": True,
                "color": "heading",
                "alignment": "left",
                "space_before": 6,
                "space_after": 3,
            },

            "h4": {"font_name": "黑体", "font_size": 12, "bold": True, "alignment": "left"},
            "h5": {"font_name": "黑体", "font_size": 12, "bold": True, "alignment": "left"},
            "h6": {"font_name": "黑体", "font_size": 12, "bold": False, "alignment": "left"},

            "body": {
                "font_name": "宋体",
                "font_size": 12,
                "line_spacing": 1.5,
                "alignment": "left",
            },

            "table": {
                "style": "Light Grid Accent 1",
                "header_bg": "table_header_bg",
                "header_font_name": "黑体",
                "header_font_size": 11,
                "header_bold": True,
                "cell_font_name": "宋体",
                "cell_font_size": 10,
            },

            "list": {"font_name": "宋体", "font_size": 12, "line_spacing": 1.3},
            "quote": {"font_name": "楷体", "font_size": 11, "italic": True},
            "code": {"font_name": "Consolas", "font_size": 10},
        },

        # 进度分析报告模板
        "progress_analysis": {
            "name": "进度分析报告",
            "description": "用于进度分析、进度对比",

            "h1": {
                "font_name": "黑体",
                "font_size": 20,
                "bold": True,
                "alignment": "center",
                "space_after": 15,
            },

            "h2": {
                "font_name": "黑体",
                "font_size": 15,
                "bold": True,
                "space_before": 12,
                "space_after": 6,
            },

            "h3": {"font_name": "黑体", "font_size": 13, "bold": True},
            "h4": {"font_name": "黑体", "font_size": 12, "bold": True},
            "h5": {"font_name": "黑体", "font_size": 12, "bold": True},
            "h6": {"font_name": "黑体", "font_size": 11, "bold": True},

            "body": {"font_name": "宋体", "font_size": 12, "line_spacing": 1.5},

            "table": {
                "style": "Light Grid Accent 1",
                "header_bg": "table_header_bg",
                "header_font_name": "黑体",
                "header_font_size": 11,
                "header_bold": True,
                "cell_font_name": "宋体",
                "cell_font_size": 11,
            },

            "list": {"font_name": "宋体", "font_size": 12},
            "quote": {"font_name": "楷体", "font_size": 11, "italic": True},
            "code": {"font_name": "Consolas", "font_size": 10},
        },

        # 整理方案模板
        "organize_plan": {
            "name": "资料整理方案",
            "description": "用于资料整理方案、归档方案",

            "h1": {
                "font_name": "黑体",
                "font_size": 20,
                "bold": True,
                "alignment": "center",
                "space_after": 15,
            },

            "h2": {
                "font_name": "黑体",
                "font_size": 15,
                "bold": True,
                "space_before": 12,
                "space_after": 6,
            },

            "h3": {"font_name": "黑体", "font_size": 13, "bold": True},
            "h4": {"font_name": "黑体", "font_size": 12, "bold": True},
            "h5": {"font_name": "黑体", "font_size": 12, "bold": True},
            "h6": {"font_name": "黑体", "font_size": 11, "bold": True},

            "body": {"font_name": "宋体", "font_size": 12, "line_spacing": 1.5},

            "table": {
                "style": "Light Grid Accent 1",
                "header_bg": "table_header_bg",
                "header_font_name": "黑体",
                "header_font_size": 11,
                "header_bold": True,
                "cell_font_name": "宋体",
                "cell_font_size": 11,
            },

            "list": {"font_name": "宋体", "font_size": 12},
            "quote": {"font_name": "楷体", "font_size": 11, "italic": True},
            "code": {"font_name": "Consolas", "font_size": 10},
        },
    }

    @classmethod
    def get_template(cls, template_name: str) -> dict:
        """
        获取模板配置

        Args:
            template_name: 模板名称

        Returns:
            模板配置字典

        Raises:
            ValueError: 模板不存在
        """
        if template_name not in cls.TEMPLATES:
            available = ", ".join(cls.TEMPLATES.keys())
            raise ValueError(
                f"未知模板: {template_name}。可用模板: {available}"
            )

        return cls.TEMPLATES[template_name]

    @classmethod
    def get_color(cls, color_name: str) -> RGBColor:
        """
        获取颜色对象

        Args:
            color_name: 颜色名称

        Returns:
            RGBColor对象
        """
        if color_name in cls.COLORS:
            color = cls.COLORS[color_name]
            if isinstance(color, RGBColor):
                return color
            # 如果是字符串(十六进制),转换为RGBColor
            elif isinstance(color, str):
                return cls.hex_to_rgb(color)

        # 默认返回黑色
        return cls.COLORS["primary"]

    @staticmethod
    def hex_to_rgb(hex_color: str) -> RGBColor:
        """
        将十六进制颜色转换为RGBColor对象

        Args:
            hex_color: 十六进制颜色(如"D9E2F3")

        Returns:
            RGBColor对象
        """
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return RGBColor(r, g, b)

    @classmethod
    def list_templates(cls) -> list:
        """
        列出所有可用模板

        Returns:
            模板信息列表
        """
        templates = []
        for name, config in cls.TEMPLATES.items():
            templates.append({
                "name": name,
                "display_name": config.get("name", name),
                "description": config.get("description", ""),
            })
        return templates
