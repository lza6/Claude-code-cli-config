# 参考：Manus 上下文工程原理

这项技能基于 Manus 的上下文工程原理，Manus 是一家人工智能代理公司，于 2025 年 12 月被 Meta 以 20 亿美元收购。

## 马努斯的​​ 6 项原则

### 原则 1：围绕 KV-Cache 进行设计

> “KV 缓存命中率是生产 AI 代理最重要的指标。”

**统计数据：**
- ~100:1 输入输出代币比率
- 缓存代币：$0.30/MTok 与未缓存代币：$3/MTok
- 10倍的成本差异！

**实施：**
- 保持提示前缀稳定（单个令牌更改会使缓存失效）
- 系统提示中没有时间戳
- 通过确定性序列化使上下文仅附加

### 原则 2：遮盖，不要摘除

不要动态删除工具（破坏 KV 缓存）。请改用 logit 掩码。

**最佳实践：** 使用一致的操作前缀（例如“browser_”、“shell_”、“file_”）以便于屏蔽。

### 原则 3：文件系统作为外部存储器

> “Markdown 是我在磁盘上的‘工作内存’。”

**公式：**
```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)
```

**压缩必须可恢复：**
- 即使网页内容被删除也保留 URL
- 删除文档内容时保留文件路径
- 永远不会丢失指向完整数据的指针

### 原则 4：通过背诵控制注意力

> “在整个任务中创建并更新 todo.md，以将全局计划纳入模型的近期关注范围内。”

**问题：** 在约 50 次工具调用后，模型忘记了最初的目标（“迷失在中间”效应）。

**解决方案：** 在每个决定之前重新阅读`task_plan.md`。目标出现在关注窗口中。

```
Start of context: [Original goal - far away, forgotten]
...many tool calls...
End of context: [Recently read task_plan.md - gets ATTENTION!]
```

### 原则 5：保留错误的内容

> “在上下文中留下错误的转折。”

**为什么：**
- 带有堆栈跟踪的失败操作让模型隐式更新信念
- 减少重复错误
- 错误恢复是“真正的代理行为的最清晰信号之一”

### 原则 6：不要少射

> “统一滋生脆弱。”

**问题：** 重复的动作-观察对会导致漂移和幻觉。

**解决方案：** 引入受控变化：
- 稍微改变措辞
- 不要盲目复制粘贴模式
- 重新校准重复性任务

---

## 3 个上下文工程策略

基于 Lance Martin 对 Manus 架构的分析。

### 策略 1：上下文缩减

**压实：**
```
Tool calls have TWO representations:
├── FULL: Raw tool content (stored in filesystem)
└── COMPACT: Reference/file path only

RULES:
- Apply compaction to STALE (older) tool results
- Keep RECENT results FULL (to guide next decision)
```

**总结：**
- 当压实达到收益递减时应用
- 使用完整工具结果生成
- 创建标准化摘要对象

### 策略 2：上下文隔离（多代理）

**建筑学：**
```
┌─────────────────────────────────┐
│         PLANNER AGENT           │
│  └─ Assigns tasks to sub-agents │
├─────────────────────────────────┤
│       KNOWLEDGE MANAGER         │
│  └─ Reviews conversations       │
│  └─ Determines filesystem store │
├─────────────────────────────────┤
│      EXECUTOR SUB-AGENTS        │
│  └─ Perform assigned tasks      │
│  └─ Have own context windows    │
└─────────────────────────────────┘
```

**关键见解：** Manus 最初使用“todo.md”进行任务规划，但发现约 33% 的操作用于更新它。转移到专门的计划代理调用执行子代理。

### 策略 3：上下文卸载

**工具设计：**
- 总共使用 <20 个原子函数
- 将完整结果存储在文件系统中，而不是上下文中
- 使用`glob`和`grep`进行搜索
- 渐进式披露：仅根据需要加载信息

---

## 代理循环

Manus 以连续的 7 步循环运行：

```
┌─────────────────────────────────────────┐
│  1. ANALYZE CONTEXT                      │
│     - Understand user intent             │
│     - Assess current state               │
│     - Review recent observations         │
├─────────────────────────────────────────┤
│  2. THINK                                │
│     - Should I update the plan?          │
│     - What's the next logical action?    │
│     - Are there blockers?                │
├─────────────────────────────────────────┤
│  3. SELECT TOOL                          │
│     - Choose ONE tool                    │
│     - Ensure parameters available        │
├─────────────────────────────────────────┤
│  4. EXECUTE ACTION                       │
│     - Tool runs in sandbox               │
├─────────────────────────────────────────┤
│  5. RECEIVE OBSERVATION                  │
│     - Result appended to context         │
├─────────────────────────────────────────┤
│  6. ITERATE                              │
│     - Return to step 1                   │
│     - Continue until complete            │
├─────────────────────────────────────────┤
│  7. DELIVER OUTCOME                      │
│     - Send results to user               │
│     - Attach all relevant files          │
└─────────────────────────────────────────┘
```

---

## Manus 创建的文件类型

|文件 |目的|创建时间 |何时更新 |
|------|---------|--------------|------------||
| `task_plan.md` |阶段跟踪、进展 |任务开始 |完成阶段后 |
| `调查结果.md` |发现、决定|任何发现之后 |查看图像/PDF 后 |
| `progress.md` |会话日志，做了什么 |在断点处|整个会议期间|
|代码文件|实施|执行前|错误之后 |

---

## 关键限制

- **单动作执行：** 每回合调用一个工具。没有并行执行。
- **需要计划：** 代理必须始终知道：目标、当前阶段、剩余阶段
- **文件是内存：**上下文=易失性。文件系统=持久性。
- **永不重复失败：** 如果操作失败，下一个操作必须不同
- **通信是一种工具：**消息类型：`info`（进度）、`ask`（阻塞）、`result`（终端）

---

## 手册统计

|公制|价值|
|--------|--------|
|每个任务的平均工具调用次数 | 〜50 |
|输入输出代币比率| 100：1 |
|收购价格| 20 亿美元 |
|收入达到 1 亿美元的时间到了 | 8 个月 |
|自推出以来的框架重构 | 5 次 |

---

## 关键名言

> “上下文窗口 = RAM（易失性、有限）。文件系统 = 磁盘（持久、无限制）。任何重要的内容都会写入磁盘。”

>“if action_failed: next_action != same_action。跟踪您尝试过的操作。改变方法。”

> “错误恢复是真正代理行为的最清晰信号之一。”

> “KV 缓存命中率是生产阶段 AI 代理最重要的指标。”

> “在上下文中留下错误的转折。”

---

＃＃ 来源

基于Manus的官方上下文工程文档：
https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
