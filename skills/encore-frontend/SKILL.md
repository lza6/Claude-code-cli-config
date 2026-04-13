---
name: encore-frontend
description: "将 React/Next.js 应用程序连接到 Encore.ts 后端。"
---

# 与 Encore 的前端集成

＃＃ 指示

Encore 提供了将前端应用程序连接到后端 API 的工具。

### 生成 TypeScript 客户端

```bash
# Generate client for local development
encore gen client --output=./frontend/src/client.ts --env=local

# Generate client for a deployed environment
encore gen client --output=./frontend/src/client.ts --env=staging
```

这会根据您的 API 定义生成完全类型化的客户端。

### 使用生成的客户端

```typescript
// frontend/src/client.ts is auto-generated
import Client from "./client";

const client = new Client("http://localhost:4000");

// Fully typed API calls
const user = await client.user.getUser({ id: "123" });
console.log(user.email);

const newUser = await client.user.createUser({
  email: "new@example.com",
  name: "New User",
});
```

### 反应示例

```tsx
// frontend/src/components/UserProfile.tsx
import { useState, useEffect } from "react";
import Client from "../client";

const client = new Client(import.meta.env.VITE_API_URL);

export function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    client.user.getUser({ id: userId })
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### 使用 TanStack 查询做出反应

```tsx
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import Client from "../client";

const client = new Client(import.meta.env.VITE_API_URL);

export function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ["user", userId],
    queryFn: () => client.user.getUser({ id: userId }),
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return <div>{user.name}</div>;
}

export function CreateUserForm() {
  const queryClient = useQueryClient();
  
  const mutation = useMutation({
    mutationFn: (data: { email: string; name: string }) => 
      client.user.createUser(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    mutation.mutate({
      email: formData.get("email") as string,
      name: formData.get("name") as string,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" required />
      <input name="name" required />
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? "Creating..." : "Create User"}
      </button>
    </form>
  );
}
```

### Next.js 服务器组件

```tsx
// app/users/[id]/page.tsx
import Client from "@/lib/client";

const client = new Client(process.env.API_URL);

export default async function UserPage({ params }: { params: { id: string } }) {
  const user = await client.user.getUser({ id: params.id });
  
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### CORS 配置

Configure CORS in your `encore.app` file:

```json
{
    "id": "my-app",
    "global_cors": {
        "allow_origins_with_credentials": [
            "http://localhost:3000",
            "https://myapp.com",
            "https://*.myapp.com"
        ]
    }
}
```

### CORS 选项

|选项|描述 |
|--------|-------------|
| `allow_origins_without_credentials` | Origins allowed for non-credentialed requests (default: `["*"]`) |
| `allow_origins_with_credentials` | Origins allowed for credentialed requests (cookies, auth headers) |
| `allow_headers` | Additional request headers to allow |
| `expose_headers` | Additional response headers to expose |
| `debug` | Enable CORS debug logging |

### 来自前端的身份验证

对于经过身份验证的请求，请传递 Authorization 标头：

```typescript
// Using fetch
const response = await fetch("http://localhost:4000/profile", {
  headers: {
    "Authorization": `Bearer ${token}`,
  },
});

// Or include credentials for cookie-based auth
const response = await fetch("http://localhost:4000/profile", {
  credentials: "include",
});
```

使用 TanStack Query，配置默认获取器：

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      queryFn: async ({ queryKey }) => {
        const response = await fetch(queryKey[0] as string, {
          headers: { Authorization: `Bearer ${getToken()}` },
        });
        if (!response.ok) throw new Error("Request failed");
        return response.json();
      },
    },
  },
});
```

### 使用普通获取

如果您不想使用生成的客户端：

```typescript
async function getUser(id: string) {
  const response = await fetch(`http://localhost:4000/users/${id}`);
  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`);
  }
  return response.json();
}

async function createUser(email: string, name: string) {
  const response = await fetch("http://localhost:4000/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, name }),
  });
  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`);
  }
  return response.json();
}
```

### 环境变量

```bash
# .env.local (Next.js)
NEXT_PUBLIC_API_URL=http://localhost:4000

# .env (Vite)
VITE_API_URL=http://localhost:4000
```

### 指南

- Use `encore gen client` to generate typed API clients
- 当您的 API 更改时重新生成客户端
- Configure CORS in `encore.app` for production domains
- Use `allow_origins_with_credentials` for authenticated requests
- Include `Authorization` header for token-based auth
- Use `credentials: "include"` for cookie-based auth
- 对 API URL 使用环境变量（每个环境不同）
- 生成的客户端自动处理错误和类型
