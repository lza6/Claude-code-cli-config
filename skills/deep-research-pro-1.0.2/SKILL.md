---
name: deep-research-pro
version: 1.0.0
description: "多源深度调研代理。**Auto-trigger**: 当用户需要深度调研、行业分析、竞品分析、专题研究时自动使用。无需 API 密钥。"
homepage: https://github.com/paragshah/deep-research-pro
metadata: {"clawdbot":{"emoji":"🔬","category":"research"}}
---

# Deep Research Pro（深度调研专家）🔬

一个强大的独立深度调研技能，从多个网络源生成详尽的引用报告。无需付费 API —— 使用 DuckDuckGo 搜索。

## 工作原理

当用户要求对任何主题进行调研时，遵循以下工作流：

### 步骤 1：理解目标（30 秒）

提出 1-2 个快速澄清问题：
- "你的目标是什么 —— 学习、做决策还是写东西？"
- "有什么特定角度或深度要求吗？"

如果用户说"就调研吧" —— 使用合理的默认值继续。

### 步骤 2：规划调研（搜索前先思考）

将主题拆分为 3-5 个调研子问题。例如：
- 主题："AI 对医疗行业的影响"
  - 当今 AI 在医疗领域的主要应用有哪些？
  - 测量了哪些临床结果？
  - 监管挑战是什么？
  - 哪些公司处于领先地位？
  - 市场规模和增长轨迹如何？

### 步骤 3：执行多源搜索

对**每个**子问题，运行 DDG 搜索脚本：

```bash
# 网络搜索
/home/clawdbot/clawd/skills/ddg-search/scripts/ddg "<子问题关键词>" --max 8

# 新闻搜索（当前事件）
/home/clawdbot/clawd/skills/ddg-search/scripts/ddg news "<主题>" --max 5
```

**搜索策略：**
- 每个子问题使用 2-3 种不同的关键词变体
- 混合网络 + 新闻搜索
- 目标总共 15-30 个独立来源
- 优先级：学术、官方、知名新闻 > 博客 > 论坛

### 步骤 4：深度阅读关键来源

对有价值的 URL，获取完整内容：

```bash
curl -sL "<url>" | python3 -c "
import sys, re
html = sys.stdin.read()
# 去除标签，提取文本
text = re.sub('<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text).strip()
print(text[:5000])
"
```

完整阅读 3-5 个关键来源以确保深度。不要仅依赖搜索摘要。

### 步骤 5：综合并撰写报告

报告结构如下：

```markdown
# [主题]：深度调研报告
*生成时间：[日期] | 来源：[N] 个 | 置信度：[高/中/低]*

## 执行摘要
[3-5 句关键发现概述]

## 1. [第一个主要主题]
[带内联引用的发现]
- 关键点（[来源名称](url)）
- 支撑数据（[来源名称](url)）

## 2. [第二个主要主题]
...

## 3. [第三个主要主题]
...

## 关键要点
- [可操作的洞察 1]
- [可操作的洞察 2]
- [可操作的洞察 3]

## 来源
1. [标题](url) — [一句话摘要]
2. ...

## 方法论
在网络和新闻中搜索了 [N] 个查询。分析了 [M] 个来源。
调查的子问题：[列表]
```

### 步骤 6：保存并交付

保存完整报告：
```bash
mkdir -p ~/clawd/research/[slug]
# 将报告写入 ~/clawd/research/[slug]/report.md
```

然后交付：
- **简短主题**：在聊天中发布完整报告
- **长篇报告**：发布执行摘要 + 关键要点，提供完整报告文件

## 质量规则

1. **每个声明都需要来源。** 不允许无来源的断言。
2. **交叉验证。** 如果只有一个来源这样说，标记为未验证。
3. **时效性很重要。** 优先选择最近 12 个月内的来源。
4. **承认知识盲区。** 如果某个子问题找不到好信息，直接说明。
5. **不要幻觉。** 如果不知道，说"未找到足够数据。"

## 示例

```
"调研核聚变能源的现状"
"深入分析 2026 年后端服务选 Rust 还是 Go"
"调研自举 SaaS 业务的最佳策略"
"美国房地产市场现在是什么情况？"
```

## 子代理使用

作为子代理启动时，包含完整的调研请求和上下文：

```
sessions_spawn(
  task: "对 [TOPIC] 进行深度调研。遵循 deep-research-pro SKILL.md 工作流。
  先阅读 /home/clawdbot/clawd/skills/deep-research-pro/SKILL.md。
  目标：[用户目标]
  特定角度：[任何具体要求]
  将报告保存到 ~/clawd/research/[slug]/report.md
  完成后，用关键发现唤醒主会话。",
  label: "research-[slug]",
  model: "opus"
)
```

## 依赖要求

- DDG 搜索脚本：`/home/clawdbot/clawd/skills/ddg-search/scripts/ddg`
- curl（用于获取完整页面）
- 无需 API 密钥！
