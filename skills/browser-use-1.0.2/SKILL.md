---
name: browser-use
description: 'Automates browser interactions. **Auto-trigger**: 当用户需要浏览网页、填表、截图、数据抓取、自动化测试时自动使用。'
allowed-tools: Bash(browser-use:*)
---

# 使用 browser-use CLI 进行浏览器自动化

`browser-use` 命令提供快速、持久的浏览器自动化功能。它跨命令保持浏览器会话，支持复杂的多步骤工作流。

## 前置条件

在使用此技能之前，必须先安装并配置 `browser-use`。运行诊断命令进行验证：

```bash
browser-use doctor
```

更多信息，请访问 https://github.com/browser-use/browser-use/blob/main/browser_use/skill_cli/README.md

## 核心工作流

1. **导航**: `browser-use open <url>` - 打开 URL（如需要则启动浏览器）
2. **检查**: `browser-use state` - 返回可点击元素及其索引
3. **交互**: 使用 state 返回的索引进行交互（`browser-use click 5`、`browser-use input 3 "text"`）
4. **验证**: `browser-use state` 或 `browser-use screenshot` 确认操作结果
5. **重复**: 浏览器在命令之间保持打开状态

## 浏览器模式

```bash
browser-use --browser chromium open <url>      # 默认：无头 Chromium
browser-use --browser chromium --headed open <url>  # 可见的 Chromium 窗口
browser-use --browser real open <url>          # 真实 Chrome（无 profile = 全新）
browser-use --browser real --profile "Default" open <url>  # 带登录会话的真实 Chrome
browser-use --browser remote open <url>        # 云端浏览器
```

- **chromium**: 快速、隔离、默认无头模式
- **real**: 使用真实 Chrome 二进制文件。不带 `--profile` 时，使用持久但空的 CLI profile（位于 `~/.config/browseruse/profiles/cli/`）。带 `--profile "ProfileName"` 时，复制你实际的 Chrome profile（Cookie、登录信息、扩展）
- **remote**: 云端托管浏览器，支持代理

## 基本命令

```bash
# 导航
browser-use open <url>                    # 导航到 URL
browser-use back                          # 后退
browser-use scroll down                   # 向下滚动（--amount N 指定像素数）

# 页面状态（始终先运行 state 获取元素索引）
browser-use state                         # 获取 URL、标题、可点击元素
browser-use screenshot                    # 截图（base64 格式）
browser-use screenshot path.png           # 将截图保存到文件

# 交互（使用 state 返回的索引）
browser-use click <index>                 # 点击元素
browser-use type "text"                   # 向焦点元素输入文本
browser-use input <index> "text"          # 点击元素，然后输入
browser-use keys "Enter"                  # 发送键盘按键
browser-use select <index> "option"       # 选择下拉菜单选项

# 数据提取
browser-use eval "document.title"         # 执行 JavaScript
browser-use get text <index>              # 获取元素文本
browser-use get html --selector "h1"      # 获取限定范围的 HTML

# 等待
browser-use wait selector "h1"            # 等待元素出现
browser-use wait text "Success"           # 等待文本出现

# 会话
browser-use sessions                      # 列出活跃会话
browser-use close                         # 关闭当前会话
browser-use close --all                   # 关闭所有会话

# AI Agent
browser-use -b remote run "task"          # 在云端运行 agent（默认异步）
browser-use task status <id>              # 检查云端任务进度
```

## 命令

### 导航与标签页
```bash
browser-use open <url>                    # 导航到 URL
browser-use back                          # 后退历史记录
browser-use scroll down                   # 向下滚动
browser-use scroll up                     # 向上滚动
browser-use scroll down --amount 1000     # 按指定像素滚动（默认：500）
browser-use switch <tab>                  # 按索引切换到标签页
browser-use close-tab                     # 关闭当前标签页
browser-use close-tab <tab>              # 关闭指定标签页
```

### 页面状态
```bash
browser-use state                         # 获取 URL、标题和可点击元素
browser-use screenshot                    # 截图（输出 base64）
browser-use screenshot path.png           # 将截图保存到文件
browser-use screenshot --full path.png    # 全页面截图
```

