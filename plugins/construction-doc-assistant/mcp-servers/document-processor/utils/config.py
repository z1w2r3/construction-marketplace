"""
MCP 服务器配置管理模块

提供配置参数管理和环境变量处理
"""
import os
from typing import Optional


class Config:
    """MCP 服务器配置类"""

    # 文件处理限制
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 100 * 1024 * 1024))  # 100MB
    MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE", 20))  # 批量处理最多20个文件

    # 解析选项
    DEFAULT_EXTRACT_TABLES = True
    DEFAULT_EXTRACT_IMAGES = False
    MAX_SUMMARY_LENGTH = int(os.getenv("MAX_SUMMARY_LENGTH", 2000))  # 摘要最大字符数
    MAX_TEXT_PREVIEW_LENGTH = 500  # 文本预览长度

    # 性能优化
    ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    CACHE_TTL = 3600  # 缓存过期时间(秒) - 1小时

    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "mcp_server.log")
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 3

    # 错误处理
    RETRY_COUNT = 3
    TIMEOUT = 30  # 超时时间(秒)

    # 支持的文件类型
    SUPPORTED_EXTENSIONS = {
        'word': ['.docx', '.doc'],
        'excel': ['.xlsx', '.xls'],
        'powerpoint': ['.pptx', '.ppt'],
        'pdf': ['.pdf'],
        'text': ['.txt', '.md']
    }

    # MIME 类型映射
    MIME_TYPES = {
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'word',
        'application/msword': 'word',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'excel',
        'application/vnd.ms-excel': 'excel',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'powerpoint',
        'application/vnd.ms-powerpoint': 'powerpoint',
        'application/pdf': 'pdf',
        'text/plain': 'text',
        'text/markdown': 'text'
    }

    # 建筑行业关键词库
    CONSTRUCTION_KEYWORDS = {
        '进度': ['完成情况', '计划完成', '实际完成', '工期', '节点', '进度', '延期', '提前'],
        '质量': ['检验', '验收', '合格', '不合格', '整改', '质量', '缺陷', '返工'],
        '安全': ['事故', '隐患', '检查', '教育', '措施', '安全', '防护', '应急'],
        '成本': ['投资', '造价', '结算', '变更', '成本', '预算', '支付'],
        '材料': ['进场', '合格证', '试验报告', '品牌', '规格', '材料', '设备'],
        '人员': ['人员', '班组', '劳务', '工人', '技术人员', '管理人员'],
        '设备': ['设备', '机械', '工具', '仪器', '车辆'],
        '环境': ['环保', '扬尘', '噪音', '污水', '固废', '文明施工']
    }

    @classmethod
    def get_file_type_by_extension(cls, file_path: str) -> Optional[str]:
        """
        根据文件扩展名获取文件类型

        Args:
            file_path: 文件路径

        Returns:
            文件类型 ('word', 'excel', 'powerpoint', 'pdf', 'text') 或 None
        """
        ext = os.path.splitext(file_path)[1].lower()
        for file_type, extensions in cls.SUPPORTED_EXTENSIONS.items():
            if ext in extensions:
                return file_type
        return None

    @classmethod
    def get_file_type_by_mime(cls, mime_type: str) -> Optional[str]:
        """
        根据 MIME 类型获取文件类型

        Args:
            mime_type: MIME 类型字符串

        Returns:
            文件类型或 None
        """
        return cls.MIME_TYPES.get(mime_type)

    @classmethod
    def is_supported_file(cls, file_path: str) -> bool:
        """
        检查文件是否支持

        Args:
            file_path: 文件路径

        Returns:
            是否支持
        """
        return cls.get_file_type_by_extension(file_path) is not None

    @classmethod
    def get_all_supported_extensions(cls) -> list:
        """
        获取所有支持的文件扩展名列表

        Returns:
            扩展名列表
        """
        extensions = []
        for exts in cls.SUPPORTED_EXTENSIONS.values():
            extensions.extend(exts)
        return extensions


# 导出配置实例
config = Config()
