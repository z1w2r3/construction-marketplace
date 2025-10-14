"""
文档解析器模块

导出所有解析器和工厂类
"""

from .base_parser import BaseParser
from .word_parser import WordParser
from .excel_parser import ExcelParser
from .ppt_parser import PowerPointParser
from .pdf_parser import PDFParser
from .factory import (
    ParserFactory,
    parse_document,
    batch_parse_documents,
    get_parser_for_file
)

__all__ = [
    # 基类
    'BaseParser',

    # 具体解析器
    'WordParser',
    'ExcelParser',
    'PowerPointParser',
    'PDFParser',

    # 工厂类和便捷函数
    'ParserFactory',
    'parse_document',
    'batch_parse_documents',
    'get_parser_for_file',
]
