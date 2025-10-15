#!/usr/bin/env python3
"""
建筑施工文档处理 MCP 服务器 - 增强版
提供完整的 Word、Excel、PowerPoint、PDF 文档解析和智能分析功能
"""

import sys
import os
import json
from typing import Any

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入工具模块
from utils import get_logger, setup_logger, handle_error, handle_file_error, ErrorHandler
from validators import validate_document, batch_validate_documents
from parsers import parse_document, batch_parse_documents
from extractors import extract_summary, extract_construction_summary

# 设置日志
logger = setup_logger("mcp_server", level="INFO")

# 尝试导入 MCP SDK
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    from mcp.server.stdio import stdio_server
except ImportError as e:
    logger.error(f"MCP SDK 未安装: {e}")
    logger.error("请运行: pip install mcp")
    sys.exit(1)

# 创建 MCP 服务器实例
server = Server("construction-doc-processor")

logger.info("建筑施工文档处理 MCP 服务器初始化...")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """列出所有可用工具"""
    return [
        # 1. 文档验证工具
        Tool(
            name="validate_document",
            description="验证文档是否可读，返回文档基本信息和可读性状态",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "文档的绝对路径"
                    }
                },
                "required": ["file_path"]
            }
        ),

        # 2. Word 文档解析
        Tool(
            name="parse_word_document",
            description="解析 Word 文档，提取文本、表格、标题结构和元数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Word 文档的绝对路径"
                    },
                    "parse_mode": {
                        "type": "string",
                        "enum": ["summary", "full"],
                        "description": "解析模式: summary=摘要模式(快速,控制token,提取前100段), full=完整模式(深度,不限制长度,提取所有内容)",
                        "default": "summary"
                    },
                    "extract_tables": {
                        "type": "boolean",
                        "description": "是否提取表格（默认 true）",
                        "default": True
                    },
                    "max_paragraphs": {
                        "type": "integer",
                        "description": "最大段落数限制（可选，仅在 parse_mode=summary 时生效）"
                    },
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "关注的关键词列表（可选）"
                    }
                },
                "required": ["file_path"]
            }
        ),

        # 3. Excel 文档解析
        Tool(
            name="parse_excel_document",
            description="解析 Excel 文档，提取工作表和单元格数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Excel 文档的绝对路径"
                    },
                    "parse_mode": {
                        "type": "string",
                        "enum": ["summary", "full"],
                        "description": "解析模式: summary=摘要模式(每个工作表最多100行), full=完整模式(提取所有行)",
                        "default": "summary"
                    },
                    "sheet_name": {
                        "type": "string",
                        "description": "指定工作表名称（可选）"
                    },
                    "max_rows": {
                        "type": "integer",
                        "description": "每个工作表最大行数（可选，仅在 parse_mode=summary 时生效，默认 100）",
                        "default": 100
                    }
                },
                "required": ["file_path"]
            }
        ),

        # 4. PowerPoint 文档解析
        Tool(
            name="parse_powerpoint_document",
            description="解析 PowerPoint 文档，提取幻灯片内容、标题和备注",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "PowerPoint 文档的绝对路径"
                    },
                    "parse_mode": {
                        "type": "string",
                        "enum": ["summary", "full"],
                        "description": "解析模式: summary=摘要模式(最多50张幻灯片), full=完整模式(提取所有幻灯片)",
                        "default": "summary"
                    },
                    "max_slides": {
                        "type": "integer",
                        "description": "最大幻灯片数（可选，仅在 parse_mode=summary 时生效，默认 50）",
                        "default": 50
                    },
                    "extract_notes": {
                        "type": "boolean",
                        "description": "是否提取备注（默认 true）",
                        "default": True
                    }
                },
                "required": ["file_path"]
            }
        ),

        # 5. PDF 文档解析
        Tool(
            name="parse_pdf_document",
            description="解析 PDF 文档，提取文本和元数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "PDF 文档的绝对路径"
                    },
                    "parse_mode": {
                        "type": "string",
                        "enum": ["summary", "full"],
                        "description": "解析模式: summary=摘要模式(最多50页), full=完整模式(提取所有页)",
                        "default": "summary"
                    },
                    "max_pages": {
                        "type": "integer",
                        "description": "最大页数（可选，仅在 parse_mode=summary 时生效，默认 50）",
                        "default": 50
                    },
                    "extract_tables": {
                        "type": "boolean",
                        "description": "是否提取表格（需要 pdfplumber，默认 false）",
                        "default": False
                    }
                },
                "required": ["file_path"]
            }
        ),

        # 6. 智能摘要提取
        Tool(
            name="extract_document_summary",
            description="从解析后的文档中智能提取摘要，支持关键词过滤",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "文档的绝对路径"
                    },
                    "focus_keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "关注的关键词列表，如 ['进度', '质量', '安全']"
                    },
                    "max_length": {
                        "type": "integer",
                        "description": "摘要最大字符数（默认 2000）",
                        "default": 2000
                    }
                },
                "required": ["file_path"]
            }
        ),

        # 7. 批量文档处理
        Tool(
            name="batch_parse_documents",
            description="批量解析多个文档，返回统一格式的结果",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "文档路径列表"
                    },
                    "extract_mode": {
                        "type": "string",
                        "enum": ["full", "summary", "metadata"],
                        "description": "提取模式：full=完整内容，summary=摘要，metadata=仅元数据",
                        "default": "summary"
                    }
                },
                "required": ["file_paths"]
            }
        ),

        # 8. 文档元数据获取
        Tool(
            name="get_document_metadata",
            description="获取文档基本元数据（文件大小、创建时间、修改时间等）",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "文档的绝对路径"
                    }
                },
                "required": ["file_path"]
            }
        ),

        # 9. Word报告生成(新增)
        Tool(
            name="generate_word_report",
            description="将Markdown报告转换为格式化的Word文档(当前版本:纯文字,不含图片)",
            inputSchema={
                "type": "object",
                "properties": {
                    "markdown_file": {
                        "type": "string",
                        "description": "Markdown源文件的绝对路径"
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Word输出文件的绝对路径"
                    },
                    "template_type": {
                        "type": "string",
                        "enum": ["project_summary", "inspection_report",
                                "progress_analysis", "organize_plan"],
                        "description": "报告模板类型:project_summary=项目总结,inspection_report=完整性检查,progress_analysis=进度分析,organize_plan=整理方案",
                        "default": "project_summary"
                    },
                    "project_info": {
                        "type": "object",
                        "description": "项目信息(用于页眉页脚)",
                        "properties": {
                            "project_name": {
                                "type": "string",
                                "description": "项目名称"
                            },
                            "report_type": {
                                "type": "string",
                                "description": "报告类型描述"
                            },
                            "generate_date": {
                                "type": "string",
                                "description": "生成日期(格式:YYYY-MM-DD)"
                            }
                        }
                    }
                },
                "required": ["markdown_file", "output_file"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """执行工具调用"""
    try:
        logger.info(f"调用工具: {name}")
        logger.debug(f"参数: {arguments}")

        # 1. 文档验证
        if name == "validate_document":
            result = validate_document(arguments["file_path"])
            return [TextContent(
                type="text",
                text=_format_validation_result(result)
            )]

        # 2-5. 文档解析工具
        elif name in ["parse_word_document", "parse_excel_document",
                      "parse_powerpoint_document", "parse_pdf_document"]:
            # 处理 parse_mode 参数
            parse_mode = arguments.get("parse_mode", "summary")

            # 根据 parse_mode 调整限制参数
            if parse_mode == "full":
                # 完整模式:移除所有限制
                if "max_paragraphs" in arguments:
                    arguments.pop("max_paragraphs")
                if "max_rows" in arguments:
                    arguments.pop("max_rows")
                if "max_slides" in arguments:
                    arguments.pop("max_slides")
                if "max_pages" in arguments:
                    arguments.pop("max_pages")

                logger.info(f"使用完整模式解析文档: {arguments['file_path']}")
            else:
                # 摘要模式:使用默认限制(如果用户未指定)
                if name == "parse_word_document" and "max_paragraphs" not in arguments:
                    arguments["max_paragraphs"] = 100
                elif name == "parse_excel_document" and "max_rows" not in arguments:
                    arguments["max_rows"] = 100
                elif name == "parse_powerpoint_document" and "max_slides" not in arguments:
                    arguments["max_slides"] = 50
                elif name == "parse_pdf_document" and "max_pages" not in arguments:
                    arguments["max_pages"] = 50

                logger.info(f"使用摘要模式解析文档: {arguments['file_path']}")

            result = parse_document(arguments["file_path"], arguments)

            # 在结果中记录使用的模式
            if result.get("status") == "success":
                result["parse_mode"] = parse_mode

            return [TextContent(
                type="text",
                text=_format_parse_result(result)
            )]

        # 6. 智能摘要提取
        elif name == "extract_document_summary":
            # 先解析文档
            parsed = parse_document(arguments["file_path"])

            # 提取摘要
            summary = extract_summary(
                parsed,
                focus_keywords=arguments.get("focus_keywords"),
                max_length=arguments.get("max_length", 2000)
            )

            return [TextContent(
                type="text",
                text=_format_summary_result(summary)
            )]

        # 7. 批量处理
        elif name == "batch_parse_documents":
            results = batch_parse_documents(arguments["file_paths"], arguments)
            return [TextContent(
                type="text",
                text=_format_batch_result(results)
            )]

        # 8. 元数据获取
        elif name == "get_document_metadata":
            result = validate_document(arguments["file_path"])
            if result["valid"]:
                return [TextContent(
                    type="text",
                    text=_format_metadata(result["file_info"])
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ 错误: {', '.join(result['errors'])}"
                )]

        # 9. Word报告生成(新增)
        elif name == "generate_word_report":
            from generators import WordGenerator

            # 获取模板类型
            template_type = arguments.get("template_type", "project_summary")

            # 创建生成器
            generator = WordGenerator(template_type=template_type)

            # 生成Word文档
            result = generator.generate(
                markdown_file=arguments["markdown_file"],
                output_file=arguments["output_file"],
                options={"project_info": arguments.get("project_info")}
            )

            return [TextContent(
                type="text",
                text=_format_generation_result(result)
            )]

        else:
            raise ValueError(f"未知工具: {name}")

    except Exception as e:
        logger.error(f"工具执行错误: {e}", exc_info=True)
        error_result = handle_error(e, {"tool": name, "arguments": arguments})
        return [TextContent(
            type="text",
            text=ErrorHandler.format_error_for_user(error_result)
        )]


def _format_validation_result(result: dict) -> str:
    """格式化验证结果"""
    if result["valid"]:
        file_info = result["file_info"]
        output = f"""✅ 文档验证通过

📄 文件信息:
  - 文件名: {file_info['name']}
  - 文件大小: {file_info['size_formatted']}
  - 文件类型: {file_info['extension']}
  - 修改时间: {file_info['modified_time']}
"""
        if result.get("warnings"):
            output += f"\n⚠️ 警告:\n"
            for warning in result["warnings"]:
                output += f"  - {warning}\n"
    else:
        output = f"""❌ 文档验证失败

错误:
"""
        for error in result["errors"]:
            output += f"  - {error}\n"

    return output


def _format_parse_result(result: dict) -> str:
    """格式化解析结果"""
    if result.get("status") == "error":
        return ErrorHandler.format_error_for_user(result)

    file_info = result.get("file_info", {})
    content = result.get("content", {})
    summary = result.get("summary", {})
    parse_mode = result.get("parse_mode", "summary")

    # 根据模式显示不同的标题
    if parse_mode == "full":
        output = f"""✅ 文档解析成功 (完整模式)

📄 文件: {file_info.get('name', 'Unknown')}
📊 解析器: {file_info.get('parser', 'Unknown')}
🔍 解析模式: 完整模式 - 已提取所有内容
"""
    else:
        output = f"""✅ 文档解析成功 (摘要模式)

📄 文件: {file_info.get('name', 'Unknown')}
📊 解析器: {file_info.get('parser', 'Unknown')}
🔍 解析模式: 摘要模式 - 已提取部分内容
"""

    # 根据解析器类型显示不同的摘要
    if 'Word' in file_info.get('parser', ''):
        output += f"""
📝 内容统计:
  - 章节数: {summary.get('total_sections', 0)}
  - 段落数: {summary.get('total_paragraphs', 0)}
  - 字符数: {summary.get('total_chars', 0)}
  - 表格数: {summary.get('total_tables', 0)}
"""
        if summary.get('section_titles'):
            output += f"\n📑 章节列表:\n"
            for title in summary['section_titles'][:10]:
                output += f"  - {title}\n"

    elif 'Excel' in file_info.get('parser', ''):
        output += f"""
📊 内容统计:
  - 工作表数: {summary.get('total_sheets', 0)}
  - 总行数: {summary.get('total_rows', 0)}
"""
        if summary.get('sheet_names'):
            output += f"\n📋 工作表列表:\n"
            for name in summary['sheet_names']:
                output += f"  - {name}\n"

    elif 'PowerPoint' in file_info.get('parser', ''):
        output += f"""
🎞️ 内容统计:
  - 幻灯片数: {summary.get('total_slides', 0)}
  - 有标题: {len(summary.get('slide_titles', []))} 张
  - 有备注: {summary.get('slides_with_notes', 0)} 张
"""
        if summary.get('slide_titles'):
            output += f"\n📑 幻灯片标题:\n"
            for title in summary['slide_titles'][:10]:
                output += f"  - {title}\n"

    elif 'PDF' in file_info.get('parser', ''):
        output += f"""
📄 内容统计:
  - 总页数: {summary.get('total_pages', 0)}
  - 已提取: {summary.get('pages_extracted', 0)} 页
  - 总字符数: {summary.get('total_text_length', 0)}
"""

    # 根据模式添加不同的提示
    if parse_mode == "full":
        output += f"\n⚠️ 提示: 完整模式返回了所有内容,可能消耗大量 token"
    else:
        output += f"\n💡 提示: 当前为摘要模式,使用 parse_mode='full' 可获取完整内容"

    return output


def _format_summary_result(summary: dict) -> str:
    """格式化摘要结果"""
    if summary.get("status") == "error":
        return f"❌ 摘要提取失败: {summary.get('message', 'Unknown error')}"

    file_info = summary.get("file_info", {})
    output = f"""✅ 智能摘要提取完成

📄 文件: {file_info.get('name', 'Unknown')}

"""

    # 主要要点
    if summary.get("main_points"):
        output += "🎯 主要要点:\n"
        for point in summary["main_points"][:10]:
            output += f"  • {point}\n"
        output += "\n"

    # 关键数据
    if summary.get("key_data"):
        output += "📊 关键数据:\n"
        for key, value in summary["key_data"].items():
            output += f"  - {key}: {value}\n"
        output += "\n"

    # 关键词搜索结果
    if summary.get("keywords_found"):
        output += f"🔍 找到关键词: {', '.join(summary['keywords_found'])}\n\n"

        if summary.get("sections_summary"):
            output += "📝 相关内容:\n"
            for keyword, items in list(summary["sections_summary"].items())[:3]:
                output += f"\n  关键词: {keyword}\n"
                for item in items[:2]:
                    if isinstance(item, dict):
                        if 'text' in item:
                            output += f"    - {item.get('section', '未知章节')}: {item['text'][:100]}...\n"
                        elif 'value' in item:
                            output += f"    - {item.get('sheet', '未知工作表')} ({item.get('row', 0)}, {item.get('col', 0)}): {item['value']}\n"

    return output


def _format_batch_result(results: list) -> str:
    """格式化批量处理结果"""
    total = len(results)
    success = sum(1 for r in results if r.get('status') == 'success')
    failed = total - success

    output = f"""✅ 批量处理完成

📊 处理统计:
  - 总文档数: {total}
  - 成功: {success}
  - 失败: {failed}

"""

    # 显示成功的文档
    if success > 0:
        output += "✅ 成功处理的文档:\n"
        for result in results:
            if result.get('status') == 'success':
                file_info = result.get('file_info', {})
                output += f"  • {file_info.get('name', 'Unknown')}\n"

    # 显示失败的文档
    if failed > 0:
        output += "\n❌ 失败的文档:\n"
        for result in results:
            if result.get('status') != 'success':
                file_info = result.get('file_info', {})
                error_msg = result.get('error_message', 'Unknown error')
                output += f"  • {file_info.get('name', 'Unknown')}: {error_msg}\n"

    return output


def _format_metadata(file_info: dict) -> str:
    """格式化元数据"""
    return f"""📄 文档元数据

文件名: {file_info.get('name', 'Unknown')}
文件大小: {file_info.get('size_formatted', 'Unknown')}
文件类型: {file_info.get('extension', 'Unknown')}
创建时间: {file_info.get('created_time', 'Unknown')}
修改时间: {file_info.get('modified_time', 'Unknown')}
文件路径: {file_info.get('path', 'Unknown')}
"""


def _format_generation_result(result: dict) -> str:
    """格式化Word生成结果"""
    if result.get("status") == "error":
        return f"""❌ Word文档生成失败

错误: {result.get('error', 'Unknown error')}
"""

    output_file = result.get('output_file', 'Unknown')
    sections_processed = result.get('sections_processed', 0)
    file_size = result.get('file_size', 0)
    warnings = result.get('warnings', [])
    template_type = result.get('template_type', 'Unknown')

    # 格式化文件大小
    if file_size < 1024:
        size_str = f"{file_size} B"
    elif file_size < 1024 * 1024:
        size_str = f"{file_size / 1024:.1f} KB"
    else:
        size_str = f"{file_size / (1024 * 1024):.1f} MB"

    # 模板类型中文名称映射
    template_names = {
        "project_summary": "项目总结报告",
        "inspection_report": "完整性检查报告",
        "progress_analysis": "进度分析报告",
        "organize_plan": "资料整理方案"
    }
    template_name = template_names.get(template_type, template_type)

    output = f"""✅ Word文档生成成功

📄 输出文件: {output_file}
📊 文件大小: {size_str}
📝 模板类型: {template_name}
🔢 处理段落: {sections_processed} 个
"""

    if warnings:
        output += f"\n⚠️ 警告信息 ({len(warnings)} 项):\n"
        for i, warning in enumerate(warnings[:5], 1):  # 最多显示5条警告
            output += f"  {i}. {warning}\n"
        if len(warnings) > 5:
            output += f"  ... 还有 {len(warnings) - 5} 条警告\n"

    output += "\n💡 提示:\n"
    output += "  - Word文档已自动排版,可直接打开编辑\n"
    output += "  - 图片功能将在Phase 2实现,当前显示占位符\n"
    output += "  - 如需调整样式,可在Word中手动修改\n"

    return output


async def main():
    """启动 MCP 服务器"""
    logger.info("=" * 60)
    logger.info("建筑施工文档处理 MCP 服务器 v1.3.0")
    logger.info("=" * 60)
    logger.info("支持的文档格式: Word (.docx), Excel (.xlsx), PowerPoint (.pptx), PDF (.pdf)")
    logger.info("提供工具: 文档验证、解析、摘要提取、批量处理、Word报告生成")
    logger.info("新增功能: 双模式解析 (summary/full) - 灵活控制解析深度")
    logger.info("=" * 60)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("服务器已停止")
    except Exception as e:
        logger.error(f"服务器错误: {e}", exc_info=True)
        sys.exit(1)