### 交互
```bash
browser-use click <index>                 # 点击元素
browser-use type "text"                   # 向焦点元素输入文本
browser-use input <index> "text"          # 点击元素，然后输入文本
browser-use keys "Enter"                  # 发送键盘按键
browser-use keys "Control+a"              # 发送组合键
browser-use select <index> "option"       # 选择下拉菜单选项
browser-use hover <index>                 # 悬停在元素上（触发 CSS :hover）
browser-use dblclick <index>              # 双击元素
browser-use rightclick <index>            # 右键点击元素（上下文菜单）
```

使用 `browser-use state` 返回的索引。

### JavaScript 与数据
```bash
browser-use eval "document.title"         # 执行 JavaScript，返回结果
browser-use get title                     # 获取页面标题
browser-use get html                      # 获取完整页面 HTML
browser-use get html --selector "h1"      # 获取指定元素的 HTML
browser-use get text <index>              # 获取元素的文本内容
browser-use get value <index>             # 获取 input/textarea 的值
browser-use get attributes <index>        # 获取元素的所有属性
browser-use get bbox <index>              # 获取边界框（x, y, 宽, 高）
```

### Cookie
```bash
browser-use cookies get                   # 获取所有 Cookie
browser-use cookies get --url <url>       # 获取指定 URL 的 Cookie
browser-use cookies set <name> <value>    # 设置 Cookie
browser-use cookies set name val --domain .example.com --secure --http-only
browser-use cookies set name val --same-site Strict  # SameSite: Strict、Lax 或 None
browser-use cookies set name val --expires 1735689600  # 过期时间戳
browser-use cookies clear                 # 清除所有 Cookie
browser-use cookies clear --url <url>     # 清除指定 URL 的 Cookie
browser-use cookies export <file>         # 将所有 Cookie 导出到 JSON 文件
browser-use cookies export <file> --url <url>  # 导出指定 URL 的 Cookie
browser-use cookies import <file>         # 从 JSON 文件导入 Cookie
```

### 等待条件
```bash
browser-use wait selector "h1"            # 等待元素可见
browser-use wait selector ".loading" --state hidden  # 等待元素消失
browser-use wait selector "#btn" --state attached    # 等待元素出现在 DOM 中
browser-use wait text "Success"           # 等待文本出现
browser-use wait selector "h1" --timeout 5000  # 自定义超时时间（毫秒）
```

### Python 执行
```bash
browser-use python "x = 42"               # 设置变量
browser-use python "print(x)"             # 访问变量（输出：42）
browser-use python "print(browser.url)"   # 访问 browser 对象
browser-use python --vars                 # 显示已定义变量
browser-use python --reset                # 清除 Python 命名空间
browser-use python --file script.py       # 执行 Python 文件
```

Python 会话跨命令保持状态。`browser` 对象提供：
- `browser.url`、`browser.title`、`browser.html` — 页面信息
- `browser.goto(url)`、`browser.back()` — 导航
- `browser.click(index)`、`browser.type(text)`、`browser.input(index, text)`、`browser.keys(keys)` — 交互
- `browser.screenshot(path)`、`browser.scroll(direction, amount)` — 视觉操作
- `browser.wait(seconds)`、`browser.extract(query)` — 工具方法

### Agent 任务

#### 远程模式选项

使用 `--browser remote` 时，可使用以下额外选项：

```bash
# 指定 LLM 模型
browser-use -b remote run "task" --llm gpt-4o
browser-use -b remote run "task" --llm claude-sonnet-4-20250514

# 代理配置（默认：us）
browser-use -b remote run "task" --proxy-country uk

# 会话复用
browser-use -b remote run "task 1" --keep-alive        # 任务完成后保持会话
browser-use -b remote run "task 2" --session-id abc-123 # 复用现有会话

# 执行模式
browser-use -b remote run "task" --flash       # 快速执行模式
browser-use -b remote run "task" --wait        # 等待完成（默认：异步）

# 高级选项
browser-use -b remote run "task" --thinking    # 扩展推理模式
browser-use -b remote run "task" --no-vision   # 禁用视觉（默认启用）

# 使用云端 profile（先创建会话，然后用 --session-id 运行）
browser-use session create --profile <cloud-profile-id> --keep-alive
# → 返回 session_id
browser-use -b remote run "task" --session-id <session-id>

# 任务配置
browser-use -b remote run "task" --start-url https://example.com  # 从指定 URL 开始
browser-use -b remote run "task" --allowed-domain example.com     # 限制导航（可重复）
browser-use -b remote run "task" --metadata key=value             # 任务元数据（可重复）
browser-use -b remote run "task" --skill-id skill-123             # 启用技能（可重复）
browser-use -b remote run "task" --secret key=value               # 秘密元数据（可重复）

# 结构化输出与评估
browser-use -b remote run "task" --structured-output '{"type":"object"}'  # 输出的 JSON schema
browser-use -b remote run "task" --judge                 # 启用评判模式
browser-use -b remote run "task" --judge-ground-truth "expected answer"
```

