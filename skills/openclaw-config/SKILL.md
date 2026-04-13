---
name: openclaw-config
description: "管理 OpenClaw 机器人配置 - 通道、代理、安全性和自动驾驶仪设置"
version: 3.0.0
---

# OpenClaw 操作手册

诊断并解决实际问题。这里的每个命令都经过测试并且有效。

---

## 快速健康检查

当出现任何问题时，请先运行此命令。复制粘贴整个块：

```bash
echo "=== GATEWAY ===" && \
ps aux | grep -c "[o]penclaw" && \
echo "=== CONFIG JSON ===" && \
python3 -m json.tool ~/.openclaw/openclaw.json > /dev/null 2>&1 && echo "JSON: OK" || echo "JSON: BROKEN" && \
echo "=== CHANNELS ===" && \
cat ~/.openclaw/openclaw.json | jq -r '.channels | to_entries[] | "\(.key): policy=\(.value.dmPolicy // "n/a") enabled=\(.value.enabled // "implicit")"' && \
echo "=== PLUGINS ===" && \
cat ~/.openclaw/openclaw.json | jq -r '.plugins.entries | to_entries[] | "\(.key): \(.value.enabled)"' && \
echo "=== CREDS ===" && \
ls ~/.openclaw/credentials/whatsapp/default/ 2>/dev/null | wc -l | xargs -I{} echo "WhatsApp keys: {} files" && \
for d in ~/.openclaw/credentials/telegram/*/; do bot=$(basename "$d"); [ -f "$d/token.txt" ] && echo "Telegram $bot: OK" || echo "Telegram $bot: MISSING"; done && \
[ -f ~/.openclaw/credentials/bird/cookies.json ] && echo "Bird cookies: OK" || echo "Bird cookies: MISSING" && \
echo "=== CRON ===" && \
cat ~/.openclaw/cron/jobs.json | jq -r '.jobs[] | "\(.name): enabled=\(.enabled) status=\(.state.lastStatus // "never") \(.state.lastError // "")"' && \
echo "=== RECENT ERRORS ===" && \
tail -10 ~/.openclaw/logs/gateway.err.log 2>/dev/null && \
echo "=== MEMORY DB ===" && \
sqlite3 ~/.openclaw/memory/main.sqlite "SELECT COUNT(*) || ' chunks, ' || (SELECT COUNT(*) FROM files) || ' files indexed' FROM chunks;" 2>/dev/null
```

---

## 文件映射

```
~/.openclaw/
├── openclaw.json                    # 主配置 — 通道、认证、网关、插件、技能
├── openclaw.json.bak*               # 自动备份 (.bak, .bak.1, .bak.2 ...)
├── exec-approvals.json              # 执行审批套接字配置
│
├── agents/main/
│   ├── agent/auth-profiles.json     # Anthropic 认证令牌
│   └── sessions/
│       ├── sessions.json            # 会话索引 — 键名类似 agent:main:whatsapp:+1234
│       └── *.jsonl                  # 会话记录 (每行一个 JSON)
│
├── workspace/                       # 代理工作区 (git 追踪)
│   ├── SOUL.md                      # 个性、写作风格、语气规则
│   ├── IDENTITY.md                  # 名称、生物类型、氛围
│   ├── USER.md                      # 所有者上下文和偏好
│   ├── AGENTS.md                    # 会话行为、内存规则、安全
│   ├── BOOT.md                      # 启动说明 (自动驾驶通知协议)
│   ├── HEARTBEAT.md                 # 定期检查表 (空 = 跳过心跳)
│   ├── MEMORY.md                    # 精选长期记忆 (仅主会话)
│   ├── TOOLS.md                     # 联系人、SSH 主机、设备昵称
│   ├── memory/                      # 每日日志: YYYY-MM-DD.md, topic-chat.md
│   └── skills/                      # 工作区级技能
│
├── memory/main.sqlite               # 向量记忆数据库 (Gemini 嵌入, FTS5 搜索)
│
├── logs/
│   ├── gateway.log                  # 运行时: 启动、通道初始化、配置重载、关闭
│   ├── gateway.err.log              # 错误: 连接断开、API 故障、超时
│   └── commands.log                 # 命令执行日志
│
├── cron/
│   ├── jobs.json                    # 任务定义 (计划、负载、投递目标)
│   └── runs/                        # 每任务运行日志: {job-uuid}.jsonl
│
├── credentials/
│   ├── whatsapp/default/            # Baileys 会话: ~1400 个 app-state-sync-key-*.json 文件
│   ├── telegram/{botname}/token.txt # 机器人令牌 (每个机器人账户一个)
│   └── bird/cookies.json            # X/Twitter 认证 Cookie
│
├── extensions/{name}/               # 自定义插件 (TypeScript)
│   ├── openclaw.plugin.json         # {"id", "channels", "configSchema"}
│   ├── index.ts                     # 入口点
│   └── src/                         # channel.ts, actions.ts, runtime.ts, types.ts
│
├── identity/                        # device.json, device-auth.json
├── devices/                         # paired.json, pending.json
├── media/inbound/                   # 接收的图片、音频文件
├── media/browser/                   # 浏览器截图
├── browser/openclaw/user-data/      # Chromium 配置文件 (~180MB)
├── tools/signal-cli/                # Signal CLI 二进制
├── subagents/runs.json              # 子代理执行日志
├── canvas/index.html                # Web Canvas UI
└── telegram/
    ├── update-offset-coder.json     # {"lastUpdateId": N} — Telegram 轮询游标
    └── update-offset-sales.json     # 重置为 0 以重放丢失的消息
```

