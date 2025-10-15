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

    def __init__(self):
        self.logger = logger

    def parse(self, markdown_text: str) -> List[Dict[str, Any]]:
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

        while i < len(lines):
            line = lines[i]

            # 跳过空行
            if not line.strip():
                i += 1
                continue

            # 1. 标题
            heading_match = re.match(self.HEADING_PATTERN, line)
            if heading_match:
                level = len(heading_match.group(1))
                text = heading_match.group(2).strip()
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
                sections.append({
                    "type": "paragraph",
                    "text": para_text
                })

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

        headers = [cell.strip() for cell in header_line.split('|')[1:-1]]
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

            cells = [cell.strip() for cell in row_line.split('|')[1:-1]]
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
