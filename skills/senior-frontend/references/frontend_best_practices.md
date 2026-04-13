# 前端最佳实践

适用于可访问性、测试、TypeScript 和 Tailwind CSS 的现代前端开发标准。

---

＃＃ 目录

- [辅助功能 (a11y)](#accessibility-a11y)
- [测试策略](#testing-strategies)
- [TypeScript 模式](#typescript-patterns)
- [Tailwind CSS](#tailwind-css)
- [项目结构](#project-struct)
- [安全](#安全)

---

## 辅助功能 (a11y)

### 语义 HTML

```tsx
// BAD - Divs for everything
<div onClick={handleClick}>Click me</div>
<div class="header">...</div>
<div class="nav">...</div>

// GOOD - Semantic elements
<button onClick={handleClick}>Click me</button>
<header>...</header>
<nav>...</nav>
<main>...</main>
<article>...</article>
<aside>...</aside>
<footer>...</footer>
```

### 键盘导航

```tsx
// Ensure all interactive elements are keyboard accessible
function Modal({ isOpen, onClose, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      // Focus first focusable element
      const focusable = modalRef.current?.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      (focusable?.[0] as HTMLElement)?.focus();

      // Trap focus within modal
      const handleTab = (e: KeyboardEvent) => {
        if (e.key === 'Tab' && focusable) {
          const first = focusable[0] as HTMLElement;
          const last = focusable[focusable.length - 1] as HTMLElement;

          if (e.shiftKey && document.activeElement === first) {
            e.preventDefault();
            last.focus();
          } else if (!e.shiftKey && document.activeElement === last) {
            e.preventDefault();
            first.focus();
          }
        }

        if (e.key === 'Escape') {
          onClose();
        }
      };

      document.addEventListener('keydown', handleTab);
      return () => document.removeEventListener('keydown', handleTab);
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      {children}
    </div>
  );
}
```

### ARIA 属性

```tsx
// Live regions for dynamic content
<div aria-live="polite" aria-atomic="true">
  {status && <p>{status}</p>}
</div>

// Loading states
<button disabled={isLoading} aria-busy={isLoading}>
  {isLoading ? 'Loading...' : 'Submit'}
</button>

// Form labels
<label htmlFor="email">Email address</label>
<input
  id="email"
  type="email"
  aria-required="true"
  aria-invalid={!!errors.email}
  aria-describedby={errors.email ? 'email-error' : undefined}
/>
{errors.email && (
  <p id="email-error" role="alert">
    {errors.email}
  </p>
)}

// Navigation
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/" aria-current={isHome ? 'page' : undefined}>Home</a></li>
    <li><a href="/about" aria-current={isAbout ? 'page' : undefined}>About</a></li>
  </ul>
</nav>

// Toggle buttons
<button
  aria-pressed={isEnabled}
  onClick={() => setIsEnabled(!isEnabled)}
>
  {isEnabled ? 'Enabled' : 'Disabled'}
</button>

// Expandable sections
<button
  aria-expanded={isOpen}
  aria-controls="content-panel"
  onClick={() => setIsOpen(!isOpen)}
>
  Show details
</button>
<div id="content-panel" hidden={!isOpen}>
  Content here
</div>
```

### 颜色对比

```tsx
// Ensure 4.5:1 contrast ratio for text (WCAG AA)
// Use tools like @axe-core/react for testing

// tailwind.config.js - Define accessible colors
module.exports = {
  theme: {
    colors: {
      // Primary with proper contrast
      primary: {
        DEFAULT: '#2563eb', // Blue 600
        foreground: '#ffffff',
      },
      // Error state
      error: {
        DEFAULT: '#dc2626', // Red 600
        foreground: '#ffffff',
      },
      // Text colors with proper contrast
      foreground: '#0f172a', // Slate 900
      muted: '#64748b', // Slate 500 - minimum 4.5:1 on white
    },
  },
};

// Never rely on color alone
<span className="text-red-600">
  <ErrorIcon aria-hidden="true" />
  <span>Error: Invalid input</span>
</span>
```

### 仅限屏幕阅读器内容

```tsx
// Visually hidden but accessible to screen readers
const srOnly = 'absolute w-px h-px p-0 -m-px overflow-hidden whitespace-nowrap border-0';

// Skip link for keyboard users
<a href="#main-content" className={srOnly + ' focus:not-sr-only focus:absolute focus:top-0'}>
  Skip to main content
</a>

// Icon buttons need labels
<button aria-label="Close menu">
  <XIcon aria-hidden="true" />
</button>

// Or use visually hidden text
<button>
  <XIcon aria-hidden="true" />
  <span className={srOnly}>Close menu</span>
</button>
```

---

## 测试策略

### 使用测试库进行组件测试

```tsx
// Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const user = userEvent.setup();
    const handleClick = jest.fn();

    render(<Button onClick={handleClick}>Click me</Button>);
    await user.click(screen.getByRole('button'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when loading', () => {
    render(<Button isLoading>Submit</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
    expect(screen.getByRole('button')).toHaveAttribute('aria-busy', 'true');
  });

  it('shows loading text when loading', () => {
    render(<Button isLoading loadingText="Submitting...">Submit</Button>);
    expect(screen.getByText('Submitting...')).toBeInTheDocument();
  });
});
```

### 钩子测试

```tsx
// useCounter.test.ts
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('initializes with custom value', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.increment();
      result.current.increment();
      result.current.reset();
    });

    expect(result.current.count).toBe(5);
  });
});
```

### 集成测试

```tsx
// LoginForm.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';
import { AuthProvider } from '@/contexts/AuthContext';

const mockLogin = jest.fn();

jest.mock('@/lib/auth', () => ({
  login: (...args: unknown[]) => mockLogin(...args),
}));

describe('LoginForm', () => {
  beforeEach(() => {
    mockLogin.mockReset();
  });

  it('submits form with valid credentials', async () => {
    const user = userEvent.setup();
    mockLogin.mockResolvedValueOnce({ user: { id: '1', name: 'Test' } });

    render(
      <AuthProvider>
        <LoginForm />
      </AuthProvider>
    );

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('test@example.com', 'password123');
    });
  });

  it('shows validation errors for empty fields', async () => {
    const user = userEvent.setup();

    render(
      <AuthProvider>
        <LoginForm />
      </AuthProvider>
    );

    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
    expect(await screen.findByText(/password is required/i)).toBeInTheDocument();
    expect(mockLogin).not.toHaveBeenCalled();
  });
});
```

### Playwright 的 E2E 测试

```typescript
// e2e/checkout.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Checkout flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.click('[data-testid="product-1"] button');
    await page.click('[data-testid="cart-button"]');
  });

  test('completes checkout with valid payment', async ({ page }) => {
    await page.click('text=Proceed to Checkout');

    // Fill shipping info
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="address"]', '123 Test St');
    await page.fill('[name="city"]', 'Test City');
    await page.selectOption('[name="state"]', 'CA');
    await page.fill('[name="zip"]', '90210');

    await page.click('text=Continue to Payment');
    await page.click('text=Place Order');

    // Verify success
    await expect(page).toHaveURL(/\/order\/confirmation/);
    await expect(page.locator('h1')).toHaveText('Order Confirmed!');
  });
});
```

---

## TypeScript 模式

### 组件道具

```tsx
// Use interface for component props
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

// Extend HTML attributes
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  isLoading?: boolean;
}

function Button({ variant = 'primary', isLoading, children, ...props }: ButtonProps) {
  return (
    <button
      {...props}
      disabled={props.disabled || isLoading}
      className={cn(variants[variant], props.className)}
    >
      {isLoading ? <Spinner /> : children}
    </button>
  );
}

// Polymorphic components
type PolymorphicProps<E extends React.ElementType> = {
  as?: E;
} & React.ComponentPropsWithoutRef<E>;

function Box<E extends React.ElementType = 'div'>({
  as,
  children,
  ...props
}: PolymorphicProps<E>) {
  const Component = as || 'div';
  return <Component {...props}>{children}</Component>;
}

// Usage
<Box as="section" id="hero">Content</Box>
<Box as="article">Article content</Box>
```

### 受歧视的工会

```tsx
// State machines with exhaustive type checking
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

function DataDisplay<T>({ state, render }: {
  state: AsyncState<T>;
  render: (data: T) => React.ReactNode;
}) {
  switch (state.status) {
    case 'idle':
      return null;
    case 'loading':
      return <Spinner />;
    case 'success':
      return <>{render(state.data)}</>;
    case 'error':
      return <ErrorMessage error={state.error} />;
    // TypeScript ensures all cases are handled
  }
}
```

### 通用组件

```tsx
// Generic list component
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
  emptyMessage?: string;
}

function List<T>({ items, renderItem, keyExtractor, emptyMessage }: ListProps<T>) {
  if (items.length === 0) {
    return <p className="text-muted">{emptyMessage || 'No items'}</p>;
  }

  return (
    <ul>
      {items.map((item, index) => (
        <li key={keyExtractor(item)}>{renderItem(item, index)}</li>
      ))}
    </ul>
  );
}

// Usage
<List
  items={users}
  keyExtractor={(user) => user.id}
  renderItem={(user) => <UserCard user={user} />}
/>
```

### 类型保护

```tsx
// User-defined type guards
interface User {
  id: string;
  name: string;
  email: string;
}

interface Admin extends User {
  role: 'admin';
  permissions: string[];
}

function isAdmin(user: User): user is Admin {
  return 'role' in user && user.role === 'admin';
}

function UserBadge({ user }: { user: User }) {
  if (isAdmin(user)) {
    // TypeScript knows user is Admin here
    return <Badge variant="admin">Admin ({user.permissions.length} perms)</Badge>;
  }

  return <Badge>User</Badge>;
}

// API response type guards
interface ApiSuccess<T> {
  success: true;
  data: T;
}

interface ApiError {
  success: false;
  error: string;
}

type ApiResponse<T> = ApiSuccess<T> | ApiError;

function isApiSuccess<T>(response: ApiResponse<T>): response is ApiSuccess<T> {
  return response.success === true;
}
```

---

## 顺风 CSS

### 具有 CVA 的组件变体

```tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700 focus-visible:ring-blue-500',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 focus-visible:ring-gray-500',
        ghost: 'hover:bg-gray-100 hover:text-gray-900',
        destructive: 'bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-500',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4 text-sm',
        lg: 'h-12 px-6 text-base',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  );
}

// Usage
<Button variant="primary" size="lg">Large Primary</Button>
<Button variant="ghost" size="icon"><MenuIcon /></Button>
```

### 响应式设计

```tsx
// Mobile-first responsive design
<div className="
  grid
  grid-cols-1          {/* Mobile: 1 column */}
  sm:grid-cols-2       {/* 640px+: 2 columns */}
  lg:grid-cols-3       {/* 1024px+: 3 columns */}
  xl:grid-cols-4       {/* 1280px+: 4 columns */}
  gap-4
  sm:gap-6
  lg:gap-8
">
  {products.map(product => <ProductCard key={product.id} product={product} />)}
</div>

// Container with responsive padding
<div className="container mx-auto px-4 sm:px-6 lg:px-8">
  Content
</div>

// Hide/show based on breakpoint
<nav className="hidden md:flex">Desktop nav</nav>
<button className="md:hidden">Mobile menu</button>
```

### 动画实用程序

```tsx
// Skeleton loading
<div className="animate-pulse space-y-4">
  <div className="h-4 bg-gray-200 rounded w-3/4" />
  <div className="h-4 bg-gray-200 rounded w-1/2" />
</div>

// Transitions
<button className="
  transition-all
  duration-200
  ease-in-out
  hover:scale-105
  active:scale-95
">
  Hover me
</button>

// Custom animations in tailwind.config.js
module.exports = {
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'spin-slow': 'spin 3s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
};

// Usage
<div className="animate-fade-in">Fading in</div>
```

---

## 项目结构

### 基于特征的结构

```
src/
├── app/                    # Next.js App Router
│   ├── (auth)/             # Auth route group
│   │   ├── login/
│   │   └── register/
│   ├── dashboard/
│   │   ├── page.tsx
│   │   └── layout.tsx
│   └── layout.tsx
├── components/
│   ├── ui/                 # Shared UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   └── index.ts
│   └── features/           # Feature-specific components
│       ├── auth/
│       │   ├── LoginForm.tsx
│       │   └── RegisterForm.tsx
│       └── dashboard/
│           ├── StatsCard.tsx
│           └── RecentActivity.tsx
├── hooks/                  # Custom React hooks
│   ├── useAuth.ts
│   ├── useDebounce.ts
│   └── useLocalStorage.ts
├── lib/                    # Utilities and configs
│   ├── utils.ts
│   ├── api.ts
│   └── constants.ts
├── types/                  # TypeScript types
│   ├── user.ts
│   └── api.ts
└── styles/
    └── globals.css
```

### 桶出口

```tsx
// components/ui/index.ts
export { Button } from './Button';
export { Input } from './Input';
export { Card, CardHeader, CardContent, CardFooter } from './Card';
export { Dialog, DialogTrigger, DialogContent } from './Dialog';

// Usage
import { Button, Input, Card } from '@/components/ui';
```

---

＃＃ 安全

### XSS预防

React 默认情况下会转义内容，这可以防止大多数 XSS 攻击。当你需要渲染 HTML 内容时：

1. **尽可能避免渲染原始 HTML**
2. **使用 DOMPurify 清理**以获取可信内容源
3. **对允许的标签和属性使用允许列表**

```tsx
// React escapes by default - this is safe
<div>{userInput}</div>

// When you must render HTML, sanitize first
import DOMPurify from 'dompurify';

function SafeHTML({ html }: { html: string }) {
  const sanitized = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
    ALLOWED_ATTR: ['href'],
  });

  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}
```

### 输入验证

```tsx
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase letter')
    .regex(/[0-9]/, 'Password must contain number'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type FormData = z.infer<typeof schema>;

function RegisterForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Input {...register('email')} error={errors.email?.message} />
      <Input type="password" {...register('password')} error={errors.password?.message} />
      <Input type="password" {...register('confirmPassword')} error={errors.confirmPassword?.message} />
      <Button type="submit">Register</Button>
    </form>
  );
}
```

### 安全 API 调用

```tsx
// Use environment variables for API endpoints
const API_URL = process.env.NEXT_PUBLIC_API_URL;

// Never include secrets in client code - use server-side API routes
// app/api/data/route.ts
export async function GET() {
  const response = await fetch('https://api.example.com/data', {
    headers: {
      'Authorization': `Bearer ${process.env.API_SECRET}`, // Server-side only
    },
  });

  return Response.json(await response.json());
}
```
