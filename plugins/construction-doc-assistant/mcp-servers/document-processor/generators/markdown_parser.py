"""
Markdown解析器

将Markdown文本解析为结构化数据(AST),用于后续转换为Word文档
"""
import re
import os
import sys
from typing import List, Dict, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import get_logger

logger = get_logger(__name__)


class MarkdownParser:
    """Markdown解析器 - 使用正则表达式解析"""

    # 正则表达式模式
    HEADING_PATTERN = r'^(#{1,6})\s+(.+)$'  # 标题
    TABLE_ROW_PATTERN = r'^\|(.+)\|$'  # 表格行
    TABLE_SEPARATOR_PATTERN = r'^\|[\s\-:]+\|$'  # 表格分隔符
    LIST_PATTERN = r'^(\s*)([-*+]|\d+\.)\s+(.+)$'  # 列表项
    QUOTE_PATTERN = r'^>\s+(.+)$'  # 引用
    CODE_BLOCK_START = r'^```(\w*)$'  # 代码块开始
    CODE_BLOCK_END = r'^```$'  # 代码块结束
    IMAGE_PATTERN = r'!\[(.*?)\]\((.*?)(?:\s+"(.*?)")?\)'  # 图片
    HORIZONTAL_RULE = r'^(\*{3,}|-{3,}|_{3,})$'  # 水平线

    # 行内样式模式
    BOLD_PATTERN = r'\*\*(.+?)\*\*'  # 粗体
    ITALIC_PATTERN = r'\*(.+?)\*'  # 斜体
    CODE_INLINE_PATTERN = r'`(.+?)`'  # 行内代码

    # 技术性元数据标记模式(需要过滤的内容)
    TECHNICAL_METADATA_PATTERNS = [
        r'^\*\*统计\*\*[:：].*?成功\s*\d+.*?失败\s*\d+',  # "**统计**: 成功5个 | 失败0个"
        r'^文档读取情况[:：].*?成功.*?失败',  # "文档读取情况: 成功X个 | 失败Y个"
        r'^\*\*来源\*\*[:：].*?claude/CLAUDE-construction\.md',  # "**来源**: 《claude/CLAUDE-construction.md》"
        r'^\*\*来源\*\*[:：].*?\(.*?个章节.*?\)',  # "**来源**: 《XXX》(41个章节,48段落)"
        r'^\*\*数据来源\*\*[:：]',  # "**数据来源**:"
        r'^##\s*[📊📋🔍]*\s*文档读取情况$',  # "## 📊 文档读取情况"
        r'^##\s*数据来源$',  # "## 数据来源"
        r'^##\s*[📋]*\s*报告质量说明$',  # "## 📋 报告质量说明"
        r'^##\s*附录[:：]\s*参考文档列表$',  # "## 附录: 参考文档列表"（如果包含技术信息）
        r'^\*\*数据准确性\*\*[:：].*本报告所有数据均来自原始文档',  # 技术性说明
        r'^\*\*信息完整性\*\*[:：]',  # 技术性说明
        r'^\*\*使用建议\*\*[:：]',  # 技术性说明（位于报告质量说明中）
        r'^\*\*生成工具\*\*[:：]',  # "**生成工具**: 建筑施工文档助手"
        r'^路径[:：]\s*/Volumes/',  # 内部文件路径
        r'提取内容[:：].*?段落.*?表格',  # "提取内容: 27段落,3个表格"
    ]

    # 需要完整删除的章节标题（包括其下所有内容）
    TECHNICAL_SECTIONS_TO_REMOVE = [
        r'^##\s*[📊📋🔍]*\s*文档读取情况\s*$',
        r'^##\s*[📋]*\s*报告质量说明\s*$',
        r'^##\s*数据来源\s*$',
    ]

    def __init__(self):
        self.logger = logger

    def is_technical_metadata(self, line: str) -> bool:
        """
        判断一行文本是否为技术性元数据

        Args:
            line: 文本行

        Returns:
            True表示是技术性元数据,应该被过滤
        """
        line_stripped = line.strip()
        for pattern in self.TECHNICAL_METADATA_PATTERNS:
            if re.match(pattern, line_stripped):
                return True
        return False

    def is_technical_section_start(self, line: str) -> bool:
        """
        判断一行是否为需要删除的技术章节开始

        Args:
            line: 文本行

        Returns:
            True表示是技术章节标题,该章节应被完整删除
        """
        line_stripped = line.strip()
        for pattern in self.TECHNICAL_SECTIONS_TO_REMOVE:
            if re.match(pattern, line_stripped):
                return True
        return False

    def parse(self, markdown_text: str, filter_technical_metadata: bool = True) -> List[Dict[str, Any]]:
        """
        解析Markdown文本为结构化段落列表

        Args:
            markdown_text: Markdown文本内容

        Returns:
            段落列表,每个段落是一个字典:
            [
                {"type": "heading", "level": 1, "text": "标题"},
                {"type": "paragraph", "text": "段落文本"},
                {"type": "table", "headers": [...], "rows": [...]},
                {"type": "list", "ordered": False, "items": [...]},
                {"type": "quote", "text": "引用"},
                {"type": "code", "text": "代码", "language": "python"},
                {"type": "image", "alt": "说明", "url": "路径"},
                {"type": "horizontal_rule"},
            ]
        """
        sections = []
        lines = markdown_text.split('\n')
        i = 0
        skip_until_next_section = False  # 用于跳过整个技术章节

        while i < len(lines):
            line = lines[i]

            # 跳过空行
            if not line.strip():
                i += 1
                continue

            # 检查是否遇到新的章节标题（##开头）
            if re.match(r'^##\s+', line):
                # 检查是否为需要删除的技术章节
                if filter_technical_metadata and self.is_technical_section_start(line):
                    self.logger.info(f"跳过技术章节: {line[:50]}...")
                    skip_until_next_section = True
                    i += 1
                    continue
                else:
                    # 遇到新的正常章节，停止跳过
                    skip_until_next_section = False

            # 如果在技术章节内，跳过所有内容直到下一个章节
            if skip_until_next_section:
                i += 1
                continue

            # 过滤技术性元数据行
            if filter_technical_metadata and self.is_technical_metadata(line):
                self.logger.debug(f"过滤技术性元数据: {line[:50]}...")
                i += 1
                continue

            # 1. 标题
            heading_match = re.match(self.HEADING_PATTERN, line)
            if heading_match:
                level = len(heading_match.group(1))
                text = heading_match.group(2).strip()
                # 清理行内格式标记
                text = self.strip_inline_styles(text)
                sections.append({
                    "type": "heading",
                    "level": level,
                    "text": text
                })
                i += 1
                continue

            # 2. 水平线
            if re.match(self.HORIZONTAL_RULE, line.strip()):
                sections.append({"type": "horizontal_rule"})
                i += 1
                continue

            # 3. 代码块
            code_match = re.match(self.CODE_BLOCK_START, line.strip())
            if code_match:
                language = code_match.group(1) or ""
                code_lines = []
                i += 1

                while i < len(lines):
                    if re.match(self.CODE_BLOCK_END, lines[i].strip()):
                        i += 1
                        break
                    code_lines.append(lines[i])
                    i += 1

                sections.append({
                    "type": "code",
                    "language": language,
                    "text": '\n'.join(code_lines)
                })
                continue

            # 4. 表格
            if re.match(self.TABLE_ROW_PATTERN, line):
                table_data = self._parse_table(lines, i)
                if table_data:
                    sections.append(table_data["section"])
                    i = table_data["next_index"]
                    continue

            # 5. 列表
            list_match = re.match(self.LIST_PATTERN, line)
            if list_match:
                list_data = self._parse_list(lines, i)
                sections.append(list_data["section"])
                i = list_data["next_index"]
                continue

            # 6. 引用
            quote_match = re.match(self.QUOTE_PATTERN, line)
            if quote_match:
                quote_lines = []
                while i < len(lines) and re.match(self.QUOTE_PATTERN, lines[i]):
                    match = re.match(self.QUOTE_PATTERN, lines[i])
                    quote_lines.append(match.group(1))
                    i += 1

                sections.append({
                    "type": "quote",
                    "text": ' '.join(quote_lines)
                })
                continue

            # 7. 图片(独立行)
            image_match = re.match(self.IMAGE_PATTERN, line.strip())
            if image_match:
                alt_text = image_match.group(1) or ""
                image_url = image_match.group(2) or ""
                title = image_match.group(3) or alt_text

                sections.append({
                    "type": "image",
                    "alt": alt_text,
                    "url": image_url,
                    "title": title,
                    "IMPLEMENTED": False  # 标记为未实现(Phase 1)
                })
                i += 1
                continue

            # 8. 普通段落
            # 收集连续的非空行作为一个段落
            para_lines = []
            while i < len(lines):
                current_line = lines[i]

                # 遇到空行、标题、列表、引用、代码块等,停止
                if not current_line.strip():
                    break
                if re.match(self.HEADING_PATTERN, current_line):
                    break
                if re.match(self.LIST_PATTERN, current_line):
                    break
                if re.match(self.QUOTE_PATTERN, current_line):
                    break
                if re.match(self.CODE_BLOCK_START, current_line):
                    break
                if re.match(self.TABLE_ROW_PATTERN, current_line):
                    break

                para_lines.append(current_line)
                i += 1

            if para_lines:
                para_text = ' '.join(para_lines)
                # 清理行内格式标记
                para_text = self.strip_inline_styles(para_text)
                sections.append({
                    "type": "paragraph",
                    "text": para_text
                })
            else:
                # 如果没有收集到段落内容,必须递增i避免无限循环
                i += 1

        return sections

    def _parse_table(self, lines: List[str], start_index: int) -> Optional[Dict]:
        """
        解析表格

        Args:
            lines: 所有行
            start_index: 开始索引

        Returns:
            {"section": {...}, "next_index": int} 或 None
        """
        i = start_index

        # 第一行应该是表头
        header_line = lines[i].strip()
        if not re.match(self.TABLE_ROW_PATTERN, header_line):
            return None

        headers = [self.strip_inline_styles(cell.strip()) for cell in header_line.split('|')[1:-1]]
        i += 1

        # 第二行应该是分隔符
        if i >= len(lines) or not re.match(self.TABLE_SEPARATOR_PATTERN, lines[i].strip()):
            # 不是标准表格,跳过
            return None

        i += 1

        # 后续行是数据行
        rows = []
        while i < len(lines):
            row_line = lines[i].strip()
            if not re.match(self.TABLE_ROW_PATTERN, row_line):
                break

            cells = [self.strip_inline_styles(cell.strip()) for cell in row_line.split('|')[1:-1]]
            rows.append(cells)
            i += 1

        return {
            "section": {
                "type": "table",
                "headers": headers,
                "rows": rows
            },
            "next_index": i
        }

    def _parse_list(self, lines: List[str], start_index: int) -> Dict:
        """
        解析列表

        Args:
            lines: 所有行
            start_index: 开始索引

        Returns:
            {"section": {...}, "next_index": int}
        """
        i = start_index
        items = []
        ordered = False

        # 检查第一个列表项,判断是有序还是无序
        first_match = re.match(self.LIST_PATTERN, lines[i])
        if first_match:
            marker = first_match.group(2)
            ordered = marker[0].isdigit()

        # 收集所有列表项
        while i < len(lines):
            list_match = re.match(self.LIST_PATTERN, lines[i])
            if not list_match:
                break

            item_text = list_match.group(3).strip()
            # 清理行内格式标记
            item_text = self.strip_inline_styles(item_text)
            items.append(item_text)
            i += 1

        return {
            "section": {
                "type": "list",
                "ordered": ordered,
                "items": items
            },
            "next_index": i
        }

    def strip_inline_styles(self, text: str) -> str:
        """
        移除Markdown行内样式标记(但保留文本)

        Args:
            text: 包含Markdown样式的文本

        Returns:
            纯文本
        """
        # 移除粗体
        text = re.sub(self.BOLD_PATTERN, r'\1', text)
        # 移除斜体
        text = re.sub(self.ITALIC_PATTERN, r'\1', text)
        # 移除行内代码
        text = re.sub(self.CODE_INLINE_PATTERN, r'\1', text)

        return text

    def extract_inline_styles(self, text: str) -> List[Dict]:
        """
        提取文本中的行内样式信息

        Args:
            text: 包含Markdown样式的文本

        Returns:
            样式列表 [{"type": "bold", "start": 0, "end": 5, "text": "粗体"}]
        """
        styles = []

        # 提取粗体
        for match in re.finditer(self.BOLD_PATTERN, text):
            styles.append({
                "type": "bold",
                "start": match.start(),
                "end": match.end(),
                "text": match.group(1)
            })

        # 提取斜体
        for match in re.finditer(self.ITALIC_PATTERN, text):
            # 排除粗体中的星号
            if not any(s["start"] <= match.start() < s["end"] for s in styles if s["type"] == "bold"):
                styles.append({
                    "type": "italic",
                    "start": match.start(),
                    "end": match.end(),
                    "text": match.group(1)
                })

        # 提取行内代码
        for match in re.finditer(self.CODE_INLINE_PATTERN, text):
            styles.append({
                "type": "code",
                "start": match.start(),
                "end": match.end(),
                "text": match.group(1)
            })

        # 按位置排序
        styles.sort(key=lambda s: s["start"])

        return styles