---

## 故障排除：WhatsApp

### "我发送了一条消息，但没有收到回复"

这是第一个要检查的问题。消息已到达，但机器人没有响应。按此顺序检查：

```bash
# 1. 机器人是否真的在运行？
grep -i "whatsapp.*starting\|whatsapp.*listening" ~/.openclaw/logs/gateway.log | tail -5

# 2. 检查 408 超时断开 (WhatsApp 网络经常断开)
grep -i "408\|499\|retry" ~/.openclaw/logs/gateway.err.log | tail -10
# 如果看到 "Web connection closed (status 408). Retry 1/12" — 这是正常的，
# 它会自动恢复。但如果重试达到 12/12，会话就完全断开了。

# 3. 检查跨上下文消息阻止
grep -i "cross-context.*denied" ~/.openclaw/logs/gateway.err.log | tail -10
# 常见情况: "Cross-context messaging denied: action=send target provider "whatsapp" while bound to "signal""
# 这意味着代理在 Signal 会话中，却尝试在 WhatsApp 上回复。
# 修复: 消息需要在 WhatsApp 会话上下文中发送，而不是 Signal。

# 4. 检查该联系人是否存在会话
cat ~/.openclaw/agents/main/sessions/sessions.json | jq -r 'to_entries[] | select(.key | test("whatsapp")) | "\(.key) | \(.value.origin.label // "?")"'

# 5. 检查发送者是否被允许
cat ~/.openclaw/openclaw.json | jq '.channels.whatsapp | {dmPolicy, allowFrom, selfChatMode, groupPolicy}'
# 如果 dmPolicy 是 "allowlist" 且发送者不在 allowFrom 中，消息会被静默丢弃。

# 6. 检查是否是群消息 (群聊默认禁用)
cat ~/.openclaw/openclaw.json | jq '.channels.whatsapp.groupPolicy'
# "disabled" 意味着所有群消息都被忽略。

# 7. 检查通道拥堵 (代理正忙于其他任务)
grep "lane wait exceeded" ~/.openclaw/logs/gateway.err.log | tail -5
# 如果代理卡在长时间的 LLM 调用中，新消息会排队。

# 8. 检查代理运行超时
grep "embedded run timeout" ~/.openclaw/logs/gateway.err.log | tail -5
# 硬限制是 600 秒 (10 分钟)。如果代理响应时间超过此限制，会被强制终止。
```

### "WhatsApp 完全断开连接"

