# Claude Code CLI 终极配置合集 🚀

这是一个高度定制化的 Claude Code CLI 配置文件库，集成了高级规则 (Rules)、自动化钩子 (Hooks)、增强技能 (Skills) 以及优化的 `settings.json`。通过使用这些配置，你可以将你的 Claude Code CLI 从一个基础的辅助工具升级为一个具备自我管理、强力审查和全中文交互能力的顶级 AI 编程代理。

## 🌟 核心功能

### 1. 自动汉化与全中文交互 (CRITICAL)
- **强制中文回复**：所有任务进度、工具输出和最终回复均使用简体中文，消除了语言障碍。
- **自动汉化意识**：内置指令让 Claude 在安装新插件时优先进行汉化处理。

### 2. 强大的钩子系统 (Hooks)
- **SessionStart**: 自动检查更新并同步会话状态。
- **PreToolUse**: 
  - **安全性防护**：在执行写入操作前进行 Prompt 注入检查和读取保护。
  - **工作流守卫**：确保操作符合预定的开发流程。
- **PostToolUse**:
  - **上下文监控**：实时监控 Token 使用情况和上下文窗口，防止性能下降。
  - **阶段性同步**：在任务的关键节点自动记录进度。
- **StatusLine**: 定制的实时状态栏显示，让你随时掌握 AI 的运行状态。

### 3. 系统级开发规则 (Rules)
- **TDD 强制执行**：默认开启测试驱动开发模式，确保代码覆盖率 ≥ 80%。
- **安全审查**：对身份验证、数据处理等敏感操作进行强制性的安全检查。
- **代码风格守卫**：强制不可变模式，追求极致的代码简洁性与可维护性。
- **多代理协作**：内置了 `planner`, `architect`, `code-reviewer` 等多种代理的编排逻辑，支持并行任务处理。

### 4. 丰富的增强技能 (Skills)
集成了来自社区和官方的顶级技能插件，包括但不限于：
- `ecc`: Everything Claude Code 增强包。
- `superpowers`: 官方增强插件。
- `planning-with-files`: 高效的文件级任务规划。
- `ui-ux-pro-max`: UI/UX 设计与评审增强。
- `sentry-skills`: Sentry 官方提供的错误分析技能。

## 📦 包含的文件

- `rules/`: 涵盖 TypeScript, Python, Golang 等多语言及通用开发规范。
- `hooks/`: 所有的自动化脚本（JS/Shell），负责监控、防护和状态显示。
- `skills/`: 预设的增强技能包。
- `settings.json`: 经过优化的全局配置文件（已脱敏）。
- `CLAUDE.md`: 行为准则指南。
- `AGENTS.md`: 代理编排与角色定义。

## 🚀 如何安装

1. **备份你的配置**：
   ```bash
   cp -r ~/.claude ~/.claude_backup
   ```

2. **克隆并覆盖**：
   将本项目中的内容复制到你的 `.claude` 根目录中：
   ```bash
   # Windows (Git Bash/WSL)
   cp -r rules/ hooks/ skills/ settings.json CLAUDE.md AGENTS.md ~/.claude/
   ```

3. **配置你的 Token**：
   打开 `~/.claude/settings.json`，将 `"your-token-here"` 替换为你真实的 `ANTHROPIC_AUTH_TOKEN`。

4. **重启 Claude Code**：
   重新运行 `claude` 命令，体验全新的自动化工作流！

## 🤝 贡献与反馈

如果你有更好的钩子脚本或规则建议，欢迎提交 PR！

---
🤖 *Generated and optimized by Antigravity*
