---
name: agent-guardian
description: Agent 体验守护系统。解决AI助手常见体验问题 ：长时间无响应、任务卡死、中英文混用、状态不透明。包含看门狗监控、智能状态汇报、即时状态查询、语言一致性过滤、消息队列追踪。适用于所有渠道 （ QQ微信//Telegram飞书//Discord等 ）。当用户抱怨等太久没回复、 “回复中英文混着”、 “不知道在干什么”时使用此技能。
---


#特工守护 🛡️

AI 助手体验守护系统——让用户永远不会觉得你"卡了"或"乱说话"。

## 问题背景

AI 助手在实际使用中常见的体验痛点：
1. **无响应** — 工具调用卡住，用户干等没反馈
2. **状态不透明** — 用户不知道AI在干什么
3. **语言混乱** — 中文对话里夹杂英文短语
4. **任务死循环** — 同一个错误反复重试

## 架构


```
┌─────────────────────────────────────────────┐
│                Agent Guardian               │
├─────────────┬──────────────┬────────────────┤
│ 🐕 看门狗    │ 📊 状态汇报   │ 🔤 语言过滤    │
│ (cron 3min) │ (cron 5min)  │ (出站 hook)    │
├─────────────┼──────────────┼────────────────┤
│ 🔍 即时查询  │ 📝 消息队列   │ ⏰ 活跃追踪    │
│ (systemd)   │ (脚本)       │ (插件 hook)    │
└─────────────┴──────────────┴────────────────┘
```


## 安装


```bash
bash {baseDir}/scripts/install.sh
```


交互式安装，会询问渠道类型和用户 ID。

安装后还需：
1. openclaw cron 添加 看门狗任务（开爪定时器见下方）
2.应用渠道插件补丁（见 __ INLINE_0 __ ）
3.重启网关

## 组件说明

# # # 🐕 看门狗（ supervisor.sh ）

每3 openclaw cron分钟由 ，开爪定时触发器检测：
- 任务卡住（ 3分钟无状态更新 ）
- 死循环（同一状态重复 5次 ）
- 错误累积（连续 3次错误 ）
- 僵尸进程

设置 cron 任务示例：

```json
{
  "name": "agent-guardian-watchdog",
  "schedule": { "kind": "cron", "expr": "*/3 * * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "读取 /tmp/agent-supervisor-report.txt，如果有告警内容就发给用户，没有就回复 HEARTBEAT_OK"
  }
}
```


# # # 📊 智能状态汇报（ smart-status-report.sh ）

系统 crontab 每5分钟执行 ，智能开关说明：
- 对话时（最近 10分钟有消息 ）→ 推送状态
- 沉默时 → 自动静默，不打扰

# # # 🔍 即时状态查询（ status-query-daemon.sh ）

用户发"状态"→ 渠道插件拦截 → 写触发文件 → 守护进程秒回
* *不经过 AI * * ，即使 AI卡死也能响应。

# # # 🔤 语言一致性过滤（ lang-filter.py + detect-language.py ）

出站消息自动检测并替换常见英文混用。
- 70 + 常见英文短语映射（金融/日常/科技）
- 技术术语白名单保护（ AI/API/GDP等不替换 ）
- 字符集 + langdetect 双重语言检测

# # # 📝 消息队列（ msg-queue.py ）

追踪每条消息的处理状态（等待→处理→完成）。
- 自动超时：加工超5分钟自动标记完成
- 日报统计：今日处理数量

### AI 干活时的状态更新

在执行任务时调用：

```bash
bash {baseDir}/scripts/update-work-state.sh working "任务描述"
```

完成时：

```bash
bash {baseDir}/scripts/update-work-state.sh done
```

出错时：

```bash
bash {baseDir}/scripts/update-work-state.sh error "任务描述" "yes"
```


## 渠道适配

- QQ机器人： 详见 __ INLINE_0 __
-通用指南: 详见 __ INLINE_1 __
- 核心原理：在入站 （收消息 ）和出站 （发消息 ）两个 HOOK 点插入 GUARDIAN 逻辑

### 不修改插件的降级模式

即使不 patch 渠道插件，补丁看门狗和定时汇报仍可独立运行。
语言过滤和即时查询需要插件 补丁 才能完全生效。

## 文件清单


```
scripts/
├── install.sh              # 一键安装
├── supervisor.sh            # 看门狗
├── update-work-state.sh     # 工作状态更新
├── smart-status-report.sh   # 智能汇报
├── status-query-daemon.sh   # 即时查询守护进程
├── detect-language.py       # 语言检测
├── lang-filter.py           # 语言过滤
├── msg-queue.py             # 消息队列
└── reset-work-state.sh      # 状态重置
references/
└── patches/
    ├── qqbot.md             # QQ Bot 适配指南
    └── generic.md           # 通用适配指南
```

