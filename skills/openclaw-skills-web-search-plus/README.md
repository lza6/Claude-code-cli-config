# 网页搜索加

> 具有 **智能自动路由** 的统一多提供商网络搜索 — 使用多信号分析自动在 **Serper**、**Tavily**、**Exa**、**You.com** 和 **SearXNG** 之间进行选择，并进行置信度评分。

[![ClawHub](https://img.shields.io/badge/ClawHub-web--search--plus-blue)](https://clawhub.ai)
[![版本](https://img.shields.io/badge/version-2.7.0-green)](https://clawhub.ai)
[![GitHub](https://img.shields.io/badge/GitHub-web--search--plus-blue)](https://github.com/robbyczgw-cla/web-search-plus)

---

## 🧠 功能 (v2.7.0)

**智能多信号路由** — 该技能使用复杂的查询分析：

- **意图分类**：购物、研究、发现、RAG/实时、隐私
- **语言模式**：“多少钱”（价格）与“如何”（研究）与“私人”（隐私）
- **实体检测**：产品+品牌组合、URL、域名
- **复杂性分析**：长查询有利于研究提供商
- **置信度评分**：了解路由决策的可靠性

```bash
python3 scripts/search.py -q "how much does iPhone 16 cost"     # → Serper (68% confidence)
python3 scripts/search.py -q "how does quantum entanglement work"  # → Tavily (86% HIGH)
python3 scripts/search.py -q "startups similar to Notion"       # → Exa (76% HIGH)
python3 scripts/search.py -q "companies like stripe.com"        # → Exa (100% HIGH - URL detected)
python3 scripts/search.py -q "summarize key points on AI"       # → You.com (68% MEDIUM - RAG intent)
python3 scripts/search.py -q "search privately without tracking" # → SearXNG (74% HIGH - privacy intent)
```

---

## 🔍 何时使用哪个提供商

### 内置 Brave Search（OpenClaw 默认）
- ✅ 一般网络搜索
- ✅注重隐私
- ✅ 快速查找
- ✅ 默认后备

### Serper（谷歌结果）
- 🛍 **产品规格、价格、购物**
- 📍 **当地企业、地点**
- 🎯 **“Google it” - 明确的 Google 结果**
- 📰 **需要购物/图片**
- 🏆 **知识图谱数据**

### Tavilly（人工智能优化研究）
- 📚 **研究问题，深入研究**
- 🔬 **复杂的多部分查询**
- 📄 **需要整页内容**（不仅仅是片段）
- 🎓 **学术/技术研究**
- 🔒 **域过滤**（可信来源）

### Exa（神经语义搜索）
- 🔗 **查找相似页面**
- 🏢 **公司/初创公司发现**
- 📝 **研究论文**
- 💻 **GitHub 项目**
- 📅 **特定日期内容**

### You.com（RAG/实时）
- 🤖 **RAG 申请**（LLM 就绪片段）
- 📰 **组合网络 + 新闻**（单个 API 调用）
- ⚡ **实时信息**（时事）
- 📋 **摘要上下文**（“最新是什么......”）
- 🔄 **实时抓取**（整页内容点播）

### SearXNG（隐私第一/自托管）
- 🔒 **隐私保护搜索**（无跟踪）
- 🌐 **多源聚合**（70+引擎）
- 💰 **0 美元 API 成本**（自托管）
- 🎯 **不同的视角**（来自多个引擎的结果）
- 🏠 **自托管环境**（完全控制）

---

＃＃ 目录

- [快速启动](#quick-start)
- [智能自动路由](#smart-auto-routing)
- [配置指南](#configuration-guide)
- [提供商深度潜水](#provider-deep-dives)
- [使用示例](#usage-examples)
- [工作流程示例](#workflow-examples)
- [优化技巧](#optimization-tips)
- [常见问题解答与故障排除](#faq--故障排除)
- [API 参考](#api-reference)

---

## 快速入门

### 选项 A：交互式设置（推荐）

```bash
# Run the setup wizard - it guides you through everything
python3 scripts/setup.py
```

该向导会解释每个提供程序、收集您的 API 密钥并自动创建“config.json”。

### 选项 B：手动设置

```bash
# 1. Set up at least one API key (or SearXNG instance)
export SERPER_API_KEY="your-key"   # https://serper.dev
export TAVILY_API_KEY="your-key"   # https://tavily.com
export EXA_API_KEY="your-key"      # https://exa.ai
export YOU_API_KEY="your-key"      # https://api.you.com
export SEARXNG_INSTANCE_URL="https://your-instance.example.com"  # Self-hosted

# 2. Run a search (auto-routed!)
python3 scripts/search.py -q "best laptop 2024"
```

### 运行搜索

```bash
# Auto-routed to best provider
python3 scripts/search.py -q "best laptop 2024"

# Or specify a provider explicitly
python3 scripts/search.py -p serper -q "iPhone 16 specs"
python3 scripts/search.py -p tavily -q "quantum computing explained" --depth advanced
python3 scripts/search.py -p exa -q "AI startups 2024" --category company
```

---

## 智能自动路由

### 它是如何运作的

当您未指定提供商时，该技能会分析您的查询并将其路由到最佳提供商：

|查询包含 |路线至 |示例|
|----------------|------------|---------|
| “价格”、“购买”、“商店”、“成本”| **蛇** | “iPhone 16 价格”|
| “我附近”、“餐厅”、“酒店” | **蛇** | “我附近的披萨”|
| “天气”、“新闻”、“最新”| **蛇** | “柏林天气”|
| “如何”、“解释”、“是什么” | **塔维利** | “TCP 是如何工作的” |
| “研究”、“研究”、“分析”| **塔维利** | “气候研究”|
| “教程”、“指南”、“学习”| **塔维利** | “Python教程”|
| “类似于”、“公司喜欢”| **埃** | “像 Stripe 这样的公司” |
| “初创公司”、“A 轮融资”| **埃** | “AI初创公司A轮” |
| “github”、“研究论文”| **埃** | “法学硕士论文 arxiv”|
| “私人”、“匿名”、“无跟踪”| **SearXNG** | “私下搜索”|
| “多个来源”、“汇总” | **SearXNG** | “所有引擎的结果” |

### 示例

```bash
# These are all auto-routed to the optimal provider:
python3 scripts/search.py -q "MacBook Pro M3 price"           # → Serper
python3 scripts/search.py -q "how does HTTPS work"            # → Tavily
python3 scripts/search.py -q "startups like Notion"           # → Exa
python3 scripts/search.py -q "best sushi restaurant near me"  # → Serper
python3 scripts/search.py -q "explain attention mechanism"    # → Tavily
python3 scripts/search.py -q "alternatives to Figma"          # → Exa
python3 scripts/search.py -q "search privately without tracking" # → SearXNG
```

### 结果缓存（v2.7.0 中的新功能！）

搜索结果**自动缓存** 1 小时以节省 API 成本：

```bash
# First request: fetches from API ($)
python3 scripts/search.py -q "AI startups 2024"

# Second request: uses cache (FREE!)
python3 scripts/search.py -q "AI startups 2024"
# Output includes: "cached": true

# Bypass cache (force fresh results)
python3 scripts/search.py -q "AI startups 2024" --no-cache

# View cache stats
python3 scripts/search.py --cache-stats

# Clear all cached results
python3 scripts/search.py --clear-cache

# Custom TTL (in seconds, default: 3600 = 1 hour)
python3 scripts/search.py -q "query" --cache-ttl 7200
```

**缓存位置：**技能目录中的`.cache/`（使用`WSP_CACHE_DIR`环境变量覆盖）

### 调试自动路由

确切了解选择提供商的原因：

```bash
python3 scripts/search.py --explain-routing -q "best laptop to buy"
```

输出：
```json
{
  "query": "best laptop to buy",
  "selected_provider": "serper",
  "reason": "matched_keywords (score=2)",
  "matched_keywords": ["buy", "best"],
  "available_providers": ["serper", "tavily", "exa"]
}
```

### 结果中的路由信息

每个搜索结果都包含路由信息：

```json
{
  "provider": "serper",
  "query": "iPhone 16 price",
  "results": [...],
  "routing": {
    "auto_routed": true,
    "selected_provider": "serper",
    "reason": "matched_keywords (score=1)",
    "matched_keywords": ["price"]
  }
}
```

---

## 配置指南

### 环境变量

创建一个 `.env` 文件或在 shell 中设置这些文件：

```bash
# Required: Set at least one
export SERPER_API_KEY="your-serper-key"
export TAVILY_API_KEY="your-tavily-key"
export EXA_API_KEY="your-exa-key"
```

### 配置文件（config.json）

`config.json` 文件允许您自定义自动路由和提供程序默认值：

```json
{
  "defaults": {
    "provider": "serper",
    "max_results": 5
  },
  
  "auto_routing": {
    "enabled": true,
    "fallback_provider": "serper",
    "provider_priority": ["serper", "tavily", "exa"],
    "disabled_providers": [],
    "keyword_mappings": {
      "serper": ["price", "buy", "shop", "cost", "deal", "near me", "weather"],
      "tavily": ["how does", "explain", "research", "what is", "tutorial"],
      "exa": ["similar to", "companies like", "alternatives", "startup", "github"]
    }
  },
  
  "serper": {
    "country": "us",
    "language": "en"
  },
  
  "tavily": {
    "depth": "basic",
    "topic": "general"
  },
  
  "exa": {
    "type": "neural"
  }
}
```

### 配置示例

#### 示例 1：禁用 Exa（仅使用 Serper + Tavily）

```json
{
  "auto_routing": {
    "disabled_providers": ["exa"]
  }
}
```

#### 示例 2：将 Tavilly 设置为默认值

```json
{
  "auto_routing": {
    "fallback_provider": "tavily"
  }
}
```

#### 示例 3：添加自定义关键字

```json
{
  "auto_routing": {
    "keyword_mappings": {
      "serper": [
        "price", "buy", "shop", "amazon", "ebay", "walmart",
        "deal", "discount", "coupon", "sale", "cheap"
      ],
      "tavily": [
        "how does", "explain", "research", "what is",
        "coursera", "udemy", "learn", "course", "certification"
      ],
      "exa": [
        "similar to", "companies like", "competitors",
        "YC company", "funded startup", "Series A", "Series B"
      ]
    }
  }
}
```

#### 示例 4：Serper 的德语语言环境

```json
{
  "serper": {
    "country": "de",
    "language": "de"
  }
}
```

#### 示例 5：禁用自动路由

```json
{
  "auto_routing": {
    "enabled": false
  },
  "defaults": {
    "provider": "serper"
  }
}
```

#### 示例 6：研究型配置

```json
{
  "auto_routing": {
    "fallback_provider": "tavily",
    "provider_priority": ["tavily", "serper", "exa"]
  },
  "tavily": {
    "depth": "advanced",
    "include_raw_content": true
  }
}
```

---

## 提供商深入研究

### Serper（Google 搜索 API）

**它是什么：** 通过 API 直接访问 Google 搜索结果 — 与您在 google.com 上看到的结果相同。

#### 优势
|实力|描述 |
|----------|-------------|
| 🎯 **准确性** |谷歌的搜索质量、知识图、特色片段|
| 🛒 **购物** |产品价格、评论、购物结果 |
| 📍 **本地** |企业列表、地图、地点 |
| 📰 **新闻** |与 Google 新闻集成的实时新闻 |
| 🖼 **图像** |谷歌图片搜索|
| ⚡ **速度** |最快的响应时间（~200-400ms）|

#### 最佳用例
- ✅ 产品规格和比较
- ✅ 购物和价格查询
- ✅ 本地商家搜索（“我附近的餐馆”）
- ✅ 快速事实查询（天气、换算、定义）
- ✅ 新闻标题和时事
- ✅ 图片搜索
- ✅ 当您需要“Google 显示的内容”时

#### 获取您的 API 密钥
1. 前往 [serper.dev](https://serper.dev)
2. 使用电子邮件或 Google 注册
3. 从仪表板复制您的 API 密钥
4. 设置`SERPER_API_KEY`环境变量

---

### Tavily（研究搜索）

**它是什么：** 专为研究和 RAG 应用程序而构建的人工智能优化搜索引擎 — 返回综合答案和完整内容。

#### 优势
|实力|描述 |
|----------|-------------|
| 📚 **研究质量** |针对全面、准确的研究进行优化 |
| 💬 **人工智能答案** |返回综合答案，而不仅仅是链接 |
| 📄 **完整内容** |可以返回完整的页面内容(raw_content) |
| 🎯 **域名过滤** |包含/排除特定域 |
| 🔬 **深度模式** |深入研究的高级搜索 |
| 📰 **主题模式** |专门针对一般内容与新闻内容 |

#### 最佳用例
- ✅ 研究需要综合答案的问题
- ✅ 学术或技术深入研究
- ✅ 当您需要实际的页面内容（而不仅仅是片段）时
- ✅ 多源信息对比
- ✅ 特定领域的研究（过滤权威来源）
- ✅ 结合背景的新闻研究
- ✅ RAG/LLM 申请

#### 获取您的 API 密钥
1. 前往[tavily.com](https://tavily.com)
2. 注册并验证邮箱
3. 导航至 API 密钥部分
4. 生成并复制您的密钥
5. 设置 `TAVILY_API_KEY` 环境变量

---

### Exa（神经搜索）

**它是什么：** 神经/语义搜索引擎可以理解含义，而不仅仅是关键字 - 找到概念上相似的内容。

#### 优势
|实力|描述 |
|----------|-------------|
| 🧠 **语义理解** |按含义查找结果，而不是关键字 |
| 🔗 **类似页面** |查找与参考 URL 类似的页面 |
| 🏢 **公司发现** |非常适合寻找初创公司、公司 |
| 📑 **类别过滤器** |按类型过滤（公司、论文、推文等）|
| 📅 **日期过滤** |精确的日期范围搜索 |
| 🎓 **学术** |非常适合研究论文和技术内容 |

#### 最佳用例
- ✅ 概念查询（“构建 X 的公司”）
- ✅ 寻找相似的公司或页面
- ✅ 初创公司和公司发现
- ✅ 研究论文发现
- ✅ 查找 GitHub 项目
- ✅ 按日期过滤搜索最近的内容
- ✅ 当关键字匹配失败时

#### 获取您的 API 密钥
1. 前往 [exa.ai](https://exa.ai)
2. 使用电子邮件或 Google 注册
3. 导航至仪表板中的 API 部分
4. 复制您的 API 密钥
5. 设置`EXA_API_KEY`环境变量

---

### SearXNG（隐私第一元搜索）

**它是什么：** 开源、自托管元搜索引擎，聚合来自 70 多个搜索引擎的结果，无需跟踪。

#### 优势
|实力|描述 |
|----------|-------------|
| 🔒 **隐私第一** |没有跟踪、没有分析、没有数据收集 |
| 🌐 **多引擎** |聚合 Google、Bing、DuckDuckGo 和 70 多个 |
| 💰 **免费** | 0 美元 API 成本（自托管、无限制查询）|
| 🎯 **多样化的结果** |从多个搜索引擎获取观点 |
| ⚙ **可定制** |选择要使用的引擎、安全搜索、语言 |
| 🏠 **自托管** |完全控制您的搜索基础设施 |

#### 最佳用例
- ✅ 隐私敏感搜索（无跟踪）
- ✅ 当您希望从多个引擎获得不同的结果时
- ✅ 注重预算（无 API 费用）
- ✅ 自托管/气隙环境
- ✅ 付费 API 受到速率限制时的回退
- ✅ 当“聚合一切”是目标时

#### 设置您的实例
```bash
# Docker (recommended, 5 minutes)
docker run -d -p 8080:8080 searxng/searxng

# Enable JSON API in settings.yml:
# search:
#   formats: [html, json]
```

1. 请参阅[docs.searxng.org](https://docs.searxng.org/admin/installation.html)
2. 通过 Docker、pip 或您喜欢的方法进行部署
3. 在 `settings.yml` 中启用 JSON 格式
4. 设置`SEARXNG_INSTANCE_URL`环境变量

---

## 用法示例

### 自动路由搜索（推荐）

```bash
# Just search — the skill picks the best provider
python3 scripts/search.py -q "Tesla Model 3 price"
python3 scripts/search.py -q "how do neural networks learn"
python3 scripts/search.py -q "YC startups like Stripe"
python3 scripts/search.py -q "search privately without tracking"
```

### Serper 选项

```bash
# Different search types
python3 scripts/search.py -p serper -q "gaming monitor" --type shopping
python3 scripts/search.py -p serper -q "coffee shop" --type places
python3 scripts/search.py -p serper -q "AI news" --type news

# With time filter
python3 scripts/search.py -p serper -q "OpenAI news" --time-range day

# Include images
python3 scripts/search.py -p serper -q "iPhone 16 Pro" --images

# Different locale
python3 scripts/search.py -p serper -q "Wetter Wien" --country at --language de
```

### 塔维利选项

```bash
# Deep research mode
python3 scripts/search.py -p tavily -q "quantum computing applications" --depth advanced

# With full page content
python3 scripts/search.py -p tavily -q "transformer architecture" --raw-content

# Domain filtering
python3 scripts/search.py -p tavily -q "AI research" --include-domains arxiv.org nature.com
```

### Exa 选项

```bash
# Category filtering
python3 scripts/search.py -p exa -q "AI startups Series A" --category company
python3 scripts/search.py -p exa -q "attention mechanism" --category "research paper"

# Date filtering
python3 scripts/search.py -p exa -q "YC companies" --start-date 2024-01-01

# Find similar pages
python3 scripts/search.py -p exa --similar-url "https://stripe.com" --category company
```

### SearXNG 选项

```bash
# Basic search
python3 scripts/search.py -p searxng -q "linux distros"

# Specific engines only
python3 scripts/search.py -p searxng -q "AI news" --engines "google,bing,duckduckgo"

# SafeSearch (0=off, 1=moderate, 2=strict)
python3 scripts/search.py -p searxng -q "privacy tools" --searxng-safesearch 2

# With time filter
python3 scripts/search.py -p searxng -q "open source projects" --time-range week

# Custom instance URL
python3 scripts/search.py -p searxng -q "test" --searxng-url "http://localhost:8080"
```

---

## 工作流程示例

### 🛒 产品研究工作流程

```bash
# Step 1: Get product specs (auto-routed to Serper)
python3 scripts/search.py -q "MacBook Pro M3 Max specs"

# Step 2: Check prices (auto-routed to Serper)
python3 scripts/search.py -q "MacBook Pro M3 Max price comparison"

# Step 3: In-depth reviews (auto-routed to Tavily)
python3 scripts/search.py -q "detailed MacBook Pro M3 Max review"
```

### 📚 学术研究工作流程

```bash
# Step 1: Understand the topic (auto-routed to Tavily)
python3 scripts/search.py -q "explain transformer architecture in deep learning"

# Step 2: Find recent papers (Exa)
python3 scripts/search.py -p exa -q "transformer improvements" --category "research paper" --start-date 2024-01-01

# Step 3: Find implementations (Exa)
python3 scripts/search.py -p exa -q "transformer implementation" --category github
```

### 🏢 竞争分析工作流程

```bash
# Step 1: Find competitors (auto-routed to Exa)
python3 scripts/search.py -q "companies like Notion"

# Step 2: Find similar products (Exa)
python3 scripts/search.py -p exa --similar-url "https://notion.so" --category company

# Step 3: Deep dive comparison (Tavily)
python3 scripts/search.py -p tavily -q "Notion vs Coda comparison" --depth advanced
```

---

## 优化技巧

### 成本优化

|提示 |储蓄|
|-----|---------|
|使用 SearXNG 进行日常查询 | **0 美元 API 成本** |
|使用自动路由（默认为 Serper，付费最便宜）|最超值|
|在“高级”之前使用 Tavily“基本” |成本降低约 50% |
|设置适当的“max_results” |线性成本节省|
|仅将 Exa 用于语义查询 |避免浪费 |

### 性能优化

|提示 |影响 |
|-----|--------|
| Serper 最快（约 200 毫秒）|用于时间敏感的查询 |
| “基本”比“高级”快得多 |快约 2 倍 |
|较低的“max_results” = 更快的响应 |线性改进 |

---

## 常见问题解答和故障排除

### 一般问题

**问：我是否需要所有三个提供商的 API 密钥？**
> 不需要。您只需要您想要使用的提供商的密钥。自动路由会跳过没有密钥的提供商。

**问：我应该从哪个提供商开始？**
> Serper — 它是最快、最便宜的，并且拥有最大的免费套餐（2,500 个查询）。

**问：我可以在一个工作流程中使用多个提供商吗？**
> 是的！这是推荐的方法。请参阅[工作流程示例](#workflow-examples)。

**问：如何降低 API 成本？**
> 使用自动路由（默认为最便宜），从较低的“max_results”开始，在“advanced”之前使用 Tavily“basic”。

### 自动路由问题

**问：为什么我的查询发送到了错误的提供商？**
> 使用 `--explain-routing` 进行调试。如果需要，将自定义关键字添加到 config.json。

**问：我可以添加自己的关键字吗？**
> 是的！编辑 `config.json` → `auto_routing.keyword_mappings`。

**问：关键词评分如何运作？**
> 多词短语获得更高的权重。 “公司喜欢”（2 个词）的得分高于“喜欢”（1 个词）。

**问：如果没有关键字匹配怎么办？**
> 使用后备提供程序（默认：Serper）。

**问：我可以强制选择特定的提供商吗？**
> 是的，使用 `-p serper`、`-p tavily` 或 `-p exa`。

### 故障排除

**错误：“缺少 API 密钥”**
```bash
# Check if key is set
echo $SERPER_API_KEY

# Set it
export SERPER_API_KEY="your-key"
```

**错误：“API 错误 (401)”**
> 您的 API 密钥无效或已过期。生成一个新的。

**错误：“API 错误 (429)”**
> 速率有限。等待并重试，或升级您的计划。

**结果为空？**
> 尝试不同的提供商、扩大您的查询范围或删除限制性过滤器。

**反应慢？**
> 减少 `max_results`，使用 Tavily `basic`，或使用 Serper（最快）。

---

## API 参考

### 输出格式

所有提供者返回统一的JSON：

```json
{
  "provider": "serper|tavily|exa",
  "query": "original search query",
  "results": [
    {
      "title": "Page Title",
      "url": "https://example.com/page",
      "snippet": "Content excerpt...",
      "score": 0.95,
      "date": "2024-01-15",
      "raw_content": "Full page content (Tavily only)"
    }
  ],
  "images": ["url1", "url2"],
  "answer": "Synthesized answer",
  "knowledge_graph": { },
  "routing": {
    "auto_routed": true,
    "selected_provider": "serper",
    "reason": "matched_keywords (score=1)",
    "matched_keywords": ["price"]
  }
}
```

### CLI 选项参考

|选项 |供应商|描述 |
|--------|------------|-------------|
| `-q, --query` |全部 |搜索查询 |
| `-p, --provider` |全部 |提供商：auto、serper、tavily、exa、you、searxng |
| `-n, --最大结果` |全部 |最大结果（默认：5）|
| `--自动` |全部 |强制自动路由 |
| `--解释路由` |全部 |调试自动路由|
| `--图像` |塔维利·塞珀 |包括图像 |
| `--国家` |瑟珀，你|国家/地区代码（默认：美国）|
| `--语言` | Serper、SearXNG |语言代码（默认：en）|
| `--类型` |蛇 |搜索/新闻/图片/视频/地点/购物 |
| `--时间范围` | Serper、SearXNG |小时/天/周/月/年|
| `--深度` |塔维利 |基础/高级 |
| `--主题` |塔维利 |一般/新闻 |
| `--原始内容` |塔维利 |包括整页内容 |
| `--exa-type` |埃克 |神经/关键字 |
| `--类别` |埃克 |公司/研究论文/新闻/pdf/github/tweet |
| `--开始日期` |埃克 |开始日期 (YYYY-MM-DD) |
| `--结束日期` |埃克 |结束日期 (YYYY-MM-DD) |
| `--相似网址` |埃克 |查找类似页面 |
| `--searxng-url` |西尔XNG |实例 URL |
| `--searxng-safesearch` |西尔XNG | 0=关闭，1=中等，2=严格 |
| `--引擎` |西尔XNG |特定引擎（google、bing、duckduckgo）|
| `--类别` |西尔XNG |搜索类别（一般、图像、新闻）|
| `--include-domains` |塔维利，Exa |仅这些域 |
| `--排除域` |塔维利，Exa |排除这些域 |
| `--紧凑` |全部 |紧凑的 JSON 输出 |

---

＃＃ 执照

麻省理工学院

---

## 链接

- [Serper](https://serper.dev) — Google 搜索 API
- [Tavily](https://tavily.com) — 人工智能研究搜索
- [Exa](https://exa.ai) — 神经搜索
- [ClawHub](https://clawhub.ai) — OpenClaw 技能
