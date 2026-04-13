---
name: planning-with-files
version: "2.10.0"
description: '为复杂任务实现 Manus 风格的基于文件的规划。**Auto-trigger**: 复杂多步骤任务、研究项目、或需要 >5 次工具调用时自动使用。创建 task_plan.md, findings.md, progress.md。'
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
hooks:
  PreToolUse:
    - matcher: "Write|Edit|Bash|Read|Glob|Grep"
      hooks:
        - type: command
          command: "cat task_plan.md 2>/dev/null | head -30 || true"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "echo '[planning-with-files] File updated. If this completes a phase, update task_plan.md status.'"
  Stop:
    - hooks:
        - type: command
          command: |
            SCRIPT_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/planning-with-files}/scripts"

            IS_WINDOWS=0
            if [ "${OS-}" = "Windows_NT" ]; then
              IS_WINDOWS=1
            else
              UNAME_S="$(uname -s 2>/dev/null || echo '')"
              case "$UNAME_S" in
                CYGWIN*|MINGW*|MSYS*) IS_WINDOWS=1 ;;
              esac
            fi

            if [ "$IS_WINDOWS" -eq 1 ]; then
              if command -v pwsh >/dev/null 2>&1; then
                pwsh -ExecutionPolicy Bypass -File "$SCRIPT_DIR/check-complete.ps1" 2>/dev/null ||
                powershell -ExecutionPolicy Bypass -File "$SCRIPT_DIR/check-complete.ps1" 2>/dev/null ||
                sh "$SCRIPT_DIR/check-complete.sh"
              else
                powershell -ExecutionPolicy Bypass -File "$SCRIPT_DIR/check-complete.ps1" 2>/dev/null ||
                sh "$SCRIPT_DIR/check-complete.sh"
              fi
            else
              sh "$SCRIPT_DIR/check-complete.sh"
            fi
---

# 使用文件进行规划

像 Manus 一样工作：使用持久化的 Markdown 文件作为"磁盘上的工作记忆"。

## 第一步：检查之前的会话（v2.2.0）

**开始工作之前**，检查是否有来自之前会话的未同步上下文：

```bash
# Linux/macOS
$(command -v python3 || command -v python) ${CLAUDE_PLUGIN_ROOT}/scripts/session-catchup.py "$(pwd)"
```

```powershell
# Windows PowerShell
& (Get-Command python -ErrorAction SilentlyContinue).Source "$env:USERPROFILE\.claude\skills\planning-with-files\scripts\session-catchup.py" (Get-Location)
```

如果追赶报告包含未同步的上下文：
1. 运行 `git diff --stat` 查看实际的代码变更
2. 读取当前的规划文件
3. 根据追赶报告和 git diff 更新规划文件
4. 然后继续执行任务

## 重要说明：文件的存放位置

- **模板**位于 `${CLAUDE_PLUGIN_ROOT}/templates/`
- **你的规划文件**存放在**你的项目目录**中

| 位置 | 存放内容 |
|----------|-----------------|
| 技能目录（`${CLAUDE_PLUGIN_ROOT}/`） | 模板、脚本、参考文档 |
| 你的项目目录 | `task_plan.md`、`findings.md`、`progress.md` |

## 快速开始

在任何复杂任务之前：

1. **创建 `task_plan.md`** — 参考 [templates/task_plan.md](templates/task_plan.md) 模板
2. **创建 `findings.md`** — 参考 [templates/findings.md](templates/findings.md) 模板
3. **创建 `progress.md`** — 参考 [templates/progress.md](templates/progress.md) 模板
4. **做决策前重新读取计划** — 刷新注意力窗口中的目标
5. **每个阶段后更新** — 标记完成，记录错误

> **注意：** 规划文件放在项目根目录，而非技能安装目录。

## 核心模式

```
上下文窗口 = 内存（易失性，容量有限）
文件系统 = 磁盘（持久化，容量无限）

→ 任何重要内容都要写入磁盘。
```

## 文件用途

| 文件 | 用途 | 何时更新 |
|------|---------|----------------|
| `task_plan.md` | 阶段、进度、决策 | 每个阶段完成后 |
| `findings.md` | 研究、发现 | 每次发现后 |
| `progress.md` | 会话日志、测试结果 | 整个会话期间 |

