@echo off
REM ========================================
REM 建筑文档处理 MCP 服务器 - Windows 安装脚本
REM ========================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   建筑文档处理 MCP 服务器安装
echo   Windows 版本
echo ========================================
echo.

REM 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python
    echo 请先安装 Python 3.8 或更高版本: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 显示 Python 版本
echo [信息] 检测到 Python 版本:
python --version
echo.

REM 检查虚拟环境是否存在
if exist "venv\" (
    echo [警告] 虚拟环境已存在
    set /p RECREATE="是否重新创建? (y/N): "
    if /i "!RECREATE!"=="y" (
        echo [信息] 删除旧虚拟环境...
        rmdir /s /q venv
    ) else (
        echo [信息] 使用现有虚拟环境
        goto :install_deps
    )
)

REM 创建虚拟环境
echo [信息] 创建虚拟环境...
python -m venv venv
if errorlevel 1 (
    echo [错误] 虚拟环境创建失败
    pause
    exit /b 1
)
echo [成功] 虚拟环境创建完成
echo.

:install_deps
REM 激活虚拟环境
echo [信息] 激活虚拟环境...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [错误] 虚拟环境激活失败
    pause
    exit /b 1
)

REM 升级 pip
echo [信息] 升级 pip...
python -m pip install --upgrade pip --quiet

REM 安装依赖
echo [信息] 安装依赖包...
echo 这可能需要几分钟时间，请耐心等待...
echo.

pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✓ 安装成功!
echo ========================================
echo.
echo [下一步] 请手动配置 MCP 服务器:
echo.
echo 1. 找到文件:
echo    %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers\.mcp.json
echo.
echo 2. 将 "command" 字段修改为:
echo    "${CLAUDE_PLUGIN_ROOT}/mcp-servers/document-processor/venv/Scripts/python.exe"
echo.
echo 或者复制 .mcp.windows.json 覆盖 .mcp.json
echo.
echo 3. 重启 VSCode 或 Claude Code
echo.
pause
