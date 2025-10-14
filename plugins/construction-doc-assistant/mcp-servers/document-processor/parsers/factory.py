"""
解析器工厂模块

根据文件类型自动选择合适的解析器
"""
from typing import Optional, Dict
from pathlib import Path
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    get_logger,
    config,
    UnsupportedFormatError
)

logger = get_logger(__name__)


class ParserFactory:
    """解析器工厂类"""

    # 解析器注册表 (延迟加载)
    _parsers: Dict = {}
    _initialized = False

    @classmethod
    def _initialize_parsers(cls):
        """初始化解析器 (延迟加载以避免循环导入)"""
        if cls._initialized:
            return

        try:
            # 导入所有解析器
            from .word_parser import WordParser
            from .excel_parser import ExcelParser
            from .ppt_parser import PowerPointParser
            from .pdf_parser import PDFParser

            # 注册解析器
            cls._parsers = {
                'word': WordParser(),
                'excel': ExcelParser(),
                'powerpoint': PowerPointParser(),
                'pdf': PDFParser()
            }

            cls._initialized = True
            logger.info(f"解析器工厂初始化完成，共注册 {len(cls._parsers)} 个解析器")

        except ImportError as e:
            logger.error(f"解析器初始化失败: {e}")
            cls._parsers = {}

    @classmethod
    def get_parser(cls, file_path: str):
        """
        根据文件路径获取合适的解析器

        Args:
            file_path: 文件路径

        Returns:
            解析器实例

        Raises:
            UnsupportedFormatError: 不支持的文件格式
        """
        # 确保解析器已初始化
        cls._initialize_parsers()

        # 根据文件扩展名确定文件类型
        file_type = config.get_file_type_by_extension(file_path)

        if file_type is None:
            ext = Path(file_path).suffix
            raise UnsupportedFormatError(
                f"不支持的文件格式: {ext}。"
                f"支持的格式: {', '.join(config.get_all_supported_extensions())}"
            )

        # 获取对应的解析器
        parser = cls._parsers.get(file_type)

        if parser is None:
            raise UnsupportedFormatError(
                f"文件类型 '{file_type}' 的解析器未注册"
            )

        logger.debug(f"为文件 {file_path} 选择解析器: {parser.__class__.__name__}")
        return parser

    @classmethod
    def parse(cls, file_path: str, options: Optional[Dict] = None) -> Dict:
        """
        自动选择解析器并解析文档

        Args:
            file_path: 文件路径
            options: 解析选项

        Returns:
            解析结果字典
        """
        try:
            # 获取解析器
            parser = cls.get_parser(file_path)

            # 使用安全解析方法
            result = parser.safe_parse(file_path, options)

            return result

        except UnsupportedFormatError as e:
            logger.error(f"不支持的文件格式: {e}")
            return {
                "status": "error",
                "file_info": {
                    "path": file_path,
                    "name": os.path.basename(file_path)
                },
                "error_message": str(e),
                "suggestions": [
                    "请使用支持的文件格式",
                    f"支持的格式: {', '.join(config.get_all_supported_extensions())}",
                    "尝试将文件转换为 PDF 格式"
                ]
            }

        except Exception as e:
            logger.error(f"解析失败: {e}", exc_info=True)
            return {
                "status": "error",
                "file_info": {
                    "path": file_path,
                    "name": os.path.basename(file_path)
                },
                "error_message": f"解析失败: {str(e)}",
                "suggestions": [
                    "检查文件是否损坏",
                    "尝试重新保存文档",
                    "查看日志获取详细错误信息"
                ]
            }

    @classmethod
    def get_available_parsers(cls) -> list:
        """
        获取所有可用的解析器列表

        Returns:
            解析器名称列表
        """
        cls._initialize_parsers()
        return list(cls._parsers.keys())

    @classmethod
    def register_parser(cls, file_type: str, parser):
        """
        注册自定义解析器

        Args:
            file_type: 文件类型 (如 'word', 'excel')
            parser: 解析器实例
        """
        cls._initialize_parsers()
        cls._parsers[file_type] = parser
        logger.info(f"注册自定义解析器: {file_type} -> {parser.__class__.__name__}")

    @classmethod
    def batch_parse(cls, file_paths: list, options: Optional[Dict] = None) -> list:
        """
        批量解析多个文档

        Args:
            file_paths: 文件路径列表
            options: 解析选项

        Returns:
            解析结果列表
        """
        results = []

        logger.info(f"开始批量解析 {len(file_paths)} 个文档")

        for i, file_path in enumerate(file_paths, 1):
            logger.info(f"解析进度: {i}/{len(file_paths)} - {os.path.basename(file_path)}")

            result = cls.parse(file_path, options)
            results.append(result)

        # 统计
        success_count = sum(1 for r in results if r.get('status') == 'success')
        logger.info(
            f"批量解析完成: 总计 {len(file_paths)}, "
            f"成功 {success_count}, "
            f"失败 {len(file_paths) - success_count}"
        )

        return results


# 便捷函数
def parse_document(file_path: str, options: Optional[Dict] = None) -> Dict:
    """解析文档的便捷函数"""
    return ParserFactory.parse(file_path, options)


def batch_parse_documents(file_paths: list, options: Optional[Dict] = None) -> list:
    """批量解析文档的便捷函数"""
    return ParserFactory.batch_parse(file_paths, options)


def get_parser_for_file(file_path: str):
    """获取文件解析器的便捷函数"""
    return ParserFactory.get_parser(file_path)
