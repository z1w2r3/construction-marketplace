---
name: filesystem-scan
description: "高效扫描文件系统,生成文档索引。用于替代 MCP 的目录扫描功能,提供轻量级、零依赖的文件元数据提取"
---

# 文件系统扫描指南

## 快速开始

使用 Python 标准库快速扫描目录,提取文件元数据:

```python
import os
from pathlib import Path
from datetime import datetime

def scan_directory(root_path, file_types=None, max_depth=10):
    """
    扫描目录,返回文件元数据列表

    参数:
        root_path: 根目录路径(字符串或 Path 对象)
        file_types: 文件类型过滤列表,如 ['.pdf', '.docx'],None 表示所有类型
        max_depth: 最大扫描深度,避免过深遍历

    返回:
        文件元数据字典列表
    """
    files = []
    root_path = Path(root_path).resolve()
    root_depth = str(root_path).count(os.sep)

    for dirpath, dirnames, filenames in os.walk(root_path):
        # 计算当前深度
        current_depth = dirpath.count(os.sep) - root_depth
        if current_depth > max_depth:
            dirnames[:] = []  # 停止深入子目录
            continue

        for filename in filenames:
            file_path = Path(dirpath) / filename

            # 过滤文件类型
            if file_types and file_path.suffix.lower() not in file_types:
                continue

            try:
                # 提取元数据
                stat = file_path.stat()
                files.append({
                    "path": str(file_path.absolute()),
                    "name": filename,
                    "extension": file_path.suffix.lower(),
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                    "modified_readable": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "relative_path": str(file_path.relative_to(root_path))
                })
            except (OSError, PermissionError) as e:
                # 记录错误但继续扫描
                print(f"⚠️  跳过文件 {file_path}: {e}", file=sys.stderr)
                continue

    return files
```

## 使用示例

### 示例 1: 扫描所有文档类型

```python
# 扫描知识库目录
docs_path = "/Users/username/Documents/knowledge-base"
files = scan_directory(docs_path)

print(f"找到 {len(files)} 个文件")
```

### 示例 2: 只扫描特定文档类型

```python
# 只扫描 PDF、Word、Excel 文档
file_types = ['.pdf', '.doc', '.docx', '.xls', '.xlsx']
files = scan_directory(
    root_path="/path/to/docs",
    file_types=file_types,
    max_depth=5
)

# 按类型统计
from collections import Counter
type_counts = Counter(f['extension'] for f in files)
print(f"文件类型分布: {dict(type_counts)}")
```

### 示例 3: 按修改时间排序

```python
files = scan_directory("/path/to/docs")

# 按修改时间倒序排序(最新的在前)
files_sorted = sorted(files, key=lambda f: f['modified'], reverse=True)

print("最新的 10 个文档:")
for f in files_sorted[:10]:
    print(f"  - {f['name']} ({f['modified_readable']})")
```

## 性能优化技巧

### 1. 限制扫描深度

```python
# 避免遍历过深的目录树
files = scan_directory(root_path, max_depth=3)
```

### 2. 早期过滤

```python
# 在 os.walk 循环中过滤,而不是之后
# 这样可以减少后续处理的数据量
```

### 3. 批量处理大量文件

```python
def scan_directory_batched(root_path, batch_size=100):
    """批量扫描,每处理一批显示进度"""
    files = []
    total = 0

    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            file_path = Path(dirpath) / filename
            # ... 提取元数据 ...
            files.append(metadata)
            total += 1

            # 每处理一批显示进度
            if total % batch_size == 0:
                print(f"📊 已扫描 {total} 个文件...")

    return files
```

### 4. 忽略特定目录

```python
def scan_directory_with_exclusions(root_path, exclude_dirs=None):
    """扫描时排除特定目录"""
    exclude_dirs = exclude_dirs or {'.git', 'node_modules', '__pycache__', '.notebooklm'}
    files = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        # 修改 dirnames 会影响后续遍历
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        for filename in filenames:
            # ... 处理文件 ...
            pass

    return files
```

