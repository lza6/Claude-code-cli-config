# Next.js 优化指南

Next.js 14+ 应用程序的性能优化技术。

---

＃＃ 目录

- [渲染策略](#rendering-strategies)
- [图像优化](#image-optimization)
- [代码分割](#code-splitting)
- [数据获取](#data-fetching)
- [缓存策略](#caching-strategies)
- [捆绑优化](#bundle-optimization)
- [核心网络生命周期](#core-web-vitals)

---

## 渲染策略

### 服务器组件（默认）

服务器组件在服务器上呈现并将 HTML 发送到客户端。用于数据量大、非交互式内容。

```tsx
// app/products/page.tsx - Server Component (default)
async function ProductsPage() {
  // This runs on the server - no client bundle impact
  const products = await db.products.findMany();

  return (
    <div className="grid grid-cols-3 gap-4">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

### 客户端组件

Use `'use client'` only when you need:
- 事件处理程序（onClick、onChange）
- 状态（useState、useReducer）
- 效果（useEffect）
- 浏览器 API（窗口、文档）

```tsx
'use client';

import { useState } from 'react';

function AddToCartButton({ productId }: { productId: string }) {
  const [isAdding, setIsAdding] = useState(false);

  async function handleClick() {
    setIsAdding(true);
    await addToCart(productId);
    setIsAdding(false);
  }

  return (
    <button onClick={handleClick} disabled={isAdding}>
      {isAdding ? 'Adding...' : 'Add to Cart'}
    </button>
  );
}
```

### 混合服务器和客户端组件

```tsx
// app/products/[id]/page.tsx - Server Component
async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);

  return (
    <div>
      {/* Server-rendered content */}
      <h1>{product.name}</h1>
      <p>{product.description}</p>

      {/* Client component for interactivity */}
      <AddToCartButton productId={product.id} />

      {/* Server component for reviews */}
      <ProductReviews productId={product.id} />
    </div>
  );
}
```

### 静态渲染与动态渲染

```tsx
// Force static generation at build time
export const dynamic = 'force-static';

// Force dynamic rendering at request time
export const dynamic = 'force-dynamic';

// Revalidate every 60 seconds (ISR)
export const revalidate = 60;

// Revalidate on-demand
import { revalidatePath, revalidateTag } from 'next/cache';

async function updateProduct(id: string, data: ProductData) {
  await db.products.update({ where: { id }, data });

  // Revalidate specific path
  revalidatePath(`/products/${id}`);

  // Or revalidate by tag
  revalidateTag('products');
}
```

---

## 图像优化

### Next.js 图像组件

```tsx
import Image from 'next/image';

// Basic optimized image
<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority // Load immediately for LCP
/>

// Responsive image
<Image
  src="/product.jpg"
  alt="Product"
  fill
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  className="object-cover"
/>

// With placeholder blur
import productImage from '@/public/product.jpg';

<Image
  src={productImage}
  alt="Product"
  placeholder="blur" // Uses imported image data
/>
```

### 远程图像配置

```js
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
        pathname: '/images/**',
      },
      {
        protocol: 'https',
        hostname: '*.cloudinary.com',
      },
    ],
    // Image formats (webp is default)
    formats: ['image/avif', 'image/webp'],
    // Device sizes for srcset
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    // Image sizes for srcset
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
};
```

### 延迟加载模式

```tsx
// Images below the fold - lazy load (default)
<Image
  src="/gallery/photo1.jpg"
  alt="Gallery photo"
  width={400}
  height={300}
  loading="lazy" // Default behavior
/>

// Above the fold - load immediately
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority
  loading="eager"
/>
```

---

## 代码分割

### 动态导入

```tsx
import dynamic from 'next/dynamic';

// Basic dynamic import
const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <ChartSkeleton />,
});

// Disable SSR for client-only components
const MapComponent = dynamic(() => import('@/components/Map'), {
  ssr: false,
  loading: () => <div className="h-[400px] bg-gray-100" />,
});

// Named exports
const Modal = dynamic(() =>
  import('@/components/ui').then(mod => mod.Modal)
);

// With suspense
const DashboardCharts = dynamic(() => import('@/components/DashboardCharts'), {
  loading: () => <Suspense fallback={<ChartsSkeleton />} />,
});
```

### 基于路由的拆分

```tsx
// app/dashboard/analytics/page.tsx
// This page only loads when /dashboard/analytics is visited
import { Suspense } from 'react';
import AnalyticsCharts from './AnalyticsCharts';

