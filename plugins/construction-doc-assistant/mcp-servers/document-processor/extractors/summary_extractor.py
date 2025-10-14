"""
摘要提取器模块

从解析后的文档中智能提取摘要信息
特别针对建筑施工行业进行优化
"""
from typing import Dict, List, Optional
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import get_logger, config

logger = get_logger(__name__)


class SummaryExtractor:
    """摘要提取器类"""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.construction_keywords = config.CONSTRUCTION_KEYWORDS

    def extract_summary(
        self,
        parsed_document: Dict,
        focus_keywords: Optional[List[str]] = None,
        max_length: int = 2000
    ) -> Dict:
        """
        从解析后的文档提取摘要

        Args:
            parsed_document: 解析后的文档字典
            focus_keywords: 关注的关键词列表
            max_length: 摘要最大长度

        Returns:
            摘要字典
        """
        if parsed_document.get('status') != 'success':
            return {
                "status": "error",
                "message": "文档解析失败，无法提取摘要"
            }

        summary = {
            "status": "success",
            "file_info": parsed_document.get('file_info', {}),
            "main_points": [],
            "key_data": {},
            "sections_summary": {},
            "keywords_found": []
        }

        content = parsed_document.get('content', {})

        # 根据文档类型选择提取策略
        parser_type = parsed_document.get('file_info', {}).get('parser', '')

        if 'Word' in parser_type:
            summary = self._extract_from_word(content, focus_keywords, summary)
        elif 'Excel' in parser_type:
            summary = self._extract_from_excel(content, focus_keywords, summary)
        elif 'PowerPoint' in parser_type:
            summary = self._extract_from_powerpoint(content, focus_keywords, summary)
        elif 'PDF' in parser_type:
            summary = self._extract_from_pdf(content, focus_keywords, summary)

        # 限制摘要长度
        summary = self._truncate_summary(summary, max_length)

        return summary

    def _extract_from_word(
        self,
        content: Dict,
        focus_keywords: Optional[List[str]],
        summary: Dict
    ) -> Dict:
        """从 Word 文档提取摘要"""
        sections = content.get('sections', {})
        tables = content.get('tables', [])
        outline = content.get('outline', [])

        # 1. 提取文档大纲作为主要要点
        if outline:
            summary['main_points'] = [
                f"{'  ' * (item['level'] - 1)}{item['text']}"
                for item in outline[:10]  # 最多10个标题
            ]

        # 2. 提取包含关键词的段落
        if focus_keywords:
            keywords_paragraphs = self._find_paragraphs_with_keywords(
                sections,
                focus_keywords
            )
            summary['sections_summary'] = keywords_paragraphs
            summary['keywords_found'] = list(keywords_paragraphs.keys())

        # 3. 提取关键数据（从表格）
        if tables:
            summary['key_data']['tables_count'] = len(tables)
            summary['key_data']['total_table_rows'] = sum(t['rows'] for t in tables)

            # 提取第一个表格的表头作为示例
            if tables and tables[0].get('headers'):
                summary['key_data']['sample_table_headers'] = tables[0]['headers']

        return summary

    def _extract_from_excel(
        self,
        content: Dict,
        focus_keywords: Optional[List[str]],
        summary: Dict
    ) -> Dict:
        """从 Excel 文档提取摘要"""
        sheets = content.get('sheets', [])

        # 1. 工作表概览
        summary['main_points'] = [
            f"工作表: {sheet['name']} ({len(sheet['data'])} 行)"
            for sheet in sheets[:5]  # 最多5个工作表
        ]

        # 2. 如果指定了关键词，搜索相关单元格
        if focus_keywords and sheets:
            keywords_data = self._find_cells_with_keywords(
                sheets,
                focus_keywords
            )
            summary['sections_summary'] = keywords_data
            summary['keywords_found'] = list(keywords_data.keys())

        # 3. 提取关键数据统计
        if sheets:
            summary['key_data']['total_sheets'] = len(sheets)
            summary['key_data']['total_rows'] = sum(len(s['data']) for s in sheets)

            # 提取第一个工作表的表头
            if sheets[0].get('headers'):
                summary['key_data']['sample_headers'] = sheets[0]['headers']

        return summary

    def _extract_from_powerpoint(
        self,
        content: Dict,
        focus_keywords: Optional[List[str]],
        summary: Dict
    ) -> Dict:
        """从 PowerPoint 文档提取摘要"""
        slides = content.get('slides', [])

        # 1. 提取幻灯片标题
        summary['main_points'] = [
            f"幻灯片 {slide['index']}: {slide['title']}"
            for slide in slides[:10]
            if slide.get('title')
        ]

        # 2. 如果指定了关键词，搜索相关内容
        if focus_keywords:
            keywords_slides = self._find_slides_with_keywords(
                slides,
                focus_keywords
            )
            summary['sections_summary'] = keywords_slides
            summary['keywords_found'] = list(keywords_slides.keys())

        # 3. 关键数据
        summary['key_data']['total_slides'] = len(slides)
        summary['key_data']['slides_with_titles'] = sum(
            1 for s in slides if s.get('title')
        )
        summary['key_data']['slides_with_notes'] = sum(
            1 for s in slides if s.get('notes')
        )

        return summary

    def _extract_from_pdf(
        self,
        content: Dict,
        focus_keywords: Optional[List[str]],
        summary: Dict
    ) -> Dict:
        """从 PDF 文档提取摘要"""
        pages = content.get('pages', [])

        # 1. 提取页面概览
        summary['main_points'] = [
            f"第 {page['page_number']} 页: {len(page['text'])} 字符"
            for page in pages[:5]
        ]

        # 2. 如果指定了关键词，搜索相关页面
        if focus_keywords:
            keywords_pages = self._find_pages_with_keywords(
                pages,
                focus_keywords
            )
            summary['sections_summary'] = keywords_pages
            summary['keywords_found'] = list(keywords_pages.keys())

        # 3. 关键数据
        summary['key_data']['total_pages'] = content.get('page_count', 0)
        summary['key_data']['pages_extracted'] = len(pages)
        summary['key_data']['total_chars'] = sum(
            page['text_length'] for page in pages
        )

        return summary

    def _find_paragraphs_with_keywords(
        self,
        sections: Dict,
        keywords: List[str]
    ) -> Dict:
        """查找包含关键词的段落"""
        results = {}

        for keyword in keywords:
            matching_paragraphs = []

            for section_name, paragraphs in sections.items():
                for para in paragraphs:
                    if keyword.lower() in para.lower():
                        matching_paragraphs.append({
                            "section": section_name,
                            "text": para[:200] + "..." if len(para) > 200 else para
                        })

            if matching_paragraphs:
                results[keyword] = matching_paragraphs[:3]  # 最多3个段落

        return results

    def _find_cells_with_keywords(
        self,
        sheets: List[Dict],
        keywords: List[str]
    ) -> Dict:
        """查找包含关键词的单元格"""
        results = {}

        for keyword in keywords:
            matching_cells = []

            for sheet in sheets:
                for row_idx, row in enumerate(sheet['data']):
                    for col_idx, cell in enumerate(row):
                        if keyword.lower() in str(cell).lower():
                            matching_cells.append({
                                "sheet": sheet['name'],
                                "row": row_idx + 1,
                                "col": col_idx + 1,
                                "value": str(cell)
                            })

            if matching_cells:
                results[keyword] = matching_cells[:5]  # 最多5个单元格

        return results

    def _find_slides_with_keywords(
        self,
        slides: List[Dict],
        keywords: List[str]
    ) -> Dict:
        """查找包含关键词的幻灯片"""
        results = {}

        for keyword in keywords:
            matching_slides = []

            for slide in slides:
                # 搜索标题和内容
                all_text = slide.get('title', '') + ' '.join(slide.get('content', []))

                if keyword.lower() in all_text.lower():
                    matching_slides.append({
                        "slide_number": slide['index'],
                        "title": slide.get('title', '无标题'),
                        "content_preview": all_text[:200] + "..." if len(all_text) > 200 else all_text
                    })

            if matching_slides:
                results[keyword] = matching_slides[:3]  # 最多3张幻灯片

        return results

    def _find_pages_with_keywords(
        self,
        pages: List[Dict],
        keywords: List[str]
    ) -> Dict:
        """查找包含关键词的页面"""
        results = {}

        for keyword in keywords:
            matching_pages = []

            for page in pages:
                if keyword.lower() in page['text'].lower():
                    matching_pages.append({
                        "page_number": page['page_number'],
                        "text_preview": page['text_preview']
                    })

            if matching_pages:
                results[keyword] = matching_pages[:3]  # 最多3页

        return results

    def _truncate_summary(self, summary: Dict, max_length: int) -> Dict:
        """截断摘要到指定长度"""
        # 这里简单处理，实际可以更智能
        # 计算当前摘要的大致长度
        import json
        current_length = len(json.dumps(summary, ensure_ascii=False))

        if current_length > max_length:
            # 截断策略：优先保留 main_points 和 key_data
            if 'sections_summary' in summary:
                # 减少 sections_summary 的内容
                for key in list(summary['sections_summary'].keys()):
                    if len(json.dumps(summary, ensure_ascii=False)) <= max_length:
                        break
                    summary['sections_summary'][key] = summary['sections_summary'][key][:1]

        return summary

    def extract_construction_keywords(
        self,
        parsed_document: Dict
    ) -> Dict:
        """
        提取建筑行业特定关键词

        Args:
            parsed_document: 解析后的文档

        Returns:
            按类别组织的关键词
        """
        all_keywords = []
        for category, keywords in self.construction_keywords.items():
            all_keywords.extend(keywords)

        # 使用所有建筑关键词提取摘要
        return self.extract_summary(
            parsed_document,
            focus_keywords=all_keywords,
            max_length=3000
        )


# 便捷函数
def extract_summary(
    parsed_document: Dict,
    focus_keywords: Optional[List[str]] = None,
    max_length: int = 2000
) -> Dict:
    """提取摘要的便捷函数"""
    extractor = SummaryExtractor()
    return extractor.extract_summary(parsed_document, focus_keywords, max_length)


def extract_construction_summary(parsed_document: Dict) -> Dict:
    """提取建筑行业摘要的便捷函数"""
    extractor = SummaryExtractor()
    return extractor.extract_construction_keywords(parsed_document)
