# 基于文件的通信协议

有关协调器和子代理如何通过文件进行通信的规范。

## 目录结构

每个代理都有一个标准化的工作空间：

```
agent-workspace/
├── SKILL.md           # Agent's skill definition (read-only for agent)
├── inbox/             # Input from orchestrator → agent
│   ├── instructions.md    # Task description and requirements
│   └── [input files]      # Any files needed for the task
├── outbox/            # Output from agent → orchestrator
│   └── [deliverables]     # Task outputs
├── workspace/         # Agent's private working area
│   └── [temp files]       # Intermediate work products
└── status.json        # Agent state tracking
```

## 状态文件规范

PH12 跟踪代理生命周期：

```json
{
  "state": "pending|running|completed|failed",
  "started": "2024-01-15T10:30:00Z",
  "completed": "2024-01-15T11:45:00Z",
  "error": null,
  "progress": {
    "current_step": "analyzing_data",
    "steps_completed": 3,
    "total_steps": 5
  },
  "metrics": {
    "files_processed": 12,
    "outputs_generated": 4
  }
}
```

### 状态转换

```
pending → running → completed
                 ↘ failed
```

**状态定义：**
- `pending`: Agent created but not yet started
- `running`: Agent actively working on task
- `completed`: Agent finished successfully
- `failed`: Agent encountered unrecoverable error

### 更新协议

1. **Orchestrator 设置**初始状态为 PH17
2. **开始工作时代理更新**至PH18
3. **完成后代理更新**至 PH19 或 PH20
4. **编排器读取**以确定下一步操作

## 收件箱协议

### instructions.md 格式

```markdown
# Task: {TASK_NAME}

## Objective
{Clear statement of what needs to be accomplished}

## Context
{Background information relevant to the task}

## Inputs Provided
- `input_file_1.txt` - Description of what this contains
- `data/` - Directory containing...

## Requirements
1. {Specific requirement 1}
2. {Specific requirement 2}

## Success Criteria
- [ ] {Measurable outcome 1}
- [ ] {Measurable outcome 2}

## Constraints
- {Time/resource constraints}
- {Quality standards}

## Output Expectations
- Place main deliverable in `outbox/{filename}`
- Include summary in `outbox/summary.md`
```

### 文件传输规则

- Orchestrator 将所有需要的文件复制到 PH21
- 代理将 PH22 视为只读
- 原始文件保留在 Orchestrator 中
- 大文件：使用引用/路径而不是副本

## 发件箱协议

### 所需的输出

每个代理必须至少提供：
1. **主要可交付成果** - 实际工作产品
2. **summary.md** - 所做工作的简要总结

### 可选输出

- `changelog.md` - Detailed log of actions taken
- `issues.md` - Problems encountered and how resolved
- `metadata.json` - Structured data about outputs

### 输出命名约定

```
outbox/
├── {primary_deliverable}.{ext}
├── summary.md
├── data/           # If multiple data outputs
│   ├── file1.csv
│   └── file2.json
└── metadata.json
```

## 工作区协议

PH26目录是代理的私有区域：

- **代理可以创建**处理所需的任何文件
- **Orchestrator 在收集期间忽略**此目录
- **清理可选** - 客服人员可以离开或清理工作空间
- **对于**中间结果、缓存、临时文件有用

## 错误处理

### 失败协议

当代理失败时：

1.更新PH27：
```json
{
  "state": "failed",
  "error": {
    "type": "ValidationError",
    "message": "Input file format invalid",
    "details": "Expected CSV, got JSON",
    "recoverable": true
  }
}
```

2.写入PH28：
```markdown
# Error Report

## Error Type
ValidationError

## Description
Input file format was invalid. Expected CSV format but received JSON.

## Attempted Recovery
Tried to convert JSON to CSV but data structure incompatible.

## Suggested Resolution
Provide input as CSV with columns: id, name, value

## Partial Work
Any completed work before failure is in outbox/partial/
```

### 恢复选项

协调器可以：
1. **重试** - 使用相同的输入重新运行
2. **修复并重试** - 正确输入并重新运行
3. **跳过** - 标记为失败，继续使用其他代理
4. **升级** - 请求人工干预

## 依赖处理

当智能体依赖彼此的输出时：

### 清单文件

Orchestrator 创建 PH29 ：

```json
{
  "depends_on": [
    {
      "agent": "data-collector",
      "outputs": ["outbox/data.json", "outbox/sources.md"],
      "copy_to": "inbox/source_data/"
    }
  ],
  "wait_for": ["data-collector", "schema-validator"]
}
```

### 顺序执行

```python
# Orchestrator pattern for dependencies
def execute_with_dependencies(agent, dependencies):
    # Wait for all dependencies
    for dep in dependencies:
        while not is_completed(dep):
            wait()

    # Copy dependency outputs to agent inbox
    for dep in dependencies:
        copy_outputs(dep.outbox, agent.inbox)

    # Start agent
    spawn_agent(agent)
```

## 并行执行

独立代理可以同时运行：

```python
# Spawn all independent agents at once
parallel_agents = identify_independent_agents(task_graph)
for agent in parallel_agents:
    spawn_agent(agent)  # Non-blocking

# Wait for all to complete
while not all_completed(parallel_agents):
    check_status_periodically()
```

## 消息传递模式

对于复杂的代理间通信：

### 共享消息队列（可选）

```
orchestrator-workspace/
└── messages/
    ├── {agent-a}_to_{agent-b}_001.json
    └── {agent-b}_to_{agent-a}_002.json
```

消息格式：
```json
{
  "from": "agent-a",
  "to": "agent-b",
  "timestamp": "2024-01-15T10:30:00Z",
  "type": "data_ready|question|answer|update",
  "content": { ... }
}
```

注意：对于完全自主的代理，更喜欢通过收件箱/发件箱进行单向通信，而不是消息传递。
