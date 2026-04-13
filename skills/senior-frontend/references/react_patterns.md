# 反应模式

用于使用 TypeScript 构建可扩展的 React 应用程序的生产就绪模式。

---

＃＃ 目录

- [组件构成](#component-composition)
- [自定义挂钩](#custom-hooks)
- [状态管理](#state-management)
- [性能模式](#performance-patterns)
- [错误边界](#error-boundaries)
- [反模式](#反模式)

---

## 组件构成

### 复合组件

在构建具有多个相关部分的可重用 UI 组件时，请使用复合组件。

```tsx
// Compound component pattern for a Select
interface SelectContextType {
  value: string;
  onChange: (value: string) => void;
}

const SelectContext = createContext<SelectContextType | null>(null);

function Select({ children, value, onChange }: {
  children: React.ReactNode;
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <SelectContext.Provider value={{ value, onChange }}>
      <div className="relative">{children}</div>
    </SelectContext.Provider>
  );
}

function SelectTrigger({ children }: { children: React.ReactNode }) {
  const context = useContext(SelectContext);
  if (!context) throw new Error('SelectTrigger must be used within Select');

  return (
    <button className="flex items-center gap-2 px-4 py-2 border rounded">
      {children}
    </button>
  );
}

function SelectOption({ value, children }: { value: string; children: React.ReactNode }) {
  const context = useContext(SelectContext);
  if (!context) throw new Error('SelectOption must be used within Select');

  return (
    <div
      onClick={() => context.onChange(value)}
      className={`px-4 py-2 cursor-pointer hover:bg-gray-100 ${
        context.value === value ? 'bg-blue-50' : ''
      }`}
    >
      {children}
    </div>
  );
}

// Attach sub-components
Select.Trigger = SelectTrigger;
Select.Option = SelectOption;

// Usage
<Select value={selected} onChange={setSelected}>
  <Select.Trigger>Choose option</Select.Trigger>
  <Select.Option value="a">Option A</Select.Option>
  <Select.Option value="b">Option B</Select.Option>
</Select>
```

### 渲染道具

当您需要与灵活渲染共享行为时，请使用渲染道具。

```tsx
interface MousePosition {
  x: number;
  y: number;
}

function MouseTracker({ render }: { render: (pos: MousePosition) => React.ReactNode }) {
  const [position, setPosition] = useState<MousePosition>({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return <>{render(position)}</>;
}

// Usage
<MouseTracker
  render={({ x, y }) => (
    <div>Mouse position: {x}, {y}</div>
  )}
/>
```

### 高阶组件 (HOC)

使用 HOC 解决跨领域问题，例如身份验证或日志记录。

```tsx
function withAuth<P extends object>(WrappedComponent: React.ComponentType<P>) {
  return function AuthenticatedComponent(props: P) {
    const { user, isLoading } = useAuth();

    if (isLoading) return <LoadingSpinner />;
    if (!user) return <Navigate to="/login" />;

    return <WrappedComponent {...props} />;
  };
}

// Usage
const ProtectedDashboard = withAuth(Dashboard);
```

---

## 自定义挂钩

### useAsync - 处理异步操作

```tsx
interface AsyncState<T> {
  data: T | null;
  error: Error | null;
  status: 'idle' | 'loading' | 'success' | 'error';
}

function useAsync<T>(asyncFn: () => Promise<T>, deps: any[] = []) {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    error: null,
    status: 'idle',
  });

  const execute = useCallback(async () => {
    setState({ data: null, error: null, status: 'loading' });
    try {
      const data = await asyncFn();
      setState({ data, error: null, status: 'success' });
    } catch (error) {
      setState({ data: null, error: error as Error, status: 'error' });
    }
  }, deps);

  useEffect(() => {
    execute();
  }, [execute]);

  return { ...state, refetch: execute };
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { data: user, status, error, refetch } = useAsync(
    () => fetchUser(userId),
    [userId]
  );

  if (status === 'loading') return <Spinner />;
  if (status === 'error') return <Error message={error?.message} />;
  if (!user) return null;

  return <Profile user={user} />;
}
```

### useDebounce - 去抖值

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
function SearchInput() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (debouncedQuery) {
      searchAPI(debouncedQuery);
    }
  }, [debouncedQuery]);

  return <input value={query} onChange={(e) => setQuery(e.target.value)} />;
}
```

### useLocalStorage - 持久状态

```tsx
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') return initialValue;
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
      }
    } catch (error) {
      console.error('Error saving to localStorage:', error);
    }
  }, [key, storedValue]);

  return [storedValue, setValue] as const;
}

