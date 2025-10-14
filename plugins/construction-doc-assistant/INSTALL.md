# 安装指南

本插件包含 Python MCP 服务器,需要安装 Python 依赖才能正常工作。

## 自动安装(推荐)

Claude Code 在安装插件时会自动提示运行安装脚本:

```bash
# 安装插件
claude marketplace install construction-doc-assistant

# 按提示运行安装脚本
cd ~/.claude/plugins/construction-doc-assistant/mcp-servers/document-processor
./install.sh
```

## 手动安装

如果自动安装失败,可以手动安装:

### 1. 进入MCP服务器目录

```bash
cd ~/.claude/plugins/construction-doc-assistant/mcp-servers/document-processor
```

或者本地开发时:

```bash
cd /path/to/construction-marketplace/plugins/construction-doc-assistant/mcp-servers/document-processor
```

### 2. 运行安装脚本

```bash
./install.sh
```

该脚本会:
- ✅ 检测 Python 版本 (需要 ≥3.8)
- ✅ 询问是否创建虚拟环境(推荐)
- ✅ 安装所有 Python 依赖
- ✅ 验证安装是否成功

### 3. 或者直接安装依赖

```bash
pip3 install -r requirements.txt
```

### 4. 验证安装

```bash
python3 -c "
import mcp
import docx
import openpyxl
import PyPDF2
import pptx
print('✅ 所有依赖已正确安装')
"
```

## 依赖列表

### 核心依赖(必需)

```txt
mcp>=1.0.0                  # MCP SDK
python-docx>=1.1.0          # Word 文档解析
openpyxl>=3.1.0             # Excel 文档解析
PyPDF2>=3.0.0               # PDF 文档解析
python-pptx>=1.0.2          # PowerPoint 文档解析
```

### 可选依赖(增强功能)

```txt
pdfplumber>=0.10.0          # PDF 表格提取
pandas>=2.0.0               # 数据分析
python-magic>=0.4.27        # MIME 类型检测
```

### 系统依赖

**macOS:**
```bash
brew install libmagic
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install libmagic1
```

**Windows:**
- 通常不需要额外的系统依赖
- python-magic 可能需要额外配置

## 常见问题

### Q1: Python 版本不符合要求

**错误**: `Python 3.8 or higher is required`

**解决**:
```bash
# 安装 Python 3.8+
# macOS:
brew install python@3.12

# Ubuntu/Debian:
sudo apt-get install python3.12
```

### Q2: pip 安装失败

**错误**: `pip install failed`

**解决**:
```bash
# 升级 pip
python3 -m pip install --upgrade pip

# 使用国内镜像(中国用户)
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: PyPDF2 导入错误

**错误**: `ModuleNotFoundError: No module named 'PyPDF2'`

**解决**:
```bash
pip3 install PyPDF2
```

### Q4: libmagic 未找到

**错误**: `libmagic not found`

**解决**:
```bash
# macOS
brew install libmagic

# Linux
sudo apt-get install libmagic1

# python-magic 是可选依赖,不影响核心功能
```

### Q5: 虚拟环境问题

如果使用虚拟环境,每次使用前需要激活:

```bash
cd ~/.claude/plugins/construction-doc-assistant/mcp-servers/document-processor
source venv/bin/activate
```

**或者**不使用虚拟环境,直接全局安装依赖。

## 验证安装

安装完成后,测试 MCP 服务器:

```bash
cd mcp-servers/document-processor

# 测试模块导入
python3 -c "
from parsers import parse_document
print('✅ MCP 服务器可以正常导入')
"

# 测试文档解析(需要提供实际文件路径)
python3 << 'EOF'
from parsers import parse_document

# 替换为实际的文档路径
result = parse_document('/path/to/your/document.docx')
print(f"状态: {result['status']}")
if result['status'] == 'success':
    print(f"文件: {result['file_info']['name']}")
    print('✅ 文档解析功能正常')
EOF
```

## 卸载

如果需要卸载插件:

```bash
# 卸载插件
claude marketplace uninstall construction-doc-assistant

# 如果使用了虚拟环境,可以删除虚拟环境目录
rm -rf ~/.claude/plugins/construction-doc-assistant/mcp-servers/document-processor/venv
```

## 更新

插件更新时,需要重新运行安装脚本:

```bash
# 更新插件
claude marketplace upgrade construction-doc-assistant

# 重新安装依赖
cd ~/.claude/plugins/construction-doc-assistant/mcp-servers/document-processor
./install.sh
```

## 获取帮助

如果遇到其他问题:

1. 查看日志: `~/.claude/logs/`
2. 提交 Issue: https://github.com/z1w2r3/construction-marketplace/issues
3. 查看文档: https://github.com/z1w2r3/construction-marketplace

---

**注意**: Python 依赖安装是**必需的**,否则文档解析功能将无法工作。
