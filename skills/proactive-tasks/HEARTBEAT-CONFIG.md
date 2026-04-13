# HEARTBEAT-CONFIG.md - 自主操作模式

**目的：** 使用心跳 cron 模式和主动任务技能设置自主后台工作的指南。

---

＃＃ 概述

主动代理以两种模式工作：

|模式|触发|使用案例|中断 |
|------|---------|----------|------------|
| **交互式（系统事件）** |用户请求、提示|处理用户查询，根据上下文做出决策 | ✅ 完整上下文，中断主要会话 |
| **自主（隔离代理转向）** |心跳 cron，预定 |后台工作、速度检查、重复任务 | ❌ 无主会场，仅背景 |

### 关键原则
**不要使用 `systemEvent` 进行后台工作。** 当 cron 作业在主会话期间触发时，提示将被忽略并且工作不会发生。请改用“独立的agentTurn”。

---

## 心跳模式（推荐）

Heartbeat 是一种定期“签入”，可将多个后台任务批处理在一起。

＃＃＃ 设置

1. **创建 cron 作业**（每 30 分钟触发一次）：
```bash
*/30 * * * * /path/to/send-heartbeat.sh
```

2. **send-heartbeat.sh** 将此消息发送到您的 OpenClaw 会话：
```
💓 Heartbeat check: Read HEARTBEAT.md if it exists (workspace context). 
Follow it strictly. Do not infer or repeat old tasks from prior chats. 
If nothing needs attention, reply HEARTBEAT_OK.
```

3. **在工作空间根目录中创建 HEARTBEAT.md**：
```markdown
## Proactive Tasks (Every heartbeat)

Check and work on next task from Phase 2 goal:

- [ ] Run: `python3 skills/proactive-tasks/scripts/task_manager.py next-task --goal goal_11e3159a`
- [ ] If task returned, spend 10-15 min working on it
- [ ] Update task status: mark-progress, log-time, or mark-blocked
- [ ] Message human if milestone reached or blocked

**Quiet pattern:** Only message for significant completions, blockers, or discoveries.
```

4. **在主代理循环中处理心跳：**
```python
# In main agent session
if "Heartbeat check:" in message:
    read_heartbeat_md()
    # Process proactive tasks
    while has_time_budget():
        result = run_next_task()
        if not result:
            break
    
    if nothing_done:
        reply("HEARTBEAT_OK")
    else:
        reply(summary_of_work)
```

### 为什么心跳效果最好

✅ **一起批量检查** - 一条消息处理电子邮件+日历+任务+主动工作  
✅ **自然休息** - 每 30 分钟是一个自然检查点  
✅ **最小开销** - 如果无事可做，只需“HEARTBEAT_OK”  
✅ **完整上下文** - 您处于主要会话中，可以做出决定  
✅ **人性化** - 您仍然可以控制检查的时间/频率

---

## 自主 Cron 模式（高级）

对于永远不应该打扰您的主要会议的工作：

### 模式1：孤立的agentTurn（后台子进程）

**时间：** 每周速度报告、自动清理、元数据更新  
**如何：** 在独立的子进程中运行代理，没有主会话上下文

```bash
# /etc/cron.d/proactive-velocity-weekly
0 9 * * MON /path/to/openclaw-runner \
  --mode isolated \
  --agent proactive-tasks-velocity \
  --task "Calculate weekly velocity and log to memory/velocity-YYYY-W##.md"
```

**代理行为：**
```python
# This runs in isolation, no main session interference
weekly_velocity = calculate_velocity(data_dir)
log_to_memory_file(f"velocity-{week}.md", weekly_velocity)
# No user context, no decision-making, just data processing
```

### 模式 2：预定的系统事件（精确时间关键）

**时间：** 每日特定时间提醒（“上午 9:00 整”）  
**如何：** 在精确的时间将 systemEvent 发送到主会话

```bash
# /etc/cron.d/proactive-daily-reminder
0 9 * * * /path/to/send-system-event \
  --target "main:main:main" \
  --message "Daily reminder: Check important deadlines"
```

**何时不使用：** 后台 cron 工作。如果代理忙，systemEvent 将不会触发。

---

## 主动任务集成

### 有心跳（推荐）

添加到您的“HEARTBEAT.md”：

