"""
解析器基类模块

定义所有文档解析器的统一接口和通用功能
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    get_logger,
    handle_file_error,
    success_response,
    ParseError
)

logger = get_logger(__name__)


class BaseParser(ABC):
    """文档解析器抽象基类"""

    def __init__(self):
        """初始化解析器"""
        self.logger = get_logger(self.__class__.__name__)

    @abstractmethod
    def parse(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> Dict:
        """
        解析文档的核心方法 (必须由子类实现)

        Args:
            file_path: 文件路径
            options: 解析选项
                - extract_tables: 是否提取表格 (默认 True)
                - extract_images: 是否提取图片信息 (默认 False)
                - max_length: 最大内容长度限制
                - keywords: 关注的关键词列表

        Returns:
            解析结果字典，统一格式:
            {
                "status": "success" | "error",
                "file_info": {
                    "path": str,
                    "name": str,
                    "extension": str,
                    "size": int,
                    "parser": str  # 解析器名称
                },
                "content": {
                    # 具体内容根据文档类型而定
                },
                "summary": {
                    # 摘要信息
                },
                "metadata": {
                    # 元数据信息
                }
            }

        Raises:
            ParseError: 解析失败时抛出
        """
        pass

    def safe_parse(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> Dict:
        """
        安全的解析方法 (带错误处理)

        Args:
            file_path: 文件路径
            options: 解析选项

        Returns:
            解析结果字典 (包含错误信息)
        """
        try:
            # 验证文件路径
            if not self._validate_file_path(file_path):
                return self._create_error_response(
                    file_path,
                    "文件路径无效或文件不存在"
                )

            # 调用子类实现的解析方法
            self.logger.info(f"开始解析文档: {file_path}")
            result = self.parse(file_path, options or {})

            self.logger.info(f"文档解析成功: {file_path}")
            return result

        except ParseError as e:
            self.logger.error(f"解析错误: {e}", exc_info=True)
            return handle_file_error(e, file_path, "解析")

        except Exception as e:
            self.logger.error(f"未预期的错误: {e}", exc_info=True)
            return handle_file_error(e, file_path, "解析")

    def _validate_file_path(self, file_path: str) -> bool:
        """验证文件路径"""
        if not file_path:
            return False

        path = Path(file_path)
        if not path.exists():
            self.logger.error(f"文件不存在: {file_path}")
            return False

        if not path.is_file():
            self.logger.error(f"路径不是文件: {file_path}")
            return False

        return True

    def _get_file_info(self, file_path: str) -> Dict:
        """
        获取文件基本信息

        Args:
            file_path: 文件路径

        Returns:
            文件信息字典
        """
        path = Path(file_path)
        stat = path.stat()

        return {
            "path": str(path.absolute()),
            "name": path.name,
            "extension": path.suffix.lower(),
            "size": stat.st_size,
            "size_formatted": self._format_size(stat.st_size),
            "parser": self.__class__.__name__
        }

    @staticmethod
    def _format_size(size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"

    def _create_success_response(
        self,
        file_path: str,
        content: Dict,
        summary: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        创建成功响应

        Args:
            file_path: 文件路径
            content: 内容字典
            summary: 摘要信息
            metadata: 元数据

        Returns:
            成功响应字典
        """
        return {
            "status": "success",
            "file_info": self._get_file_info(file_path),
            "content": content,
            "summary": summary or {},
            "metadata": metadata or {}
        }

    def _create_error_response(self, file_path: str, error_message: str) -> Dict:
        """
        创建错误响应

        Args:
            file_path: 文件路径
            error_message: 错误消息

        Returns:
            错误响应字典
        """
        return {
            "status": "error",
            "file_info": {
                "path": file_path,
                "name": os.path.basename(file_path) if file_path else "Unknown",
                "parser": self.__class__.__name__
            },
            "error_message": error_message,
            "suggestions": [
                "检查文件是否存在",
                "确认文件格式是否正确",
                "尝试重新保存文档"
            ]
        }

    def _extract_text_preview(self, text: str, max_length: int = 500) -> str:
        """
        提取文本预览

        Args:
            text: 完整文本
            max_length: 最大长度

        Returns:
            截断后的文本
        """
        if not text:
            return ""

        if len(text) <= max_length:
            return text

        return text[:max_length] + "..."

    def _filter_empty_lines(self, lines: list) -> list:
        """
        过滤空行

        Args:
            lines: 文本行列表

        Returns:
            过滤后的列表
        """
        return [line for line in lines if line and line.strip()]

    def get_supported_extensions(self) -> list:
        """
        获取支持的文件扩展名列表

        Returns:
            扩展名列表
        """
        return []

    def __repr__(self) -> str:
        """字符串表示"""
        return f"<{self.__class__.__name__}>"
