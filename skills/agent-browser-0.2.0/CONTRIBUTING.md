# 提高代理浏览器技能

此技能包含代理浏览器 CLI。在报告问题之前确定问题所在。

## 问题报告指南

### 在此存储库中打开一个问题，如果

- 技能文档不清楚或缺失
- SKILL.md 中的示例不起作用
- 您需要使用带有此技能包装器的 CLI 的帮助
- 该技能缺少命令或功能

### 在代理浏览器存储库中打开一个问题，如果

- CLI 崩溃或抛出错误
- 命令的行为与记录的不符
- 您发现浏览器自动化中存在错误
- 您需要 CLI 中的新功能

## 在提出问题之前

1.安装最新版本
```bash
   npm install -g agent-browser@latest
   ```

2. 在终端中测试命令以隔离问题

## 问题报告模板

使用此模板提供必要的信息。

```markdown
### Description
[Provide a clear and concise description of the bug]

### Reproduction Steps
1. [First Step]
2. [Second Step]
3. [Observe error]

### Expected Behavior
[Describe what you expected to happen]

### Environment Details
- **Skill Version:** [e.g. 1.0.2]
- **agent-browser Version:** [output of agent-browser --version]
- **Node.js Version:** [output of node -v]
- **Operating System:** [e.g. macOS Sonoma, Windows 11, Ubuntu 22.04]

### Additional Context
- [Full error output or stack trace]
- [Screenshots]
- [Website URLs where the failure occurred]
```

## 添加新命令到技能中

当上游 CLI 添加新命令时更新 SKILL.md。
- 保留安装部分
- 在正确的类别中添加新命令
- 包括使用示例