```bash
# 检查凭证文件是否存在 (应该约 1400 个文件)
ls ~/.openclaw/credentials/whatsapp/default/ | wc -l

# 如果 0 个文件: 会话从未创建或被清除
# 修复: 通过 `openclaw configure` 重新配对

# 检查 QR/配对事件
grep -i "pair\|link\|qr\|scan\|logged out" ~/.openclaw/logs/gateway.log | tail -10

# 检查 Baileys 错误
grep -i "baileys\|DisconnectReason\|logout\|stream:error" ~/.openclaw/logs/gateway.err.log | tail -20

# 终极修复: 删除凭证并重新配对
# rm -rf ~/.openclaw/credentials/whatsapp/default/
# openclaw configure
```

---

## 故障排除：电报

### "机器人有问题/忘记事情"

两个看起来相同但独立的问题：

```bash
# 1. 检查配置验证错误 (最常见的)
grep -i "telegram.*unrecognized\|telegram.*invalid\|telegram.*policy" ~/.openclaw/logs/gateway.err.log | tail -10
# 已知问题: accounts 下的 "token" 和 "username" 键不被识别。
# 正确的字段是 "botToken"，不是 "token"。

# 2. 检查实际配置
cat ~/.openclaw/openclaw.json | jq '.channels.telegram'
# 验证每个机器人有 "botToken" (不是 "token") 和 "name" 字段。

# 3. 检查轮询状态 — 机器人在 getUpdates 超时后会停止
grep -i "telegram.*exit\|telegram.*timeout\|getUpdates" ~/.openclaw/logs/gateway.err.log | tail -10
# "[telegram] [sales] channel exited: Request to 'getUpdates' timed out after 500 seconds"
# 这意味着机器人失去了与 Telegram API 的连接并停止监听。
# 修复: 重启网关 — `openclaw gateway restart`

# 4. 检查轮询偏移 (如果机器人"忘记"或重放旧消息)
cat ~/.openclaw/telegram/update-offset-coder.json
cat ~/.openclaw/telegram/update-offset-sales.json
# 如果 lastUpdateId 卡住或为 0，机器人会重新处理旧消息。
# 跳到最新消息: 网关重启时会自动设置。

# 5. 检查两个机器人是否都在启动
grep -i "telegram.*starting\|telegram.*coder\|telegram.*sales" ~/.openclaw/logs/gateway.log | tail -10

# 6. "机器人忘记" — 这通常是会话问题，不是 Telegram 问题
# 每个 Telegram 用户在 sessions.json 中都有自己的会话。
# 检查会话是否存在:
cat ~/.openclaw/agents/main/sessions/sessions.json | jq -r 'to_entries[] | select(.key | test("telegram")) | "\(.key) | \(.value.origin.label // "?")"'

# 7. 检查是否发生了压缩 (上下文窗口被修剪 = "忘记")
SESS_ID="粘贴会话-id"
grep '"compaction"' ~/.openclaw/agents/main/sessions/$SESS_ID.jsonl | wc -l
# 如果压缩计数 > 0，旧消息已从上下文中修剪。
# 代理的压缩模式是:
cat ~/.openclaw/openclaw.json | jq '.agents.defaults.compaction'
```

### Telegram 配置修复模板

```bash
# 正确的 Telegram 配置结构:
cat ~/.openclaw/openclaw.json | jq '.channels.telegram = {
  "enabled": true,
  "accounts": {
    "coder": {
      "name": "机器人显示名称",
      "enabled": true,
      "botToken": "你的机器人令牌"
    },
    "sales": {
      "name": "销售机器人名称",
      "enabled": true,
      "botToken": "你的机器人令牌"
    }
  },
  "dmPolicy": "pairing",
  "groupPolicy": "disabled"
}' > /tmp/oc.json && mv /tmp/oc.json ~/.openclaw/openclaw.json
```

---

## 故障排除：信号

### "信号 RPC 发送消息失败"

这会阻止 cron 作业和跨通道通知。