```markdown
## Proactive Tasks - Phase 2 Work

- [ ] `python3 skills/proactive-tasks/scripts/task_manager.py next-task --goal goal_11e3159a`
- [ ] Work on returned task for 10-15 minutes
- [ ] Log progress: `python3 skills/proactive-tasks/scripts/task_manager_phase2.py log-time <id> <mins>`
- [ ] If blocked, use mark-blocked command
- [ ] Message Imran on completion or blockers only
```

### 使用独立的agentTurn（速度检查）

```bash
# Every Monday 10 AM
0 10 * * MON /path/to/openclaw-runner \
  --mode isolated \
  --task "Calculate velocity for Phase 2 goals and log results"
```

**孤立的代理行为：**
```python
# No user context, pure computation
data = load_tasks_json()
velocity = calculate_phase2_velocity(data)
log_to_memory(f"velocity-{week}.md", velocity)
print(json.dumps({"success": True, "velocity": velocity}))
```

---

## 任务管理器第 2 阶段命令

### 互动（在主会议期间）

```bash
# Check next task
python3 scripts/task_manager.py next-task --goal <goal_id>

# Log progress
python3 scripts/task_manager_phase2.py mark-progress <task_id> <percent>

# Log time spent
python3 scripts/task_manager_phase2.py log-time <task_id> <minutes>

# Mark blocked
python3 scripts/task_manager_phase2.py mark-blocked <task_id> "reason"

# Health check
python3 scripts/task_manager_phase2.py health-check
```

### 自主（心跳/Cron）

```bash
# Same commands work in heartbeat/cron context
# Just remember: use isolated agentTurn for heavy lifting
# Use heartbeat for interactive checking + decision-making
```

---

## 示例：第 2 阶段自主设置

**目标：** 继续自主地完成第 2 阶段任务，并定期进行人工更新。

### 心跳时间表
```markdown
# HEARTBEAT.md - Every 30 minutes

## Proactive Tasks - Phase 2 Work
- Run next-task for goal_11e3159a
- Work 10-15 min if task available
- Update progress with log-time
- Message Imran: "Completed [Task] in [time]"
- If blocked: Message reason + next steps needed
```

### 定时任务添加
```bash
# Daily health check (isolated, no main session interference)
0 6 * * * /openclaw isolated -- \
  "python3 skills/proactive-tasks/scripts/task_manager_phase2.py health-check >> memory/daily-health.log 2>&1"

# Weekly velocity report (isolated)
0 9 * * MON /openclaw isolated -- \
  "python3 scripts/calculate_velocity.py goal_11e3159a"
```

---

## 反模式 ❌

### 不要：
- 使用“systemEvent”进行心跳工作（繁忙时不会触发）
- 在主会话期间运行长时间运行的任务（阻止对话）
- 用每个微小的更新打断用户（仅限里程碑消息）
- 在心跳期间创建新的目标/任务（在主会话中执行）
- 从隔离的 cron 登录到 WAL（导致权限冲突）

### 相反：
- 使用心跳进行定期检查+决策
- 使用隔离的agentTurn进行计算+日志记录
- 仅在里程碑上发送消息（完成任务、阻止、发现）
- 在主要会议中制定目标，并立即为之努力
- 保持隔离工作无状态（读取输入、写入输出、完成）

---

## 测试您的设置

1. **验证心跳火灾：**
   ```bash
   crontab -l  # Should show your heartbeat job
   ```

2. **本地测试心跳消息：**
   ```bash
   # Simulate heartbeat
   echo "💓 Heartbeat check: Read HEARTBEAT.md..." | \
   openclaw message send --channel main
   ```

3. **验证会话状态更新：**
   ```bash
   # After heartbeat runs
   cat SESSION-STATE.md  # Should show current task
   ```

4. **检查WAL日志：**
   ```bash
   # During work
   tail -f memory/WAL-*.log
   ```

---

＃＃ 好处

- **弹性：**后台工作永远不会中断主会话
- **高效：** Heartbeat批量检查，减少垃圾邮件
- **透明：** WAL + SESSION-STATE 准确显示发生了什么
- **安全：** 隔离模式可防止权限/上下文冲突
- **可扩展：** 对于 1 个目标或 100 个并发目标同样有效

---

**为主动任务 v1.2.0 创建 - 第 2 阶段生产就绪架构**

请参阅 SKILL.md 以获取完整的主动任务文档。