## 关键规则

### 1. 首先创建计划
复杂任务没有 `task_plan.md` 绝不开始。没有例外。

### 2. 两步规则
> "每进行 2 次查看/浏览/搜索操作后，立即将关键发现保存到文本文件。"

这可以防止视觉/多模态信息丢失。

### 3. 决策前先阅读
在做重大决策之前，读取计划文件。这能让目标保持在注意力窗口中。

### 4. 行动后更新
完成任何阶段后：
- 标记阶段状态：`in_progress` → `complete`
- 记录遇到的任何错误
- 记录已创建/修改的文件

### 5. 记录所有错误
每个错误都要记录在计划文件中。这能积累知识并防止重复犯错。

```markdown
## 遇到的错误
| 错误 | 尝试次数 | 解决方案 |
|-------|---------|------------|
| FileNotFoundError | 1 | 创建了默认配置文件 |
| API timeout | 2 | 添加了重试逻辑 |
```

### 6. 绝不重复失败的操作
```
if action_failed:
    next_action != same_action
```
跟踪你尝试过的内容。改变方法。

## 三次失败协议

```
尝试 1：诊断与修复
  → 仔细阅读错误信息
  → 识别根本原因
  → 应用针对性修复

尝试 2：替代方案
  → 同样的错误？换不同的方法
  → 换工具？换库？
  → 绝不要重复完全相同的失败操作

尝试 3：更广泛的反思
  → 质疑假设
  → 搜索解决方案
  → 考虑更新计划

3 次失败后：升级给用户
  → 说明你尝试了什么
  → 分享具体的错误信息
  → 请求指导
```

## 读取 vs 写入决策矩阵

| 情况 | 操作 | 原因 |
|-----------|--------|--------|
| 刚写了一个文件 | 不要读取 | 内容仍在上下文中 |
| 查看了图片/PDF | 立即写入发现 | 多模态信息 → 转为文本以防丢失 |
| 浏览器返回了数据 | 写入文件 | 截图不会持久化 |
| 开始新阶段 | 读取计划/发现 | 上下文过时时重新定位 |
| 发生错误 | 读取相关文件 | 需要当前状态来修复 |
| 间隔后恢复 | 读取所有规划文件 | 恢复状态 |

## 五问重启测试

如果你能回答这些问题，说明你的上下文管理很扎实：

| 问题 | 答案来源 |
|----------|---------------|
| 我在哪？ | task_plan.md 中的当前阶段 |
| 我要去哪？ | 剩余阶段 |
| 目标是什么？ | 计划中的目标陈述 |
| 我学到了什么？ | findings.md |
| 我做了什么？ | progress.md |

## 何时使用此模式

**适用于：**
- 多步骤任务（3 步及以上）
- 研究任务
- 构建/创建项目
- 需要大量工具调用的任务
- 任何需要组织的任务

**可跳过：**
- 简单问题
- 单文件编辑
- 快速查找

## 模板

开始时复制这些模板：

- [templates/task_plan.md](templates/task_plan.md) — 阶段跟踪
- [templates/findings.md](templates/findings.md) — 研究存储
- [templates/progress.md](templates/progress.md) — 会话日志

## 脚本

辅助自动化脚本：

- `scripts/init-session.sh` — 初始化所有规划文件
- `scripts/check-complete.sh` — 验证所有阶段是否完成
- `scripts/session-catchup.py` — 从之前的会话恢复上下文（v2.2.0）

## 高级主题

- **Manus 原则：** 参见 [reference.md](reference.md)
- **实际示例：** 参见 [examples.md](examples.md)

## 反模式

| 不要这样做 | 应该这样做 |
|-------|------------|
| 用 TodoWrite 做持久化 | 创建 task_plan.md 文件 |
| 声明一次目标就忘记 | 决策前重新读取计划 |
| 隐藏错误并静默重试 | 将错误记录到计划文件 |
| 把所有内容塞进上下文 | 将大型内容存储在文件中 |
| 立即开始执行 | 首先创建计划文件 |
| 重复失败的操作 | 跟踪尝试次数，改变方法 |
| 在技能目录中创建文件 | 在项目目录中创建文件 |