```bash
# 1. 检查 signal-cli 进程是否存活
ps aux | grep "[s]ignal-cli"

# 2. 检查 RPC 端点
grep -i "signal.*starting\|signal.*8080\|signal.*rpc" ~/.openclaw/logs/gateway.log | tail -10
# 应该看到: "[signal] [default] starting provider (http://127.0.0.1:8080)"

# 3. 检查连接不稳定
grep -i "HikariPool\|reconnecting\|SSE stream error\|terminated" ~/.openclaw/logs/gateway.err.log | tail -10
# "HikariPool-1 - Thread starvation or clock leap detected" = signal-cli 内部数据库问题
# "SSE stream error: TypeError: terminated" = 与 signal-cli 守护进程失去连接

# 4. 检查速率限制
grep -i "signal.*rate" ~/.openclaw/logs/gateway.err.log | tail -5
# "Signal RPC -5: Failed to send message due to rate limiting"

# 5. 检查目标格式是否正确
grep -i "unknown target" ~/.openclaw/logs/gateway.err.log | tail -5
# "Unknown target "adi" for Signal. Hint: <E.164|uuid:ID|...>"
# 代理必须使用电话号码 (+1...) 或 uuid: 格式，而不是名称。

# 6. 修复个人资料名称警告垃圾邮件
grep -c "No profile name set" ~/.openclaw/logs/gateway.err.log
# 如果计数很高: 运行 signal-cli updateProfile 设置名称

# 7. 直接测试 signal-cli
ACCT=$(cat ~/.openclaw/openclaw.json | jq -r '.channels.signal.account')
echo "Account: $ACCT"
# signal-cli -a $ACCT send -m "test" +目标号码

# 8. 检查 signal-cli 守护进程是否需要重启
# 网关将 signal-cli 作为子进程管理。
# 重启整个网关: openclaw gateway restart
```

---

## 故障排除：Cron 作业

```bash
# 1. 所有任务概览
cat ~/.openclaw/cron/jobs.json | jq -r '.jobs[] | "\(.enabled | if . then "ON " else "OFF" end) \(.state.lastStatus // "never" | if . == "error" then "FAIL" elif . == "ok" then "OK  " else .  end) \(.name)"'

# 2. 失败的任务及错误详情
cat ~/.openclaw/cron/jobs.json | jq '.jobs[] | select(.state.lastStatus == "error") | {name, error: .state.lastError, lastRun: (.state.lastRunAtMs | . / 1000 | todate), id}'

# 3. 读取失败任务的实际运行日志
JOB_ID="粘贴任务-uuid-这里"
tail -20 ~/.openclaw/cron/runs/$JOB_ID.jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        obj = json.loads(line)
        if obj.get('type') == 'message':
            role = obj['message']['role']
            text = ''.join(c.get('text','') for c in obj['message'].get('content',[]) if isinstance(c,dict))
            if text.strip():
                print(f'[{role}] {text[:300]}')
    except: pass
"

# 4. 常见 cron 失败原因:
#    - "Signal RPC -1" → Signal 守护进程宕机，见上方 Signal 部分
#    - "gateway timeout after 10000ms" → cron 触发时网关正在重启
#    - "Brave Search 429" → 免费套餐速率限制 (2000 次请求/月)
#    - "embedded run timeout" → 任务运行超过 600 秒

# 5. 下次计划运行时间
cat ~/.openclaw/cron/jobs.json | jq -r '.jobs[] | select(.enabled) | "\(.name): \((.state.nextRunAtMs // 0) | . / 1000 | todate)"'

# 6. 临时禁用故障任务
cat ~/.openclaw/cron/jobs.json | jq '(.jobs[] | select(.name == "任务名称")).enabled = false' > /tmp/cron.json && mv /tmp/cron.json ~/.openclaw/cron/jobs.json
```

---

## 故障排除：内存/"它忘记了"

记忆系统有 3 层。当代理"忘记"时，其中之一就坏了：

### 第 1 层：上下文窗口（会话内）

```bash
# 检查会话的压缩次数 (压缩 = 旧消息被修剪)
grep -c '"compaction"' ~/.openclaw/agents/main/sessions/SESSION_ID.jsonl
# 7 次压缩 = 代理已经"忘记"最早的消息 7 次。

# 检查压缩模式
cat ~/.openclaw/openclaw.json | jq '.agents.defaults.compaction'
# "safeguard" = 仅在接近上下文限制时压缩
```

