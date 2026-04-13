---
name: senior-frontend
description: "React、Next.js、TypeScript 和 Tailwind CSS 应用程序的前端开发技能。在构建 React 组件、优化 Next.js 性能、分析包大小、搭建前端项目、实现可访问性或检查前端代码质量时使用。"
risk: "安全的"
source: "PH47"
date_added: "2026-03-07"
---

# 高级前端

React/Next.js 应用程序的前端开发模式、性能优化和自动化工具。

## 何时使用
- 使用 TypeScript 和 Tailwind CSS 搭建新的 React 或 Next.js 项目时使用。
- 在生成新组件或自定义 Hook 时使用。
- 在分析和优化前端应用程序的包大小时使用。
- 用于实现或审查高级 React 模式，例如复合组件或渲染属性。
- 用于确保可访问性合规性并实施稳健的测试策略。

## 目录

- [项目脚手架](#项目脚手架)
- [组件生成](#组件生成)
- [包分析](#包分析)
- [React 模式](#react-模式)
- [Next.js 优化](#nextjs-优化)
- [可访问性和测试](#可访问性和测试)

---

## 项目脚手架

使用 TypeScript、Tailwind CSS 和最佳实践配置生成新的 Next.js 或 React 项目。

### 工作流：创建新的前端项目

1. 使用你的项目名称和模板运行脚手架：

```bash
   python scripts/frontend_scaffolder.py my-app --template nextjs
```

2. 添加可选功能（auth、api、forms、testing、storybook）：

```bash
   python scripts/frontend_scaffolder.py dashboard --template nextjs --features auth,api
```

3. 导航到项目并安装依赖：

```bash
   cd my-app && npm install
```

4. 启动开发服务器：

```bash
   npm run dev
```

### 脚手架选项

| 选项 | 描述 |
| -------------------- | ------------------------------------------------- |
| `--template nextjs` | Next.js 14+ 带 App Router 和 Server Components |
| `--template react` | React + Vite 带 TypeScript |
| `--features auth` | 添加 NextAuth.js 认证 |
| `--features api` | 添加 React Query + API 客户端 |
| `--features forms` | 添加 React Hook Form + Zod 验证 |
| `--features testing` | 添加 Vitest + Testing Library |
| `--dry-run` | 预览文件而不创建它们 |

### 生成的结构（Next.js）

```
my-app/
├── app/
│   ├── layout.tsx        # 根布局，包含字体
│   ├── page.tsx          # 首页
│   ├── globals.css       # Tailwind + CSS 变量
│   └── api/health/route.ts
├── components/
│   ├── ui/               # Button, Input, Card
│   └── layout/           # Header, Footer, Sidebar
├── hooks/                # useDebounce, useLocalStorage
├── lib/                  # utils (cn), constants
├── types/                # TypeScript 接口
├── tailwind.config.ts
├── next.config.js
└── package.json
```

---

## 组件生成

使用 TypeScript、测试和 Storybook 故事生成 React 组件。

### 工作流：创建新组件

1. 生成客户端组件：

```bash
   python scripts/component_generator.py Button --dir src/components/ui
```

2. 生成服务器组件：

```bash
   python scripts/component_generator.py ProductCard --type server
```

3. 生成测试和故事文件：

```bash
   python scripts/component_generator.py UserProfile --with-test --with-story
```

4. 生成自定义 Hook：

```bash
   python scripts/component_generator.py FormValidation --type hook
```

### 生成器选项

| 选项 | 描述 |
| ---------------- | -------------------------------------------------------- |
| `--type client` | 带 'use client' 的客户端组件（默认） |
| `--type server` | 异步服务器组件 |
| `--type hook` | 自定义 React Hook |
| `--with-test` | 包含测试文件 |
| `--with-story` | 包含 Storybook 故事 |
| `--flat` | 在输出目录中创建，不包含子目录 |
| `--dry-run` | 预览而不创建文件 |

### 生成的组件示例

```tsx
"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";

interface ButtonProps {
  className?: string;
  children?: React.ReactNode;
}

export function Button({ className, children }: ButtonProps) {
  return <div className={cn("", className)}>{children}</div>;
}
```

---

## 包分析

分析 package.json 和项目结构以获得包优化机会。

### 工作流：优化包大小

1. 在你的项目上运行分析器：

```bash
   python scripts/bundle_analyzer.py /path/to/project
```

2. 查看健康评分和问题：

```
   Bundle Health Score: 75/100 (C)

   HEAVY DEPENDENCIES:
     moment (290KB)
       Alternative: date-fns (12KB) or dayjs (2KB)

     lodash (71KB)
       Alternative: lodash-es with tree-shaking
```

3. 通过替换重量级依赖来应用建议的修复。

4. 以详细模式重新运行以检查导入模式：

```bash
   python scripts/bundle_analyzer.py . --verbose
```

### 包评分解读

| 分数 | 等级 | 行动 |
| ------ | -----| ------------------------------------------ |
| 90-100 | A | 包经过充分优化 |
| 80-89 | B | 可用的小优化 |
| 70-79 | C | 替换重量级依赖 |
| 60-69 | D | 多重问题需关注 |
| 0-59 | F | 关键的包大小问题

### 检测到的重量级依赖

分析器可识别这些常见的重量级包：

| 包 | 大小 | 替代方案 |
| ------------- | -----| ------------------------------------------ |
| moment | 290KB | date-fns (12KB) 或 dayjs (2KB) |
| lodash | 71KB | lodash-es 配合 tree-shaking |
| axios | 14KB | 原生 fetch 或 ky (3KB) |
| jQuery | 87KB | 原生 DOM API |
| @mui/material | 大 | shadcn/ui 或 Radix UI |

---

## React 模式

参考：`references/react_patterns.md`

### 复合组件

在相关组件之间共享状态：

```tsx
const Tabs = ({ children }) => {
  const [active, setActive] = useState(0);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      {children}
    </TabsContext.Provider>
  );
};

Tabs.List = TabList;
Tabs.Panel = TabPanel;

// 用法
<Tabs>
  <Tabs.List>
    <Tabs.Tab>One</Tabs.Tab>
    <Tabs.Tab>Two</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel>Content 1</Tabs.Panel>
  <Tabs.Panel>Content 2</Tabs.Panel>
</Tabs>;
```

### 自定义 Hook

提取可复用逻辑：

```tsx
function useDebounce<T>(value: T, delay = 500): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// 用法
const debouncedSearch = useDebounce(searchTerm, 300);
```

### 渲染属性

共享渲染逻辑：

```tsx
function DataFetcher({ url, render }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(url)
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, [url]);

  return render({ data, loading });
}

// 用法
<DataFetcher
  url="/api/users"
  render={({ data, loading }) =>
    loading ? <Spinner /> : <UserList users={data} />
  }
/>;
```

---

## Next.js 优化

参考：`references/nextjs_optimization_guide.md`

### 服务器组件 vs 客户端组件

默认使用服务器组件。仅在需要时添加 `use client`：

- 事件处理程序（onClick、onChange）
- 状态（useState、useReducer）
- 副作用（useEffect）
- 浏览器 API

```tsx
// 服务器组件（默认）— 不含 'use client'
async function ProductPage({ params }) {
  const product = await getProduct(params.id); // 服务器端获取

  return (
    <div>
      <h1>{product.name}</h1>
      <AddToCartButton productId={product.id} /> {/* 客户端组件 */}
    </div>
  );
}

// 客户端组件
"use client";
function AddToCartButton({ productId }) {
  const [adding, setAdding] = useState(false);
  return <button onClick={() => addToCart(productId)}>添加</button>;
}
```

### 图片优化

```tsx
import Image from 'next/image';

// 首屏内容 — 立即加载
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority
/>

// 响应式图片，使用 fill
<div className="relative aspect-video">
  <Image
    src="/product.jpg"
    alt="Product"
    fill
    sizes="(max-width: 768px) 100vw, 50vw"
    className="object-cover"
  />
</div>
```

### 数据获取模式

```tsx
// 并行获取
async function Dashboard() {
  const [user, stats] = await Promise.all([getUser(), getStats()]);
  return <div>...</div>;
}

// 使用 Suspense 流式渲染
async function ProductPage({ params }) {
  return (
    <div>
      <ProductDetails id={params.id} />
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={params.id} />
      </Suspense>
    </div>
  );
}
```

---

## 可访问性和测试

参考：`references/frontend_best_practices.md`

### 可访问性清单

1. **语义化 HTML**：使用正确的元素（`<button>`、`<nav>`、`<main>`）
2. **键盘导航**：所有交互元素均可聚焦
3. **ARIA 标签**：为图标和复杂小组件提供标签
4. **颜色对比度**：普通文本最小 4.5:1
5. **焦点指示器**：可见的焦点状态

```tsx
// 可访问的按钮
<button
  type="button"
  aria-label="关闭对话框"
  onClick={onClose}
  className="focus-visible:ring-2 focus-visible:ring-blue-500"
>
  <XIcon aria-hidden="true" />
</button>

// 为键盘用户提供的跳转链接
<a href="#main-content" className="sr-only focus:not-sr-only">
  跳到主要内容
</a>
```

### 测试策略

```tsx
// 使用 React Testing Library 进行组件测试
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

test("button triggers action on click", async () => {
  const onClick = vi.fn();
  render(<Button onClick={onClick}>Click me</Button>);

  await userEvent.click(screen.getByRole("button"));
  expect(onClick).toHaveBeenCalledTimes(1);
});

// 测试可访问性
test("dialog is accessible", async () => {
  render(<Dialog open={true} title="Confirm" />);

  expect(screen.getByRole("dialog")).toBeInTheDocument();
  expect(screen.getByRole("dialog")).toHaveAttribute("aria-labelledby");
});
```

---

## 快速参考

### 通用 Next.js 配置

```js
// next.config.js
const nextConfig = {
  images: {
    remotePatterns: [{ hostname: "cdn.example.com" }],
    formats: ["image/avif", "image/webp"],
  },
  experimental: {
    optimizePackageImports: ["lucide-react", "@heroicons/react"],
  },
};
```

### Tailwind CSS 工具类

```tsx
// 使用 cn() 的条件类
import { cn } from "@/lib/utils";

<button
  className={cn(
    "px-4 py-2 rounded",
    variant === "primary" && "bg-blue-500 text-white",
    disabled && "opacity-50 cursor-not-allowed",
  )}
/>;
```

### TypeScript 模式

```tsx
// 带 children 的 Props
interface CardProps {
  className?: string;
  children: React.ReactNode;
}

// 泛型组件
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map(renderItem)}</ul>;
}
```

---

## 资源

- React 模式: `references/react_patterns.md`
- Next.js 优化: `references/nextjs_optimization_guide.md`
- 最佳实践: `references/frontend_best_practices.md`
