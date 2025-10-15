"""
文档生成器基类

定义文档生成器的通用接口和方法
"""
import os
import sys
from typing import Dict, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import get_logger

logger = get_logger(__name__)


class BaseGenerator:
    """文档生成器基类"""

    def __init__(self):
        self.logger = logger

    def generate(self,
                 source_file: str,
                 output_file: str,
                 options: Optional[Dict[str, Any]] = None) -> Dict:
        """
        生成文档(子类实现)

        Args:
            source_file: 源文件路径
            output_file: 输出文件路径
            options: 生成选项

        Returns:
            生成结果字典
        """
        raise NotImplementedError("子类必须实现generate方法")

    def validate_input(self, source_file: str) -> bool:
        """
        验证输入文件

        Args:
            source_file: 源文件路径

        Returns:
            验证是否通过

        Raises:
            FileNotFoundError: 文件不存在
        """
        if not os.path.exists(source_file):
            raise FileNotFoundError(f"源文件不存在: {source_file}")

        if not os.path.isfile(source_file):
            raise ValueError(f"源路径不是文件: {source_file}")

        return True

    def validate_output(self, output_file: str) -> bool:
        """
        验证输出路径

        Args:
            output_file: 输出文件路径

        Returns:
            验证是否通过
        """
        output_dir = os.path.dirname(output_file)

        # 如果输出目录不存在,创建它
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
                self.logger.info(f"创建输出目录: {output_dir}")
            except Exception as e:
                raise ValueError(f"无法创建输出目录 {output_dir}: {e}")

        # 检查输出文件是否可写
        if os.path.exists(output_file):
            if not os.access(output_file, os.W_OK):
                raise ValueError(f"输出文件不可写: {output_file}")
        else:
            # 检查目录是否可写
            if output_dir and not os.access(output_dir, os.W_OK):
                raise ValueError(f"输出目录不可写: {output_dir}")

        return True

    def create_success_response(self,
                               output_file: str,
                               **kwargs) -> Dict:
        """
        创建成功响应

        Args:
            output_file: 输出文件路径
            **kwargs: 其他响应字段

        Returns:
            成功响应字典
        """
        response = {
            "status": "success",
            "output_file": output_file,
            "file_size": os.path.getsize(output_file) if os.path.exists(output_file) else 0,
        }
        response.update(kwargs)
        return response

    def create_error_response(self, error: str, **kwargs) -> Dict:
        """
        创建错误响应

        Args:
            error: 错误信息
            **kwargs: 其他响应字段

        Returns:
            错误响应字典
        """
        response = {
            "status": "error",
            "error": str(error)
        }
        response.update(kwargs)
        return response

    def create_warning_response(self,
                               output_file: str,
                               warnings: list,
                               **kwargs) -> Dict:
        """
        创建带警告的成功响应

        Args:
            output_file: 输出文件路径
            warnings: 警告信息列表
            **kwargs: 其他响应字段

        Returns:
            响应字典
        """
        response = self.create_success_response(output_file, **kwargs)
        response["warnings"] = warnings
        return response

    def format_file_size(self, size_bytes: int) -> str:
        """
        格式化文件大小

        Args:
            size_bytes: 字节数

        Returns:
            格式化后的文件大小字符串
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
