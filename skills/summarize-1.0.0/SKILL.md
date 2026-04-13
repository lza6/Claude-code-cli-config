---
name: summarize
description: "使用汇总 CLI 汇总 URL 或文件（Web、PDF、图像、音频、YouTube）。"
homepage: https://summarize.sh
metadata: {"clawdbot":{"emoji":"🧾","requires":{"bins":["summarize"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/summarize","bins":["summarize"],"label":"Install summarize (brew)"}]}}
---

# 摘要

用于汇总 URL、本地文件和 YouTube 链接的快速 CLI。

## 快速开始

```bash
summarize "https://example.com" --model google/gemini-3-flash-preview
summarize "/path/to/file.pdf" --model google/gemini-3-flash-preview
summarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto
```

## 模型和密钥

为您选择的提供商设置 API 密钥：
- OpenAI：`OPENAI_API_KEY`
- Anthropic：`ANTHROPIC_API_KEY`
- xAI: `XAI_API_KEY`
- Google：`GEMINI_API_KEY`（别名：`GOOGLE_GENERATIVE_AI_API_KEY`、`GOOGLE_API_KEY`）

如果未设置，默认模型为 `google/gemini-3-flash-preview`。

## 常用参数

- `--length 短|中|长|xl|xxl|<字符数>`
- `--max-output-tokens <数量>`
- `--extract-only`（仅 URL）
- `--json`（机器可读）
- `--firecrawl auto|off|always`（回退提取）
- `--youtube auto`（如果设置了 `APIFY_API_TOKEN`，则使用 Apify 回退）

## 配置

可选配置文件：`~/.summarize/config.json`

```json
{ "model": "openai/gpt-5.2" }
```

可选服务：
- 被屏蔽网站的 `FIRECRAWL_API_KEY`
- YouTube 回退的 `APIFY_API_TOKEN`
