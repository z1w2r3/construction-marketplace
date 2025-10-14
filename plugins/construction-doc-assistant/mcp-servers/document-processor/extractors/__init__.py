"""
信息提取器模块

导出摘要提取器和相关功能
"""

from .summary_extractor import (
    SummaryExtractor,
    extract_summary,
    extract_construction_summary
)

__all__ = [
    'SummaryExtractor',
    'extract_summary',
    'extract_construction_summary',
]
