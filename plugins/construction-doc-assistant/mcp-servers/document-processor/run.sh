#!/usr/bin/env bash
# MCP 服务器启动脚本 - Unix/macOS
# 自动激活虚拟环境并运行服务器

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 激活虚拟环境
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
    # 使用 -u 确保输出不缓冲(重要: MCP 需要实时输出)
    exec python -u "$SCRIPT_DIR/server.py"
else
    echo "[ERROR] 虚拟环境不存在" >&2
    echo "[ERROR] 请先运行: cd '$SCRIPT_DIR' && ./install.sh" >&2
    exit 1
fi
