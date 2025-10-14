"""
统一错误处理模块

提供友好的错误信息和建议
"""
import os
from typing import Dict, Optional
from .logger import get_logger

logger = get_logger(__name__)


class DocumentProcessError(Exception):
    """文档处理基础异常类"""
    pass


class FileValidationError(DocumentProcessError):
    """文件验证异常"""
    pass


class ParseError(DocumentProcessError):
    """文档解析异常"""
    pass


class UnsupportedFormatError(DocumentProcessError):
    """不支持的文件格式异常"""
    pass


class ErrorHandler:
    """统一错误处理器"""

    # 错误类型到友好提示的映射
    ERROR_SUGGESTIONS = {
        'FileNotFoundError': {
            'message': '文件不存在',
            'suggestions': [
                '请检查文件路径是否正确',
                '确认文件名拼写是否正确',
                '检查文件是否已被移动或删除'
            ]
        },
        'PermissionError': {
            'message': '权限不足',
            'suggestions': [
                '请检查文件访问权限',
                '尝试使用管理员权限运行',
                '确认文件未被其他程序占用'
            ]
        },
        'BadZipFile': {
            'message': 'Office 文档已损坏或格式错误',
            'suggestions': [
                '尝试使用 Office 软件打开并重新保存文档',
                '将文档转换为 PDF 格式后重试',
                '检查文档是否完整下载'
            ]
        },
        'zipfile.BadZipFile': {
            'message': 'Office 文档已损坏或格式错误',
            'suggestions': [
                '尝试使用 Office 软件打开并重新保存文档',
                '将文档转换为 PDF 格式后重试',
                '检查文档是否完整下载'
            ]
        },
        'MemoryError': {
            'message': '内存不足',
            'suggestions': [
                '文件过大，建议分批处理',
                '关闭其他占用内存的程序',
                '尝试压缩文件大小'
            ]
        },
        'UnicodeDecodeError': {
            'message': '文件编码问题',
            'suggestions': [
                '建议使用 UTF-8 编码保存文档',
                '尝试用文本编辑器打开并转换编码',
                '检查文档是否包含特殊字符'
            ]
        },
        'TimeoutError': {
            'message': '处理超时',
            'suggestions': [
                '文件内容较多，处理时间较长',
                '建议提取关键页面或章节',
                '尝试简化文档内容'
            ]
        },
        'OSError': {
            'message': '系统错误',
            'suggestions': [
                '检查磁盘空间是否充足',
                '确认文件路径长度不超过系统限制',
                '检查文件系统是否正常'
            ]
        }
    }

    @classmethod
    def handle_error(
        cls,
        error: Exception,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        处理异常并返回友好的错误信息

        Args:
            error: 异常对象
            context: 上下文信息 (如文件路径、操作类型等)

        Returns:
            包含错误信息的字典
        """
        error_type = type(error).__name__
        error_message = str(error)

        # 记录完整错误到日志
        logger.error(
            f"错误类型: {error_type}, 消息: {error_message}",
            exc_info=True
        )

        # 获取友好的错误提示
        error_info = cls.ERROR_SUGGESTIONS.get(
            error_type,
            {
                'message': '未知错误',
                'suggestions': ['请联系技术支持', '查看日志获取详细信息']
            }
        )

        result = {
            'status': 'error',
            'error_type': error_type,
            'error_message': error_message,
            'user_message': error_info['message'],
            'suggestions': error_info['suggestions']
        }

        # 添加上下文信息
        if context:
            result['context'] = context

        return result

    @classmethod
    def handle_file_error(
        cls,
        error: Exception,
        file_path: str,
        operation: str = '处理'
    ) -> Dict:
        """
        处理文件相关错误

        Args:
            error: 异常对象
            file_path: 文件路径
            operation: 操作描述

        Returns:
            错误信息字典
        """
        context = {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'operation': operation
        }

        result = cls.handle_error(error, context)

        # 添加文件特定的信息
        result['file_info'] = {
            'path': file_path,
            'name': os.path.basename(file_path),
            'exists': os.path.exists(file_path)
        }

        if os.path.exists(file_path):
            try:
                result['file_info']['size'] = os.path.getsize(file_path)
                result['file_info']['extension'] = os.path.splitext(file_path)[1]
            except Exception as e:
                logger.warning(f"无法获取文件信息: {e}")

        return result

    @classmethod
    def create_success_response(
        cls,
        data: Dict,
        message: str = '操作成功'
    ) -> Dict:
        """
        创建成功响应

        Args:
            data: 数据内容
            message: 成功消息

        Returns:
            成功响应字典
        """
        return {
            'status': 'success',
            'message': message,
            'data': data
        }

    @classmethod
    def create_warning_response(
        cls,
        data: Dict,
        warnings: list,
        message: str = '操作完成但有警告'
    ) -> Dict:
        """
        创建警告响应

        Args:
            data: 数据内容
            warnings: 警告信息列表
            message: 响应消息

        Returns:
            警告响应字典
        """
        return {
            'status': 'warning',
            'message': message,
            'data': data,
            'warnings': warnings
        }

    @classmethod
    def format_error_for_user(cls, error_dict: Dict) -> str:
        """
        将错误字典格式化为用户友好的文本

        Args:
            error_dict: 错误信息字典

        Returns:
            格式化的错误文本
        """
        lines = [
            f"❌ {error_dict.get('user_message', '操作失败')}",
            ""
        ]

        # 添加文件信息
        if 'file_info' in error_dict:
            file_info = error_dict['file_info']
            lines.append(f"文件: {file_info.get('name', 'Unknown')}")
            if not file_info.get('exists', True):
                lines.append("⚠️ 文件不存在")
            lines.append("")

        # 添加建议
        if 'suggestions' in error_dict:
            lines.append("建议操作:")
            for i, suggestion in enumerate(error_dict['suggestions'], 1):
                lines.append(f"  {i}. {suggestion}")
            lines.append("")

        # 添加技术信息 (可选)
        if 'error_type' in error_dict:
            lines.append(f"技术信息: {error_dict['error_type']}")

        return "\n".join(lines)


# 便捷函数
def handle_error(error: Exception, context: Optional[Dict] = None) -> Dict:
    """处理异常的便捷函数"""
    return ErrorHandler.handle_error(error, context)


def handle_file_error(error: Exception, file_path: str, operation: str = '处理') -> Dict:
    """处理文件错误的便捷函数"""
    return ErrorHandler.handle_file_error(error, file_path, operation)


def success_response(data: Dict, message: str = '操作成功') -> Dict:
    """创建成功响应的便捷函数"""
    return ErrorHandler.create_success_response(data, message)


def warning_response(data: Dict, warnings: list, message: str = '操作完成但有警告') -> Dict:
    """创建警告响应的便捷函数"""
    return ErrorHandler.create_warning_response(data, warnings, message)