### 任务管理
```bash
browser-use task list                     # 列出最近任务
browser-use task list --limit 20          # 显示更多任务
browser-use task list --status finished   # 按状态过滤（finished, stopped）
browser-use task list --session <id>      # 按会话 ID 过滤
browser-use task list --json              # JSON 输出

browser-use task status <task-id>         # 获取任务状态（仅最新步骤）
browser-use task status <task-id> -c      # 所有步骤含推理过程
browser-use task status <task-id> -v      # 所有步骤含 URL 和操作
browser-use task status <task-id> --last 5  # 仅最后 N 步
browser-use task status <task-id> --step 3  # 指定步骤编号
browser-use task status <task-id> --reverse # 最新的在前

browser-use task stop <task-id>           # 停止运行中的任务
browser-use task logs <task-id>           # 获取任务执行日志
```

### 云端会话管理
```bash
browser-use session list                  # 列出云端会话
browser-use session list --limit 20       # 显示更多会话
browser-use session list --status active  # 按状态过滤
browser-use session list --json           # JSON 输出

browser-use session get <session-id>      # 获取会话详情 + 实时 URL
browser-use session get <session-id> --json

browser-use session stop <session-id>     # 停止会话
browser-use session stop --all            # 停止所有活跃会话

browser-use session create                          # 使用默认值创建
browser-use session create --profile <id>           # 使用云端 profile
browser-use session create --proxy-country uk       # 使用地理代理
browser-use session create --start-url https://example.com
browser-use session create --screen-size 1920x1080
browser-use session create --keep-alive
browser-use session create --persist-memory

browser-use session share <session-id>              # 创建公开分享 URL
browser-use session share <session-id> --delete     # 删除公开分享
```

### 隧道
```bash
browser-use tunnel <port>           # 启动隧道（返回 URL）
browser-use tunnel <port>           # 幂等 - 返回现有 URL
browser-use tunnel list             # 显示活跃隧道
browser-use tunnel stop <port>      # 停止隧道
browser-use tunnel stop --all       # 停止所有隧道
```

### 会话管理
```bash
browser-use sessions                      # 列出活跃会话
browser-use close                         # 关闭当前会话
browser-use close --all                   # 关闭所有会话
```

### Profile 管理

#### 本地 Chrome Profile（`--browser real`）
```bash
browser-use -b real profile list          # 列出本地 Chrome profile
browser-use -b real profile cookies "Default"  # 显示 profile 中的 Cookie 域名
```

#### 云端 Profile（`--browser remote`）
```bash
browser-use -b remote profile list            # 列出云端 profile
browser-use -b remote profile list --page 2 --page-size 50
browser-use -b remote profile get <id>        # 获取 profile 详情
browser-use -b remote profile create          # 创建新的云端 profile
browser-use -b remote profile create --name "My Profile"
browser-use -b remote profile update <id> --name "New"
browser-use -b remote profile delete <id>
```

#### 同步
```bash
browser-use profile sync --from "Default" --domain github.com  # 指定域名
browser-use profile sync --from "Default"                      # 完整 profile
browser-use profile sync --from "Default" --name "Custom Name" # 自定义名称
```

## 服务器控制
```bash
browser-use server logs                   # 查看服务器日志
```

## 常见工作流

### 暴露本地开发服务器

当你有本地开发服务器且需要云端浏览器访问时使用。

**核心工作流：** 启动开发服务器 → 创建隧道 → 远程浏览隧道 URL。

```bash
# 1. 启动你的开发服务器
npm run dev &  # localhost:3000

# 2. 通过 Cloudflare 隧道暴露
browser-use tunnel 3000
# → url: https://abc.trycloudflare.com

# 3. 现在云端浏览器可以访问你的本地服务器了
browser-use --browser remote open https://abc.trycloudflare.com
browser-use state
browser-use screenshot
```

