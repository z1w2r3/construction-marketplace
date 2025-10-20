# MCP 服务器平台兼容性说明

## 概述

NotebookLM Assistant 插件的 MCP 服务器现已支持跨平台运行:
- ✅ macOS
- ✅ Linux
- ✅ Windows

## 启动方式

### 自动启动 (推荐)

`.mcp.json` 配置文件使用 `python` 命令直接运行服务器,无需手动选择平台:

```json
{
  "mcpServers": {
    "notebooklm-report-generator": {
      "command": "python",
      "args": ["${CLAUDE_PLUGIN_ROOT}/mcp-servers/report-generator/server.py"],
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_ROOT}/mcp-servers",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### 手动启动

如果需要手动启动 MCP 服务器进行调试,可以使用平台特定的脚本:

#### macOS / Linux

```bash
cd mcp-servers/report-generator
./run.sh
```

或:

```bash
cd mcp-servers/filesystem-indexer
./run.sh
```

#### Windows

```cmd
cd mcp-servers\report-generator
run.bat
```

或:

```cmd
cd mcp-servers\filesystem-indexer
run.bat
```

## Python 环境要求

### 所有平台

- Python 3.8 或更高版本
- pip 包管理器

### 依赖安装

所有平台使用相同的命令安装依赖:

```bash
# Report Generator
cd mcp-servers/report-generator
pip install -r requirements.txt

# Filesystem Indexer
cd mcp-servers/filesystem-indexer
pip install -r requirements.txt
```

### Windows 特别说明

**Python 命令:**
- Windows 上通常使用 `python` 而不是 `python3`
- 确保 Python 已添加到系统 PATH 环境变量

**虚拟环境:**
- Windows 虚拟环境激活脚本位于: `venv\Scripts\activate.bat`
- Unix/Linux/macOS 位于: `venv/bin/activate`

**路径分隔符:**
- Windows 使用反斜杠 `\`
- Unix/Linux/macOS 使用正斜杠 `/`
- Python 代码已使用 `os.path` 和 `pathlib.Path` 处理跨平台路径

## 故障排查

### Windows 常见问题

#### 问题 1: `python` 命令未找到

**解决方案:**
1. 确认 Python 已正确安装
2. 运行 `python --version` 检查版本
3. 如果失败,将 Python 安装目录添加到 PATH

#### 问题 2: 脚本执行策略错误

**错误信息:**
```
无法加载文件 xxx.ps1,因为在此系统上禁止运行脚本
```

**解决方案:**
```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 问题 3: 编码问题

**解决方案:**
确保控制台使用 UTF-8 编码:
```cmd
chcp 65001
```

### macOS / Linux 常见问题

#### 问题 1: 权限被拒绝

**解决方案:**
```bash
chmod +x mcp-servers/*/run.sh
```

#### 问题 2: `python3` 命令未找到

**解决方案:**
- macOS: 安装 Xcode Command Line Tools 或 Homebrew Python
- Linux: `sudo apt install python3` 或 `sudo yum install python3`

## 测试验证

在所有平台上,可以通过以下方式验证 MCP 服务器是否正常工作:

```bash
# 测试 Python 环境
python -c "import mcp; print('MCP SDK installed')"

# 测试服务器启动
cd mcp-servers/report-generator
python server.py
# 应该看到: "启动 NotebookLM Report Generator MCP Server..."
# 使用 Ctrl+C 停止

# 在 Claude Code 中验证
# 重启 Claude Code,检查 MCP 服务器状态应为 "running"
```

## 更新日志

### 2025-10-20
- ✅ 修复 `server.py` 中文引号语法错误
- ✅ 添加 Windows 批处理启动脚本 (`run.bat`)
- ✅ 更新 `.mcp.json` 使用跨平台 `python` 命令
- ✅ 安装缺失的 `reportlab` 依赖
- ✅ 创建平台兼容性文档

## 贡献指南

在开发新的 MCP 工具时,请遵循以下跨平台最佳实践:

1. **路径处理**: 使用 `pathlib.Path` 或 `os.path`
2. **命令行参数**: 避免依赖特定 shell 语法
3. **编码**: 显式使用 UTF-8 编码
4. **环境变量**: 使用 `os.environ` 访问
5. **测试**: 在多个平台上测试代码

## 参考资料

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [Claude Code 插件开发指南](https://docs.claude.com/claude-code)
- [Python 跨平台最佳实践](https://docs.python.org/3/library/os.html)