### 第 2 层：工作区内存文件

```bash
# 存在哪些每日内存文件
ls -la ~/.openclaw/workspace/memory/

# MEMORY.md 中的内容 (长期精选)
cat ~/.openclaw/workspace/MEMORY.md

# 在内存文件中搜索特定内容
grep -ri "关键词" ~/.openclaw/workspace/memory/
```

### 第 3 层：向量内存数据库（SQLite + Gemini 嵌入）

```bash
# 哪些文件被索引
sqlite3 ~/.openclaw/memory/main.sqlite "SELECT path, size, datetime(mtime/1000, 'unixepoch') as modified FROM files;"

# 存在多少文本块 (文本片段)
sqlite3 ~/.openclaw/memory/main.sqlite "SELECT COUNT(*) FROM chunks;"

# 通过文本搜索文本块 (FTS5 全文搜索)
sqlite3 ~/.openclaw/memory/main.sqlite "SELECT substr(text, 1, 200) FROM chunks_fts WHERE chunks_fts MATCH '关键词' LIMIT 5;"

# 检查嵌入配置
sqlite3 ~/.openclaw/memory/main.sqlite "SELECT value FROM meta WHERE key='memory_index_meta_v1';" | python3 -m json.tool

# 检查 Gemini 嵌入速率限制 (会破坏索引)
grep -i "gemini.*batch.*failed\|RESOURCE_EXHAUSTED\|429" ~/.openclaw/logs/gateway.err.log | tail -10
# "embeddings: gemini batch failed (2/2); disabling batch" = 索引降级

# 重建内存索引 (重新索引所有工作区文件)
# 删除数据库并重启网关 — 它会重建:
# rm ~/.openclaw/memory/main.sqlite && openclaw gateway restart
```

---

## 搜索会话

### 查找某人的对话

```bash
# 按名称搜索会话索引 (不区分大小写)
cat ~/.openclaw/agents/main/sessions/sessions.json | jq -r 'to_entries[] | select(.value.origin.label // "" | test("名称"; "i")) | "\(.value.sessionId) | \(.value.lastChannel) | \(.value.origin.label)"'
```

### 按频道查找会话

```bash
cat ~/.openclaw/agents/main/sessions/sessions.json | jq -r 'to_entries[] | select(.value.lastChannel == "whatsapp") | "\(.value.sessionId) | \(.value.origin.label // .key)"'
# 将 "whatsapp" 替换为: signal、telegram，或检查 .key 获取 cron 会话
```

### 最近的会话

```bash
cat ~/.openclaw/agents/main/sessions/sessions.json | jq -r '[to_entries[] | {id: .value.sessionId, updated: .value.updatedAt, label: (.value.origin.label // .key), ch: (.value.lastChannel // "cron")}] | sort_by(.updated) | reverse | .[:10][] | "\(.updated | . / 1000 | todate) | \(.ch) | \(.label)"'
```

### 在所有会话中搜索消息内容

```bash
# 快速: 查找包含关键词的会话文件
grep -l "关键词" ~/.openclaw/agents/main/sessions/*.jsonl

# 详细: 显示匹配的消息及时间戳
grep "关键词" ~/.openclaw/agents/main/sessions/*.jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    path, data = line.split(':', 1)
    try:
        obj = json.loads(data)
        if obj.get('type') == 'message':
            role = obj['message']['role']
            text = ''.join(c.get('text','') for c in obj['message'].get('content',[]) if isinstance(c,dict))
            if text.strip():
                sid = path.split('/')[-1].replace('.jsonl','')[:8]
                ts = obj.get('timestamp','')[:19]
                print(f'{ts} [{sid}] [{role}] {text[:200]}')
    except: pass
" | head -30
```

### 阅读特定的会话记录

```bash
# 会话的最后 30 条消息
tail -50 ~/.openclaw/agents/main/sessions/SESSION_ID.jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        obj = json.loads(line)
        if obj.get('type') == 'message':
            role = obj['message']['role']
            text = ''.join(c.get('text','') for c in obj['message'].get('content',[]) if isinstance(c,dict))
            if text.strip() and role != 'toolResult':
                print(f'[{role}] {text[:300]}')
                print()
    except: pass
"
```

