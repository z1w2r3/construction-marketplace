"""
日志系统配置模块

提供统一的日志记录功能
重要：MCP 服务器只能将日志输出到 stderr，不能输出到 stdout
"""
import sys
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional
from .config import config


def setup_logger(
    name: str = "mcp_document_processor",
    level: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    设置日志记录器

    Args:
        name: 日志记录器名称
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 日志文件路径 (可选)

    Returns:
        配置好的 Logger 实例
    """
    logger = logging.getLogger(name)

    # 如果已经配置过，直接返回
    if logger.handlers:
        return logger

    # 设置日志级别
    log_level = level or config.LOG_LEVEL
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 1. stderr 处理器 - 必需，MCP 服务器标准输出
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.INFO)
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)

    # 2. 文件处理器 - 可选，用于持久化日志
    if log_file or config.LOG_FILE:
        try:
            file_handler = RotatingFileHandler(
                log_file or config.LOG_FILE,
                maxBytes=config.LOG_MAX_SIZE,
                backupCount=config.LOG_BACKUP_COUNT,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)  # 文件记录更详细的日志
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            # 如果文件日志失败，只记录到 stderr
            logger.error(f"无法创建文件日志处理器: {e}")

    # 防止日志传播到父 logger
    logger.propagate = False

    logger.info(f"日志系统初始化完成 - 级别: {log_level}")
    return logger


def get_logger(name: str = "mcp_document_processor") -> logging.Logger:
    """
    获取日志记录器实例

    Args:
        name: 日志记录器名称

    Returns:
        Logger 实例
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger = setup_logger(name)
    return logger


# 创建默认日志记录器
default_logger = get_logger()


# 便捷函数
def debug(msg: str, *args, **kwargs):
    """记录 DEBUG 级别日志"""
    default_logger.debug(msg, *args, **kwargs)


def info(msg: str, *args, **kwargs):
    """记录 INFO 级别日志"""
    default_logger.info(msg, *args, **kwargs)


def warning(msg: str, *args, **kwargs):
    """记录 WARNING 级别日志"""
    default_logger.warning(msg, *args, **kwargs)


def error(msg: str, *args, **kwargs):
    """记录 ERROR 级别日志"""
    default_logger.error(msg, *args, **kwargs)


def critical(msg: str, *args, **kwargs):
    """记录 CRITICAL 级别日志"""
    default_logger.critical(msg, *args, **kwargs)


def exception(msg: str, *args, **kwargs):
    """记录异常信息 (包含堆栈跟踪)"""
    default_logger.exception(msg, *args, **kwargs)
