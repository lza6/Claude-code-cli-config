# 变更日志 - Web 搜索 Plus

## [2.7.0] - 2026-02-14

### ✨ 已添加
- “.cache/provider_health.json”中的提供者冷却时间跟踪
- 提供商故障的指数冷却时间：**1m → 5m → 25m → 1h（上限）**
- 瞬态故障的重试策略（超时、429、503）：最多 2 次带退避的重试 **1s → 3s → 9s**
- 从完整请求上下文中散列的更智能的缓存键（查询/提供程序/最大结果+区域设置、新鲜度、时间范围、主题、搜索引擎、包含新闻和相关参数）
- 在回退合并期间通过规范化 URL 进行跨提供商结果重复数据删除

### 🔧 已更改
- 当冷却时间处于活动状态时，冷却提供者会在路由中被跳过
- 成功请求后，提供者健康状况会自动重置
- 后备输出现在包括重复数据删除元数据：
  - `去重：true|false`
  - `metadata.dedup_count`


## [2.6.5] - 2026-02-11

### 🆕 基于文件的结果缓存

添加本地缓存以节省重复搜索的 API 成本：

#### 特点
- **自动缓存**：搜索结果默认缓存在本地
- **1 小时 TTL**：结果在 3600 秒后过期（可配置）
- **缓存指示器**：响应包括 `cached: true/false` 和 `cache_age_seconds`
- **零成本重复**：缓存的请求不会命中 API

#### 新的 CLI 选项
- `--cache-ttl SECONDS` — 自定义缓存 TTL（默认值：3600）
- `--no-cache` — 绕过缓存，始终获取新鲜数据
- `--clear-cache` — 删除所有缓存的结果
- `--cache-stats` — 显示缓存统计信息（条目、大小、年龄）

#### 配置
- **缓存目录**：技能目录中的`.cache/`
- **环境变量**：`WSP_CACHE_DIR`覆盖位置
- **缓存密钥**：基于查询 + 提供者 + max_results (SHA256)

#### 用法示例
```bash
# First request costs API credits
python3 scripts/search.py -q "AI startups"

# Second request is FREE (uses cache)
python3 scripts/search.py -q "AI startups"

# Force fresh results
python3 scripts/search.py -q "AI startups" --no-cache

# View stats
python3 scripts/search.py --cache-stats

# Clear everything
python3 scripts/search.py --clear-cache
```

#### 技术细节
- 缓存文件：带有元数据的 JSON（_cache_timestamp、_cache_key 等）
- 自动清理访问过期条目
- 妥善处理损坏的缓存文件

## [2.6.1] - 2026-02-04

- 隐私清理：从文档中删除了硬编码路径和个人信息

## [2.5.0] - 2026-02-03

### 🆕 新提供商：SearXNG（隐私优先元搜索）

添加 SearXNG 作为第五个搜索提供商，专注于隐私和自托管搜索：

#### 特点
- **隐私保护**：无跟踪，无分析 - 您的搜索保持私密
- **多源聚合**：查询70+上游引擎（Google、Bing、DuckDuckGo等）
- **0 美元 API 成本**：自托管 = 无限制查询，无需 API 费用
- **多样化结果**：在一个查询中获取多个搜索引擎的观点
- **可定制**：选择要使用的引擎、设置安全搜索级别、语言首选项

#### 自动路由信号
通往 SearXNG 的新隐私/多源意图检测路线用于：
- 隐私查询：“私人”、“匿名”、“无跟踪”、“无跟踪”
- 多来源：“汇总结果”、“多个来源”、“多样化视角”
- 预算/免费：“免费搜索”、“无 API 成本”、“自托管搜索”
- 德语：“privat”、“anonym”、“ohne Tracking”、“verschiedene quellen”

#### 用法示例
```bash
# Auto-routed
python3 scripts/search.py -q "search privately without tracking"  # → SearXNG

# Explicit
python3 scripts/search.py -p searxng -q "linux distros"
python3 scripts/search.py -p searxng -q "AI news" --engines "google,bing,duckduckgo"
python3 scripts/search.py -p searxng -q "privacy tools" --searxng-safesearch 2
```

＃＃＃＃ 配置
```json
{
  "searxng": {
    "instance_url": "https://your-instance.example.com",
    "safesearch": 0,
    "engines": null,
    "language": "en"
  }
}
```

#### 设置
SearXNG 需要启用 JSON 格式的自托管实例：
```bash
# Docker setup (5 minutes)
docker run -d -p 8080:8080 searxng/searxng

# Enable JSON in settings.yml:
# search:
#   formats: [html, json]

# Set instance URL
export SEARXNG_INSTANCE_URL="http://localhost:8080"
```

请参阅：https://docs.searxng.org/admin/installation.html

### 📊 更新了提供商比较

|特色|蛇 |塔维利 |埃克 |友网 |西尔XNG |
|--------|:------:|:------:|:---:|:-------:|:-------:|
|隐私第一 | ✗ | ✗ | ✗ | ✗ | ✓✓ |
|自托管 | ✗ | ✗ | ✗ | ✗ | ✓ |
| API 成本 | $$ | $$ | $$ | $ | **免费** |
|多引擎 | ✗ | ✗ | ✗ | ✗ | ✓ (70+) |

