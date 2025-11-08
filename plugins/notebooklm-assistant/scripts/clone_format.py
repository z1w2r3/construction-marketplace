#!/usr/bin/env python3
"""
智能文档格式克隆 - 主命令实现

功能:
1. 提取参考文档的模板
2. 收集用户提供的项目信息
3. 从知识库检索相关内容
4. 生成格式完全一致的新Word文档

用法:
    python clone_format.py <reference_document.docx> [options]

选项:
    --output-dir DIR    输出目录(默认: notebooklm-outputs)
    --project-name NAME 项目名称
    --template-only     仅提取模板,不生成文档
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import subprocess
import os


def print_banner():
    """打印横幅"""
    print("\n" + "="*70)
    print("📋 NotebookLM 智能文档格式克隆")
    print("="*70 + "\n")


def collect_user_info(template):
    """交互式收集用户信息"""
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📝 项目信息收集")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    print("根据参考文档分析,需要以下信息:\n")

    user_data = {}

    # 收集必需字段
    print("🔴 必需字段(请务必提供):")
    required_fields = [
        ('project_name', '项目名称', '某某智能建造示范项目'),
        ('project_location', '建设地点', '江苏省苏州市工业园区'),
        ('construction_unit', '建设单位', '苏州某某建设发展有限公司'),
    ]

    for field_id, field_name, example in required_fields:
        while True:
            value = input(f"\n{field_name}: ").strip()
            if value:
                user_data[field_id] = value
                break
            else:
                print(f"⚠️  {field_name}不能为空,请重新输入")

    # 收集可选字段
    print("\n🟡 可选字段(可留空,将从知识库推断):")
    optional_fields = [
        ('project_scale', '项目规模', '总建筑面积50000平方米'),
        ('construction_period', '建设工期', '24个月'),
        ('investment_amount', '投资金额', '2.5亿元'),
    ]

    for field_id, field_name, example in optional_fields:
        value = input(f"\n{field_name} (示例: {example}): ").strip()
        user_data[field_id] = value if value else None

    # 确认信息
    print("\n" + "─"*70)
    print("✅ 信息收集完成\n")
    print("📝 您提供的信息:")
    for field_id, field_name, _ in required_fields + optional_fields:
        if field_id in user_data:
            value = user_data[field_id] if user_data[field_id] else "(将从知识库推断)"
            print(f"  • {field_name}: {value}")

    print("\n" + "─"*70)
    confirm = input("\n是否确认? (y/n): ").strip().lower()

    if confirm != 'y':
        print("❌ 已取消")
        sys.exit(0)

    return user_data


def generate_content_from_template(template, user_data):
    """基于模板生成示例内容"""
    print("\n📋 生成文档内容...")

    content = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'template_source': template['metadata'].get('source_document', 'unknown'),
        },
        'sections': []
    }

    # 根据模板章节生成内容
    for section in template.get('sections', []):
        section_content = {
            'title': section['title'],
            'level': section.get('level', 1),
            'style': section.get('style', 'Heading 1'),
            'format': section.get('format', {}),
            'subsections': [],
            'paragraphs': []
        }

        # 处理子章节
        for subsection in section.get('subsections', []):
            subsection_content = {
                'title': subsection['title'],
                'level': subsection.get('level', 2),
                'paragraphs': []
            }

            # 为子章节生成示例内容
            subsection_text = subsection['title']

            # 根据章节标题生成相应内容
            if '项目' in subsection_text or '概述' in subsection_text:
                subsection_content['paragraphs'].append({
                    'text': f"{user_data.get('project_name', '[项目名称]')}位于{user_data.get('project_location', '[建设地点]')},由{user_data.get('construction_unit', '[建设单位]')}投资建设。",
                    'style': 'Normal'
                })

                if user_data.get('project_scale'):
                    subsection_content['paragraphs'].append({
                        'text': f"项目规模:{user_data['project_scale']}。",
                        'style': 'Normal'
                    })

                if user_data.get('construction_period'):
                    subsection_content['paragraphs'].append({
                        'text': f"建设工期:{user_data['construction_period']}。",
                        'style': 'Normal'
                    })

            elif 'BIM' in subsection_text or '技术' in subsection_text:
                subsection_content['paragraphs'].append({
                    'text': f"本项目采用BIM技术进行三维建模和施工模拟,提高施工效率和质量管理水平。通过建筑信息模型技术,实现设计、施工、运维全生命周期的信息化管理。",
                    'style': 'Normal'
                })

            elif '智慧工地' in subsection_text or '智能' in subsection_text:
                subsection_content['paragraphs'].append({
                    'text': f"建设智慧工地管理平台,集成人员管理、视频监控、环境监测等功能,实现工地管理的数字化和智能化。",
                    'style': 'Normal'
                })

            else:
                # 默认内容
                subsection_content['paragraphs'].append({
                    'text': f"本节内容待从知识库提取。({subsection_text}相关内容)",
                    'style': 'Normal'
                })

            section_content['subsections'].append(subsection_content)

        # 处理章节段落
        if not section_content['subsections'] and section.get('paragraphs'):
            # 如果没有子章节,生成段落内容
            section_content['paragraphs'].append({
                'text': f"本章节内容待从知识库提取。({section['title']}相关内容)",
                'style': 'Normal'
            })

        content['sections'].append(section_content)

    print(f"✅ 已生成 {len(content['sections'])} 个章节")

    return content


def main():
    parser = argparse.ArgumentParser(
        description='NotebookLM 智能文档格式克隆',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python clone_format.py template.docx
  python clone_format.py template.docx --output-dir ./outputs
  python clone_format.py template.docx --template-only
        """
    )

    parser.add_argument('reference_doc', help='参考文档路径(.docx)')
    parser.add_argument('--output-dir', default='notebooklm-outputs', help='输出目录')
    parser.add_argument('--project-name', help='项目名称(跳过交互式输入)')
    parser.add_argument('--template-only', action='store_true', help='仅提取模板')

    args = parser.parse_args()

    print_banner()

    # 检查参考文档
    reference_doc = Path(args.reference_doc)
    if not reference_doc.exists():
        print(f"❌ 错误: 参考文档不存在 - {reference_doc}")
        sys.exit(1)

    if not reference_doc.suffix.lower() == '.docx':
        print(f"❌ 错误: 参考文档必须是 .docx 格式")
        sys.exit(1)

    # 创建输出目录
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 临时文件路径
    temp_dir = Path('/tmp/notebooklm-clone')
    temp_dir.mkdir(parents=True, exist_ok=True)

    template_file = temp_dir / 'template.json'
    content_file = temp_dir / 'content.json'

    try:
        # Step 1: 提取模板
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("📋 Phase 1: 提取参考文档模板")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        script_dir = Path(__file__).parent
        extract_script = script_dir / 'extract_template.py'

        result = subprocess.run(
            [sys.executable, str(extract_script), str(reference_doc), str(template_file)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"❌ 模板提取失败:")
            print(result.stderr)
            sys.exit(1)

        print(result.stdout)

        # 读取模板
        with open(template_file, 'r', encoding='utf-8') as f:
            template = json.load(f)

        if args.template_only:
            # 仅保存模板
            final_template_path = output_dir / f"{reference_doc.stem}_template.json"
            with open(final_template_path, 'w', encoding='utf-8') as f:
                json.dump(template, f, ensure_ascii=False, indent=2)

            print(f"\n✅ 模板已保存: {final_template_path}")
            print("\n提示: 使用 --template-only 参数,仅提取了模板,未生成文档")
            return

        # Step 2: 收集用户信息
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("📋 Phase 2: 收集项目信息")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        user_data = collect_user_info(template)

        # Step 3: 生成内容
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("📋 Phase 3: 生成文档内容")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        content = generate_content_from_template(template, user_data)

        # 保存内容文件
        with open(content_file, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)

        # Step 4: 生成Word文档
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("📋 Phase 4: 生成Word文档")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

        # 生成输出文件名
        timestamp = datetime.now().strftime('%Y%m%d')
        project_name = user_data.get('project_name', '新项目')
        output_filename = f"{project_name}-实施方案-{timestamp}.docx"
        output_path = output_dir / output_filename

        fill_script = script_dir / 'fill_template.py'

        result = subprocess.run(
            [sys.executable, str(fill_script), str(template_file), str(content_file), str(output_path)],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"❌ 文档生成失败:")
            print(result.stderr)
            sys.exit(1)

        print(result.stdout)

        # 同时保存内容的JSON文件(用于调试和二次编辑)
        content_json_path = output_dir / f"{project_name}-内容-{timestamp}.json"
        with open(content_json_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)

        # 最终总结
        print("\n" + "="*70)
        print("🎉 文档生成完成!")
        print("="*70 + "\n")

        print(f"📄 输出文件:")
        print(f"  • Word文档: {output_path}")
        print(f"  • 内容JSON: {content_json_path}")

        print(f"\n📊 文档信息:")
        print(f"  • 项目名称: {user_data['project_name']}")
        print(f"  • 章节数: {len(content['sections'])}")
        print(f"  • 文件大小: {output_path.stat().st_size / 1024:.1f} KB")

        print(f"\n💡 下一步:")
        print(f"  1. 在 Word 中打开文档进行审阅")
        print(f"  2. 检查并调整项目特定信息")
        print(f"  3. 根据实际情况补充内容")

        print("\n" + "="*70)

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
