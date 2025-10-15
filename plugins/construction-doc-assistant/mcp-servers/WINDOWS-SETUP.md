# Windows 用户安装指南

## 快速开始 (3 步完成)

### 1. 安装 Python 依赖

打开 **命令提示符** 或 **PowerShell**,执行:

```powershell
cd %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers\document-processor
install.bat
```

或直接在文件资源管理器中双击 `install.bat`。

### 2. 配置 MCP 服务器

```powershell
cd %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers
setup-windows.bat
```

这个脚本会自动:
- 备份原配置文件
- 将 `run.sh` 替换为 `run.bat`
- 显示修改结果

### 3. 重启 VSCode

```
Ctrl + Shift + P → 输入 "Reload Window" → 回车
```

---

## 验证安装

重启后,运行任意插件命令(如 `/construction-help`),应该看到 MCP 服务器正常工作。

检查 MCP 状态:
```
/debug mcp
```

应显示:
```
✓ construction-doc-processor: running
```

---

## 原理说明

### 为什么 Windows 需要额外配置?

Windows 和 Unix 系统的脚本扩展名不同:
- **Unix/macOS**: `.sh` 脚本
- **Windows**: `.bat` 脚本

默认配置使用 `run.sh`,在 Windows 下不可执行。

### `setup-windows.bat` 做了什么?

自动修改 `.mcp.json` 配置文件:

**修改前:**
```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/mcp-servers/document-processor/run.sh"
}
```

**修改后:**
```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/mcp-servers/document-processor/run.bat"
}
```

---

## 常见问题

### Q1: `install.bat` 提示 "未找到 Python"

**解决方案:**
1. 下载并安装 Python 3.8+: https://www.python.org/downloads/
2. 安装时**务必勾选** "Add Python to PATH"
3. 重新打开命令提示符,再次运行 `install.bat`

### Q2: `setup-windows.bat` 提示 "找不到 PowerShell"

**解决方案:**

使用手动方式修改配置:

1. 用记事本打开文件:
   ```
   %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers\.mcp.json
   ```

2. 找到第 4 行,将:
   ```json
   "command": "${CLAUDE_PLUGIN_ROOT}/mcp-servers/document-processor/run.sh",
   ```

   改为:
   ```json
   "command": "${CLAUDE_PLUGIN_ROOT}/mcp-servers/document-processor/run.bat",
   ```

3. 保存并重启 VSCode

### Q3: MCP 服务器显示 "failed"

**排查步骤:**

1. **检查虚拟环境是否存在**:
   ```powershell
   dir %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers\document-processor\venv
   ```

   如果不存在,重新运行:
   ```powershell
   cd %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers\document-processor
   install.bat
   ```

2. **手动测试启动脚本**:
   ```powershell
   cd %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers\document-processor
   run.bat
   ```

   查看具体错误信息

3. **检查依赖是否完整**:
   ```powershell
   venv\Scripts\pip.exe list
   ```

   应包含: `mcp`, `python-docx`, `openpyxl`, `PyPDF2`, `pdfplumber` 等

### Q4: 路径包含空格或中文

通常不会有问题,因为:
- `run.bat` 脚本已正确处理路径引号
- `${CLAUDE_PLUGIN_ROOT}` 由 Claude Code 自动展开

如果仍有问题,建议:
1. 避免在用户名或安装路径中使用空格和特殊字符
2. 使用默认安装路径

---

## 卸载

如需卸载插件:

```powershell
# 删除虚拟环境
cd %USERPROFILE%\.claude\plugins\marketplaces\construction-marketplace\plugins\construction-doc-assistant\mcp-servers\document-processor
rmdir /s /q venv

# 在 Claude Code 中卸载插件
/plugin uninstall construction-doc-assistant
```

---

## 文件说明

| 文件 | 作用 |
|------|------|
| `install.bat` | 安装 Python 依赖到虚拟环境 |
| `run.bat` | 启动 MCP 服务器(自动激活虚拟环境) |
| `setup-windows.bat` | 自动配置 .mcp.json 文件 |
| `.mcp.json` | MCP 服务器配置文件 |

---

## 技术支持

遇到问题?请提供以下信息:

1. Windows 版本: 运行 `winver`
2. Python 版本: 运行 `python --version`
3. 错误截图或日志
4. 配置文件内容

提交 Issue: https://github.com/z1w2r3/construction-marketplace/issues