### 🔧 技术变更

- 添加了具有完整错误处理功能的“search_searxng()”函数
- 向 QueryAnalyzer 添加了“PRIVACY_SIGNALS”以实现自动路由
- 使用 SearXNG 选项更新了设置向导（实例 URL 验证）
- 使用 searchxng 部分更新了 config.example.json
- 新的 CLI 参数：`--searxng-url`、`--searxng-safesearch`、`--engines`、`--categories`

---

## [2.4.4] - 2026-02-03

### 📝 文档：提供者计数修复

- **修正：**“您可以使用 1、2 或全部 3”→“1、2、3 或全部 4”（我们现在有 4 个提供商！）
- **影响：** 设置向导的准确文档

## [2.4.3] - 2026-02-03

### 📝 文档：更新了自述文件

- **添加：** SKILL.md 中 You.com 的“v2.4.2 新增功能”徽章
- **影响：** ClawHub 自述文件现在正确地将 You.com 突出显示为新功能

## [2.4.2] - 2026-02-03

### 🐛 关键修复：You.com API 配置

- **已修复：** 主机名不正确（`api.ydc-index.io` → `ydc-index.io`）
- **已修复：** 标头名称不正确（`X-API-Key`→`X-API-KEY` 大写）
- **影响：** You.com 现在可以正常工作 - 之前给出 403 Forbidden
- **状态：** ✅ 全面测试并正常工作

## [2.4.1] - 2026-02-03

### 🐛 错误修复：You.com URL 编码

- **修复：** You.com 查询的 URL 编码 - 空格和特殊字符现在已正确编码
- **影响：** 带空格的查询（例如“OpenClaw AI 框架”）现在可以正常工作
- **技术：**为参数编码添加了`urllib.parse.quote`

## [2.4.0] - 2026-02-03

### 🆕 新提供商：You.com

添加 You.com 作为第四个搜索提供商，针对 RAG 应用程序和实时信息进行了优化：

#### 特点
- **LLM-Ready Snippets**：预先提取的、查询感知的文本摘录，非常适合输入人工智能模型
- **统一网络 + 新闻**：在单个 API 调用中获取网页和新闻文章
- **Live Crawling**：以 Markdown 格式按需获取整页内容（`--livecrawl`）
- **自动新闻分类**：根据查询意图智能包含新闻结果
- **新鲜度控制**：按最近发生时间（日、周、月、年或日期范围）过滤
- **安全搜索支持**：内容过滤（关闭、中等、严格）

#### 自动路由信号
新的 RAG/实时意图检测路由到 You.com，用于：
- RAG 上下文查询：“总结”、“关键点”、“tldr”、“上下文”
- 实时信息：“最新消息”、“当前状态”、“现在”、“正在发生什么”
- 信息综合：“最新情况”、“情况”、“主要要点”

#### 用法示例
```bash
# Auto-routed
python3 scripts/search.py -q "summarize key points about AI regulation"  # → You.com

# Explicit
python3 scripts/search.py -p you -q "climate change" --livecrawl all
python3 scripts/search.py -p you -q "tech news" --freshness week
```

＃＃＃＃ 配置
```json
{
  "you": {
    "country": "US",
    "language": "en",
    "safesearch": "moderate",
    "include_news": true
  }
}
```

#### API 密钥设置
```bash
export YOU_API_KEY="your-key"  # Get from https://api.you.com
```

### 📊 更新了提供商比较

|特色 |蛇 |塔维利 |埃克 |友网 |
|--------|:------:|:------:|:---:|:-------:|
|速度| ⚡⚡⚡ | ⚡⚡ | ⚡⚡ | ⚡⚡⚡ |
|新闻整合| ✓ | ✗ | ✗ | ✓ |
| RAG 优化 | ✗ | ✓ | ✗ | ✓✓ |
|整页内容 | ✗ | ✓ | ✓ | ✓ |

---

## [2.1.5] - 2026-01-27

### 📝 文档

- 添加了关于不在 OpenClaw 核心配置中使用 Tavily/Serper/Exa 的警告
- Core OpenClaw 仅支持 `brave` 作为内置提供程序
- 该技能的提供者必须通过环境变量和脚本使用，而不是“openclaw.json”

## [2.1.0] - 2026-01-23

### 🧠 智能多信号路由

通过复杂的查询分析彻底检修自动路由：

#### 意图分类
- **购物意图**：检测价格模式（“多少钱”、“成本”）、购买信号（“购买”、“订单”）、交易关键字以及产品+品牌组合
- **研究意图**：识别解释模式（“如何”、“为什么”）、分析信号（“优点和缺点”、“比较”）、学习关键字和复杂的多子句查询
- **发现意图**：识别相似模式（“相似”、“替代”）、公司发现信号、URL/域检测和学术模式