## 错误处理

### 处理权限错误

```python
import sys

try:
    stat = file_path.stat()
except PermissionError as e:
    # 记录到 stderr,继续扫描其他文件
    print(f"⚠️  权限不足,跳过: {file_path}", file=sys.stderr)
    continue
except OSError as e:
    # 处理其他系统错误(如文件被删除、损坏等)
    print(f"⚠️  系统错误,跳过: {file_path} - {e}", file=sys.stderr)
    continue
```

### 处理符号链接

```python
def scan_directory_safe(root_path):
    """安全扫描,避免符号链接导致的无限循环"""
    for dirpath, dirnames, filenames in os.walk(root_path, followlinks=False):
        # followlinks=False 避免跟随符号链接
        pass
```

## 输出格式

### 标准元数据格式

```python
{
    "path": "/absolute/path/to/file.pdf",           # 绝对路径
    "name": "file.pdf",                             # 文件名
    "extension": ".pdf",                            # 扩展名(小写)
    "size": 1048576,                                # 字节数
    "modified": 1729500000.123,                     # Unix 时间戳
    "modified_readable": "2025-10-21 14:30:00",     # 可读时间
    "relative_path": "docs/2025/file.pdf"           # 相对路径
}
```

### 保存为 JSON

```python
import json

files = scan_directory("/path/to/docs")

# 保存为 JSON
with open("index.json", "w", encoding="utf-8") as f:
    json.dump({
        "total_files": len(files),
        "scanned_at": datetime.now().isoformat(),
        "files": files
    }, f, ensure_ascii=False, indent=2)
```

## 与现有代码集成

### 替代 MCP scan_directory 工具

```python
# 旧代码(MCP 调用)
# result = mcp_tool_call("scan_directory", {
#     "directory": root_path,
#     "file_types": [".pdf", ".docx"],
#     "max_depth": 10
# })

# 新代码(直接调用函数)
files = scan_directory(
    root_path=root_path,
    file_types=[".pdf", ".docx"],
    max_depth=10
)
```

## 常见问题

### Q: 如何处理大型目录(10000+ 文件)?

A: 使用生成器模式避免一次性加载所有数据:

```python
def scan_directory_generator(root_path, file_types=None):
    """生成器版本,逐个返回文件元数据"""
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            file_path = Path(dirpath) / filename
            if file_types and file_path.suffix.lower() not in file_types:
                continue

            try:
                stat = file_path.stat()
                yield {
                    "path": str(file_path.absolute()),
                    "name": filename,
                    # ... 其他字段 ...
                }
            except Exception:
                continue

# 使用
for file_info in scan_directory_generator("/large/directory"):
    process_file(file_info)  # 逐个处理,不占用大量内存
```

### Q: 扫描速度慢怎么办?

A:
1. 减少 `max_depth` 限制深度
2. 使用 `file_types` 过滤,减少处理的文件数
3. 排除不需要的目录(如 `.git`, `node_modules`)

### Q: 如何获取文件的 MIME 类型?

A: 使用 `mimetypes` 模块:

```python
import mimetypes

file_path = "/path/to/document.pdf"
mime_type, encoding = mimetypes.guess_type(file_path)
print(f"MIME 类型: {mime_type}")  # application/pdf
```

## 最佳实践

1. **总是使用 Path 对象**: 提供跨平台兼容性
2. **错误容忍**: 单个文件失败不应中断整个扫描
3. **显示进度**: 大量文件时提供进度反馈
4. **早期过滤**: 尽早过滤不需要的文件和目录
5. **文档化假设**: 明确记录预期的目录结构和文件类型

## 相关 Skills

- [document-preview](../document-preview/SKILL.md) - 文档预览提取
- [pdf](../pdf/SKILL.md) - PDF 处理
- [docx](../docx/SKILL.md) - Word 处理
- [xlsx](../xlsx/SKILL.md) - Excel 处理
