@echo off
REM NotebookLM Report Generator MCP Server 启动脚本 (Windows)

SET SCRIPT_DIR=%~dp0

REM 激活虚拟环境(如果存在)
IF EXIST "%SCRIPT_DIR%venv\Scripts\activate.bat" (
    CALL "%SCRIPT_DIR%venv\Scripts\activate.bat"
)

REM 运行 MCP 服务器
python "%SCRIPT_DIR%server.py"