// Usage
const [theme, setTheme] = useLocalStorage('theme', 'light');
```

### useMediaQuery - 响应式设计

```tsx
function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    setMatches(media.matches);

    const listener = (e: MediaQueryListEvent) => setMatches(e.matches);
    media.addEventListener('change', listener);
    return () => media.removeEventListener('change', listener);
  }, [query]);

  return matches;
}

// Usage
function ResponsiveNav() {
  const isMobile = useMediaQuery('(max-width: 768px)');
  return isMobile ? <MobileNav /> : <DesktopNav />;
}
```

### usePrevious - 跟踪以前的值

```tsx
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

// Usage
function Counter() {
  const [count, setCount] = useState(0);
  const prevCount = usePrevious(count);

  return (
    <div>
      Current: {count}, Previous: {prevCount}
    </div>
  );
}
```

---

## 状态管理

### 上下文与Reducer

对于多个组件需要访问的复杂状态。

```tsx
// types.ts
interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  total: number;
}

type CartAction =
  | { type: 'ADD_ITEM'; payload: CartItem }
  | { type: 'REMOVE_ITEM'; payload: string }
  | { type: 'UPDATE_QUANTITY'; payload: { id: string; quantity: number } }
  | { type: 'CLEAR_CART' };

// reducer.ts
function cartReducer(state: CartState, action: CartAction): CartState {
  switch (action.type) {
    case 'ADD_ITEM': {
      const existingItem = state.items.find(i => i.id === action.payload.id);
      if (existingItem) {
        return {
          ...state,
          items: state.items.map(item =>
            item.id === action.payload.id
              ? { ...item, quantity: item.quantity + 1 }
              : item
          ),
        };
      }
      return {
        ...state,
        items: [...state.items, { ...action.payload, quantity: 1 }],
      };
    }
    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter(i => i.id !== action.payload),
      };
    case 'UPDATE_QUANTITY':
      return {
        ...state,
        items: state.items.map(item =>
          item.id === action.payload.id
            ? { ...item, quantity: action.payload.quantity }
            : item
        ),
      };
    case 'CLEAR_CART':
      return { items: [], total: 0 };
    default:
      return state;
  }
}

// context.tsx
const CartContext = createContext<{
  state: CartState;
  dispatch: React.Dispatch<CartAction>;
} | null>(null);

function CartProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(cartReducer, { items: [], total: 0 });

  // Compute total whenever items change
  const stateWithTotal = useMemo(() => ({
    ...state,
    total: state.items.reduce((sum, item) => sum + item.price * item.quantity, 0),
  }), [state.items]);

  return (
    <CartContext.Provider value={{ state: stateWithTotal, dispatch }}>
      {children}
    </CartContext.Provider>
  );
}

function useCart() {
  const context = useContext(CartContext);
  if (!context) throw new Error('useCart must be used within CartProvider');
  return context;
}
```

### Zustand（轻量级替代方案）

```tsx
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthStore {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      login: async (email, password) => {
        const { user, token } = await authAPI.login(email, password);
        set({ user, token });
      },
      logout: () => set({ user: null, token: null }),
    }),
    { name: 'auth-storage' }
  )
);

// Usage
function Profile() {
  const { user, logout } = useAuthStore();
  return user ? <div>{user.name} <button onClick={logout}>Logout</button></div> : null;
}
```

---

## 性能模式

### React.memo 与自定义比较

```tsx
interface ListItemProps {
  item: { id: string; name: string; count: number };
  onSelect: (id: string) => void;
}

