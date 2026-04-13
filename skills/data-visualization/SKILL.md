---
name: data-visualization
description: "数据可视化专家，涵盖图表选择、色彩理论和标注最佳实践。支持图表类型（柱状图、折线图、散点图、热力图）、坐标轴规则和数据叙事。用于：图表、图形、仪表板、报告、演示文稿、信息图、数据故事。触发词：data visualization, chart, graph, data chart, bar chart, line chart, scatter plot, data viz, visualization, dashboard chart, infographic data, data presentation, chart design, plot, heatmap, pie chart alternative"
allowed-tools: "重击（infsh *）"
---

# 数据可视化

通过 [inference.sh](https://inference.sh) CLI 创建清晰、有效的数据可视化。

## 快速入门

> 需要 inference.sh CLI (`infsh`)。 [安装说明](https://raw.githubusercontent.com/inference-sh/skills/refs/heads/main/cli-install.md)

```bash
infsh login

# Generate a chart with Python
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nmonths = [\"Jan\", \"Feb\", \"Mar\", \"Apr\", \"May\", \"Jun\"]\nrevenue = [42, 48, 55, 61, 72, 89]\n\nfig, ax = plt.subplots(figsize=(10, 6))\nax.bar(months, revenue, color=\"#3b82f6\", width=0.6)\nax.set_ylabel(\"Revenue ($K)\")\nax.set_title(\"Monthly Revenue Growth\", fontweight=\"bold\")\nfor i, v in enumerate(revenue):\n    ax.text(i, v + 1, f\"${v}K\", ha=\"center\", fontweight=\"bold\")\nplt.tight_layout()\nplt.savefig(\"revenue.png\", dpi=150)\nprint(\"Saved\")"
}'
```


## 图表选择指南

### 哪个图表代表哪个数据？

|数据关系|最佳图表|切勿使用 |
|------------------|----------|------------|
| **随时间变化** |折线图|饼图|
| **比较类别** |条形图（许多类别的水平）|折线图|
| **整体的一部分** |堆叠条形图、树状图 |饼图（有争议，但：条形图总是更清晰）|
| **分布** |直方图、箱线图 |条形图|
| **相关性** |散点图 |条形图|
| **排名** |水平条形图|竖条、饼图 |
| **地理** |等值线地图 |条形图|
| **随着时间的推移组成** |堆积面积图 |多个饼图|
| **单一指标** |大数字（KPI卡）|任何图表（大材小用）|
| **流程/过程** |桑基图|条形图|

### 饼图问题

饼图几乎总是错误的选择：

```
❌ Pie chart problems:
   - Hard to compare similar-sized slices
   - Can't show more than 5-6 categories
   - 3D pie charts are always wrong
   - Impossible to read exact values

✅ Use instead:
   - Horizontal bar chart (easy comparison)
   - Stacked bar (part of whole)
   - Treemap (hierarchical parts)
   - Just a table (if precision matters)
```

## 设计规则

### 轴

|规则|为什么 |
|------|-----|
| Y 轴始终从 0 开始（条形图）|防止视觉误导 |
|折线图可以从 0 以上开始 |当显示变化时，而不是绝对值 |
|标记两个轴 |读者不必猜测单位 |
|删除不必要的网格线 |减少视觉噪音 |
|使用水平标签|竖排文字难以阅读 |
|按值对条形图排序 |除非有原因，否则不要使用字母顺序 |

＃＃＃ 颜色

|原理|应用 |
|------------|------------|
| **每张图表最多 5-7 种颜色** |更多内容变得难以阅读 |
| **强调一件事** |灰色的一切，颜色的焦点|
| **顺序**大小 |浅→暗为低→高|
| **正/负的分歧** |红色←中性→蓝色|
| **针对团体的分类** |不同的色调，相似的亮度|
| **色盲安全** |避免仅使用红色/绿色 - 添加形状或标签 |
| **含义一致** |如果蓝色=收入，那么到处都保持蓝色|

### 好的调色板

```python
# Sequential (low to high)
sequential = ["#eff6ff", "#bfdbfe", "#60a5fa", "#2563eb", "#1d4ed8"]

# Diverging (negative to positive)
diverging = ["#ef4444", "#f87171", "#d1d5db", "#34d399", "#10b981"]

# Categorical (distinct groups)
categorical = ["#3b82f6", "#f59e0b", "#10b981", "#8b5cf6", "#ef4444"]

# Colorblind-safe
cb_safe = ["#0077BB", "#33BBEE", "#009988", "#EE7733", "#CC3311"]
```

### 文本和标签

|元素|规则|
|---------|------|
| **标题** |陈述洞察力，而不是数据类型。 “第二季度收入翻倍”而不是“第二季度收入图表”|
| **注释** |直接在图表上标注出关键数据点 |
| **传奇** |尽可能避免 - 直接在图表线/条上标记 |
| **字体大小** |演示文稿最小 12 像素、14 像素以上 |
| **数字格式** |对于大数使用 K、M、B（42K 而不是 42,000）|
| **数据标签** |当精确值很重要时添加到条形/点 |

## 图表食谱

### 折线图（时间序列）

```bash
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(12, 6))\nfig.patch.set_facecolor(\"white\")\n\nmonths = [\"Jan\", \"Feb\", \"Mar\", \"Apr\", \"May\", \"Jun\", \"Jul\", \"Aug\", \"Sep\", \"Oct\", \"Nov\", \"Dec\"]\nthis_year = [120, 135, 148, 162, 178, 195, 210, 228, 245, 268, 290, 320]\nlast_year = [95, 102, 108, 115, 122, 130, 138, 145, 155, 165, 178, 190]\n\nax.plot(months, this_year, color=\"#3b82f6\", linewidth=2.5, marker=\"o\", markersize=6, label=\"2024\")\nax.plot(months, last_year, color=\"#94a3b8\", linewidth=2, linestyle=\"--\", label=\"2023\")\nax.fill_between(range(len(months)), last_year, this_year, alpha=0.1, color=\"#3b82f6\")\n\nax.annotate(\"$320K\", xy=(11, 320), fontsize=14, fontweight=\"bold\", color=\"#3b82f6\")\nax.annotate(\"$190K\", xy=(11, 190), fontsize=12, color=\"#94a3b8\")\n\nax.set_ylabel(\"Revenue ($K)\", fontsize=12)\nax.set_title(\"Revenue grew 68% year-over-year\", fontsize=16, fontweight=\"bold\")\nax.legend(fontsize=12)\nax.spines[\"top\"].set_visible(False)\nax.spines[\"right\"].set_visible(False)\nax.grid(axis=\"y\", alpha=0.3)\nplt.tight_layout()\nplt.savefig(\"line-chart.png\", dpi=150)\nprint(\"Saved\")"
}'
```

### 水平条形图（比较）

```bash
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(10, 6))\n\ncategories = [\"Email\", \"Social\", \"SEO\", \"Paid Ads\", \"Referral\", \"Direct\"]\nvalues = [12, 18, 35, 22, 8, 5]\ncolors = [\"#94a3b8\"] * len(values)\ncolors[2] = \"#3b82f6\"  # Highlight the winner\n\n# Sort by value\nsorted_pairs = sorted(zip(values, categories, colors))\nvalues, categories, colors = zip(*sorted_pairs)\n\nax.barh(categories, values, color=colors, height=0.6)\nfor i, v in enumerate(values):\n    ax.text(v + 0.5, i, f\"{v}%\", va=\"center\", fontsize=12, fontweight=\"bold\")\n\nax.set_xlabel(\"% of Total Traffic\", fontsize=12)\nax.set_title(\"SEO drives the most traffic\", fontsize=16, fontweight=\"bold\")\nax.spines[\"top\"].set_visible(False)\nax.spines[\"right\"].set_visible(False)\nplt.tight_layout()\nplt.savefig(\"bar-chart.png\", dpi=150)\nprint(\"Saved\")"
}'
```

### KPI / 大数字卡

```bash
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"display:flex;gap:20px;padding:20px;background:white;font-family:system-ui\"><div style=\"background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:24px;width:200px;text-align:center\"><p style=\"color:#64748b;font-size:14px;margin:0\">Monthly Revenue</p><p style=\"font-size:48px;font-weight:900;margin:8px 0;color:#1e293b\">$89K</p><p style=\"color:#22c55e;font-size:14px;margin:0\">↑ 23% vs last month</p></div><div style=\"background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:24px;width:200px;text-align:center\"><p style=\"color:#64748b;font-size:14px;margin:0\">Active Users</p><p style=\"font-size:48px;font-weight:900;margin:8px 0;color:#1e293b\">12.4K</p><p style=\"color:#22c55e;font-size:14px;margin:0\">↑ 8% vs last month</p></div><div style=\"background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:24px;width:200px;text-align:center\"><p style=\"color:#64748b;font-size:14px;margin:0\">Churn Rate</p><p style=\"font-size:48px;font-weight:900;margin:8px 0;color:#1e293b\">2.1%</p><p style=\"color:#ef4444;font-size:14px;margin:0\">↑ 0.3% vs last month</p></div></div>"
}'
```

### 热图

```bash
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport numpy as np\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(10, 6))\n\ndays = [\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\", \"Sat\", \"Sun\"]\nhours = [\"9AM\", \"10AM\", \"11AM\", \"12PM\", \"1PM\", \"2PM\", \"3PM\", \"4PM\", \"5PM\"]\ndata = np.random.randint(10, 100, size=(len(hours), len(days)))\ndata[2][1] = 95  # Tuesday 11AM peak\ndata[2][3] = 88  # Thursday 11AM\n\nim = ax.imshow(data, cmap=\"Blues\", aspect=\"auto\")\nax.set_xticks(range(len(days)))\nax.set_yticks(range(len(hours)))\nax.set_xticklabels(days, fontsize=12)\nax.set_yticklabels(hours, fontsize=12)\n\nfor i in range(len(hours)):\n    for j in range(len(days)):\n        color = \"white\" if data[i][j] > 60 else \"black\"\n        ax.text(j, i, data[i][j], ha=\"center\", va=\"center\", fontsize=10, color=color)\n\nax.set_title(\"Website Traffic by Day & Hour\", fontsize=16, fontweight=\"bold\")\nplt.colorbar(im, label=\"Visitors\")\nplt.tight_layout()\nplt.savefig(\"heatmap.png\", dpi=150)\nprint(\"Saved\")"
}'
```

## 用数据讲故事

### 叙事弧线

|步骤|做什么 |示例|
|------|------------|---------|
| 1. **背景** |设置读者需要了解的内容 | “我们每月跟踪客户获取成本”|
| 2. **紧张** |显示问题或更改 | “第三季度 CAC 增长 40%” |
| 3. **决议** |展示见解或解决方案 | “但 LTV 增加了 80%，因此单位经济效益有所改善”|

### 标题为洞察力

```
❌ Descriptive titles (what the chart shows):
   "Q3 Revenue by Product Line"
   "Monthly Active Users 2024"
   "Customer Satisfaction Survey Results"

✅ Insight titles (what the chart means):
   "Enterprise product drives 70% of revenue growth"
   "User growth accelerated after the free tier launch"
   "Support response time is the #1 satisfaction driver"
```

### 注释技术

|技术|何时使用 |
|------------|------------|
| **标注标签** |突出显示特定数据点（“峰值：320K”）|
| **参考线** |显示目标/基准（“目标：100K”）|
| **阴影区域** |标记时间段（“产品发布窗口”）|
| **箭头+文字** |引起人们对趋势变化的关注 |
| **行前/行后** |显示事件的影响 |

## 深色模式图表

```bash
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\n# Dark theme\nplt.rcParams.update({\n    \"figure.facecolor\": \"#0f172a\",\n    \"axes.facecolor\": \"#0f172a\",\n    \"axes.edgecolor\": \"#334155\",\n    \"axes.labelcolor\": \"white\",\n    \"text.color\": \"white\",\n    \"xtick.color\": \"white\",\n    \"ytick.color\": \"white\",\n    \"grid.color\": \"#1e293b\"\n})\n\nfig, ax = plt.subplots(figsize=(12, 6))\nmonths = [\"Jan\", \"Feb\", \"Mar\", \"Apr\", \"May\", \"Jun\"]\nvalues = [45, 52, 58, 72, 85, 98]\n\nax.plot(months, values, color=\"#818cf8\", linewidth=3, marker=\"o\", markersize=8)\nax.fill_between(range(len(months)), values, alpha=0.15, color=\"#818cf8\")\nax.set_title(\"MRR Growth: On track for $100K\", fontsize=18, fontweight=\"bold\")\nax.set_ylabel(\"MRR ($K)\", fontsize=13)\nax.spines[\"top\"].set_visible(False)\nax.spines[\"right\"].set_visible(False)\nax.grid(axis=\"y\", alpha=0.2)\n\nfor i, v in enumerate(values):\n    ax.annotate(f\"${v}K\", (i, v), textcoords=\"offset points\", xytext=(0, 12), ha=\"center\", fontsize=11, fontweight=\"bold\")\n\nplt.tight_layout()\nplt.savefig(\"dark-chart.png\", dpi=150, facecolor=\"#0f172a\")\nprint(\"Saved\")"
}'
```

## 常见错误

|错误|问题 |修复|
|---------|---------|-----|
|饼图|难以比较，总是具有误导性 |使用条形图或树状图 |
| Y 轴不从 0 开始（条形图）|夸大差异|条形从 0 开始，可以截断线条 |
|颜色太多| Visual noise, confusing |最多 5-7 种颜色，仅突出显示重要的内容 |
|无标题或通用标题 |读者不知其真知 |标题 = 要点，而不是数据类型 |
| 3D 图表 |扭曲数据，看起来不专业 |始终使用 2D |
|双 Y 轴 |具有误导性，难以阅读 |使用两个单独的图表 |
|条形图上按字母顺序排序 |隐藏故事|按值排序（最大的在前）|
|轴上没有标签 |读者无法解读|始终标有单位 |
| Chartjunk（装饰元素）|分散数据注意力删除所有不传达信息的内容 |
|红色/绿色仅用于颜色编码 |色盲用户无法阅读 |使用形状、图案或色盲安全调色板 |

## 相关技能

```bash
npx skills add inference-sh/skills@pitch-deck-visuals
npx skills add inference-sh/skills@technical-blog-writing
npx skills add inference-sh/skills@competitor-teardown
```

浏览所有应用程序：`infsh 应用程序列表`