#### 语言模式检测
- “多少钱”/“价格”→ 购物 (Serper)
- “如何”/“为什么”/“解释”→ 研究（Tavily）
- “公司喜欢”/“类似”/“替代品”→ 发现 (Exa)
- 产品+品牌名称组合→购物（Serper）
- 查询中的 URL 和域 → 类似搜索 (Exa)

#### 查询分析功能
- **复杂性评分**：长、多子句查询被路由到研究提供商
- **URL检测**：自动检测URL/域触发Exa类似搜索
- **品牌认知度**：科技品牌（苹果、三星、索尼等）及产品条款 → 购物
- **近期信号**：“最新”、“2026”、“重大”增强新闻模式

#### 置信度评分
- **高 (70-100%)**：信号匹配强，路由非常可靠
- **中 (40-69%)**：匹配良好，应该效果很好
- **低 (0-39%)**：查询不明确，使用后备提供程序
- 基于绝对信号强度+相对于替代品的相对余量的信心

#### 增强的调试模式
```bash
python3 scripts/search.py --explain-routing -q "your query"
```

现在显示：
- 具有置信度的路由决策
- 所有提供者分数
- 具有权重的顶级匹配信号
- 查询分析（复杂性、URL 检测、新近度焦点）
- 每个提供商的所有匹配模式

### 🔧 技术变更

#### 查询分析器类
新的“QueryAnalyzer”类具有：
- `SHOPPING_SIGNALS`：超过 25 种购物意图加权模式
- `RESEARCH_SIGNALS`：30 多个用于研究意图的加权模式
- `DISCOVERY_SIGNALS`：20 多个用于发现意图的加权模式
- `LOCAL_NEWS_SIGNALS`：超过 25 种本地/新闻查询模式
- `BRAND_PATTERNS`：技术品牌检测正则表达式

#### 信号加权
- 多词短语获得更高的权重（例如，“how much”= 4.0 vs“price”= 3.0）
- 强信号：价格模式 (4.0)、相似性模式 (5.0)、URL (5.0)
- 媒介信号：产品术语（2.5）、学习关键词（2.5）
- 奖励评分：产品+品牌组合（+3.0）、复杂查询（+2.5）

#### 改进的输出格式
```json
{
  "routing": {
    "auto_routed": true,
    "provider": "serper",
    "confidence": 0.78,
    "confidence_level": "high",
    "reason": "high_confidence_match",
    "top_signals": [{"matched": "price", "weight": 3.0}],
    "scores": {"serper": 7.0, "tavily": 0.0, "exa": 0.0}
  }
}
```

### 📚 文档更新

- **SKILL.md**：使用信号表和置信度评分指南完全重写
- **README.md**：更新了智能路由示例和置信度
- **常见问题解答**：更新以解释多信号分析

### 🧪 测试结果

|查询 |供应商|信心|信号|
|--------|----------|------------|---------|
| “iPhone 16 多少钱”|蛇 | 68% | “多少钱”，品牌+产品|
| “量子纠缠是如何工作的”|塔维利 | 86% 高 | “如何”、“是什么”、“影响”|
| “类似于Notion的初创公司”|埃克 | 76% 高 | “类似于”、“A 系列”|
| “像 stripe.com 这样的公司” |埃克 | 100% 高 |检测到 URL，“公司喜欢” |
| “MacBook Pro M3 规格评测”|蛇 | 70% 高 |品牌+产品、“规格”、“评论”|
| “特斯拉” |蛇 | 0% 低 |无信号（后备）|
| “关于变形金刚的 arxiv 论文”|埃克 | 58% | “arxiv”|
| “2026 年最新人工智能新闻”|蛇 | 77% 高 | “最新”、“新闻”、“2026” |

---

## [2.0.0] - 2026-01-23

### 🎉 主要特点

#### 智能自动路由
- **基于查询分析自动选择提供商**
- 无需手动选择提供商 - 只需搜索即可！
- 用于路由决策的智能关键字匹配
- 查询类型的模式检测（购物、研究、发现）
- 供应商选择的评分系统

#### 用户配置
- **config.json**：完全控制自动路由行为
- **可配置的关键字映射**：添加您自己的路由关键字
- **提供商优先级**：设置决胜顺序
- **禁用提供商**：关闭您没有 API 密钥的提供商
- **启用/禁用自动路由**：根据需要选择加入或选择退出

#### 调试工具
- **--explain-routing** 标志：确切了解选择提供商的原因
- JSON 响应中的详细路由元数据
- 显示匹配的关键字和路由分数

### 📚 文档

- **README.md**：带有示例的完整自动路由指南
- **SKILL.md**：详细路由逻辑和配置参考
- **常见问题解答部分**：有关自动路由的常见问题
- **配置示例**：常见用例的预构建配置

---

## [1.0.x] - 初始版本

- 多提供商搜索：Serper、Tavily、Exa
- 使用“-p”标志手动选择提供商
- 统一JSON输出格式
- 特定于提供商的选项（--depth、--category、--similar-url 等）
- Tavilly/Exa 的域名过滤
- Exa 的日期过滤