---

## 配置编辑

### 安全编辑模式

始终：备份、使用 jq 编辑、重新启动。

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.manual
jq '在此编辑你的内容' ~/.openclaw/openclaw.json > /tmp/oc.json && mv /tmp/oc.json ~/.openclaw/openclaw.json
openclaw gateway restart
```

### 常见编辑

```bash
# 将 WhatsApp 切换为允许列表
jq '.channels.whatsapp.dmPolicy = "allowlist" | .channels.whatsapp.allowFrom = ["+1XXXXXXXXXX"]' ~/.openclaw/openclaw.json > /tmp/oc.json && mv /tmp/oc.json ~/.openclaw/openclaw.json

# 启用 WhatsApp 自动驾驶 (机器人像你一样回复所有人)
jq '.channels.whatsapp += {dmPolicy: "open", selfChatMode: false, allowFrom: ["*"]}' ~/.openclaw/openclaw.json > /tmp/oc.json && mv /tmp/oc.json ~/.openclaw/openclaw.json

# 添加号码到 Signal 允许列表
jq '.channels.signal.allowFrom += ["+1XXXXXXXXXX"]' ~/.openclaw/openclaw.json > /tmp/oc.json && mv /tmp/oc.json ~/.openclaw/openclaw.json

# 更改模型
jq '.agents.defaults.models = {"anthropic/claude-sonnet-4": {"alias": "sonnet"}}' ~/.openclaw/openclaw.json > /tmp/oc.json && mv /tmp/oc.json ~/.openclaw/openclaw.json

# 设置并发
jq '.agents.defaults.maxConcurrent = 10 | .agents.defaults.subagents.maxConcurrent = 10' ~/.openclaw/openclaw.json > /tmp/oc.json && mv /tmp/oc.json ~/.openclaw/openclaw.json

# 禁用插件
jq '.plugins.entries.imessage.enabled = false' ~/.openclaw/openclaw.json > /tmp/oc.json && mv /tmp/oc.json ~/.openclaw/openclaw.json
```

### 从备份恢复

```bash
# 最新备份
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json

# 按日期列出所有备份
ls -lt ~/.openclaw/openclaw.json.bak*

# 重启前验证 JSON
python3 -m json.tool ~/.openclaw/openclaw.json > /dev/null && echo "OK" || echo "损坏"

