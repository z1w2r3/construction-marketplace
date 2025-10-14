"""
工具模块

提供配置管理、日志记录、错误处理等工具函数
"""

from .config import Config, config
from .logger import (
    get_logger,
    setup_logger,
    debug,
    info,
    warning,
    error,
    critical,
    exception
)
from .error_handler import (
    ErrorHandler,
    DocumentProcessError,
    FileValidationError,
    ParseError,
    UnsupportedFormatError,
    handle_error,
    handle_file_error,
    success_response,
    warning_response
)

__all__ = [
    # 配置
    'Config',
    'config',

    # 日志
    'get_logger',
    'setup_logger',
    'debug',
    'info',
    'warning',
    'error',
    'critical',
    'exception',

    # 错误处理
    'ErrorHandler',
    'DocumentProcessError',
    'FileValidationError',
    'ParseError',
    'UnsupportedFormatError',
    'handle_error',
    'handle_file_error',
    'success_response',
    'warning_response',
]
