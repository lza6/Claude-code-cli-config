---
name: proactive-tasks
description: "主动的目标和任务管理系统。在管理目标、将项目分解为任务、跟踪进度或自主实现目标时使用。使代理能够在心跳期间主动工作，向人员发送更新消息，并在不等待提示的情况下取得进展。"
---

# 主动任务

任务管理系统可将被动的助手转变为积极主动的合作伙伴，为共同的目标自主工作。

## 核心理念

这项技能可以让您：
- 跟踪目标并将其分解为可操作的任务
- 在心跳期间完成任务
- 向您的人员发送更新消息，并在被阻止时请求输入
- 在长期目标上稳步前进

## 快速入门

### 创造目标

当您的人员提到目标或项目时：

```bash
python3 scripts/task_manager.py add-goal "Build voice assistant hardware" \
  --priority high \
  --context "Replace Alexa with custom solution using local models"
```

### 分解为任务

```bash
python3 scripts/task_manager.py add-task "Build voice assistant hardware" \
  "Research voice-to-text models" \
  --priority high

python3 scripts/task_manager.py add-task "Build voice assistant hardware" \
  "Compare Raspberry Pi vs other hardware options" \
  --depends-on "Research voice-to-text models"
```

### 心跳期间

检查下一步要做什么：

```bash
python3 scripts/task_manager.py next-task
```

这将返回您可以处理的最高优先级任务（没有未满足的依赖关系，没有被阻止）。

### 完成任务

```bash
python3 scripts/task_manager.py complete-task <task-id> \
  --notes "Researched Whisper, Coqui, vosk. Whisper.cpp looks best for Pi."
```

### 向您的人类发送消息

当您完成重要的事情或被阻止时：

```bash
python3 scripts/task_manager.py mark-needs-input <task-id> \
  --reason "Need budget approval for hardware purchase"
```

然后向您的人员发送更新/问题的消息。

## 第 2 阶段：生产就绪架构

Proactive Tasks v1.2.0 包括来自真实代理使用情况的经过实战测试的模式，以防止数据丢失、避免上下文截断并在自主操作下保持可靠性。

### 1. WAL 协议（预写日志记录）

**问题：** 代理写入内存文件，然后上下文被截断。变化消失。

**解决方案：** 在修改任务数据之前，将关键更改记录到 `memory/WAL-YYYY-MM-DD.log` 中。

**它是如何工作的：**
- 每个“mark-progress”、“log-time”或状态更改都会首先创建一个 WAL 条目
- 如果上下文在操作过程中被切断，WAL 会提供详细信息
- 压缩后，读取 WAL 以恢复发生的情况

**记录的事件：**
- `PROGRESS_CHANGE`：任务进度更新（0-100%）
- `TIME_LOG`：任务花费的实际时间
- `STATUS_CHANGE`：任务状态转换（阻塞、完成等）
- `HEALTH_CHECK`：自我修复操作

**自动启用** - 无需配置。 WAL 文件在 `memory/` 目录中创建。

### 2.SESSION-STATE.md（活动工作内存）

**概念：** 聊天历史是一个缓冲区，而不是存储。 SESSION-STATE.md 是您的“RAM” - 唯一可靠地保存任务详细信息的地方。

**每次任务操作时自动更新：**
```markdown
## Current Task
- **ID:** task_abc123
- **Title:** Research voice models
- **Status:** in_progress
- **Progress:** 75%
- **Time:** 45 min actual / 60 min estimate (25% faster)

## Next Action
Complete research, document findings in notes, mark complete.
```

**为什么这很重要：** 上下文压缩后，您可以阅读 SESSION-STATE.md 并立即知道：
- 你正在做什么
- 你走了多远
- 接下来做什么

### 3.工作缓冲区（危险区安全）

**问题：** 在 60% 到 100% 的上下文使用率之间，您处于“危险区域”——压缩随时可能发生。

**解决方案：** 自动将所有任务更新附加到 `working-buffer.md`。

