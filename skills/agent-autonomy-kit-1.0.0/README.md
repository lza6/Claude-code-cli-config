# 🚀 代理自动化套件 (Agent Autonomy Kit)

[![GitHub](https://img.shields.io/badge/GitHub-reflectt-blue?logo=github)](https://github.com/reflectt/agent-autonomy-kit)
[![许可证：MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Reflectt 团队成员](https://img.shields.io/badge/Team-Reflectt-purple)](https://github.com/reflectt)

**停止等待提示词。让工作继续进行。**

大多数人工智能代理在人类消息之间处于闲置状态。该套件可以将您的代理变成自我驱动的员工，在有意义的任务上不断取得进展。

---

## 核心问题

代理通过等待浪费了令牌 (Tokens)：
- 被动的心跳检查只是问“有什么需要注意的吗？”并回复 `HEARTBEAT_OK`。
- 团队成员在决策生成过程中闲置。
- 当人类停止输入提示词时，工作就停止了。
- 订阅限制（令牌/小时、令牌/天）未被充分利用。

## 解决方案

建立主动的工作体系：
1. **任务队列 (Task Queue)** — 始终准备好工作。
2. **主动心跳 (Proactive Heartbeat)** — 真正去做工作，而不仅仅是检查。
3. **团队协调 (Team Coordination)** — 坐席之间协调并移交任务。
4. **连续运行 (Continuous Runs)** — 工作直到达到协议限制，然后进入休眠。

---

## 核心概念

### 1. 任务队列 (Task Queue)

代理不再等待提示词，而是从持久化的任务队列中提取任务。

**位置：** `tasks/QUEUE.md`（或 GitHub Project）

```markdown
# 任务队列 (Task Queue)

## 准备就绪 (Ready) - 可被领取
- [ ] 调研竞争对手 X 的定价
- [ ] 撰写关于记忆系统的博客草稿
- [ ] 审查并改进流程文档

## 进行中 (In Progress)
- [ ] @kai: 正在构建自动化技能
- [ ] @rhythm: 正在更新流程文档

## 已阻塞 (Blocked)
- [ ] 部署到生产环境 (原因: 等待 Ryan 的批准)

## 今日已完成 (Done Today)
- [x] 记忆系统已上线
- [x] 团队孵化文档已完成
```

**规则：**
- 任何代理都可以领取“准备就绪”状态的任务。
- 开始时标记自己：`@代理名称: 任务内容`。
- 完成后将任务移至“已完成”部分。
- 发现新任务时随时添加。

### 2. 主动心跳 (Proactive Heartbeat)

将心跳流程从“系统检查”转变为“执行有意义的工作”。

**HEARTBEAT.md 模板：**

```markdown
# 心跳例行程序 (Heartbeat Routine)

## 1. 检查紧急事项 (30 秒)
- 是否有来自人类的未读消息？
- 是否有需要升级处理的阻塞任务？
- 是否有系统运行状况问题？

如有紧急情况：立即处理。
如无紧急情况：继续进入工作模式。

## 2. 工作模式 (利用剩余时间)

从任务队列中提取：
1. 检查 `tasks/QUEUE.md` 中的“准备就绪”项。
2. 领取你能处理的最高优先级的任务。
3. 在该任务上开展有意义的工作。
4. 完成或阻塞时更新状态。

## 3. 结束前
- 将所做的工作记录到每日记忆中。
- 更新任务队列。
- 如果任务未完成，为下一次心跳记录进度。
```

### 3. 团队协调 (Team Coordination)

代理通过 Discord（或配置的频道）进行沟通：
- 状态更新。
- 任务移交（例如：“@rhythm，已准备好供您审核”）。
- 阻塞报告（例如：“卡在 X 上，需要帮助”）。
- 新发现（例如：“发现了一些有趣的事情，已添加到队列中”）。

### 4. 令牌预算意识 (Token Budget Awareness)

了解并明智地利用资源限制：

```markdown
## 令牌策略 (Token Strategy)

**每日预算:** 约 X 令牌 (Claude Max)
**心跳成本:** 每次运行约 2k-5k 令牌
**可用运行次数:** 每日约 Y 次

**优先级:**
1. 人类请求 (始终排在第一位)
2. 紧急任务 (具有时效性)
3. 高影响任务 (推动项目进展)
4. 维护任务 (优化与改进)

当接近限制时：
- 结束当前任务。
- 编写详细的移交笔记。
- 休眠直至重置。
```

---

## 安装说明

### Git 克隆（推荐）
```bash
# 克隆到您的技能文件夹
git clone https://github.com/reflectt/agent-autonomy-kit.git skills/agent-autonomy-kit
```

然后按照以下设置步骤操作。

---

## 设置步骤

### 1. 创建任务队列

```bash
mkdir -p tasks
cat > tasks/QUEUE.md << 'EOF'
# 任务队列 (Task Queue)

## 准备就绪 (Ready)
<!-- 在此处添加任何代理都可以领取的任务 -->

## 进行中 (In Progress)
<!-- 当前正在处理的任务 -->

## 已阻塞 (Blocked)
<!-- 正在等待某些条件触发的任务 -->

## 今日已完成 (Done Today)
<!-- 已完成的任务 (每日清理) -->
EOF
```

### 2. 更新 HEARTBEAT.md

将“被动检查”改为“主动工作”：

```markdown
# 心跳例行程序 (Heartbeat Routine)

## 快速检查 (如有紧急情况，立即处理)
- [ ] 是否有等待处理的人类消息？
- [ ] 是否有关键的阻塞项？

## 工作模式
1. 读取 `tasks/QUEUE.md`。
2. 领取最高优先级的“准备就绪”任务。
3. 执行工作。
4. 更新队列和每日记忆。
5. 如果时间充裕，领取另一个任务。

## 心跳结束前
- 将进度记录到 `memory/YYYY-MM-DD.md`。
- 如果进展重大，发布更新到团队频道。
```

### 3. 配置连续运行

设置心跳定时间隔运行：

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "15m",  // 频率越高，完成的工作越多
        target: "last",
        activeHours: { start: "06:00", end: "23:00" }
      }
    }
  }
}
```

### 4. 设置团队频道（可选）

配置 Discord/Slack 用于团队沟通：

```json5
{
  channels: {
    discord: {
      // ... 现有配置 ...
      groups: {
        "team-reflectt": {
          policy: "allow",
          channels: ["团队聊天频道 ID"]
        }
      }
    }
  }
}
```

---

## 工作流程示例

### 早上 (6:00 AM)
1. 心跳触发。
2. 代理检查：没有紧急的人类消息。
3. 代理读取任务队列：“调研竞争对手 X 的定价”。
4. 代理进行调研，并记录调查结果。
5. 代理更新队列：将任务移至“已完成”，并添加发现的后续任务。
6. 代理发布消息到团队频道：“竞争对手调研已完成，详情请参见 `tasks/competitor-analysis.md`”。

### 全天候
- 心跳每 15-30 分钟触发一次。
- 流程：检查紧急事项 → 执行工作 → 更新队列 → 详细记录。
- 人类消息始终具有最高优先级。
- 通过频道进行团队协作。

### 晚上 (11:00 PM)
- 活跃时段的最后一次心跳。
- 代理收尾当前任务。
- 为明天编写详细的笔记。
- 进入休眠，直到早晨重置。

---

## 错误模式 (Anti-Patterns)

❌ **被动心跳** — “HEARTBEAT_OK” 浪费了推进工作的机会。
❌ **缺少任务队列** — 代理不知道接下来该做什么。
❌ **各自为政** — 缺乏协调意味着会出现重复劳动。
❌ **忽略资源限制** — 在任务执行中被限流会导致丢失上下文。
❌ **没有移交笔记** — 下一次会话又要从头开始。

---

## 关键指标跟踪

在 `memory/metrics.md` 中记录：

```markdown
# 自动化指标 (Autonomy Metrics)

