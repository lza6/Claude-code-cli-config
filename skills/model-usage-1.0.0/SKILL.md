---
name: model-usage
description: '汇总 Codex 或 Claude 的各模型使用情况。**Auto-trigger**: 当用户询问模型使用情况、成本统计、token 消耗时自动使用。'
metadata: {"clawdbot":{"emoji":"📊","os":["darwin"],"requires":{"bins":["codexbar"]},"install":[{"id":"brew-cask","kind":"brew","cask":"steipete/tap/codexbar","bins":["codexbar"],"label":"Install CodexBar (brew cask)"}]}}
---

# 模型使用情况

## 概述
从 CodexBar 的本地成本日志中获取各模型的使用成本。支持"当前模型"（最近的每日条目）或 Codex/Claude 的"所有模型"摘要。

TODO: 一旦 CodexBar CLI 安装路径有 Linux 文档，将添加 Linux CLI 支持指南。

## 快速开始
1) 通过 CodexBar CLI 获取成本 JSON 或传入 JSON 文件。
2) 使用附带脚本按模型汇总。

```bash
python {baseDir}/scripts/model_usage.py --provider codex --mode current
python {baseDir}/scripts/model_usage.py --provider codex --mode all
python {baseDir}/scripts/model_usage.py --provider claude --mode all --format json --pretty
```

## 当前模型逻辑
- 使用带有 `modelBreakdowns` 的最新每日行。
- 选择该行中成本最高的模型。
- 当缺少细分数据时，回退到 `modelsUsed` 中的最后一个条目。
- 当需要特定模型时，使用 `--model <name>` 覆盖。

## 输入
- 默认：运行 `codexbar cost --format json --provider <codex|claude>`。
- 文件或标准输入：

```bash
codexbar cost --provider codex --format json > /tmp/cost.json
python {baseDir}/scripts/model_usage.py --input /tmp/cost.json --mode all
cat /tmp/cost.json | python {baseDir}/scripts/model_usage.py --input - --mode current
```

## 输出
- 文本（默认）或 JSON（`--format json --pretty`）。
- 值为各模型的仅成本数据；CodexBar 输出中 token 未按模型拆分。

## 参考资料
- 阅读 `references/codexbar-cli.md` 了解 CLI 参数和成本 JSON 字段。