**注意：** 隧道与会话独立。它们在 `browser-use close` 后仍然存活，可单独管理。必须先安装 Cloudflared — 运行 `browser-use doctor` 检查。

### 使用 Profile 进行认证浏览

当任务需要浏览用户已登录的网站时使用（例如 Gmail、GitHub、内部工具）。

**核心工作流：** 检查现有 profile → 询问用户使用哪种模式和哪个 profile → 使用该 profile 浏览。仅在不存在合适 profile 时同步 Cookie。

**在浏览认证网站之前，Agent 必须：**
1. 询问用户使用 **real**（本地 Chrome）还是 **remote**（云端）浏览器
2. 列出该模式下可用的 profile
3. 询问使用哪个 profile
4. 如果没有 profile 包含正确的 Cookie，提供同步选项（见下文）

#### 步骤 1：检查现有 profile

```bash
# 选项 A：本地 Chrome profile（--browser real）
browser-use -b real profile list
# → Default: Person 1 (user@gmail.com)
# → Profile 1: Work (work@company.com)

# 选项 B：云端 profile（--browser remote）
browser-use -b remote profile list
# → abc-123: "Chrome - Default (github.com)"
# → def-456: "Work profile"
```

#### 步骤 2：使用选定的 profile 浏览

```bash
# 真实浏览器 — 使用本地 Chrome 中的现有登录会话
browser-use --browser real --profile "Default" open https://github.com

# 云端浏览器 — 使用带同步 Cookie 的云端 profile
browser-use --browser remote --profile abc-123 open https://github.com
```

用户已经通过认证 — 无需再次登录。

**注意：** 云端 profile 的 Cookie 可能会过期。如果认证失败，请从本地 Chrome profile 重新同步 Cookie。

#### 步骤 3：同步 Cookie（仅在需要时）

如果用户想使用云端浏览器但没有云端 profile 包含正确的 Cookie，请从本地 Chrome profile 同步。

**同步之前，Agent 必须：**
1. 询问使用哪个本地 Chrome profile
2. 询问要同步哪些域名 — 不要默认同步完整 profile
3. 确认后再继续

**检查本地 profile 有哪些 Cookie：**
```bash
browser-use -b real profile cookies "Default"
# → youtube.com: 23
# → google.com: 18
# → github.com: 2
```

**指定域名同步（推荐）：**
```bash
browser-use profile sync --from "Default" --domain github.com
# 创建新的云端 profile: "Chrome - Default (github.com)"
# 仅同步 github.com 的 Cookie
```

**完整 profile 同步（谨慎使用）：**
```bash
browser-use profile sync --from "Default"
# 同步所有 Cookie — 包含敏感数据、跟踪 Cookie、每个会话令牌
```
仅在用户明确需要完整浏览器状态时使用。

**细粒度控制（高级）：**
```bash
# 将 Cookie 导出到文件，手动编辑，然后导入
browser-use --browser real --profile "Default" cookies export /tmp/cookies.json
browser-use --browser remote --profile <id> cookies import /tmp/cookies.json
```

**使用同步后的 profile：**
```bash
browser-use --browser remote --profile <id> open https://github.com
```

### 运行子 Agent

使用云端会话并行运行自主浏览器 Agent。

**核心工作流：** 用 `run` 启动任务 → 用 `task status` 轮询 → 收集结果 → 清理会话。

- **会话 = Agent**：每个云端会话是一个独立的浏览器 Agent，拥有自己的状态
- **任务 = 工作**：分配给 Agent 的任务；一个 Agent 可以顺序运行多个任务
- **会话生命周期**：一旦停止，会话无法恢复 — 需要启动新会话

#### 启动任务

