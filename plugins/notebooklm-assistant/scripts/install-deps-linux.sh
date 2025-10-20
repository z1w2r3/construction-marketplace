#!/bin/bash
# NotebookLM Assistant 依赖安装脚本 (Linux - Ubuntu/Debian)
# 自动检测并安装所有必需和可选依赖

set -e

echo "🚀 开始安装 NotebookLM Assistant 依赖..."
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检测 Linux 发行版
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo -e "${RED}❌ 无法检测 Linux 发行版${NC}"
    exit 1
fi

# 更新包管理器
echo -e "${BLUE}[1/6] 更新包管理器...${NC}"
if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]]; then
    sudo apt-get update -qq
    echo -e "${GREEN}✅ 包管理器已更新${NC}"
elif [[ "$OS" == "centos" ]] || [[ "$OS" == "rhel" ]] || [[ "$OS" == "fedora" ]]; then
    sudo yum update -y -q
    echo -e "${GREEN}✅ 包管理器已更新${NC}"
else
    echo -e "${YELLOW}⚠️  未知的 Linux 发行版: $OS${NC}"
    echo "请手动安装以下依赖: python3, pip, pandoc"
    exit 1
fi
echo ""

# 检查并安装 Python
echo -e "${BLUE}[2/6] 检查 Python 3...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python 3 未安装,正在安装...${NC}"
    if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]]; then
        sudo apt-get install -y -qq python3 python3-pip
    else
        sudo yum install -y -q python3 python3-pip
    fi
    echo -e "${GREEN}✅ Python 3 安装完成${NC}"
else
    echo -e "${GREEN}✅ Python 3 已安装: $(python3 --version)${NC}"
fi
echo ""

# 检查并安装 Pandoc
echo -e "${BLUE}[3/6] 检查 Pandoc (必需)...${NC}"
if ! command -v pandoc &> /dev/null; then
    echo -e "${YELLOW}⚠️  Pandoc 未安装,正在安装...${NC}"
    if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]]; then
        sudo apt-get install -y -qq pandoc
    else
        sudo yum install -y -q pandoc
    fi
    echo -e "${GREEN}✅ Pandoc 安装完成${NC}"
else
    echo -e "${GREEN}✅ Pandoc 已安装: $(pandoc --version | head -1)${NC}"
fi
echo ""

# 检查并安装 LibreOffice
echo -e "${BLUE}[4/6] 检查 LibreOffice (可选,用于 PDF 转换)...${NC}"
if ! command -v soffice &> /dev/null; then
    read -p "是否安装 LibreOffice? (y/n, 默认 y): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
        echo -e "${YELLOW}⚠️  正在安装 LibreOffice...${NC}"
        if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]]; then
            sudo apt-get install -y -qq libreoffice
        else
            sudo yum install -y -q libreoffice
        fi
        echo -e "${GREEN}✅ LibreOffice 安装完成${NC}"
    else
        echo -e "${YELLOW}⏭  跳过 LibreOffice 安装${NC}"
    fi
else
    echo -e "${GREEN}✅ LibreOffice 已安装${NC}"
fi
echo ""

# 检查并安装 Poppler
echo -e "${BLUE}[5/6] 检查 Poppler (可选,用于 PDF 图像转换)...${NC}"
if ! command -v pdftoppm &> /dev/null; then
    read -p "是否安装 Poppler? (y/n, 默认 y): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
        echo -e "${YELLOW}⚠️  正在安装 Poppler...${NC}"
        if [[ "$OS" == "ubuntu" ]] || [[ "$OS" == "debian" ]]; then
            sudo apt-get install -y -qq poppler-utils
        else
            sudo yum install -y -q poppler-utils
        fi
        echo -e "${GREEN}✅ Poppler 安装完成${NC}"
    else
        echo -e "${YELLOW}⏭  跳过 Poppler 安装${NC}"
    fi
else
    echo -e "${GREEN}✅ Poppler 已安装${NC}"
fi
echo ""

# 安装 Python MCP 服务器依赖
echo -e "${BLUE}[6/6] 安装 Python MCP 服务器依赖...${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(dirname "$SCRIPT_DIR")"

# 安装 report-generator 依赖
if [ -f "$PLUGIN_ROOT/mcp-servers/report-generator/requirements.txt" ]; then
    echo "  安装 report-generator 依赖..."
    pip3 install -q -r "$PLUGIN_ROOT/mcp-servers/report-generator/requirements.txt"
    echo -e "${GREEN}  ✅ Report Generator 依赖已安装${NC}"
else
    echo -e "${RED}  ❌ 未找到 report-generator/requirements.txt${NC}"
fi

# 安装 filesystem-indexer 依赖
if [ -f "$PLUGIN_ROOT/mcp-servers/filesystem-indexer/requirements.txt" ]; then
    echo "  安装 filesystem-indexer 依赖..."
    pip3 install -q -r "$PLUGIN_ROOT/mcp-servers/filesystem-indexer/requirements.txt"
    echo -e "${GREEN}  ✅ Filesystem Indexer 依赖已安装${NC}"
else
    echo -e "${RED}  ❌ 未找到 filesystem-indexer/requirements.txt${NC}"
fi
echo ""

# 完成
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 所有依赖安装完成!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "下一步:"
echo "  1. 重启 Claude Code"
echo "  2. 运行 /help skills 验证插件加载"
echo "  3. 尝试使用文档处理功能"
echo ""
echo "如有问题,请查看: $PLUGIN_ROOT/INSTALL.md"
echo ""
