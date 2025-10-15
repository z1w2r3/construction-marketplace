#!/usr/bin/env bash
# 跨平台 MCP 服务器启动脚本 (Unix/macOS)

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 激活虚拟环境并运行服务器
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
    exec python "$SCRIPT_DIR/server.py"
else
    echo "错误: 虚拟环境不存在,请先运行 install.sh" >&2
    exit 1
fi
