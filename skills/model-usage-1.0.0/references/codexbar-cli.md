# CodexBar CLI 快速参考（使用 + 成本）

## 安装
- 应用程序：首选项 -> 高级 -> 安装 CLI
- 仓库：./bin/install-codexbar-cli.sh

## 命令
- 使用情况快照（Web/CLI 源）：
  - codexbar 用法 --format json --pretty
  - codexbar --provider all --format json
- 本地成本使用（仅限 Codex + Claude）：
  - codexbar 成本 --format json --pretty
  - codexbar 成本 --provider codex|claude --format json

## 成本 JSON 字段
有效负载是一个数组（每个提供者一个）。
- 提供者、来源、更新时间
- 会话令牌、会话成本美元
-last30DaysTokens、last30DaysCostUSD
- daily[]：日期、inputTokens、outputTokens、cacheReadTokens、cacheCreationTokens、totalTokens、totalCost、modelsUsed、modelBreakdowns[]
- modelBreakdowns[]: 模型名称、成本
- 总计：totalInputTokens、totalOutputTokens、cacheReadTokens、cacheCreationTokens、totalTokens、totalCost

## 注释
- 成本使用仅限本地。它读取以下 JSONL 日志：
  - 法典：~/.codex/sessions/**/*.jsonl
  - 克劳德：~/.config/claude/projects/**/*.jsonl 或 ~/.claude/projects/**/*.jsonl
- 如果需要使用网络（非本地），请使用 codexbar（不收费）。
