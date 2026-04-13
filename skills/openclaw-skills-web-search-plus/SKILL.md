---
name: web-search-plus
version: 2.7.2
description: "具有智能自动路由的统一搜索技能。使用多信号分析自动在 Serper (Google)、Tavily (研究)、Exa (神经)、You.com (RAG/实时) 和 SearXNG (隐私/自托管) 之间进行选择，并进行置信度评分。"
tags: [search, web-search, serper, tavily, exa, you, searxng, google, research, semantic-search, auto-routing, multi-provider, shopping, rag, free-tier, privacy, self-hosted]
metadata: {"openclaw":{"requires":{"bins":["python3","bash"],"env":{"SERPER_API_KEY":"optional","TAVILY_API_KEY":"optional","EXA_API_KEY":"optional","YOU_API_KEY":"optional","SEARXNG_INSTANCE_URL":"optional"},"note":"只需一个提供商密钥。所有都是可选的。"}}}
---

# 网页搜索 Plus

**停止选择搜索提供商。让技能为你做事。**

这项技能可将你连接到 5 个搜索提供商（Serper、Tavily、Exa、You.com、SearXNG），并自动为每个查询选择最佳搜索提供商。购物问题？→ Google 结果。研究问题？→ 深度研究引擎。想要隐私？→ 自托管选项。

---

## ✨ 有何不同？

- **只需搜索** — 无需考虑使用哪个提供商
- **智能路由** — 分析你的查询并自动选择最佳提供商
- **5 个提供商，1 个界面** — Google 结果、研究引擎、神经搜索、RAG 优化和隐私优先集于一身
- **只需 1 个密钥即可使用** — 从任何单个提供商开始，稍后添加更多提供商
- **提供免费选项** — SearXNG 完全免费（自托管）

---

## 🚀 快速入门

```bash
# 交互式设置（推荐首次运行）
python3 scripts/setup.py

# 或手动：复制配置并添加密钥
cp config.example.json config.json
```

该向导解释每个提供程序、收集 API 密钥并配置默认值。

---

## 🔑 API 密钥

你只需要**一把**钥匙即可开始。稍后添加更多提供商以获得更好的覆盖范围。

