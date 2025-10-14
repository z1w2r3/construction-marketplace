"""
文档验证器模块

提供文档可读性验证和基本信息检测
"""
import os
from typing import Dict, List, Optional
from pathlib import Path

# 尝试导入 python-magic，如果不可用则降级
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    config,
    get_logger,
    FileValidationError
)

logger = get_logger(__name__)


class DocumentValidator:
    """文档验证器类"""

    def __init__(self):
        """初始化验证器"""
        self.max_file_size = config.MAX_FILE_SIZE
        self.supported_extensions = config.get_all_supported_extensions()

    def validate(self, file_path: str) -> Dict:
        """
        验证文档

        Args:
            file_path: 文件路径

        Returns:
            验证结果字典
            {
                "valid": bool,
                "file_info": {...},
                "warnings": [...],
                "errors": [...]
            }
        """
        result = {
            "valid": True,
            "file_info": {},
            "warnings": [],
            "errors": []
        }

        try:
            # 1. 检查文件是否存在
            if not self._check_file_exists(file_path, result):
                result["valid"] = False
                return result

            # 2. 获取文件基本信息
            file_info = self._get_file_info(file_path)
            result["file_info"] = file_info

            # 3. 检查文件扩展名
            if not self._check_extension(file_path, result):
                result["warnings"].append(f"文件扩展名 {file_info['extension']} 可能不受支持")

            # 4. 检查文件大小
            if not self._check_file_size(file_info['size'], result):
                result["warnings"].append(
                    f"文件大小 {self._format_size(file_info['size'])} 较大，处理可能较慢"
                )

            # 5. 检查文件权限
            if not self._check_permissions(file_path, result):
                result["valid"] = False
                return result

            # 6. 检查MIME类型 (如果可用)
            if MAGIC_AVAILABLE:
                mime_type = self._get_mime_type(file_path)
                result["file_info"]["mime_type"] = mime_type
                if not self._check_mime_type(mime_type, result):
                    result["warnings"].append(f"MIME类型 {mime_type} 可能与文件扩展名不匹配")

            # 7. 尝试打开文件验证完整性
            if not self._check_file_integrity(file_path, result):
                result["valid"] = False
                result["errors"].append("文件可能已损坏或格式不正确")

            logger.info(
                f"文档验证完成: {file_path} - "
                f"有效: {result['valid']}, "
                f"警告: {len(result['warnings'])}, "
                f"错误: {len(result['errors'])}"
            )

        except Exception as e:
            logger.error(f"验证过程出错: {e}", exc_info=True)
            result["valid"] = False
            result["errors"].append(f"验证失败: {str(e)}")

        return result

    def _check_file_exists(self, file_path: str, result: Dict) -> bool:
        """检查文件是否存在"""
        if not os.path.exists(file_path):
            result["errors"].append(f"文件不存在: {file_path}")
            logger.error(f"文件不存在: {file_path}")
            return False

        if not os.path.isfile(file_path):
            result["errors"].append(f"路径不是文件: {file_path}")
            logger.error(f"路径不是文件: {file_path}")
            return False

        return True

    def _get_file_info(self, file_path: str) -> Dict:
        """获取文件基本信息"""
        path = Path(file_path)
        stat = path.stat()

        return {
            "path": str(path.absolute()),
            "name": path.name,
            "extension": path.suffix.lower(),
            "size": stat.st_size,
            "size_formatted": self._format_size(stat.st_size),
            "created_time": stat.st_ctime,
            "modified_time": stat.st_mtime,
            "is_symlink": path.is_symlink()
        }

    def _check_extension(self, file_path: str, result: Dict) -> bool:
        """检查文件扩展名是否支持"""
        ext = Path(file_path).suffix.lower()
        if ext not in self.supported_extensions:
            logger.warning(f"不支持的文件扩展名: {ext}")
            return False
        return True

    def _check_file_size(self, size: int, result: Dict) -> bool:
        """检查文件大小"""
        if size > self.max_file_size:
            logger.warning(
                f"文件大小 {self._format_size(size)} 超过限制 "
                f"{self._format_size(self.max_file_size)}"
            )
            return False

        if size == 0:
            result["warnings"].append("文件大小为0，可能是空文件")
            logger.warning("空文件")
            return False

        return True

    def _check_permissions(self, file_path: str, result: Dict) -> bool:
        """检查文件权限"""
        if not os.access(file_path, os.R_OK):
            result["errors"].append("文件不可读，请检查权限")
            logger.error(f"文件不可读: {file_path}")
            return False
        return True

    def _get_mime_type(self, file_path: str) -> Optional[str]:
        """获取文件MIME类型"""
        if not MAGIC_AVAILABLE:
            return None

        try:
            mime = magic.Magic(mime=True)
            return mime.from_file(file_path)
        except Exception as e:
            logger.warning(f"无法获取MIME类型: {e}")
            return None

    def _check_mime_type(self, mime_type: Optional[str], result: Dict) -> bool:
        """检查MIME类型是否受支持"""
        if mime_type is None:
            return True  # 无法检测时跳过

        file_type = config.get_file_type_by_mime(mime_type)
        if file_type is None:
            logger.warning(f"不支持的MIME类型: {mime_type}")
            return False

        return True

    def _check_file_integrity(self, file_path: str, result: Dict) -> bool:
        """检查文件完整性 - 尝试读取前1KB"""
        try:
            with open(file_path, 'rb') as f:
                # 读取前1KB数据
                data = f.read(1024)

                # 检查是否为空
                if not data:
                    logger.warning("文件内容为空")
                    return False

                # 对于Office文档，检查是否为有效的ZIP文件
                ext = Path(file_path).suffix.lower()
                if ext in ['.docx', '.xlsx', '.pptx']:
                    # Office 2007+ 文档是ZIP格式，应以PK开头
                    if not data.startswith(b'PK'):
                        logger.warning("Office文档格式可能不正确 (非ZIP格式)")
                        return False

                # 对于PDF，检查魔术数字
                elif ext == '.pdf':
                    if not data.startswith(b'%PDF'):
                        logger.warning("PDF文档格式可能不正确")
                        return False

                return True

        except Exception as e:
            logger.error(f"文件完整性检查失败: {e}")
            return False

    @staticmethod
    def _format_size(size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"

    def quick_validate(self, file_path: str) -> bool:
        """
        快速验证文档 - 仅检查基本条件

        Args:
            file_path: 文件路径

        Returns:
            是否有效
        """
        try:
            # 检查存在性
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                return False

            # 检查扩展名
            ext = Path(file_path).suffix.lower()
            if ext not in self.supported_extensions:
                return False

            # 检查大小
            size = os.path.getsize(file_path)
            if size == 0 or size > self.max_file_size:
                return False

            # 检查权限
            if not os.access(file_path, os.R_OK):
                return False

            return True

        except Exception as e:
            logger.error(f"快速验证失败: {e}")
            return False

    def batch_validate(self, file_paths: List[str]) -> Dict:
        """
        批量验证多个文档

        Args:
            file_paths: 文件路径列表

        Returns:
            批量验证结果
        """
        results = {
            "total": len(file_paths),
            "valid": [],
            "invalid": [],
            "warnings": []
        }

        for file_path in file_paths:
            validation = self.validate(file_path)

            if validation["valid"]:
                results["valid"].append({
                    "path": file_path,
                    "info": validation["file_info"]
                })
            else:
                results["invalid"].append({
                    "path": file_path,
                    "errors": validation["errors"]
                })

            if validation["warnings"]:
                results["warnings"].append({
                    "path": file_path,
                    "warnings": validation["warnings"]
                })

        logger.info(
            f"批量验证完成: 总计 {results['total']}, "
            f"有效 {len(results['valid'])}, "
            f"无效 {len(results['invalid'])}"
        )

        return results


# 创建全局验证器实例
validator = DocumentValidator()


# 便捷函数
def validate_document(file_path: str) -> Dict:
    """验证文档的便捷函数"""
    return validator.validate(file_path)


def quick_validate_document(file_path: str) -> bool:
    """快速验证文档的便捷函数"""
    return validator.quick_validate(file_path)


def batch_validate_documents(file_paths: List[str]) -> Dict:
    """批量验证文档的便捷函数"""
    return validator.batch_validate(file_paths)
