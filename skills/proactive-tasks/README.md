# 主动任务 v1.1.0 - ReadyforClawdHub

**状态：** 准备好提交 ClawdHub  
**版本：** 1.1.0  
**最后更新：** 2026-02-12

＃＃ 概述

Proactive Tasks 是一个适用于 AI 代理的生产就绪型自主任务管理系统。与简单的待办事项列表不同，它可以：

- **进度跟踪** — 0-100% 完成，不是二进制完成/未完成
- **时间跟踪** — 测量实际时间与估计时间，建立速度
- **速度预测** — “每天执行 2.5 个任务，您将在 6 天内完成”
- **重复自动化** — 每日站会、每周回顾自行运行
- **特定阻碍因素** — 确切了解任务被卡住的原因
- **自主心跳集成** — 检查任务、处理任务、报告

## 主要特点

### 任务管理
- 制定目标并将其分解为任务
- 设置优先级（低、中、高）
- 跟踪任务之间的依赖关系
- 更新状态（待处理、进行中、阻止、需要输入、已完成）

### 进度和时间
- 跟踪 0-100% 的进度
- 记录实际花费时间与估计时间
- 自动计算方差并构建速度数据
- 预测完成日期

### 重复任务
- 每日、每周、每月自动化
- 完成后自动创建下一个事件
- 估计重复工作的时间

### 智能状态
- 将任务标记为因特定原因而被阻止
- 准备好后自动解锁
- 区分“卡住”和“等待输入”

### 速度跟踪
- 每天完成的任务
- 根据速度估计完成时间
- 用于改进估计的数据

## 技术细节

**存储：** JSON (tasks.json)  
**脚本：** Python 3.7+  
**依赖关系：** 无（仅限标准库）

## 命令

＃＃＃ 核
```bash
# Create goal
python3 scripts/task_manager.py add-goal "Build voice assistant"

# Add task
python3 scripts/task_manager.py add-task "Build voice assistant" "Research models"

# Get next task
python3 scripts/task_manager.py next-task

# Complete task
python3 scripts/task_manager.py complete-task <task-id> --notes "..."

# List status
python3 scripts/task_manager.py status
```

### 第 1 阶段（增强）
```bash
# Track progress
python3 scripts/task_manager_phase1.py mark-progress <task-id> 50

# Log time
python3 scripts/task_manager_phase1.py log-time <task-id> 45

# Block with reason
python3 scripts/task_manager_phase1.py mark-blocked <task-id> "Waiting on API key"

# Create recurring
python3 scripts/task_manager_phase1.py create-recurring <goal-id> "Weekly review" --recurring weekly

# Show velocity
python3 scripts/task_manager_phase1.py show-velocity <goal-id>
```

## 心跳集成

添加到 HEARTBEAT.md：

```markdown
## Proactive Tasks (Every heartbeat) 🚀

- [ ] Run `python3 skills/proactive-tasks/scripts/task_manager.py next-task`
- [ ] If task returned, work for 10-15 minutes
- [ ] Log progress and time: `mark-progress` + `log-time`
- [ ] If blocked, explain: `mark-blocked <id> "<reason>"`
- [ ] Message human with meaningful updates only
```

＃＃ 哲学

**不要等待被告知要做什么。**而是：

1. 检查哪些工作需要做
2. 自主地做
3.定期报告进展情况
4. 知道自己何时陷入困境并寻求帮助

这将代理从被动的工具转变为主动的合作伙伴。

＃＃ 比较

|特色 |主动任务 | Excel |概念 |吉拉 |
|--------|-----------------|--------|--------|-----|
|目标/任务层次结构 | ✅ | ❌ | ✅ | ✅ |
|进度 0-100% | ✅ | ✅ | ✅ | ✅ |
|时间追踪 | ✅ | ✅ | ⚠️ | ✅ |
|速度预测| ✅ | ❌ | ❌ | ✅ |
|重复性任务 | ✅ | ❌ | ⚠️ | ✅ |
|封锁原因 | ✅ | ❌ | ⚠️ | ✅ |
| **JSON（便携式）** | ✅ | ❌ | ❌ | ❌ |
| **CLI（自动化）** | ✅ | ❌ | ❌ | ⚠️ |
| **无依赖性** | ✅ | ❌ | ❌ | ❌ |

## 用例

**自主代理：**
- 无需等待提示即可实现目标
- 通过心跳报告进度
- 优雅地处理依赖关系和阻止程序
- 确切知道工作何时完成

**团队协调：**
- 团队领导分配目标
- 代理自主工作
- 速度预测时间线
- 堵塞很快就会浮现出来

**长期项目：**
- 将目标分解为可实现的任务
- 每周跟踪进度
- 随着时间的推移改进估计
- 庆祝里程碑

＃＃ 建筑学

受到 **Proactive Agent v3.1.0** 的启发：
- 清晰的关注点分离（CLI、数据、逻辑）
- JSON 存储以实现可移植性
- 最小的依赖性
- 可扩展的命令结构

**第一阶段**增加了生产功能：
- 进度粒度
- 时间指标
- 速度预测
- 重复自动化

**第二阶段**（计划中）：
- WAL协议（上下文保存）
- SESSION-STATE.md（活动工作内存）
- 自我修复（自动修复失败的任务）
- 进化护栏（VFM/ADL）

＃＃ 入门

1. **安装：** 复制到~/.openclaw/workspace/skills/proactive-tasks
2. **运行：** `python3 script/task_manager.py add-goal "我的第一个目标"`
3. **集成：** 添加到 HEARTBEAT.md 并开始工作

## 测试

```bash
# Test basic workflow
python3 scripts/task_manager.py add-goal "Test goal"
python3 scripts/task_manager.py add-task "Test goal" "Test task"
python3 scripts/task_manager.py next-task
python3 scripts/task_manager.py complete-task <id>

# Test Phase 1
python3 scripts/task_manager_phase1.py mark-progress <id> 50
python3 scripts/task_manager_phase1.py log-time <id> 30
python3 scripts/task_manager_phase1.py show-velocity <goal-id>
```

＃＃ 支持

**文件：**
- SKILL.md — 完整指南
- PHASE1-UPDATE.md — 新内容
- CLI_REFERENCE.md — 所有命令

**作者：** Toki (toki@openclaw.ai)  
**许可证：** 麻省理工学院  
**存储库：** github.com/ImrKhn03/proactive-tasks（即将推出）

---

## 版本历史

**v1.1.0** (2026-02-12)
- ✨ 进度跟踪（0-100%）
- ✨ 时间记录和方差
- ✨ 重复任务（每日/每周/每月）
- ✨ 有原因的封锁
- ✨ 速度预测
- 📝 第一阶段文档

**v1.0.0** (2026-02-05)
- ✨ 目标和任务管理
- ✨ 任务依赖关系
- ✨ 优先级
- ✨ 状态追踪
- ✨ 心跳整合

---

**准备生产。经过自主代理的战斗测试。受到行业领导者的启发。**
