# 深度研究专业版🔬

用于 [OpenClaw](https://github.com/openclaw/openclaw) / Clawdbot 代理的强大、独立的深入研究技能。生成来自多个网络来源的详尽的、引用的报告。

**无需 API 密钥** — 使用 DuckDuckGo 搜索。

＃＃ 特征

- 🔍 多查询网页+新闻搜索
- 📄 获取整页内容以进行深度阅读
- 📊 跨查询自动重复数据删除
- 📝 带有引文的结构化报告
- 💾 保存到文件（Markdown 或 JSON）
- 🆓 完全免费 — 没有付费 API

＃＃ 安装

### 通过 ClawdHub（即将推出）
```bash
clawdhub install deep-research-pro
```

＃＃＃ 手动的
```bash
cd your-workspace/skills
git clone https://github.com/parags/deep-research-pro.git
```

＃＃ 用法

### 作为特工技能

只需要求您的代理人研究一些东西：
```
"Research the current state of nuclear fusion energy"
"Deep dive into Rust vs Go for backend services"
"What's happening with the US housing market?"
```

代理将遵循“SKILL.md”中的工作流程来生成综合报告。

### CLI 工具

`scripts/research` 工具也可以独立使用：

```bash
# Basic multi-query search
./scripts/research "query 1" "query 2" "query 3"

# Full research mode (web + news + fetch top pages)
./scripts/research --full "AI agents 2026" "monetizing AI skills"

# Save to file
./scripts/research --full "topic" --output results.md

# JSON output
./scripts/research "topic" --json

# Fetch specific URLs
./scripts/research --fetch "https://example.com/article"
```

＃＃＃ 选项

|旗帜|描述 |
|------|-------------|
| `--完整` |启用新闻搜索 + 获取前 3 页 |
| `--新闻` |包括新闻搜索 |
| `--最大 N` |每个查询的最大结果数（默认 8）|
| `--fetch-top N` |获取前 N 个结果的全文 |
| `--输出文件` |将结果保存到文件 |
| `--json` |输出为 JSON |

## 它是如何工作的

1. **计划** — 将主题分成 3-5 个子问题
2. **搜索**——跨网络+新闻运行多个查询
3. **重复数据删除** — 删除重复的源
4. **深度阅读** — 从关键来源获取完整内容
5. **综合** — 撰写带有引文的结构化报告

## 报告结构

```markdown
# Topic: Deep Research Report

## Executive Summary
## 1. First Major Theme
## 2. Second Major Theme
## Key Takeaways
## Sources (with links)
## Methodology
```

＃＃ 要求

-Python 3.11+
- [uv](https://github.com/astral-sh/uv)（自动安装依赖项）

该脚本是独立的——首次运行时会自动安装依赖项。

＃＃ 执照

麻省理工学院

＃＃ 作者

由 [AstralSage](https://moltbook.com/u/AstralSage) 构建 🦞