const ListItem = React.memo(
  function ListItem({ item, onSelect }: ListItemProps) {
    return (
      <div onClick={() => onSelect(item.id)}>
        {item.name} ({item.count})
      </div>
    );
  },
  (prevProps, nextProps) => {
    // Only re-render if item data changed
    return (
      prevProps.item.id === nextProps.item.id &&
      prevProps.item.name === nextProps.item.name &&
      prevProps.item.count === nextProps.item.count
    );
  }
);
```

### useMemo 进行昂贵的计算

```tsx
function DataTable({ data, sortColumn, filterText }: {
  data: Item[];
  sortColumn: string;
  filterText: string;
}) {
  const processedData = useMemo(() => {
    // Filter
    let result = data.filter(item =>
      item.name.toLowerCase().includes(filterText.toLowerCase())
    );

    // Sort
    result = [...result].sort((a, b) => {
      const aVal = a[sortColumn as keyof Item];
      const bVal = b[sortColumn as keyof Item];
      return aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
    });

    return result;
  }, [data, sortColumn, filterText]);

  return (
    <table>
      {processedData.map(item => (
        <tr key={item.id}>{/* ... */}</tr>
      ))}
    </table>
  );
}
```

### useCallback 用于稳定引用

```tsx
function ParentComponent() {
  const [items, setItems] = useState<Item[]>([]);

  // Stable reference - won't cause child re-renders
  const handleItemClick = useCallback((id: string) => {
    setItems(prev => prev.map(item =>
      item.id === id ? { ...item, selected: !item.selected } : item
    ));
  }, []);

  const handleAddItem = useCallback((newItem: Item) => {
    setItems(prev => [...prev, newItem]);
  }, []);

  return (
    <>
      <ItemList items={items} onItemClick={handleItemClick} />
      <AddItemForm onAdd={handleAddItem} />
    </>
  );
}
```

### 长列表的虚拟化

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // estimated row height
    overscan: 5,
  });

  return (
    <div ref={parentRef} className="h-[400px] overflow-auto">
      <div
        style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}
      >
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            {items[virtualRow.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## 误差边界

### 基于类的错误边界

```tsx
interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    this.props.onError?.(error, errorInfo);
    // Log to error reporting service
    console.error('Error caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="p-4 bg-red-50 border border-red-200 rounded">
          <h2 className="text-red-800 font-bold">Something went wrong</h2>
          <p className="text-red-600">{this.state.error?.message}</p>
          <button
            onClick={() => this.setState({ hasError: false, error: null })}
            className="mt-2 px-4 py-2 bg-red-600 text-white rounded"
          >
            Try Again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Usage
<ErrorBoundary
  fallback={<ErrorFallback />}
  onError={(error) => trackError(error)}
>
  <MyComponent />
</ErrorBoundary>
```

### 带有错误边界的悬念

```tsx
function DataComponent() {
  return (
    <ErrorBoundary fallback={<ErrorMessage />}>
      <Suspense fallback={<LoadingSpinner />}>
        <AsyncDataLoader />
      </Suspense>
    </ErrorBoundary>
  );
}
```

---

## 反模式

### 避免：在 JSX 中创建内联对象/数组

```tsx
// BAD - Creates new object every render, causes re-renders
<Component style={{ color: 'red' }} items={[1, 2, 3]} />

// GOOD - Define outside or use useMemo
const style = { color: 'red' };
const items = [1, 2, 3];
<Component style={style} items={items} />

// Or with useMemo for dynamic values
const style = useMemo(() => ({ color: theme.primary }), [theme.primary]);
```

### 避免：索引作为动态列表的关键

```tsx
// BAD - Index keys break with reordering/filtering
{items.map((item, index) => (
  <Item key={index} data={item} />
))}

// GOOD - Use stable unique ID
{items.map(item => (
  <Item key={item.id} data={item} />
))}
```

### 避免：支柱钻井

```tsx
// BAD - Passing props through many levels
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <UserInfo user={user} />
    </Sidebar>
  </Layout>
</App>

// GOOD - Use Context
const UserContext = createContext<User | null>(null);

function App() {
  return (
    <UserContext.Provider value={user}>
      <Layout>
        <Sidebar>
          <UserInfo />
        </Sidebar>
      </Layout>
    </UserContext.Provider>
  );
}

function UserInfo() {
  const user = useContext(UserContext);
  return <div>{user?.name}</div>;
}
```

### 避免：直接改变状态

```tsx
// BAD - Mutates state directly
const addItem = (item: Item) => {
  items.push(item); // WRONG
  setItems(items);  // Won't trigger re-render
};

// GOOD - Create new array
const addItem = (item: Item) => {
  setItems(prev => [...prev, item]);
};

// GOOD - For objects
const updateUser = (field: string, value: string) => {
  setUser(prev => ({ ...prev, [field]: value }));
};
```

### 避免：派生状态的 useEffect

```tsx
// BAD - Unnecessary effect and extra render
const [items, setItems] = useState<Item[]>([]);
const [total, setTotal] = useState(0);

useEffect(() => {
  setTotal(items.reduce((sum, item) => sum + item.price, 0));
}, [items]);

// GOOD - Compute during render
const [items, setItems] = useState<Item[]>([]);
const total = items.reduce((sum, item) => sum + item.price, 0);

// Or useMemo for expensive calculations
const total = useMemo(
  () => items.reduce((sum, item) => sum + item.price, 0),
  [items]
);
```
