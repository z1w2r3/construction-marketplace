# 初始化 NotebookLM 知识库

初始化智能文档助手的知识库配置，创建项目结构和配置文件。

---

你现在要帮助用户初始化一个 NotebookLM 知识库。

## 执行步骤

### 1. 收集信息

交互式询问用户以下信息:
- **知识库名称**（可选，默认使用当前目录名）
- **文档源路径**（必需，可以是单个目录或多个路径，用逗号分隔）
- **知识库用途描述**（可选，帮助 Claude 理解上下文，如"项目文档"、"研究资料"等）

### 2. 验证路径

对每个用户提供的路径，使用 Bash 工具验证:
```bash
ls -la "用户提供的路径"
```

如果路径无效，提示用户重新输入。

### 3. 创建知识库结构

使用 Bash 工具创建目录:
```bash
mkdir -p .notebooklm/{index,cache,sessions}
mkdir -p notebooklm-outputs/{summaries,insights,reports,chat-history}
```

### 4. 生成初始配置

使用 Write 工具创建 `.notebooklm/config.md`:

```markdown
# NotebookLM 知识库配置

## 基本信息
- **知识库名称**: [用户提供的名称]
- **创建时间**: [当前时间]
- **用途描述**: [用户提供的描述]

## 文档源路径
- [路径1]
- [路径2]
- ...

## 输出目录
- 摘要: `notebooklm-outputs/summaries/`
- 洞察: `notebooklm-outputs/insights/`
- 报告: `notebooklm-outputs/reports/`
- 对话历史: `notebooklm-outputs/chat-history/`

## 索引文件
- 元数据索引: `.notebooklm/index/metadata.json`
- 缓存: `.notebooklm/cache/`

## 使用建议
1. 运行 `/notebook-index` 生成文档索引
2. 使用 `/notebook-ask` 进行智能问答
3. 使用 `/notebook-report` 生成专业报告

---
*配置文件由 NotebookLM Assistant 自动生成*
```

### 5. 自动触发索引生成

配置完成后，提示用户:
```
✅ 知识库配置已完成！

正在扫描文档并生成索引...
```

然后使用 **Skill tool** 调用 `filesystem-scan` skill 扫描所有文档源路径:
- 对每个路径调用 filesystem-scan skill
- 合并所有索引结果
- 保存到 `.notebooklm/index/metadata.json`

### 6. 输出完成信息

显示初始化结果:
```
🎉 NotebookLM 知识库已就绪！

📊 文档统计:
- 总文档数: [N]
- PDF: [X] 个
- Word: [Y] 个
- Excel: [Z] 个
- PowerPoint: [W] 个
- 其他: [V] 个

📁 已创建目录:
- .notebooklm/ - 配置和索引
- notebooklm-outputs/ - 输出文件

💡 下一步操作:
- 提问: `/notebook-ask 你的问题`
- 深度研究: `/notebook-research 主题`
- 生成报告: `/notebook-report analysis "报告主题"`
- 进入对话: `/notebook-chat`

📖 帮助: `/notebook-help`
```

## 重要提示

⚠️ **只读原则**: 所有对文档源路径的访问都是只读的，绝不修改用户的原始文档。

✅ **路径处理**: 支持绝对路径和相对路径，自动转换为绝对路径存储。

🔒 **安全性**: 验证路径存在且可访问，避免访问敏感系统目录。