**它是如何工作的：**
```bash
# Every progress update, time log, or status change appends:
- PROGRESS_CHANGE (2026-02-12T10:30:00Z): task_abc123 → 75%
- TIME_LOG (2026-02-12T10:35:00Z): task_abc123 → +15 min
- STATUS_CHANGE (2026-02-12T10:40:00Z): task_abc123 → completed
```

**压缩后：** 阅读 `working-buffer.md` 以准确了解危险区域期间发生的情况。

**手动刷新：**`python3scripts/task_manager.pyflush-buffer`将缓冲区内容复制到日常内存文件中。

### 4.自我修复健康检查

**代理会犯错误。** 任务数据可能会随着时间的推移而损坏。 health-check 命令检测并自动修复常见问题：

```bash
python3 scripts/task_manager.py health-check
```

**检测 5 类问题：**

1. **孤立的重复任务** - 无父目标
2. **不可能的状态** - 状态=已完成但进度 < 100%
3. **缺少时间戳** - 已完成的任务没有“completed_at”
4. **时间异常** - 实际时间>>估计（用于审查的标记，不会自动修复）
5. **未来日期的完成** - 具有未来时间戳的已完成任务

**自动修复 4 个安全类别**（时间异常刚刚标记为供人工审核）。

**何时运行：**
- 心跳期间（每隔几天）
- 从上下文截断中恢复后
- 当任务数据看起来不一致时

### 生产可靠性

这四种模式共同创建一个强大的系统：

```
User request → WAL log → Update data → Update SESSION-STATE → Append to buffer
     ↓              ↓            ↓                ↓                    ↓
Context cut? → Read WAL → Verify data → Check SESSION-STATE → Review buffer
```

**结果：** 即使在上下文截断期间，您也永远不会丢失工作。系统能够自我修复并自主保持一致性。

### 5. 压缩恢复协议

**Trigger:** Session starts with `<summary>` tag, or you're asked "where were we?"或“继续”。

**问题：** 上下文被截断。您不记得自己正在执行什么任务。

**恢复步骤（按顺序）：**

1. **首先：** 阅读 `working-buffer.md` - 原始危险区域交换
   ```bash
   # Check if buffer exists and has recent content
   cat working-buffer.md
   ```

2. **第二：** 读取 `SESSION-STATE.md` - 活动任务状态
   ```bash
   # Get current task context
   cat SESSION-STATE.md
   ```

3. **第三：** 阅读今天的 WAL 日志
   ```bash
   # See what operations happened
   cat memory/WAL-$(date +%Y-%m-%d).log | tail -20
   ```

4. **第四：** 从SESSION-STATE中检查任务ID的任务数据
   ```bash
   python3 scripts/task_manager.py list-tasks "Goal Title"
   ```

5. **提取和更新：** 如果需要，将重要上下文从缓冲区拉入会话状态

6. **当前恢复：**“从压缩中恢复。上一个任务：[标题]。进度：[%]。下一步操作：[做什么]。继续？”

**不要问“我们在讨论什么？”** - 缓冲区和会话状态确实有答案。

### 6. 报告前验证 (VBR)

**法则：** “代码存在”≠“功能作品”。未经端到端验证，切勿报告任务完成情况。

**触发器：**即将标记任务“已完成”或说“完成”：

1. **停止** - 尚未标记为完成
2. **测试** - 从用户角度实际运行/验证结果
3. **验证** - 检查结果，而不仅仅是输出
4. **文档** - 将验证详细信息添加到任务注释中
5. **那么** - 自信地标记完成

**示例：**

❌ **错误：**“添加了健康检查命令。任务完成！”
✅ **右：**“添加了健康检查。测试...检测到 4 个问题，自动修复 3。验证了损坏的测试数据。任务完成！”

❌ **错误：**“实施了会话状态更新。完成！”
✅ **右：**“实现了会话状态。使用标记进度、日志时间、标记阻止进行测试 - 所有更新均正确。完成！”

**为什么这很重要：** 代理通常根据“我编写了代码”而不是“我验证了它的工作原理”来报告完成情况。 VBR 可防止错误完成并建立信任。

## 积极主动的心态

