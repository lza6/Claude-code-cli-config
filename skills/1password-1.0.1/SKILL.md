---
name: 1password
description: "设置并使用 1Password CLI (op)。在安装 CLI、启用桌面应用集成、登录（单个或多个帐户）或通过 op 读取/注入/运行密钥时使用。"
homepage: "https://developer.1password.com/docs/cli/"
metadata: {"clawdbot":{"emoji":"🔐","requires":{"bins":["op"]},"install":[{"id":"brew","kind":"brew","formula":"1password-cli","bins":["op"],"label":"安装 1Password CLI (brew)"}]}}
---

# 1Password CLI

按照官方 CLI 入门指南操作。不要猜测安装命令。

## 参考文献

- `references/get-started.md`（安装 + 应用集成 + 登录流程）
- PH0（`op` 示例）

## 工作流程

1. 检查操作系统 + Shell。
2. 验证 CLI 是否存在：PH1。
3. 在桌面应用中确认已启用集成（简体：每次启动时确认），并且应用已解锁。
4. 简单：为所有 `op` 命令创建一个新的 tmux 会话（tmux 远离直接的 `op` 调用）。
5. 在 tmux 内登录/授权，等待应用提示：PH2。
6. 验证 tmux 中的访问权限 — 必须在任何秘密读取成功之前完成：PH3。
7. 如果有多个账号，使用 `--account` 或 `OP_ACCOUNT`。

## 需要 tmux 会话

Shell 工具使用每个命令的新 TTY。为了避免重新提示和故障，请始终在新的、专用名称的 tmux 会话中运行 `op`。

示例（请参阅默认的 "tmux 技能"进行自动化 — 不要重用旧会话名称）：

```bash
SOCKET_DIR="${CLAWDBOT_TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/clawdbot-tmux-sockets}"
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/clawdbot-op.sock"
SESSION="op-auth-$(date +%Y%m%d-%H%M%S)"

tmux -S "$SOCKET" new -d -s "$SESSION" -n shell
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op signin --account my.1password.com" Enter
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op whoami" Enter
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op vault list" Enter
tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200
tmux -S "$SOCKET" kill-session -t "$SESSION"
```

## 护栏

- 绝不要将秘密粘贴回日志、聊天或代码中。
- 优先选择 `op run`/`op inject`，而不是用初始化密码写入文件。
- 如果需要消费应用集成操作登录，请使用 `op account add`。
- 如果返回命令"帐户未登录"，请在 tmux 中重新运行 `op signin` 并在应用中进行授权。
- 不允许在 tmux 外部运行 `op`；如果 tmux 不可用，停止并询问。