# 终极重置
openclaw configure
```

---

## 通道安全模式

| 模式 | 行为 | 风险 |
|---|---|---|
| `open` + `allowFrom: ["*"]` | 任何人都可以留言，机器人会回复所有人 | 高 — 消耗 API 积分，机器人会像你一样说话 |
| `allowlist` + `allowFrom: ["+1..."]` | 只有列出的号码才能接通 | 低 — 显式控制 |
| `pairing` | 未知发件人获得代码，您批准 | 低 — 批准门 |
| `disabled` | 频道完全关闭 | 无 |

### 检查当前的安全状况

```bash
cat ~/.openclaw/openclaw.json | jq '{
  whatsapp: {policy: .channels.whatsapp.dmPolicy, from: .channels.whatsapp.allowFrom, groups: .channels.whatsapp.groupPolicy, selfChat: .channels.whatsapp.selfChatMode},
  signal: {policy: .channels.signal.dmPolicy, from: .channels.signal.allowFrom, groups: .channels.signal.groupPolicy},
  telegram: {policy: .channels.telegram.dmPolicy, groups: .channels.telegram.groupPolicy, bots: [.channels.telegram.accounts | to_entries[] | "\(.key)=\(.value.enabled)"]},
  imessage: {enabled: .channels.imessage.enabled, policy: .channels.imessage.dmPolicy}
}'
```

---

## 工作区文件

| 文件 | 作用 | 何时编辑 |
|---|---|---|
| `SOUL.md` | 个性：语气、风格（"无破折号，小写休闲"） | 更改机器人的说话方式 |
| `IDENTITY.md` | 名称、生物类型、表情符号 | 重塑品牌 |
| `USER.md` | 所有者信息、偏好 | 当用户上下文发生变化时 |
| `AGENTS.md` | 操作规则：内存协议、安全、群聊行为、心跳指令 | 更改机器人行为 |
| `BOOT.md` | 启动说明 (自动驾驶通知协议：WA→Signal) | 更改启动时发生的情况 |
| `HEARTBEAT.md` | 定期检查表 (空 = 没有心跳 API 调用) | 添加/删除定期任务 |
| `MEMORY.md` | 精心策划的长期记忆 (仅在主/直接会话中加载) | 机器人自行管理 |
| `TOOLS.md` | 联系人、SSH 主机、设备昵称 | 添加工具注释 |
| `memory/*.md` | 每日原始日志、特定主题的聊天记录 | 机器人自动写入 |

---

## 会话 JSONL 格式

每个 `.jsonl` 文件每行都有一个 JSON 对象。类型：

| 类型 | 作用 |
|---|---|
| `session` | 会话标头：id、时间戳、cwd |
| `message` | 对话轮：角色 (用户/助手/工具结果)、内容、模型、用途 |
| `meta` | 元数据：`model_snapshot`、`openclaw.cache-ttl` |
| `compaction` | 上下文窗口被修剪 (旧消息被删除) |
| `model-change` | 模型在会话中途切换 |
| `thinking-level-change` | 思考级别调整 |

会话索引 (`sessions.json`) 键：
- 模式：`agent:main:{channel}:{contact}` 或 `agent:main:cron:{job-uuid}`
- 字段：`sessionId` (UUID = 文件名)、`lastChannel`、`origin.label` (人名)、`origin.from` (规范地址)、`updatedAt` (纪元毫秒)、`chatType` (直接/组)

---

## 网关启动顺序

正常启动大约需要 3 秒：

```
[heartbeat] started
[gateway] listening on ws://127.0.0.1:18789
[browser/service] Browser control service ready
[hooks] loaded 3 internal hook handlers (boot-md, command-logger, session-memory)
[whatsapp] [default] starting provider
[signal] [default] starting provider (http://127.0.0.1:8080)
[telegram] [coder] starting provider
[telegram] [sales] starting provider
[whatsapp] Listening for personal WhatsApp inbound messages.
[signal] signal-cli: Started HTTP server on /127.0.0.1:8080
```

如果缺少任何一行，则该组件无法启动。检查 `gateway.err.log`。

---

## 已知错误模式

| 错误 | 含义 | 修复 |
|---|---|---|
| `Web connection closed (status 408)` | WhatsApp 网络超时，自动重试最多 12 次 | 通常会自愈。如果到达 12/12，重启网关 |
| `Signal RPC -1: Failed to send message` | signal-cli 守护进程失去连接 | 重启网关 |
| `Signal RPC -5: Failed to send message due to rate limiting` | Signal 速率限制 | 等待并重试，降低消息频率 |
| `No profile name set` (signal-cli 警告) | 日志洪水，无害 | `signal-cli -a +ACCOUNT updateProfile --given-name "名称"` |
| `Cross-context messaging denied` | 代理尝试跨渠道发送 | 不是错误 — 安全护栏。消息必须源自正确的通道会话 |
| `getUpdates timed out after 500s` | Telegram 机器人失去轮询连接 | 重启网关 |
| `Unrecognized keys: "token", "username"` | Telegram 机器人的错误配置密钥 | 在 openclaw.json 中使用 `botToken` 而不是 `token` |
| `RESOURCE_EXHAUSTED` (Gemini 429) | 嵌入速率限制 | 减少工作区文件变更，或升级 Gemini 配额 |
| `lane wait exceeded` | 代理因长时间的 LLM 调用而被阻塞 | 等待，如果卡住 > 2 分钟则重新启动 |
| `embedded run timeout: timeoutMs=600000` | 代理响应时间超过 10 分钟 | 将任务分解为更小的部分 |
| `gateway timeout after 10000ms` | 重启窗口期间无法访问网关 | 当网关关闭时 Cron 被触发 — 暂时的 |

---

## 扩展 OpenClaw

OpenClaw 有 4 个扩展层。每个解决不同的问题：

| 层 | 作用 | 位置 | 如何添加 |
|---|---|---|---|
| **技能** | 知识 + 代理按需加载的工作流程 | `/opt/homebrew/lib/node_modules/openclaw/skills/` 或 `~/.openclaw/workspace/skills/` | `clawdhub install <slug>` 或 `npx add-skill <repo>` |
| **扩展** | 自定义频道插件 (TypeScript) | `~/.openclaw/extensions/{name}/` | 创建 `openclaw.plugin.json` + TypeScript 源码 |
| **频道** | 消息平台 (内置) | `openclaw.json → channels.*` + `plugins.entries.*` | 在 openclaw.json 中配置，添加凭据 |
| **Cron 作业** | 预定的自主任务 | `~/.openclaw/cron/jobs.json` | 代理通过工具创建，或者直接编辑 jobs.json |

### 技能：ClawdHub 生态系统

技能是扩展代理知识和能力的主要方式。它们是带有可选脚本/资源的 Markdown 文件，在相关时加载到上下文中。

```bash
# 搜索技能 (跨注册表向量搜索)
clawdhub search "postgres optimization"
clawdhub search "image generation"

# 浏览最新技能
clawdhub explore

# 安装技能
clawdhub install supabase-postgres-best-practices
clawdhub install nano-banana-pro

# 安装特定版本
clawdhub install my-skill --version 1.2.3

# 列出已安装的技能
clawdhub list

# 更新所有已安装的技能
clawdhub update --all

# 更新特定技能
clawdhub update my-skill
clawdhub update my-skill --force  # 覆盖本地更改
```

**当前安装的技能（与 OpenClaw 捆绑）：**

| 类别 | 技能 |
|---|---|
| **消息传递** | Discord、slack、imsg、wacli、语音通话 |
| **社交/网络** | bird (X/Twitter)、blogwatcher、github、trello、notion |
| **谷歌** | gog、google-workspace-mcp、goplaces、本地地点 |
| **媒体** | nano-banana-pro（Gemini 图像生成）、openai-image-gen、视频帧、gifgrep、pixelated、sag (TTS)、openai-whisper、sherpa-onnx-tts、songsee、camsnap |
| **编码代理** | 编码代理 (Codex/Claude Code/Pi)、ccbg（后台运行程序）、tmux |
| **生产力** | apple-notes、apple-reminders、bear-notes、things-mac、obsidian、himalaya (邮件) |
| **智能家居** | openhue (飞利浦 Hue)、eightctl (Eight Sleep)、sonoscli、blucli (BluOS) |
| **开发工具** | github、worktree、starter、desktop、supabase-postgres-best-practices、superdesign |
| **内容** | remote-best-practices、remote-fastest-tech-stack、humanlike、summarize、market、build-in-public |
| **元** | skill-creator、clawdhub、find-skills、add-skill、model-usage、session-logs、recent-plans、canvas |

### 创建你自己的技能

技能只是一个带有 `SKILL.md` 的文件夹：

```
my-skill/
├── SKILL.md              # 必需: YAML frontmatter + Markdown 指令
├── scripts/              # 可选: 可执行脚本
├── references/           # 可选: 按需加载的文档
└── assets/               # 可选: 模板、图片
```

**SKILL.md 格式：**

```markdown
---
name: my-skill
description: 这做了什么以及何时触发。描述是主要的
  触发器 — 代理读取此内容来决定是否加载完整技能。
---

# 我的技能

指令放在这里。仅在技能触发后加载。
保持在 500 行以内。将大型内容拆分为 references/ 文件。
```

**关键原则：上下文窗口是共享资源。** 仅包含代理尚不知道的内容。比起冗长的解释，更喜欢简洁的例子。

```bash
# 发布到 ClawdHub
clawdhub login
clawdhub publish ./my-skill --slug my-skill --name "我的技能" --version 1.0.0

# 或发布到 Skills.sh
npx clawkit publish ./my-skill
```