export default function AnalyticsPage() {
  return (
    <Suspense fallback={<AnalyticsSkeleton />}>
      <AnalyticsCharts />
    </Suspense>
  );
}
```

### 代码分割的并行路由

```
app/
├── dashboard/
│   ├── @analytics/
│   │   └── page.tsx    # Loaded in parallel
│   ├── @metrics/
│   │   └── page.tsx    # Loaded in parallel
│   ├── layout.tsx
│   └── page.tsx
```

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  analytics,
  metrics,
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  metrics: React.ReactNode;
}) {
  return (
    <div className="grid grid-cols-2 gap-4">
      {children}
      <Suspense fallback={<AnalyticsSkeleton />}>{analytics}</Suspense>
      <Suspense fallback={<MetricsSkeleton />}>{metrics}</Suspense>
    </div>
  );
}
```

---

## 数据获取

### 服务器端数据获取

```tsx
// Parallel data fetching
async function Dashboard() {
  // Start both requests simultaneously
  const [user, stats, notifications] = await Promise.all([
    getUser(),
    getStats(),
    getNotifications(),
  ]);

  return (
    <div>
      <UserHeader user={user} />
      <StatsPanel stats={stats} />
      <NotificationList notifications={notifications} />
    </div>
  );
}
```

### 充满悬念的直播

```tsx
import { Suspense } from 'react';

async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);

  return (
    <div>
      {/* Immediate content */}
      <h1>{product.name}</h1>
      <p>{product.description}</p>

      {/* Stream reviews - don't block page */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={params.id} />
      </Suspense>

      {/* Stream recommendations */}
      <Suspense fallback={<RecommendationsSkeleton />}>
        <Recommendations productId={params.id} />
      </Suspense>
    </div>
  );
}

// Slow data component
async function Reviews({ productId }: { productId: string }) {
  const reviews = await getReviews(productId); // Slow query
  return <ReviewList reviews={reviews} />;
}
```

### 请求记忆

```tsx
// Next.js automatically dedupes identical requests
async function Layout({ children }) {
  const user = await getUser(); // Request 1
  return <div>{children}</div>;
}

async function Header() {
  const user = await getUser(); // Same request - cached!
  return <div>Hello, {user.name}</div>;
}

// Both components call getUser() but only one request is made
```

---

## 缓存策略

### 获取缓存选项

```tsx
// Cache indefinitely (default for static)
fetch('https://api.example.com/data');

// No cache - always fresh
fetch('https://api.example.com/data', { cache: 'no-store' });

// Revalidate after time
fetch('https://api.example.com/data', {
  next: { revalidate: 3600 } // 1 hour
});

// Tag-based revalidation
fetch('https://api.example.com/products', {
  next: { tags: ['products'] }
});

// Later, revalidate by tag
import { revalidateTag } from 'next/cache';
revalidateTag('products');
```

### 路由段配置

```tsx
// app/products/page.tsx

// Revalidate every hour
export const revalidate = 3600;

// Or force dynamic
export const dynamic = 'force-dynamic';

// Generate static params at build
export async function generateStaticParams() {
  const products = await getProducts();
  return products.map(p => ({ id: p.id }));
}
```

###用于自定义缓存的unstable_cache

```tsx
import { unstable_cache } from 'next/cache';

const getCachedUser = unstable_cache(
  async (userId: string) => {
    const user = await db.users.findUnique({ where: { id: userId } });
    return user;
  },
  ['user-cache'],
  {
    revalidate: 3600, // 1 hour
    tags: ['users'],
  }
);

// Usage
const user = await getCachedUser(userId);
```

---

## 捆绑优化

### 分析包大小

```bash
# Install analyzer
npm install @next/bundle-analyzer

# Update next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // config
});

# Run analysis
ANALYZE=true npm run build
```

### Tree Shaking 导入

```tsx
// BAD - Imports entire library
import _ from 'lodash';
const result = _.debounce(fn, 300);

// GOOD - Import only what you need
import debounce from 'lodash/debounce';
const result = debounce(fn, 300);

// GOOD - Named imports (tree-shakeable)
import { debounce } from 'lodash-es';
```

### 优化依赖关系

```js
// next.config.js
module.exports = {
  // Transpile specific packages
  transpilePackages: ['ui-library', 'shared-utils'],

  // Optimize package imports
  experimental: {
    optimizePackageImports: ['lucide-react', '@heroicons/react'],
  },

  // External packages for server
  serverExternalPackages: ['sharp', 'bcrypt'],
};
```

