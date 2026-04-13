# 故障排除指南

## 缓存问题 (v2.7.0+)

### 缓存不工作/总是获取新鲜数据

**症状：**
- 每个请求都会到达API
- `"cached": false` 即使对于重复查询

**解决方案：**
1. 检查缓存目录是否存在且可写：
   ```bash
   ls -la .cache/  # Should exist in skill directory
   ```
2.验证`--no-cache`没有被传递
3.检查磁盘空间是否已满
4.确保查询完全相同（包括provider和max_results）

### 缓存中的过时结果

**症状：**
- 获取过时的信息
- 缓存 TTL 似乎太长

**解决方案：**
1. 使用 `--no-cache` 强制使用新结果
2.减少TTL：`--cache-ttl 1800`（30分钟）
3.清除缓存：`python3 script/search.py --clear-cache`

### 缓存变得太大

**症状：**
- 磁盘空间已满
- `.cache/` 中有许多 .json 文件

**解决方案：**
1.定期清除缓存：
   ```bash
   python3 scripts/search.py --clear-cache
   ```
2.设置一个cron作业每周清理一次
3. 使用较小的 TTL，以便条目过期得更快

### 缓存时“权限被拒绝”

**症状：**
- 在 stderr 中缓存写入错误
- 搜索有效但不缓存

**解决方案：**
1.检查目录权限：`chmod 755 .cache/`
2. 使用自定义缓存目录： `export WSP_CACHE_DIR="/tmp/wsp-cache"`

---

## 常见问题

### “未找到 API 密钥”错误

**症状：**
```
Error: No API key found for serper
```

**解决方案：**
1. 检查技能文件夹中是否存在“.env”，格式为“export VAR=value”
2. 自 v2.2.0 起，密钥从技能的`.env`自动加载
3.或者在系统环境中设置：`export SERPER_API_KEY="..."`
4. 验证 config.json 中的密钥格式：
   ```json
   { "serper": { "api_key": "your-key" } }
   ```

**优先顺序：** config.json > .env > 环境变量

---

### 得到空结果

**症状：**
- 搜索没有返回结果
- JSON 输出中的 `"results": []`

**解决方案：**
1. 检查 API 密钥是否有效（尝试提供商的 Web 仪表板）
2. 使用“-p”尝试不同的提供程序
3.有些查询没有结果（非常小众的话题）
4. 检查提供商是否有速率限制
5. 验证互联网连接

**调试：**
```bash
python3 scripts/search.py -q "test query" --verbose
```

---

### 速率有限

**症状：**
```
Error: 429 Too Many Requests
Error: Rate limit exceeded
```

**好消息：** 自 v2.2.5 起，自动回退开始生效！如果一个提供商达到速率限制，脚本会自动尝试下一个提供商。

**解决方案：**
1. 等待速率限制重置（通常为 1 小时或一天结束时）
2. 使用不同的提供程序：“-p tavilly”而不是“-p serper”
3. 检查免费套餐限制：
   - Serper：总共 2,500 个免费
   - Tavily：1,000/月免费
   - 例如：1,000/月免费
4. 升级到付费级别以获得更高的限额
5.使用SearXNG（自托管，无限制）

**回退信息：** 当使用回退时，响应将包括 `routing.fallback_used: true`。

---

### SearXNG：“403 禁止”

**症状：**
```
Error: 403 Forbidden
Error: JSON format not allowed
```

**原因：** 大多数公共 SearXNG 实例禁用 JSON API 以防止机器人滥用。

**解决方案：** 自托管您自己的实例：
```bash
docker run -d -p 8080:8080 searxng/searxng
```

然后在“settings.yml”中启用 JSON：
```yaml
search:
  formats:
    - html
    - json  # Add this!
```

重新启动容器并更新您的配置：
```json
{
  "searxng": {
    "instance_url": "http://localhost:8080"
  }
}
```

---

### SearXNG：响应慢

**症状：**
- SearXNG 需要 2-5 秒
- 其他提供商速度更快

**说明：** 这是预期行为。 SearXNG 并行查询 70 多个上游引擎，这比直接 API 调用需要更长的时间。

**权衡：** 较慢但保护隐私 + 多源 + 0 美元成本。

**解决方案：**
1. 接受隐私利益的权衡
2. 限制引擎以获得更快的结果：
   ```bash
   python3 scripts/search.py -p searxng -q "query" --engines "google,bing"
   ```
3.使用SearXNG作为后备（放在优先级列表的最后）

---

### 自动路由选择了错误的提供商

**症状：**
- 有关研究的询问请联系 Serper
- 有关购物的查询请前往 Tavily

**调试：**
```bash
python3 scripts/search.py --explain-routing -q "your query"
```

这显示了完整的分析：
```json
{
  "query": "how much does iPhone 16 Pro cost",
  "routing_decision": {
    "provider": "serper",
    "confidence": 0.68,
    "reason": "moderate_confidence_match"
  },
  "scores": {"serper": 7.0, "tavily": 0.0, "exa": 0.0},
  "top_signals": [
    {"matched": "how much", "weight": 4.0},
    {"matched": "brand + product detected", "weight": 3.0}
  ]
}
```

**解决方案：**
1. 使用显式提供程序覆盖：`-p tavilly`
2. 重新表述查询以更明确地表达意图
3.调整config.json中的`confidence_threshold`（默认：0.3）

---

### 配置未加载

**症状：**
- 未应用对 config.json 的更改
- 使用默认值代替

**解决方案：**
1.检查JSON语法（使用验证器）
2. 确保文件位于技能目录中：`/path/to/skills/web-search-plus/config.json`
3.检查文件权限
4. 运行安装向导重新生成：
   ```bash
   python3 scripts/setup.py --reset
   ```

**验证 JSON：**
```bash
python3 -m json.tool config.json
```

---

### 缺少 Python 依赖项

**症状：**
```
ModuleNotFoundError: No module named 'requests'
```

**解决方案：**
```bash
pip3 install requests
```

或者安装所有依赖项：
```bash
pip3 install -r requirements.txt
```

---

### 超时错误

**症状：**
```
Error: Request timeout after 30s
```

**原因：**
- 网络连接速度慢
- 提供商 API 问题
- SearXNG实例重载

**解决方案：**
1.重试（临时问题）
2.切换提供者：`-p serper`
3. 检查您的互联网连接
4. 如果使用 SearXNG，请检查实例运行状况

---

### 重复结果

**症状：**
- 相同的结果出现多次
- 提供商之间的结果重叠

**解决方案：** 当使用自动回退或多个提供程序时，这是预期的。该技能不会在提供商之间进行重复数据删除。

对于单一提供商结果：
```bash
python3 scripts/search.py -p serper -q "query"
```

---

## 调试模式

详细调试：

```bash
# Verbose output
python3 scripts/search.py -q "query" --verbose

# Show routing decision
python3 scripts/search.py -q "query" --explain-routing

# Dry run (no actual search)
python3 scripts/search.py -q "query" --dry-run

# Test specific provider
python3 scripts/search.py -p tavily -q "query" --verbose
```

---

## 获取帮助

**仍然卡住吗？**

1.查看`README.md`中的完整文档
2. 运行安装向导：`python3 scripts/setup.py`
3. 查看“FAQ.md”以了解常见问题
4.打开问题：https://github.com/robbyczgw-cla/web-search-plus/issues