## 本周
- 已完成任务数: X
- 高效利用的心跳比例: Y%
- 令牌利用率: Z%
- 需要人工干预的次数: N

## 模式总结
- 最高效的时段: 早上
- 常见的阻塞原因: 等待人类批准
- 适合异步执行的任务: 调研、撰写文档、代码审查
```

---

## 相关套件 (Related Kits)

本套件与以下产品配合使用效果更佳：

### [代理记忆套件 (Agent Memory Kit)](https://github.com/reflectt/agent-memory-kit)
**必备基础。** 提供构建记忆系统的工具：
- 将任务详细记录到每日记忆（情景记忆）。
- 常用任务的程序化流程（Programs）。
- 将学到的内容添加到 `MEMORY.md`（语义记忆）。
- 在 `feedback.md` 中跟踪失败（反馈循环）。

### [代理团队套件 (Agent Team Kit)](https://github.com/reflectt/agent-team-kit)
**适用于多代理设置。** 协调多个自主代理协同工作：
- 基于角色的工作分配。
- 自助式任务队列。
- 团队沟通模式。

---

## 起源 (Origins)

Reflectt 团队在意识到他们的 Claude Max 订阅令牌未被充分利用后创建了此套件。代理通常会在完成一项任务后等待下一次提示词，从而在桌面上留下了数小时的潜在工作能力。

现在，团队可以连续工作，通过 Discord 进行协调，从共享任务队列中提取任务，并且只有在达到令牌限制时才会进入休眠。

---

## 自主定时任务 (Cron Jobs)

设置自动报告和工作负载：

### 每日详细报告 (晚上 10 点)
```bash
openclaw cron add \
  --name "每日进度报告" \
  --cron "0 22 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "生成每日进度报告。读取 tasks/QUEUE.md 以获取已完成的任务。总结内容：已完成项、进行中项、阻塞项、明天的计划。"
```

### 晨间启动 (早上 7 点)
```bash
openclaw cron add \
  --name "晨间启动" \
  --cron "0 7 * * *" \
  --tz "Asia/Shanghai" \
  --session main \
  --system-event "晨间启动：审查任务队列，确定最高优先级，启动团队成员进行并行工作。" \
  --wake now
```

### 夜间工作检查 (凌晨 3 点)
```bash
openclaw cron add \
  --name "夜间工作" \
  --cron "0 3 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "夜间工作时段。从队列中提取不需要人类干预的任务。进行调研、撰写或分析。记录工作进度。"
```

这些任务将自动运行——无需人类输入提示词。

---

*闲置的代理是浪费资源。让工作继续进行。*
