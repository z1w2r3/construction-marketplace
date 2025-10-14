"""
PDF 文档解析器模块

解析 .pdf 格式的 PDF 文档
提取文本、元数据等信息
"""
from typing import Dict, List, Optional, Any
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_parser import BaseParser
from utils import get_logger, ParseError

logger = get_logger(__name__)


class PDFParser(BaseParser):
    """PDF 文档解析器"""

    def __init__(self):
        super().__init__()

    def get_supported_extensions(self) -> list:
        """获取支持的文件扩展名"""
        return ['.pdf']

    def parse(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> Dict:
        """
        解析 PDF 文档

        Args:
            file_path: PDF 文档路径
            options: 解析选项
                - max_pages: 最大页数
                - extract_tables: 是否提取表格 (需要 pdfplumber)

        Returns:
            解析结果字典
        """
        try:
            import PyPDF2
        except ImportError:
            raise ParseError(
                "缺少 PyPDF2 库，请运行: pip install PyPDF2"
            )

        options = options or {}
        max_pages = options.get('max_pages', 50)
        extract_tables = options.get('extract_tables', False)

        try:
            # 打开 PDF 文件
            self.logger.info(f"加载 PDF 文档: {file_path}")

            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)

                # 提取内容
                content = {}

                # 1. 获取页数
                page_count = len(reader.pages)
                content['page_count'] = page_count

                # 2. 提取页面文本
                pages_data = []
                pages_to_read = min(page_count, max_pages)

                for i in range(pages_to_read):
                    page = reader.pages[i]
                    page_text = page.extract_text()

                    page_data = {
                        "page_number": i + 1,
                        "text": page_text,
                        "text_length": len(page_text),
                        "text_preview": self._extract_text_preview(page_text, 500)
                    }

                    pages_data.append(page_data)

                content['pages'] = pages_data

                # 3. 如果需要提取表格（使用 pdfplumber）
                if extract_tables:
                    try:
                        tables = self._extract_tables_with_pdfplumber(
                            file_path,
                            pages_to_read
                        )
                        content['tables'] = tables
                    except ImportError:
                        self.logger.warning("pdfplumber 未安装，跳过表格提取")
                        content['tables'] = []

                # 4. 生成摘要
                summary = self._generate_summary(content)

                # 5. 提取元数据
                metadata = self._extract_metadata(reader)

                return self._create_success_response(
                    file_path,
                    content,
                    summary,
                    metadata
                )

        except Exception as e:
            self.logger.error(f"PDF 文档解析失败: {e}", exc_info=True)
            raise ParseError(f"PDF 文档解析失败: {str(e)}")

    def _extract_tables_with_pdfplumber(
        self,
        file_path: str,
        max_pages: int
    ) -> List[Dict]:
        """
        使用 pdfplumber 提取表格

        Args:
            file_path: PDF 文件路径
            max_pages: 最大页数

        Returns:
            表格列表
        """
        try:
            import pdfplumber
        except ImportError:
            raise ImportError("需要 pdfplumber 库来提取表格")

        tables = []

        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                if i >= max_pages:
                    break

                page_tables = page.extract_tables()

                for table_idx, table in enumerate(page_tables):
                    if table:
                        tables.append({
                            "page": i + 1,
                            "table_index": table_idx,
                            "rows": len(table),
                            "cols": len(table[0]) if table else 0,
                            "data": table
                        })

        self.logger.info(f"从 PDF 提取表格: {len(tables)} 个")
        return tables

    def _extract_metadata(self, reader) -> Dict:
        """提取元数据"""
        metadata = {}

        try:
            info = reader.metadata

            if info:
                if '/Author' in info:
                    metadata['author'] = info['/Author']

                if '/Title' in info:
                    metadata['title'] = info['/Title']

                if '/Subject' in info:
                    metadata['subject'] = info['/Subject']

                if '/Creator' in info:
                    metadata['creator'] = info['/Creator']

                if '/Producer' in info:
                    metadata['producer'] = info['/Producer']

                if '/CreationDate' in info:
                    metadata['creation_date'] = str(info['/CreationDate'])

                if '/ModDate' in info:
                    metadata['modification_date'] = str(info['/ModDate'])

        except Exception as e:
            self.logger.warning(f"提取元数据失败: {e}")

        return metadata

    def _generate_summary(self, content: Dict) -> Dict:
        """生成摘要"""
        total_text_length = sum(
            page['text_length'] for page in content['pages']
        )

        summary = {
            "total_pages": content['page_count'],
            "pages_extracted": len(content['pages']),
            "total_text_length": total_text_length
        }

        if 'tables' in content:
            summary["total_tables"] = len(content['tables'])

        return summary
