---
name: find-skills
description: "当用户提出诸如"我如何做 X"、"为 X 找到一项技能"、"是否有一项技能可以..."或表达对扩展功能的兴趣等问题时，帮助用户发现并安装代理技能。当用户正在寻找可能作为可安装技能存在的功能时，应使用此技能。"
---

# 技能查找器

此技能可帮助您从开放代理技能生态系统中发现并安装技能。

## 何时使用此技能

当用户执行以下操作时使用此技能：

- 询问"我如何做 X"，其中 X 可能是具有现有技能的常见任务
- 说"找到 X 的技能"或"有 X 的技能吗"
- 询问"你能做 X 吗"，其中 X 是一项专门能力
- 表示有兴趣扩展代理能力
- 想要搜索工具、模板或工作流
- 提到他们希望在特定领域（设计、测试、部署等）获得帮助

## 什么是技能 CLI？

Skills CLI (`npx skills`) 是开放代理技能生态系统的包管理器。技能是模块化包，可通过专业知识、工作流和工具扩展代理能力。

**关键命令：**

- `npx skills find [query]` — 通过关键字交互式搜索技能
- `npx skills add <package>` — 从 GitHub 等来源安装技能
- `npx skills check` — 检查技能更新
- `npx skills update` — 更新所有已安装的技能

**浏览技能：** https://skills.sh/

## 如何帮助用户找到技能

### 第 1 步：了解他们的需求

当用户寻求帮助时，请识别：

1. 领域（例如，React、测试、设计、部署）
2. 具体任务（例如，编写测试、创建动画、审查 PR）
3. 这是否是一项足够常见的任务，可能已有现成技能

### 第 2 步：搜索技能

使用相关查询运行 find 命令：

```bash
npx skills find [query]
```

例如：

- 用户询问"如何让我的 React 应用更快？" → `npx skills find react performance`
- 用户询问"你能帮我进行 PR 审查吗？" → `npx skills find pr review`
- 用户询问"我需要创建变更日志" → `npx skills find changelog`

该命令将返回如下结果：

```
使用 npx skills add <owner/repo@skill> 安装

vercel-labs/agent-skills@vercel-react-best-practices
└ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### 步骤 3：向用户提供选项

当您找到相关技能时，将其呈现给用户：

1. 技能名称及作用
2. 他们可以运行的安装命令
3. 在 Skills.sh 上了解更多信息的链接

响应示例：

```
我找到了一个可能有帮助的技能！"vercel-react-best-practices" 技能提供了
来自 Vercel 工程团队的 React 和 Next.js 性能优化指南。

安装方法：
npx skills add vercel-labs/agent-skills@vercel-react-best-practices

了解更多信息：https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### 第 4 步：提供安装

如果用户想继续，您可以为他们安装技能：

```bash
npx skills add <owner/repo@skill> -g -y
```

`-g` 标志表示全局安装（用户级别），`-y` 跳过确认提示。

## 常用技能类别

搜索时，请考虑以下常见类别：

| 类别 | 示例查询 |
| ---------------- | ---------------------------------------------------- |
| Web 开发 | react, nextjs, typescript, css, tailwind |
| 测试 | test, jest, playwright, e2e |
| 开发运维 | deploy, docker, kubernetes, ci-cd |
| 文档 | docs, readme, changelog, api docs |
| 代码质量 | review, lint, refactor, best practices |
| 设计 | ui, ux, design systems, accessibility |
| 生产力 | workflow, automation, git |

## 有效搜索的技巧

1. **使用特定的关键字**："react test" 比仅仅 "test" 更好
2. **尝试替代术语**：如果 "deploy" 不起作用，请尝试 "deployment" 或 "ci-cd"
3. **检查流行来源**：许多技能来自 `vercel-labs/agent-skills` 或 `ComposioHQ/awesome-claude-skills`

## 当没有找到技能时

如果不存在相关技能：

1. 确认没有找到现有技能
2. 主动提出利用你的一般能力直接帮助完成任务
3. 建议用户使用 `npx skills init` 创建自己的技能

示例：

```
我搜索了与 "xyz" 相关的技能，但没有找到匹配项。
我仍然可以直接帮你完成这个任务！要我继续吗？

如果这是你经常做的事情，你可以创建自己的技能：
npx skills init my-xyz-skill
```