| 提供商 | 免费套餐 | 最适合 | 注册 |
|----------|------------|----------|---------|
| **Serper** | 2,500/月 | 购物、价格、本地、新闻 | [serper.dev](https://serper.dev) |
| **Tavily** | 1,000/月 | 研究、解释、学术 | [tavily.com](https://tavily.com) |
| **Exa** | 1,000/月 | "类似于 X"，初创公司，论文 | [exa.ai](https://exa.ai) |
| **You.com** | 有限 | 实时信息、AI/RAG 上下文 | [api.you.com](https://api.you.com) |
| **SearXNG** | **免费** ✅ | 隐私、多源、0 美元成本 | 自托管 |

**设置你的密钥：**

```bash
# 选项 A：.env 文件（推荐）
export SERPER_API_KEY="your-key"
export TAVILY_API_KEY="your-key"

# 选项 B：config.json
{ "serper": { "api_key": "your-key" } }
```

---

## 🎯 何时使用哪个提供商

| 我想... | 提供商 | 示例查询 |
|--------------|----------|---------------|
| 查找产品价格 | **Serper** | "iPhone 16 Pro Max 价格" |
| 查找附近的餐馆/商店 | **Serper** | "我附近最好的披萨" |
| 了解事物如何运作 | **Tavily** | "HTTPS 加密是如何工作的" |
| 深入研究 | **Tavily** | "气候变化研究 2024" |
| 寻找像 X 这样的公司 | **Exa** | "类似于 Notion 的初创公司" |
| 查找研究论文 | **Exa** | "Transformer 架构论文" |
| 获取实时信息 | **You.com** | "最新 AI 监管新闻" |
| 搜索而不被追踪 | **SearXNG** | 任何事情，私下里 |

**专业提示：** 正常搜索即可！自动路由可以正确处理大多数查询。需要时用 `-p provider` 覆盖。

---

## 🧠 自动路由的工作原理

该技能会查看你的查询并选择最佳的提供商：

```bash
"iPhone 16 price"              → Serper (购物关键词)
"how does quantum computing work" → Tavily (研究问题)
"companies like stripe.com"    → Exa (检测到 URL，相似性)
"latest news on AI"            → You.com (实时意图)
"search privately"             → SearXNG (隐私关键词)
```

**如果选择错误怎么办？** 覆盖它：`python3 scripts/search.py -p tavily -q "your query"`

**调试路由：** `python3 scripts/search.py --explain-routing -q "your query"`

---

## 📖 使用示例

### 让自动路由选择（推荐）

```bash
python3 scripts/search.py -q "Tesla Model 3 price"
python3 scripts/search.py -q "explain machine learning"
python3 scripts/search.py -q "startups like Figma"
```

### 强制指定特定提供商

```bash
python3 scripts/search.py -p serper -q "weather Berlin"
python3 scripts/search.py -p tavily -q "quantum computing" --depth advanced
python3 scripts/search.py -p exa --similar-url "https://stripe.com" --category company
python3 scripts/search.py -p you -q "breaking tech news" --include-news
python3 scripts/search.py -p searxng -q "linux distros" --engines "google,bing"
```

---

## ⚙ 配置

```json
{
  "auto_routing": {
    "enabled": true,
    "fallback_provider": "serper",
    "confidence_threshold": 0.3,
    "disabled_providers": []
  },
  "serper": {"country": "us", "language": "en"},
  "tavily": {"depth": "advanced"},
  "exa": {"type": "neural"},
  "you": {"country": "US", "include_news": true},
  "searxng": {"instance_url": "https://your-instance.example.com"}
}
```

---

## 📊 提供商比较

| 特性 | Serper | Tavily | Exa | You.com | SearXNG |
|--------|:------:|:------:|:---:|:-------:|:-------:|
| 速度 | ⚡⚡⚡ | ⚡⚡ | ⚡⚡ | ⚡⚡⚡ | ⚡⚡ |
| 事实准确性 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 语义理解 | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| 整页内容 | ✗ | ✓ | ✓ | ✓ | ✗ |
| 购物/本地 | ✓ | ✗ | ✗ | ✗ | ✓ |
| 查找类似页面 | ✗ | ✗ | ✓ | ✗ | ✗ |
| RAG 优化 | ✗ | ✓ | ✗ | ✓✓ | ✗ |
| 隐私优先 | ✗ | ✗ | ✗ | ✗ | ✓✓ |
| API 成本 | $$ | $$ | $$ | $ | **免费** |

---

## ❓ 常见问题

### 我是否需要所有提供商的 API 密钥？
**不需要。** 你只需要你想要使用的提供商的密钥。从一个开始（推荐 Serper），稍后添加更多。

### 我应该从哪个提供商开始？
**Serper** — 最快、最便宜、最大的免费套餐（每月 2,500 个查询），并且可以很好地处理大多数查询。

### 如果我用完免费查询怎么办？
该技能会自动回退到你配置的其他提供者。或者切换到 SearXNG（无限制，自托管）。

### 这要多少钱？
- **免费层级：** 2,500 (Serper) + 1,000 (Tavily) + 1,000 (Exa) = 4,500+ 免费搜索/月
- **SearXNG：** 完全免费（如果你在 VPS 上自行托管，则只需约 5 美元/月）
- **付费计划：** 起价约为每月 10-50 美元，具体取决于提供商

### SearXNG 真的是私密的吗？
**是的，如果是自托管的话。** 你控制服务器，无需跟踪，无需分析。公共实例取决于运营商的策略。

### 如何设置 SearXNG？
```bash
# Docker（5 分钟）
docker run -d -p 8080:8080 searxng/searxng
```
然后在 `settings.yml` 中启用 JSON API。参阅 [docs.searxng.org](https://docs.searxng.org/admin/installation.html)。

### 为什么它将我的查询路由到"错误"的提供商？
有时查询是不明确的。使用 `--explain-routing` 查看原因，然后根据需要使用 `-p provider` 覆盖。

---

## 🔄 自动回退

如果一个提供程序失败（速率限制、超时、错误），该技能会自动尝试下一个提供程序。发生这种情况时，你将在响应中看到 `routing.fallback_used: true`。

---

## 📤 输出格式

```json
{
  "provider": "serper",
  "query": "iPhone 16 price",
  "results": [{"title": "...", "url": "...", "snippet": "...", "score": 0.95}],
  "routing": {
    "auto_routed": true,
    "provider": "serper",
    "confidence": 0.78,
    "confidence_level": "high"
  }
}
```

---

## ⚠ 重要提示

**Tavily、Serper 和 Exa 不是核心 OpenClaw 提供商。**

❌ 不要修改这些 `~/.openclaw/openclaw.json`
✅ 使用此技能的脚本 — 从 `.env` 自动加载密钥

---

## 🔒 安全

**SearXNG SSRF 保护：** SearXNG 实例 URL 通过深度防御进行验证：
- 仅强制执行 `http`/`https` 方案
- 阻止云元数据端点（169.254.169.254、metadata.google.internal）
- 解析主机名并阻止私有/内部 IP（环回、RFC1918、链路本地、保留）
- 有意在专用网络上自行托管的运营商可以设置 `SEARXNG_ALLOW_PRIVATE=1`

## 📚 更多文档

- **[FAQ.md](FAQ.md)** — 更多问题的详细解答
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — 修复常见错误
- **[README.md](README.md)** — 完整技术参考

---

## 🔗 快速链接

- [Serper](https://serper.dev) — Google 搜索 API
- [Tavily](https://tavily.com) — AI 研究搜索
- [Exa](https://exa.ai) — 神经搜索
- [You.com](https://api.you.com) — RAG/实时搜索
- [SearXNG](https://docs.searxng.org) — 隐私优先元搜索
