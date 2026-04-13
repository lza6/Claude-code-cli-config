# 常见问题

## 缓存（v2.7.0 中的新功能！）

### 缓存是如何工作的？
搜索结果会自动在本地缓存 1 小时（3600 秒）。当您再次进行相同的查询时，您可以以 0 美元的 API 成本获得即时结果。缓存键基于：查询文本+提供程序+ max_results。

### 缓存结果存储在哪里？
默认位于技能文件夹内的`.cache/`目录中。使用“WSP_CACHE_DIR”环境变量覆盖：
```bash
export WSP_CACHE_DIR="/path/to/custom/cache"
```

### 如何查看缓存统计信息？
```bash
python3 scripts/search.py --cache-stats
```
这显示了总条目数、大小、最旧/最新条目以及按提供商细分。

### 如何清除缓存？
```bash
python3 scripts/search.py --clear-cache
```

### 我可以更改缓存 TTL 吗？
是的！默认值为 3600 秒（1 小时）。设置每个请求的自定义 TTL：
```bash
python3 scripts/search.py -q "query" --cache-ttl 7200  # 2 hours
```

### 如何跳过缓存？
使用“--no-cache”始终获取新结果：
```bash
python3 scripts/search.py -q "query" --no-cache
```

### 我如何知道结果是否已缓存？
响应内容包括：
- `"cached": true/false` — 结果是否来自缓存
- `"cache_age_seconds": 1234` — 缓存结果的年龄（缓存时）

---

＃＃ 一般的

### 自动路由如何决定使用哪个提供商？
多信号分析根据以下因素对每个提供商进行评分：价格模式、解释短语、相似性关键字、URL、产品+品牌组合和查询复杂性。得分最高者获胜。使用“--explain-routing”查看决策细目。

### 如果选择了错误的提供商怎么办？
用 `-p serper/tavily/exa` 覆盖。检查“--explain-routing”以了解为什么它选择不同。

### “低信心”是什么意思？
查询不明确（例如，“Tesla”可以是汽车、股票或公司）。落回毒蛇身边。结果可能会有所不同。

### 我可以禁用提供商吗？
是的！在 config.json 中： `"disabled_providers": ["exa"]`

---

## API 密钥

### 我需要哪些 API 密钥？
至少一个密钥（或 SearXNG 实例）。您可以仅使用 Serper、Tavily、Exa、You.com 或 SearXNG。缺少密钥=该提供者被跳过。

### 我在哪里可以获得 API 密钥？
- Serper：https://serper.dev（2,500 个免费查询，无需信用卡）
- Tavily：https://tavily.com（每月 1,000 次免费搜索）
- Exa：https://exa.ai（每月 1,000 次免费搜索）
- You.com：https://api.you.com（有限免费测试层）
- SearXNG：自托管，无需密钥！ https://docs.searxng.org/admin/installation.html

### 如何设置 API 密钥？
两个选项（均自动加载）：

**选项 A：.env 文件**
```bash
export SERPER_API_KEY="your-key"
```

**选项 B：config.json** (v2.2.1+)
```json
{ "serper": { "api_key": "your-key" } }
```

---

## 路由详细信息

### 我如何知道哪个提供商处理了我的搜索？
检查 JSON 输出中的“routing.provider”，或聊天响应中的“[🔍 搜索方式：Provider]”。

### 为什么有时会选择 Serper 来解决研究问题？
如果查询包含品牌/产品信号（例如“Tesla FSD 如何工作”），则购物意图可能会超过研究意图。用“-p tavilly”覆盖。

### 置信阈值是多少？
默认值：0.3 (30%)。低于此 = 低置信度，使用后备。可在 config.json 中调整。

---

## You.com 特定

### 我什么时候应该使用 You.com 而不是其他提供商？
You.com 擅长：
- **RAG 应用程序**：预提取的片段可供 LLM 使用
- **实时信息**：时事、突发新闻、状态更新
- **组合来源**：Web + 新闻导致单个 API 调用
- **总结任务**：“……的最新情况”、“……的要点”

### 实时抓取功能是什么？
You.com 可以按需获取整页内容。对网络结果使用“--livecrawl web”，对新闻文章使用“--livecrawl news”，对两者都使用“--livecrawl all”。内容以 Markdown 格式返回。

### You.com 是否自动包含新闻？
是的！当您的查询具有新闻意图时，You.com 的智能分类会自动包含相关新闻结果。您还可以使用“--include-news”显式启用它。

---

## SearXNG 特定

### 我需要自己的 SearXNG 实例吗？
是的！ SearXNG 是自托管的。大多数公共实例禁用 JSON API 以防止机器人滥用。您需要运行自己的实例并启用 JSON 格式。请参阅：https://docs.searxng.org/admin/installation.html

### 如何设置 SearXNG？
Docker 是最简单的方法：
```bash
docker run -d -p 8080:8080 searxng/searxng
```
然后在“settings.yml”中启用 JSON：
```yaml
search:
  formats:
    - html
    - json
```

### 为什么我收到“403 Forbidden”？
您的实例上禁用了 JSON API。在“search.formats”下的“settings.yml”中启用它。

