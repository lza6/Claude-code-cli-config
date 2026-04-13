---
name: workspace-context-linter
description: "诊断始终加载的工作区上下文文件，例如 AGENTS.md、SOUL.md、USER.md、MEMORY.md 和 TOOLS.md。当您想要减少上下文膨胀、检测重复的规则、发现放错位置的内容、识别超重部分或在重新组织核心上下文文件之前审核它们是否仍然符合其预期角色时使用。"
---

# 工作区上下文 Linter

审核核心工作区上下文文件而不重写它们。

## 核心工作流程
1. 加载现有的核心上下文文件。
2. 总结每个文件可能的作用。
3. Detect duplicate rule themes, overweight sections, and misplaced content.
4. 制作一份包含优先事项和建议行动的文本报告。

## 根据需要阅读参考文献
- 阅读 `references/rules.md` 了解 lint 类别和严重性模型。
- 阅读“references/report-format.md”以获取输出结构。
- 阅读 `references/file-roles.md` 了解每个核心上下文文件通常应包含的内容。
- 在决定内容应移动到哪里时，请阅读“references/move-guidelines.md”。
- 在打包或发布之前阅读 `references/release-minimal.md`，以便第一个公共表面保持最小。

## 根据需要使用脚本
- 使用 `scripts/context_linter.py [--scope core|core+memory|custom] [--paths ...] [--output report.txt]` 运行 linter。

## 操作规则
- 更喜欢诊断而不是自动编辑。
- 将重复视为维护问题，除非它们造成真正的执行模糊性。
- 将超重部分视为提取候选，而不是自动删除。
- 保持第一个版本专注于核心上下文文件和文本报告。
