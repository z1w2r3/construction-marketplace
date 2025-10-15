@echo off
REM ========================================
REM Windows 自动配置脚本
REM 功能: 自动修改 .mcp.json 使用 Windows 路径
REM ========================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   建筑文档助手 - Windows 自动配置
echo ========================================
echo.

REM 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM 检查 .mcp.json 是否存在
if not exist ".mcp.json" (
    echo [错误] 找不到 .mcp.json 文件
    echo 当前目录: %CD%
    pause
    exit /b 1
)

echo [信息] 找到配置文件: .mcp.json
echo.

REM 备份原配置
if not exist ".mcp.json.backup" (
    echo [信息] 创建备份: .mcp.json.backup
    copy /y .mcp.json .mcp.json.backup >nul
) else (
    echo [信息] 备份文件已存在,跳过备份
)

REM 修改配置文件:将 run.sh 改为 run.bat
echo [信息] 修改配置文件...

powershell -Command "(Get-Content .mcp.json) -replace 'run\.sh', 'run.bat' | Set-Content .mcp.json"

if errorlevel 1 (
    echo [错误] 配置修改失败
    pause
    exit /b 1
)

echo [成功] 配置已更新
echo.

REM 显示修改后的配置
echo ----------------------------------------
echo 修改后的配置:
echo ----------------------------------------
type .mcp.json
echo ----------------------------------------
echo.

echo ========================================
echo   ✓ 配置完成!
echo ========================================
echo.
echo [下一步] 请重启 VSCode 或 Claude Code:
echo    Ctrl + Shift + P → "Reload Window"
echo.
pause
