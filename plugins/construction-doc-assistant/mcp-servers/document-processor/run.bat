@echo off
REM 跨平台 MCP 服务器启动脚本 (Windows)

setlocal

REM 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"

REM 激活虚拟环境并运行服务器
if exist "%SCRIPT_DIR%venv\Scripts\activate.bat" (
    call "%SCRIPT_DIR%venv\Scripts\activate.bat"
    python "%SCRIPT_DIR%server.py"
) else (
    echo 错误: 虚拟环境不存在，请先运行 install.bat 1>&2
    exit /b 1
)
