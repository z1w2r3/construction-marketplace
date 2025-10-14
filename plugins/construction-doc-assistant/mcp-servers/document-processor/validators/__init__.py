"""
验证模块

提供文档验证功能
"""

from .file_validator import (
    DocumentValidator,
    validator,
    validate_document,
    quick_validate_document,
    batch_validate_documents
)

__all__ = [
    'DocumentValidator',
    'validator',
    'validate_document',
    'quick_validate_document',
    'batch_validate_documents',
]
