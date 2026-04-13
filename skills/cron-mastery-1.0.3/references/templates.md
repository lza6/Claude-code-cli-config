# Cron 示例和模板

## 一次性提醒（推送通知/可靠）

**上下文：** 用户说“提醒我 15 分钟后检查烤箱。”
**最适合：** 必须 ping 用户电话的计时器。

```json
{
  "action": "add",
  "job": {
    "name": "Oven Timer",
    "schedule": {
      "kind": "at",
      "at": "2026-02-16T21:15:00+02:00"
    },
    "payload": {
      "kind": "agentTurn",
      "message": "DELIVER THIS EXACT MESSAGE TO THE USER WITHOUT MODIFICATION OR COMMENTARY:\n\n🔥 OVEN CHECK! It's been 15 minutes."
    },
    "sessionTarget": "isolated",
    "delivery": {
      "mode": "announce",
      "channel": "telegram",
      "to": "1027899060"
    },
    "wakeMode": "now"
  }
}
```

## 看门人（系统维护）

**背景：** 每天清理已完成的一次性作业。
**最适合：** 在主会话中以完全工具访问权限运行。

```json
{
  "action": "add",
  "job": {
    "name": "Daily Cron Sweep",
    "schedule": {
      "kind": "every",
      "everyMs": 86400000
    },
    "payload": {
      "kind": "systemEvent",
      "text": "Time for the 24-hour cron sweep. List all cron jobs (includeDisabled: true). Delete any disabled jobs with lastStatus: ok. Report results."
    },
    "sessionTarget": "main",
    "wakeMode": "now"
  }
}
```

## 复杂任务（重复/异步）

**上下文：** 用户说“每天早上 8 点总结我的电子邮件。”

```json
{
  "action": "add",
  "job": {
    "name": "Morning Briefing",
    "schedule": {
      "kind": "cron",
      "expr": "0 8 * * *",
      "tz": "Africa/Cairo"
    },
    "payload": {
      "kind": "agentTurn",
      "message": "Good morning! Search for unread emails and top tech news, then summarize them."
    },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "delivery": {
      "mode": "announce",
      "channel": "telegram",
      "to": "1027899060"
    }
  }
}
```
