#!/bin/bash
# NotebookLM Report Generator MCP Server 启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 激活虚拟环境（如果存在）
if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# 运行 MCP 服务器
exec python3 "$SCRIPT_DIR/server.py"
