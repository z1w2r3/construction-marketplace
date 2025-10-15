@echo off
REM MCP 服务器启动脚本 - Windows
REM 自动激活虚拟环境并运行服务器

setlocal

REM 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"

REM 激活虚拟环境
if exist "%SCRIPT_DIR%venv\Scripts\activate.bat" (
    call "%SCRIPT_DIR%venv\Scripts\activate.bat"
    REM 使用 -u 确保输出不缓冲(重要: MCP 需要实时输出)
    python -u "%SCRIPT_DIR%server.py"
) else (
    echo [ERROR] 虚拟环境不存在 1>&2
    echo [ERROR] 请先运行: cd /d "%SCRIPT_DIR%" ^&^& install.bat 1>&2
    exit /b 1
)
