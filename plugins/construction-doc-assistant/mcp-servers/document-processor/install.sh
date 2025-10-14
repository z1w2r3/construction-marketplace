#!/bin/bash
# ============================================
# 建筑文档处理 MCP 服务器 - 依赖安装脚本
# ============================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  建筑文档处理 MCP 服务器 - 安装${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 1. 检测 Python 版本
echo -e "${YELLOW}[1/6]${NC} 检测 Python 版本..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误: 未找到 python3${NC}"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

python_version=$(python3 --version 2>&1 | awk '{print $2}')
python_major=$(echo "$python_version" | cut -d. -f1)
python_minor=$(echo "$python_version" | cut -d. -f2)

echo -e "${GREEN}✓${NC} 检测到 Python 版本: $python_version"

if [[ "$python_major" -lt 3 ]] || [[ "$python_major" -eq 3 && "$python_minor" -lt 8 ]]; then
    echo -e "${RED}❌ 错误: 需要 Python 3.8 或更高版本${NC}"
    echo "当前版本: $python_version"
    exit 1
fi

# 2. 询问是否创建虚拟环境
echo ""
echo -e "${YELLOW}[2/6]${NC} 虚拟环境配置..."
read -p "是否创建 Python 虚拟环境? (推荐) [y/N]: " create_venv

if [[ "$create_venv" =~ ^[Yy]$ ]]; then
    echo "创建虚拟环境..."
    python3 -m venv venv

    # 激活虚拟环境
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi

    echo -e "${GREEN}✓${NC} 虚拟环境已创建并激活"
    echo -e "${BLUE}提示:${NC} 下次使用前请运行: source venv/bin/activate"
else
    echo "跳过虚拟环境创建"
fi

# 3. 升级 pip
echo ""
echo -e "${YELLOW}[3/6]${NC} 升级 pip..."
python3 -m pip install --upgrade pip --quiet
echo -e "${GREEN}✓${NC} pip 已升级到最新版本"

# 4. 安装核心依赖
echo ""
echo -e "${YELLOW}[4/6]${NC} 安装核心依赖包..."
echo "这可能需要几分钟时间，请耐心等待..."

if python3 -m pip install -r requirements.txt; then
    echo -e "${GREEN}✓${NC} 核心依赖安装成功"
else
    echo -e "${RED}❌ 核心依赖安装失败${NC}"
    echo "请检查网络连接或手动运行: pip install -r requirements.txt"
    exit 1
fi

# 5. 安装系统依赖 (macOS)
echo ""
echo -e "${YELLOW}[5/6]${NC} 检查系统依赖..."

if [[ "$OSTYPE" == "darwin"* ]]; then
    if command -v brew &> /dev/null; then
        echo "检测到 Homebrew，安装 libmagic..."
        brew install libmagic 2>/dev/null || echo "libmagic 可能已安装"
        echo -e "${GREEN}✓${NC} 系统依赖检查完成"
    else
        echo -e "${YELLOW}⚠${NC}  未检测到 Homebrew"
        echo "python-magic 可能无法正常工作"
        echo "建议安装 Homebrew: https://brew.sh"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux 系统检测到"
    echo "如需 python-magic，请手动安装: sudo apt-get install libmagic1"
else
    echo "Windows 系统检测到"
    echo "python-magic 在 Windows 上可能需要额外配置"
fi

# 6. 验证安装
echo ""
echo -e "${YELLOW}[6/6]${NC} 验证安装..."

python3 << 'PYEOF'
import sys

# 必需的包
required_packages = {
    'mcp': 'MCP SDK',
    'docx': 'python-docx (Word)',
    'openpyxl': 'openpyxl (Excel)',
    'pptx': 'python-pptx (PowerPoint)',
    'PyPDF2': 'PyPDF2 (PDF)'
}

# 可选的包
optional_packages = {
    'pdfplumber': 'pdfplumber (PDF 表格提取)',
    'pandas': 'pandas (数据分析)',
    'magic': 'python-magic (MIME 检测)'
}

print("\n核心包验证:")
all_required_ok = True
for module, name in required_packages.items():
    try:
        __import__(module)
        print(f"  ✓ {name}")
    except ImportError:
        print(f"  ✗ {name} - 缺失")
        all_required_ok = False

print("\n可选包验证:")
for module, name in optional_packages.items():
    try:
        __import__(module)
        print(f"  ✓ {name}")
    except ImportError:
        print(f"  ○ {name} - 未安装(可选)")

if not all_required_ok:
    print("\n❌ 核心包安装不完整")
    sys.exit(1)
else:
    print("\n✓ 所有核心包已正确安装")
PYEOF

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  ✓ 安装成功!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "下一步操作:"
    echo "  1. 测试服务器: python3 server.py"
    echo "  2. 查看文档: cat README.md"
    echo ""
    if [[ "$create_venv" =~ ^[Yy]$ ]]; then
        echo "提示: 下次使用前请激活虚拟环境:"
        echo "  source venv/bin/activate"
        echo ""
    fi
else
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}  ✗ 安装失败${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo "请检查上方的错误信息，或手动运行:"
    echo "  pip install -r requirements.txt"
    exit 1
fi