### 字体优化

```tsx
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto-mono',
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${robotoMono.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  );
}
```

---

## 核心网络生命力

### 最大内容涂料 (LCP)

```tsx
// Optimize LCP hero image
import Image from 'next/image';

export default function Hero() {
  return (
    <section className="relative h-[600px]">
      <Image
        src="/hero.jpg"
        alt="Hero"
        fill
        priority // Preload for LCP
        sizes="100vw"
        className="object-cover"
      />
      <div className="relative z-10">
        <h1>Welcome</h1>
      </div>
    </section>
  );
}

// Preload critical resources in layout
export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <link rel="preload" href="/hero.jpg" as="image" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### 累积布局偏移 (CLS)

```tsx
// Prevent CLS with explicit dimensions
<Image
  src="/product.jpg"
  alt="Product"
  width={400}
  height={300}
/>

// Or use aspect ratio
<div className="aspect-video relative">
  <Image src="/video-thumb.jpg" alt="Video" fill />
</div>

// Skeleton placeholders
function ProductCard({ product }: { product?: Product }) {
  if (!product) {
    return (
      <div className="animate-pulse">
        <div className="h-48 bg-gray-200 rounded" />
        <div className="h-4 bg-gray-200 rounded mt-2 w-3/4" />
        <div className="h-4 bg-gray-200 rounded mt-1 w-1/2" />
      </div>
    );
  }

  return (
    <div>
      <Image src={product.image} alt={product.name} width={300} height={200} />
      <h3>{product.name}</h3>
      <p>{product.price}</p>
    </div>
  );
}
```

### 首次输入延迟 (FID) / 与下一次绘制的交互 (INP)

```tsx
// Defer non-critical JavaScript
import Script from 'next/script';

export default function Layout({ children }) {
  return (
    <html>
      <body>
        {children}

        {/* Load analytics after page is interactive */}
        <Script
          src="https://analytics.example.com/script.js"
          strategy="afterInteractive"
        />

        {/* Load chat widget when idle */}
        <Script
          src="https://chat.example.com/widget.js"
          strategy="lazyOnload"
        />
      </body>
    </html>
  );
}

// Use web workers for heavy computation
// app/components/DataProcessor.tsx
'use client';

import { useEffect, useState } from 'react';

function DataProcessor({ data }: { data: number[] }) {
  const [result, setResult] = useState<number | null>(null);

  useEffect(() => {
    const worker = new Worker(new URL('../workers/processor.js', import.meta.url));

    worker.postMessage(data);
    worker.onmessage = (e) => setResult(e.data);

    return () => worker.terminate();
  }, [data]);

  return <div>Result: {result}</div>;
}
```

### 衡量绩效

```tsx
// app/components/PerformanceMonitor.tsx
'use client';

import { useReportWebVitals } from 'next/web-vitals';

export function PerformanceMonitor() {
  useReportWebVitals((metric) => {
    switch (metric.name) {
      case 'LCP':
        console.log('LCP:', metric.value);
        break;
      case 'FID':
        console.log('FID:', metric.value);
        break;
      case 'CLS':
        console.log('CLS:', metric.value);
        break;
      case 'TTFB':
        console.log('TTFB:', metric.value);
        break;
    }

    // Send to analytics
    analytics.track('web-vital', {
      name: metric.name,
      value: metric.value,
      id: metric.id,
    });
  });

  return null;
}
```

---

## 快速参考

### 绩效检查表

|面积 |优化|影响 |
|------|-------------|--------|
|图片 | LCP 优先使用下一个/图像 |高|
|字体|使用 next/font 进行显示：swap |中等|
|代码|重型部件的动态进口|高|
|数据|使用 Promise.all 并行获取 |高|
|渲染 |默认服务器组件 |高|
|缓存|适当配置重新验证 |中等|
|捆绑 | Tree-shake 导入，分析大小 |中等|

### 配置模板

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [{ hostname: 'cdn.example.com' }],
    formats: ['image/avif', 'image/webp'],
  },
  experimental: {
    optimizePackageImports: ['lucide-react'],
  },
  headers: async () => [
    {
      source: '/(.*)',
      headers: [
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'X-Frame-Options', value: 'DENY' },
      ],
    },
  ],
};

module.exports = nextConfig;
```
