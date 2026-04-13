---
name: agent-autonomy-kit
version: 1.0.0
description: "停止等待提示词，让工作继续进行。"
homepage: https://github.com/itskai-dev/agent-autonomy-kit
metadata:
  openclaw:
    emoji: "🚀"
    category: 生产力
---

# 代理自动化套件 (Agent Autonomy Kit)

将您的代理从被动响应转变为主动执行。

## 快速入门

1. 创建包含“准备就绪 (Ready) / 进行中 (In Progress) / 已阻塞 (Blocked) / 已完成 (Done)”部分的任务队列。
2. 更新心跳流程 (Heartbeat)，使其能从队列中提取并执行任务。
3. 为夜间工作和每日报告设置定时任务 (Cron jobs)。
4. 无需人为提示，观察工作自动推进。

## 核心概念

- **任务队列 (Task Queue)** — 始终准备好待办工作。
- **主动心跳 (Proactive Heartbeat)** — 真正去执行工作，而不仅仅是检查状态。
- **连续操作 (Continuous Ops)** — 持续工作直到达到资源限制。

更多详细文档，请参见 `README.md`。
