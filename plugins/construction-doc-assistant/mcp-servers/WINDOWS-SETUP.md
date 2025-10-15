# Windows 用户安装指南

## 问题说明

在 Windows 系统下,Python 虚拟环境的路径与 Unix/macOS 不同:

- **Unix/macOS**: `venv/bin/python`
- **Windows**: `venv\Scripts\python.exe`

因此需要手动修改 MCP 配置文件。

---

## 安装步骤

### 1. 运行 Windows 安装脚本

在插件安装目录下,找到并运行 `install.bat`:

```powershell
# 方式 1: 使用命令提示符
cd %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers\document-processor
install.bat

# 方式 2: 使用 PowerShell
cd $env:USERPROFILE\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers\document-processor
.\install.bat
```

或者直接双击文件管理器中的 `install.bat`。

### 2. 修改 MCP 配置文件

**方式 A: 使用预配置文件 (推荐)**

```powershell
# 进入 MCP 配置目录
cd %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers

# 备份原配置
copy .mcp.json .mcp.json.backup

# 使用 Windows 配置
copy .mcp.windows.json .mcp.json
```

**方式 B: 手动修改**

编辑文件:
```
%USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers\.mcp.json
```

将第 4 行的 `command` 字段从:
```json
"command": "${CLAUDE_PLUGIN_ROOT}/mcp-servers/document-processor/venv/bin/python",
```

改为:
```json
"command": "${CLAUDE_PLUGIN_ROOT}/mcp-servers/document-processor/venv/Scripts/python.exe",
```

### 3. 验证配置

检查修改后的配置文件:

```powershell
type %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers\.mcp.json
```

应该看到:
```json
{
  "mcpServers": {
    "construction-doc-processor": {
      "command": "${CLAUDE_PLUGIN_ROOT}/mcp-servers/document-processor/venv/Scripts/python.exe",
      ...
    }
  }
}
```

### 4. 重启 VSCode

```
Ctrl + Shift + P → 输入 "Reload Window" → 回车
```

### 5. 验证 MCP 服务器状态

重启后,在 Claude Code 中查看 MCP 状态:

```
/debug mcp
```

应该显示:
```
✓ construction-doc-processor: running
```

---

## 常见问题

### Q1: install.bat 提示 "未找到 Python"

**解决方案**:
1. 安装 Python 3.8+: https://www.python.org/downloads/
2. 安装时勾选 "Add Python to PATH"
3. 重新打开命令提示符

### Q2: MCP 服务器状态显示 "failed"

**排查步骤**:

1. **检查虚拟环境是否存在**:
   ```powershell
   dir %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers\document-processor\venv\Scripts\python.exe
   ```

   如果不存在,重新运行 `install.bat`

2. **手动测试 Python 脚本**:
   ```powershell
   cd %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers\document-processor
   venv\Scripts\python.exe server.py
   ```

   查看错误信息

3. **检查依赖是否安装完整**:
   ```powershell
   venv\Scripts\pip.exe list
   ```

   应该包含: mcp, python-docx, openpyxl, PyPDF2, pdfplumber 等

### Q3: 路径中包含空格或中文

如果路径包含空格或中文字符,需要确保:

1. Python 和 pip 正确安装
2. 使用引号包裹路径:
   ```json
   "command": "\"${CLAUDE_PLUGIN_ROOT}/mcp-servers/document-processor/venv/Scripts/python.exe\""
   ```

---

## 卸载

如需卸载,只需删除虚拟环境:

```powershell
cd %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers\document-processor
rmdir /s /q venv
```

---

## 技术支持

如果遇到其他问题,请提供以下信息:

1. Windows 版本: `winver`
2. Python 版本: `python --version`
3. 完整错误日志
4. MCP 配置文件内容

提交 Issue: https://github.com/z1w2r3/construction-marketplace/issues