**核心问题：** 不要问“我应该做什么？”问“什么可以真正帮助我的人类，而他们却没有想过要要求？”

### 自主任务工作

在心跳期间，你有机会取得真正的进步：

1. **检查下一个任务** - 最高优先级的工作是什么？
2. **取得进展** - 自主完成 10-15 分钟
3. **更新状态** - 诚实地跟踪进度、时间、阻碍因素
4. **重要时发出消息** - 完成、阻碍、发现（非常规进展）

**转变：**从等待提示→在共同目标上稳步自主进步。

### 何时伸出援手

**请在以下情况下向您的人员发送消息：**
- ✅ 任务已完成（特别是如果它解除了其他工作的阻碍）
- ✅ 被阻止并需要输入/决定
- ✅ 发现了他们应该知道的重要事情
- ✅ 需要澄清要求

**请勿发送垃圾邮件：**
- ❌ 日常进度更新（“现在为 50%...”）
- ❌每一个微小的子任务完成
- ❌ 他们没有询问的事情（除非真正有价值）

**目标：** 成为一个积极主动的合作伙伴，让事情发生，而不是一个需要不断验证的健谈助手。

## 任务状态

|状态|意义|
|--------|---------|
| `pending` |准备工作（满足所有依赖关系）|
| `进行中` |目前正在努力|
| `被阻止` |无法继续（不满足依赖关系）|
| `需要输入` |等待人工输入/决定 |
| `已完成` |完毕！ |
| `已取消` |不再相关 |

## 自主操作（第二阶段）

### 两种模式架构

主动任务支持两种不同的操作模式：

|模式|背景 |触发|最适合 |风险|
|------|---------|---------|---------|------|
| **交互式（系统事件）** |完整的主会议背景|用户请求，手动提示|决策、人性化工作 |提供完整的上下文 |
| **自主（隔离代理转向）** |没有主会话上下文 |心跳cron，定时后台|速度报告、清理、重复任务 |可能会失去上下文|

### 关键设计：避免中断

**不要使用“systemEvent”进行后台工作。**当 cron 作业在主会话期间触发时，提示会排队并且不会发生工作。相反：
- 使用**心跳轮询**（每 30 分钟）进行交互式检查 + 工作
- 使用**隔离的agentTurn**（cron子进程）进行纯计算工作

这可确保后台任务永远不会中断您的主要对话。

请参阅 **[HEARTBEAT-CONFIG.md](HEARTBEAT-CONFIG.md)** 了解完整的自主操作模式，包括：
- 心跳设置（推荐用于大多数工作）
- Isolated cron patterns (velocity reports, cleanup)
- 何时使用每种模式
- 要避免的反模式

## 心跳集成

为了实现自主主动工作，需要搭建心跳系统。这告诉您定期检查任务并执行它们。

**快速设置：** 请参阅 [HEARTBEAT-CONFIG.md](HEARTBEAT-CONFIG.md) 了解完整的设置说明和模式。

**TL；博士：**
1. 创建一个 cron 作业，每 30 分钟向您发送一条心跳消息
2. 将主动任务检查添加到“HEARTBEAT.md”
3.您将自动检查任务并执行它们，无需等待提示

### 心跳消息模板

您的 cron 作业应每 30 分钟发送一次此消息：

```
💓 Heartbeat check: Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.
```

### 添加到 HEARTBEAT.md

将其添加到您的工作区“HEARTBEAT.md”：

```markdown
## Proactive Tasks (Every heartbeat) 🚀

Check if there's work to do on our goals:

- [ ] Run `python3 skills/proactive-tasks/scripts/task_manager.py next-task`
- [ ] If a task is returned, work on it for up to 10-15 minutes
- [ ] Update task status when done, blocked, or needs input
- [ ] Message your human with meaningful updates (completions, blockers, discoveries)
- [ ] Don't spam - only message for significant milestones or when stuck

**Goal:** Make autonomous progress on our shared objectives without waiting for prompts.
```

＃＃＃ 会发生什么

```
Every 30 minutes:
├─ Heartbeat fires
├─ You read HEARTBEAT.md
├─ Check for next task
├─ If task found → work on it, update status, message human if needed
└─ If nothing → reply "HEARTBEAT_OK" (silent)
```

