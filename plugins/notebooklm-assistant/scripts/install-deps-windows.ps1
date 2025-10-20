# NotebookLM Assistant 依赖安装脚本 (Windows PowerShell)
# 自动检测并安装所有必需和可选依赖

Write-Host "🚀 开始安装 NotebookLM Assistant 依赖..." -ForegroundColor Cyan
Write-Host ""

# 检查是否以管理员身份运行
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  警告: 建议以管理员身份运行此脚本" -ForegroundColor Yellow
    Write-Host "某些安装可能需要管理员权限" -ForegroundColor Yellow
    Write-Host ""
}

# 检查 Python
Write-Host "[1/5] 检查 Python 3..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python 已安装: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python 未安装" -ForegroundColor Red
    Write-Host "请访问 https://www.python.org/downloads/ 下载并安装 Python 3.8+" -ForegroundColor Yellow
    Write-Host "安装时请勾选 'Add Python to PATH'" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "是否继续安装其他依赖? (y/n)"
    if ($continue -ne 'y') {
        exit 1
    }
}
Write-Host ""

# 检查 pip
Write-Host "[2/5] 检查 pip..." -ForegroundColor Blue
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✅ pip 已安装: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip 未安装" -ForegroundColor Red
    Write-Host "通常 pip 会随 Python 一起安装,请检查 Python 安装" -ForegroundColor Yellow
}
Write-Host ""

# 检查 Pandoc
Write-Host "[3/5] 检查 Pandoc (必需)..." -ForegroundColor Blue
try {
    $pandocVersion = pandoc --version 2>&1 | Select-Object -First 1
    Write-Host "✅ Pandoc 已安装: $pandocVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Pandoc 未安装" -ForegroundColor Red
    Write-Host ""
    Write-Host "请按以下步骤安装 Pandoc:" -ForegroundColor Yellow
    Write-Host "1. 访问: https://pandoc.org/installing.html" -ForegroundColor Yellow
    Write-Host "2. 下载 Windows installer (.msi)" -ForegroundColor Yellow
    Write-Host "3. 运行安装程序" -ForegroundColor Yellow
    Write-Host "4. 重新打开 PowerShell 使 PATH 生效" -ForegroundColor Yellow
    Write-Host ""

    $openBrowser = Read-Host "是否打开 Pandoc 下载页面? (y/n)"
    if ($openBrowser -eq 'y') {
        Start-Process "https://pandoc.org/installing.html"
    }
}
Write-Host ""

# 检查 LibreOffice (可选)
Write-Host "[4/5] 检查 LibreOffice (可选,用于 PDF 转换)..." -ForegroundColor Blue
$libreOfficePath = "C:\Program Files\LibreOffice\program\soffice.exe"
if (Test-Path $libreOfficePath) {
    Write-Host "✅ LibreOffice 已安装" -ForegroundColor Green
} else {
    Write-Host "⚠️  LibreOffice 未安装" -ForegroundColor Yellow
    $installLibre = Read-Host "是否安装 LibreOffice? (y/n, 默认 n)"
    if ($installLibre -eq 'y') {
        Write-Host "请访问: https://www.libreoffice.org/download/" -ForegroundColor Yellow
        Start-Process "https://www.libreoffice.org/download/"
    } else {
        Write-Host "⏭  跳过 LibreOffice 安装" -ForegroundColor Yellow
    }
}
Write-Host ""

# 安装 Python MCP 服务器依赖
Write-Host "[5/5] 安装 Python MCP 服务器依赖..." -ForegroundColor Blue

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pluginRoot = Split-Path -Parent $scriptDir

# 安装 report-generator 依赖
$reportGenReq = Join-Path $pluginRoot "mcp-servers\report-generator\requirements.txt"
if (Test-Path $reportGenReq) {
    Write-Host "  安装 report-generator 依赖..." -ForegroundColor Gray
    pip install -q -r $reportGenReq
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Report Generator 依赖已安装" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Report Generator 依赖安装失败" -ForegroundColor Red
    }
} else {
    Write-Host "  ❌ 未找到 report-generator\requirements.txt" -ForegroundColor Red
}

# 安装 filesystem-indexer 依赖
$fsIndexerReq = Join-Path $pluginRoot "mcp-servers\filesystem-indexer\requirements.txt"
if (Test-Path $fsIndexerReq) {
    Write-Host "  安装 filesystem-indexer 依赖..." -ForegroundColor Gray
    pip install -q -r $fsIndexerReq
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Filesystem Indexer 依赖已安装" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Filesystem Indexer 依赖安装失败" -ForegroundColor Red
    }
} else {
    Write-Host "  ❌ 未找到 filesystem-indexer\requirements.txt" -ForegroundColor Red
}
Write-Host ""

# 完成
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host "🎉 依赖安装完成!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host ""
Write-Host "下一步:" -ForegroundColor Cyan
Write-Host "  1. 如果安装了新的软件,请重新打开 PowerShell 使 PATH 生效" -ForegroundColor White
Write-Host "  2. 重启 Claude Code" -ForegroundColor White
Write-Host "  3. 运行 /help skills 验证插件加载" -ForegroundColor White
Write-Host "  4. 尝试使用文档处理功能" -ForegroundColor White
Write-Host ""
$installMdPath = Join-Path $pluginRoot "INSTALL.md"
Write-Host "如有问题,请查看: $installMdPath" -ForegroundColor Gray
Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