```bash
# 单个任务（默认异步 — 立即返回）
browser-use -b remote run "搜索 AI 新闻并总结前 3 篇文章"
# → task_id: task-abc, session_id: sess-123

# 并行任务 — 每个任务获得独立会话
browser-use -b remote run "研究竞品 A 定价"
# → task_id: task-1, session_id: sess-a
browser-use -b remote run "研究竞品 B 定价"
# → task_id: task-2, session_id: sess-b
browser-use -b remote run "研究竞品 C 定价"
# → task_id: task-3, session_id: sess-c

# 同一会话中的顺序任务（复用 Cookie、登录状态等）
browser-use -b remote run "登录 example.com" --keep-alive
# → task_id: task-1, session_id: sess-123
browser-use task status task-1  # 等待完成
browser-use -b remote run "导出设置" --session-id sess-123
# → task_id: task-2, session_id: sess-123（同一会话）
```

#### 管理与停止

```bash
browser-use task list --status finished      # 查看已完成的任务
browser-use task stop task-abc               # 停止任务（如使用 --keep-alive 会话可能继续）
browser-use session stop sess-123            # 停止整个会话（终止其所有任务）
browser-use session stop --all               # 停止所有会话
```

#### 监控

**任务状态设计为节省令牌。** 默认输出最简化 — 仅在需要时展开：

| 模式 | 标志 | 令牌消耗 | 使用时机 |
|------|------|----------|----------|
| 默认 | （无） | 低 | 轮询进度 |
| 紧凑 | `-c` | 中 | 需要完整推理 |
| 详细 | `-v` | 高 | 调试操作 |

```bash
# 对于长时间任务（50+ 步）
browser-use task status <id> -c --last 5   # 仅最后 5 步
browser-use task status <id> -v --step 10  # 检查特定步骤
```

**实时视图**：`browser-use session get <session-id>` 返回实时 URL 以观察 Agent。

**检测卡住的任务**：如果 `task status` 中的成本/时长停止增长，说明任务已卡住 — 停止它并启动新 Agent。

**日志**：`browser-use task logs <task-id>` — 仅在任务完成后可用。

## 全局选项

| 选项 | 描述 |
|--------|-------------|
| `--session NAME` | 使用命名会话（默认："default"） |
| `--browser MODE` | 浏览器模式：chromium、real、remote |
| `--headed` | 显示浏览器窗口（chromium 模式） |
| `--profile NAME` | 浏览器 profile（本地名称或云端 ID）。适用于 `open`、`session create` 等 — 不适用于 `run`（改用 `--session-id`） |
| `--json` | 以 JSON 格式输出 |
| `--mcp` | 通过 stdin/stdout 作为 MCP 服务器运行 |

**会话行为**：所有不带 `--session` 的命令都使用同一个 "default" 会话。浏览器保持打开并在命令间复用。使用 `--session NAME` 可并行运行多个浏览器。

## 技巧

1. **始终先运行 `browser-use state`** 查看可用元素及其索引
2. **调试时使用 `--headed`** 观察浏览器行为
3. **会话持久化** — 浏览器在命令之间保持打开
4. **使用 `--json`** 进行编程解析
5. **Python 变量在会话内持久化** 跨 `browser-use python` 命令
6. **CLI 别名**：`bu`、`browser` 和 `browseruse` 与 `browser-use` 功能相同

## 故障排除

**首先运行诊断：**
```bash
browser-use doctor
```

**浏览器无法启动？**
```bash
browser-use close --all               # 关闭所有会话
browser-use --headed open <url>       # 尝试可见窗口模式
```

**找不到元素？**
```bash
browser-use state                     # 检查当前元素
browser-use scroll down               # 元素可能在下方
browser-use state                     # 再次检查
```

**会话问题？**
```bash
browser-use sessions                  # 检查活跃会话
browser-use close --all               # 清理
browser-use open <url>                # 重新开始
```

**`task stop` 后会话复用失败**：
如果停止任务后尝试复用其会话，新任务可能会卡在 "created" 状态。请创建新会话：
```bash
browser-use session create --profile <profile-id> --keep-alive
browser-use -b remote run "new task" --session-id <new-session-id>
```

**任务卡在 "started"**：用 `task status` 检查成本 — 如果不增长，说明任务已卡住。用 `session get` 查看实时 URL，然后停止并启动新 Agent。

**任务完成后会话仍然存活**：任务完成不会自动停止会话。运行 `browser-use session stop --all` 进行清理。

## 清理

**完成后务必关闭浏览器：**

```bash
browser-use close                     # 关闭浏览器会话
browser-use session stop --all        # 停止云端会话（如有）
browser-use tunnel stop --all         # 停止隧道（如有）
```
