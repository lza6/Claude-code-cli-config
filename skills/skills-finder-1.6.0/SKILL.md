---
name: skills-finder
version: 1.6.0
description: 智能 Skill 匹配器，实时搜索多个 Skill 市场（ClawHub 和 Skills.sh）。支持任意语言的用户输入、多步 Skill 链接和一键安装。
---

# Skills Finder 🔍

**智能 Skill 发现引擎，可搜索多个 Skill 市场并为您推荐最适合任务的 Skill。**

---

## 🎯 何时使用

**当用户想要查找或安装 Skill 时自动触发：**

| 用户意图 | 示例 |
|-------------|----------|
| 查找 Skill | "帮我找个...", "find a skill", "buscar herramienta", "スキルを探して" |
| 搜索功能 | "有什么 skill 能做...", "what can you do", "有什么工具" |
| 安装 Skill | "安装...", "install", "instalar", "インストール" |
| 获取推荐 | "推荐...", "recommend", "recomendar", "おすすめ" |

---

## 🌍 通用语言支持

**此 Skill 支持用户使用任意语言输入！**

### 支持的语言（真正通用）

此 Skill 支持**所有语言和文字系统**，包括但不限于：

| 语言体系 | 示例 |
|-----------------|----------|
| **欧洲语言** | English, Spanish, French, German, Italian, Portuguese, Russian |
| **亚洲语言** | Chinese (中文), Japanese (日本語), Korean (한국어), Vietnamese, Thai |
| **中东语言** | Arabic, Hebrew, Persian, Turkish |
| **南亚语言** | Hindi, Bengali, Tamil, Urdu |
| **非洲语言** | Swahili, Zulu, Amharic |
| **特殊输入** | Emoji 表情查询 📱💻🔍 |

---

## 🌐 支持的 Skill 市场

### 1. ClawHub (clawhub.ai)
```bash
npx clawhub@latest search "<query>"
npx clawhub@latest install <name>
```
- 可用 Skill 数量 **5,400+**
- 开源 AI 助手 Skill
- 基于评分的推荐

### 2. Skills CLI (skills.sh)
```bash
npx skills find "<query>"
npx skills add <package>
```
- **Skills.sh** - 开放式 Agent Skill 包管理器
- 扩展 Agent 能力的模块化包
- 专业知识、工作流和工具

---

## ⚡ 快速命令

```bash
# 搜索 Skill (支持任意语言)
~/.openclaw/workspace/skills/skills-finder/scripts/skill-finder.sh search "your query"

# 搜索特定市场
~/.openclaw/workspace/skills/skills-finder/scripts/skill-finder.sh search "query" --source clawhub
~/.openclaw/workspace/skills/skills-finder/scripts/skill-finder.sh search "query" --source skills

# 搜索全部 (默认)
~/.openclaw/workspace/skills/skills-finder/scripts/skill-finder.sh search "query" --source all

# 从特定来源安装
~/.openclaw/workspace/skills/skills-finder/scripts/skill-finder.sh install <name> --source clawhub
~/.openclaw/workspace/skills/skills-finder/scripts/skill-finder.sh install <package> --source skills

# 列出已安装的 Skill
~/.openclaw/workspace/skills/skills-finder/scripts/skill-finder.sh list
```

---

## 🔗 多步 Skill 链式调用

**对于需要多个 Skill 协同完成的复杂任务，搜索会自动检测并推荐 Skill 链。**

### 链式检测

| 任务类型 | 示例 | 结果 |
|-----------|---------|--------|
| 单个 Skill | "天气 skill" | 直接推荐 |
| 多步骤任务 | "搜索新闻发送到微信" | Skill 链 + 组合建议 |

---

## 📋 使用示例

### 示例 1：搜索全部来源
```
User: 找个天气 skill

→ ClawHub: weather (3.898⭐)
→ Skills: @skills/weather

Results from both marketplaces shown!
```

### 示例 2：搜索指定来源
```
User: find a skill for GitHub

→ Searching ClawHub only:
  - github (3.636⭐)
  - github-cli (3.538⭐)
```

### 示例 3：多语言
```
User: 天気を調べて
→ ClawHub: weather
→ Skills: @skills/weather
```

---

## 🔧 实现方式

### 双来源搜索

```bash
# Search ClawHub
npx clawhub@latest search "<query>"

# Search Skills.sh
npx skills find "<query>"

# Both results merged and ranked
```

### 来源优先级

| 来源 | 优先级 | 适用场景 |
|--------|----------|----------|
| ClawHub | 默认 | 通用 AI 助手 Skill |
| Skills.sh | 备选 | 专用工作流 |

---

## ⚠️ 重要说明

### 为什么有两个来源？

1. **ClawHub** - 大型 AI 助手 Skill 收录库 (5,400+)
2. **Skills.sh** - 面向 Agent 的专用工作流和工具

默认同时搜索两个来源以获取全面的结果。

### 速率限制

- **ClawHub**：60 次请求/小时 (登录后更高)
- **Skills.sh**：通过 `npx skills --help` 查看

---

## 📦 依赖项

- Node.js + npx
- curl
- jq

---

## 总结

**一句话概括：用户使用任意语言输入 → 同时搜索 ClawHub 和 Skills.sh → 以用户语言回复 → 为复杂任务推荐 Skill 链**

---
