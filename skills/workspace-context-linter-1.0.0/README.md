# Workspace Context Linter（工作区上下文检查工具）

Workspace Context Linter 用于审计**始终加载的工作区上下文文件**，例如 `AGENTS.md`、`SOUL.md`、`USER.md`、`MEMORY.md` 和 `TOOLS.md`。

它旨在帮助发现：
- 重复的规则或偏好
- 常驻上下文中过重的段落
- 内容可能放错文件角色的情况
- 在整理上下文之前最值得优先清理的项

## 检查内容
- 核心上下文文件的角色摘要
- 核心文件之间的重复主题
- 可能更适合作为引用的过重段落
- 基于文件角色的误放内容

## 当前范围
这一版主要聚焦于：
- 核心上下文文件
- 文本报告
- 诊断而非自动编辑
- 带角色感知的重复严重度判断

它**不会**自动重写文件。

## 用法
```bash
scripts/context_linter.py [--scope core|core+memory|custom] [--paths ...] [--output report.txt]
```

示例：
```bash
scripts/context_linter.py --scope core --output context-report.txt
```

## 输出内容
报告包括：
- 摘要
- 文件角色摘要
- 优先级排名
- 重复项
- 过重段落
- 误放内容
- 建议的移动操作