### SearXNG 的 API 成本是多少？
**0 美元！** SearXNG 是免费且开源的。您只需支付托管费用（约 5 美元/月 VPS）。无限查询。

### 我什么时候应该使用 SearXNG？
- **隐私敏感查询**：无跟踪，无分析
- **注重预算**：API 成本为 0 美元
- **多样化结果**：聚合 70 多个搜索引擎
- **自托管要求**：完全控制您的搜索基础设施
- **后备提供商**：当付费 API 受到速率限制时

### 我可以限制 SearXNG 使用哪些搜索引擎吗？
是的！使用“--engines google,bing,duckduckgo”指定引擎，或在“config.json”中配置默认​​值。

---

## 提供商选择

### 我应该使用哪个提供商？

|查询类型 |最佳供应商|为什么 |
|------------|-------------|-----|
| **购物**（“购买笔记本电脑”、“便宜的鞋子”）| **蛇** | Google 购物、价格比较、本地商店 |
| **研究**（“X 是如何工作的？”、“解释 Y”）| **塔维利** |研究深入，学术品质，整版内容|
| **初创公司/论文**（“像 X 这样的公司”、“arxiv 论文”）| **埃** |语义/神经搜索，启动发现 |
| **RAG/实时**（“总结最新”、“当前事件”）| **You.com** |法学硕士准备片段，结合网络+新闻 |
| **隐私**（“搜索而不跟踪”）| **SearXNG** |无跟踪、多源、自托管 |

**提示：**启用自动路由，让技能自动选择！ 🎯

### 我需要全部 5 个提供商吗？
**不！** 所有提供商都是可选的。您可以使用：
- **1 个提供商**（例如，一切都只有 Serper）
- **2-3 个提供商**（例如，Serper + You.com 可以满足大多数需求）
- **全部 5**（最大灵活性 + 后备选项）

### API 的费用是多少？

|供应商|免费套餐 |付费计划 |
|----------|------------|------------|
| **蛇** |每月 2,500 次查询 | $50/月（5,000 个查询）|
| **塔维利** |每月 1,000 次查询 | $150/月（10,000 次查询）|
| **埃** |每月 1,000 次查询 | $1,000/月（100,000 次查询）|
| **You.com** |有限免费 | ~$10/月（根据使用情况而变化）|
| **SearXNG** | **免费** ✅ |仅 VPS 成本（如果自托管，则约为 5 美元/月）|

**预算提示：** 使用 SearXNG 作为主要查询 + 其他作为专门查询的后备！

### SearXNG 到底有多私密？

|设置 |隐私级别 |
|--------|----------------|
| **自托管（您的 VPS）** | ⭐⭐⭐⭐⭐ 一切由你掌控 |
| **自托管（Docker 本地）** | ⭐⭐⭐⭐⭐ 完全私密 |
| **公共实例** | ⭐⭐⭐ 取决于运营商的日志政策 |

**最佳实践：** 如果隐私至关重要，请自行托管。

### 哪个提供商的结果最好？

|公制|获胜者 |
|--------|--------|
| **最准确的事实** | Serper（谷歌）|
| **最适合研究深度** |塔维利 |
| **最适合语义查询** |埃克 |
| **最适合 RAG/AI 环境** |友网 |
| **最多样化的来源** | SearXNG（70+ 引擎）|
| **最私密** | SearXNG（自托管）|

**建议：** 启用多个提供商+自动路由以获得最佳整体体验。

### 自动路由是如何工作的？
该技能分析您的关键字和模式查询：

```python
"buy cheap laptop"     → Serper (shopping signals)
"how does AI work?"    → Tavily (research/explanation)
"companies like X"     → Exa (semantic/similar)
"summarize latest news" → You.com (RAG/real-time)
"search privately"     → SearXNG (privacy signals)
```

**置信阈值：** 仅当置信度 > 30% 时才路由。否则使用默认提供程序。

**覆盖：** 使用 `-pprovider` 强制使用特定的提供程序。

---

## 生产使用

### 我可以在生产中使用它吗？
**是的！** Web-search-plus 已做好生产准备：
- ✅ 错误处理与自动回退
- ✅ 速率限制保护
- ✅ 超时处理（每个提供商 30 秒）
- ✅ API 密钥安全（.env + config.json gitignored）
- ✅ 5 个冗余提供商

**提示：** 监控 API 使用情况以避免超出免费套餐！

### 如果我用完 API 积分怎么办？
1. **后备链：** 其他启用的提供商自动接管
2. **使用SearXNG：**切换到自托管（无限查询）
3. **升级计划：** 付费等级有更高的限制
4. **速率限制：** 使用 `disabled_providers` 暂时跳过耗尽的 API

---

## 更新

### 如何更新到最新版本？

**通过 ClawHub（推荐）：**
```bash
clawhub update web-search-plus --registry "https://www.clawhub.ai" --no-input
```

**手动：**
```bash
cd /path/to/workspace/skills/web-search-plus/
git pull origin main
python3 scripts/setup.py  # Re-run to configure new features
```

### 我可以在哪里报告错误或请求功能？
- **GitHub 问题：** https://github.com/robbyczgw-cla/web-search-plus/issues
- **ClawHub：** https://www.clawhub.ai/skills/web-search-plus
