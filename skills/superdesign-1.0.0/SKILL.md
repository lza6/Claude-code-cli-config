---
name: frontend-design
description: "用于创建美观、现代 UI 的专家前端设计指南。在构建登陆页面、仪表板或任何用户界面时使用。"
metadata: {"clawdbot":{"emoji":"🎨"}}
---

# 前端设计技巧

在创建 UI 组件、登陆页面、仪表板或任何前端设计工作时使用此技能。

## 设计工作流程

遵循以下结构化方法进行 UI 设计：

1. **布局设计** — 思考组件结构，创建 ASCII 线框
2. **主题设计** — 定义颜色、字体、间距、阴影
3. **动画设计** - 规划微交互和过渡
4. **实现**——生成实际代码

### 1.布局设计

在编码之前，以 ASCII 格式绘制布局：

```
┌─────────────────────────────────────┐
│         HEADER / NAV BAR            │
├─────────────────────────────────────┤
│                                     │
│            HERO SECTION             │
│         (Title + CTA)               │
│                                     │
├─────────────────────────────────────┤
│   FEATURE   │  FEATURE  │  FEATURE  │
│     CARD    │   CARD    │   CARD    │
├─────────────────────────────────────┤
│            FOOTER                   │
└─────────────────────────────────────┘
```

### 2. 主题指南

**颜色规则：**
- 切勿使用通用引导程序风格的蓝色 (#007bff) — 它看起来已经过时了
- 对于现代颜色定义，更喜欢 oklch()
- 使用语义颜色变量（--primary、--secondary、--muted 等）
- 从一开始就考虑浅色和深色模式

**字体选择（谷歌字体）：**
```
Sans-serif: Inter, Roboto, Poppins, Montserrat, Outfit, Plus Jakarta Sans, DM Sans, Space Grotesk
Monospace: JetBrains Mono, Fira Code, Source Code Pro, IBM Plex Mono, Space Mono, Geist Mono
Serif: Merriweather, Playfair Display, Lora, Source Serif Pro, Libre Baskerville
Display: Architects Daughter, Oxanium
```

**间距和阴影：**
- 使用一致的间距刻度（0.25rem 基准）
- 阴影应该是微妙的——避免浓重的阴影
- 也考虑使用 oklch() 作为阴影颜色

### 3.主题模式

**现代深色模式（Vercel/Linear 风格）：**
```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.970 0 0);
  --muted: oklch(0.970 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --border: oklch(0.922 0 0);
  --radius: 0.625rem;
  --font-sans: Inter, system-ui, sans-serif;
}
```

**新粗野主义（90 年代网络复兴）：**
```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0 0 0);
  --primary: oklch(0.649 0.237 26.97);
  --secondary: oklch(0.968 0.211 109.77);
  --accent: oklch(0.564 0.241 260.82);
  --border: oklch(0 0 0);
  --radius: 0px;
  --shadow: 4px 4px 0px 0px hsl(0 0% 0%);
  --font-sans: DM Sans, sans-serif;
  --font-mono: Space Mono, monospace;
}
```

**玻璃态：**
```css
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
}
```

### 4. 动画指南

**规划的微观语法：**
```
button: 150ms [S1→0.95→1] press
hover: 200ms [Y0→-2, shadow↗]
fadeIn: 400ms ease-out [Y+20→0, α0→1]
slideIn: 350ms ease-out [X-100→0, α0→1]
bounce: 600ms [S0.95→1.05→1]
```

**常见模式：**
- 进入动画：300-500ms，缓出
- 悬停状态：150-200ms
- 按钮按下：100-150ms
- 页面转换：300-400ms

### 五、实施细则

**顺风CSS：**
```html
<!-- Import via CDN for prototypes -->
<script src="https://cdn.tailwindcss.com"></script>
```

**Flowbite（组件库）：**
```html
<link href="https://cdn.jsdelivr.net/npm/flowbite@2.0.0/dist/flowbite.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/flowbite@2.0.0/dist/flowbite.min.js"></script>
```

**图标（Lucide）：**
```html
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
<script>lucide.createIcons();</script>
```

**图片：**
- 使用真实的占位符服务：Unsplash、placehold.co
- 切勿编造图片网址
- 示例：`https://images.unsplash.com/photo-xxx?w=800&h=600`

### 6.响应式设计

始终设计移动优先且响应式：

```css
/* Mobile first */
.container { padding: 1rem; }

/* Tablet */
@media (min-width: 768px) {
  .container { padding: 2rem; }
}

/* Desktop */
@media (min-width: 1024px) {
  .container { max-width: 1200px; margin: 0 auto; }
}
```

### 7. 辅助功能

- 使用语义 HTML（标题、主要、导航、部分、文章）
- 包括正确的标题层次结构（h1 → h2 → h3）
- 为交互元素添加咏叹调标签
- 确保足够的色彩对比度（最低 4.5:1）
- 支持键盘导航

### 8. 组件设计技巧

**卡片：**
- 微妙的阴影，而不是沉重的阴影
- 一致的填充（p-4 到 p-6）
- 悬停状态：轻微抬起+阴影增加

**按钮：**
- 清晰的视觉层次（主要、次要、幽灵）
- 足够的触摸目标（最小 44x44 像素）
- 加载和禁用状态

**表格：**
- 清除输入上方的标签
- 可见焦点状态
- 内联验证反馈
- 字段之间有足够的间距

**导航：**
- 长页面的粘性标题
- 清晰的活动状态指示
- 适合移动设备的汉堡菜单

---

## 快速参考

|元素|推荐|
|--------|----------------|
|主要字体 | Inter, 服装, DM Sans |
|代码字体| JetBrains Mono、Fira 代码 |
|边界半径| 0.5rem - 1rem（现代），0（野兽派）|
|影子|微妙，最多 1-2 层 |
|间距| 4px 基本单位 (0.25rem) |
|动画| 150-400ms，缓出|
|颜色 | oklch() 对于现代，避免通用蓝色 |

---

*基于 SuperDesign 模式 — https://superdesign.dev*