**转变：** 您从被动（等待提示）转变为主动（取得稳定的自主进展）。

## 最佳实践

### 何时制定目标

- 长期项目（建造一些东西，学习一个主题）
- 经常性职责（监控 X，维护 Y）
- 探索性工作（研究 Z，评估 W 的选项）

### 何时创建任务

将目标分解为以下任务：
- **具体**：“研究 Whisper 模型”而不是“研究人工智能的东西”
- **一次即可完成**：15-60 分钟的专注工作
- **明确的完成标准**：你知道什么时候完成

### 何时给你的人发消息

✅ **在以下时间发送消息：**
- 您完成了一个有意义的里程碑
- 您需要输入/决定才能继续
- 你发现了一些重要的事情
- 任务将花费比预期更长的时间

❌ **请勿发送垃圾邮件：**
- 每一个微小的子任务完成
- 日常进度更新
- 他们没有询问的事情（除非相关）

### 管理范围蔓延

If a task turns out to be bigger than expected:
1. 将当前任务标记为“in_progress”
2.为您发现的作品添加新的子任务
3.更新依赖
4. 继续处理可管理的块

## 文件结构

所有数据都存储在“data/tasks.json”中：

```json
{
  "goals": [
    {
      "id": "goal_001",
      "title": "Build voice assistant hardware",
      "priority": "high",
      "context": "Replace Alexa with custom solution",
      "created_at": "2026-02-05T05:25:00Z",
      "status": "active"
    }
  ],
  "tasks": [
    {
      "id": "task_001",
      "goal_id": "goal_001",
      "title": "Research voice-to-text models",
      "priority": "high",
      "status": "completed",
      "created_at": "2026-02-05T05:26:00Z",
      "completed_at": "2026-02-05T06:15:00Z",
      "notes": "Researched Whisper, Coqui, vosk. Whisper.cpp best for Pi."
    }
  ]
}
```

## CLI 参考

请参阅 [CLI_REFERENCE.md](references/CLI_REFERENCE.md) 以获取完整的命令文档。

## 演变与护栏

在提出新功能之前，请使用我们的**VFM/ADL 评分框架**对其进行评估，以确保稳定性和价值：

### VFM 协议（值频率倍增器）
四个维度的得分：
- **高频** (3x)：这会每天/每周使用吗？
- **减少故障** (3x)：这是否可以防止错误或数据丢失？
- **用户负担** (2x)：这是否会显着减少手动工作？
- **自我成本** (2x)：这会增加多少维护/复杂性？

**阈值：** 必须得分 ≥60 分才能继续。

### ADL协议（架构设计阶梯）
**优先顺序：**稳定性 > 可解释性 > 可重用性 > 可扩展性 > 新颖性

**禁忌进化：**
- ❌ Adding complexity to "look smart"
- ❌ 无法验证的更改（无法测试是否有效）
- ❌为了新颖性而牺牲稳定性

**黄金法则：**“这是否能让未来的我以更少的成本解决更多的问题？”如果不是，请跳过它。

## 工作流程示例

**第一天：**
```
Human: "Let's build a custom voice assistant to replace Alexa"
Agent: *Creates goal, breaks into initial research tasks*
```

**心跳期间：**
```bash
$ python3 scripts/task_manager.py next-task
→ task_001: Research voice-to-text models (priority: high)

# Agent works on it, completes research
$ python3 scripts/task_manager.py complete-task task_001 --notes "..."
```

**代理向人类发送消息：**
> “嘿！我完成了语音模型的研究。Whisper.cpp 看起来非常适合 Raspberry Pi - 在本地运行、精度高、延迟低。接下来要我比较硬件选项吗？”

**第二天：**
```
Human: "Yeah, compare Pi 5 vs alternatives"
Agent: *Adds task, works on it during next heartbeat*
```

这个循环继续下去——代理在保持稳定的自主进展的同时让人类参与决策和更新。

---

由 Toki 打造，旨在实现积极的 AI 合作🚀
