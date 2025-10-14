# 检查插件安装状态
检查建筑施工文档助手插件的安装状态,验证所有依赖是否正确安装。

---

你现在要执行**插件安装检查**任务。

## 检查步骤

### 1. 显示欢迎信息

```
正在检查建筑施工文档助手插件安装状态...
```

### 2. 检查插件版本

使用 Read 工具读取插件配置文件:
- 读取: `.claude-plugin/plugin.json`
- 显示插件名称和版本号

### 3. 检查 MCP 服务器目录

使用 Bash 工具检查目录是否存在:
```bash
ls -la mcp-servers/document-processor/
```

显示目录内容,确认以下文件存在:
- ✅ server.py
- ✅ requirements.txt
- ✅ install.sh

### 4. 检查 Python 环境

```bash
python3 --version
```

显示 Python 版本,检查是否 >= 3.8

### 5. 检查 Python 依赖

运行以下检查脚本:

```bash
python3 << 'EOF'
import sys

# 核心依赖
required_packages = {
    'mcp': 'MCP SDK',
    'docx': 'python-docx',
    'openpyxl': 'openpyxl',
    'PyPDF2': 'PyPDF2',
    'pptx': 'python-pptx'
}

print("\n📦 核心依赖检查:")
all_ok = True
for module, name in required_packages.items():
    try:
        __import__(module)
        print(f"  ✅ {name}")
    except ImportError:
        print(f"  ❌ {name} - 未安装")
        all_ok = False

# 可选依赖
optional_packages = {
    'pdfplumber': 'pdfplumber',
    'pandas': 'pandas'
}

print("\n📦 可选依赖检查:")
for module, name in optional_packages.items():
    try:
        __import__(module)
        print(f"  ✅ {name}")
    except ImportError:
        print(f"  ⚪ {name} - 未安装(可选)")

if all_ok:
    print("\n✅ 所有核心依赖已正确安装!")
    sys.exit(0)
else:
    print("\n❌ 部分核心依赖缺失,请运行安装脚本")
    sys.exit(1)
EOF
```

### 6. 测试 MCP 解析器

如果依赖都已安装,尝试导入解析器模块:

```bash
python3 << 'EOF'
import sys
import os

# 添加路径
sys.path.insert(0, 'mcp-servers/document-processor')

try:
    from parsers import parse_document
    print("\n✅ MCP 解析器模块加载成功!")
    print("   文档解析功能可以正常使用")
except Exception as e:
    print(f"\n❌ MCP 解析器模块加载失败: {e}")
    sys.exit(1)
EOF
```

### 7. 生成检查报告

根据检查结果,显示总结信息:

**如果全部通过**:
```
╔══════════════════════════════════════════════════╗
║  ✅ 插件安装检查通过                              ║
╚══════════════════════════════════════════════════╝

插件版本: construction-doc-assistant v1.0.2
Python 版本: 3.x.x
MCP 服务器: ✅ 可用
文档解析功能: ✅ 可用

您可以开始使用插件了!

快速开始:
  1. /construction-init      - 初始化项目配置
  2. /construction-index     - 生成文档索引
  3. /construction-help      - 查看完整帮助
```

**如果有问题**:
```
╔══════════════════════════════════════════════════╗
║  ⚠️  插件安装不完整                               ║
╚══════════════════════════════════════════════════╝

发现以下问题:
  ❌ Python 依赖未安装

解决方法:

1. 进入 MCP 服务器目录:
   cd mcp-servers/document-processor

2. 运行安装脚本:
   ./install.sh

3. 或手动安装依赖:
   pip3 install -r requirements.txt

4. 再次检查安装状态:
   /construction-check-install

详细说明请查看: INSTALL.md
```

### 8. 提供帮助链接

显示获取帮助的方式:
```
📚 文档资源:
  - 安装指南: INSTALL.md
  - 使用手册: README.md
  - GitHub: https://github.com/z1w2r3/construction-marketplace

💬 获取帮助:
  - 提交 Issue: https://github.com/z1w2r3/construction-marketplace/issues
  - 查看帮助: /construction-help
```

---

## 注意事项

1. **路径问题**: 所有检查命令都相对于插件根目录执行
2. **错误处理**: 如果某个检查失败,继续执行后续检查,最后汇总显示
3. **友好提示**: 对于每个问题,提供明确的解决方案
4. **不修改文件**: 这是只读检查命令,不会修改任何文件
