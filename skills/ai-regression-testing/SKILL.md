---
name: ai-regression-testing
description: "AI 辅助开发的回归测试策略。包括无数据库依赖的沙盒模式 API 测试、自动化缺陷检查工作流，以及用于捕捉同一模型编写并评审代码时产生的 AI 盲区的模式。"
origin: ECC
---

# AI 回归测试 (AI Regression Testing)

专门为 AI 辅助开发设计的测试模式。在这种开发模式下，同一个模型既编写代码又评审代码，往往会产生系统性的盲区，而这些盲区只能通过自动化测试来捕捉。

## 何时激活

- AI 代理（如 Claude Code, Cursor, Codex）修改了 API 路由或后端逻辑。
- 发现并修复了一个缺陷 —— 需要防止该缺陷再次引入。
- 项目具有沙盒/模拟 (Sandbox/Mock) 模式，可用于无数据库依赖的测试。
- 代码更改后运行 `/bug-check` 或类似的评审命令。
- 存在多个代码路径（如沙盒 vs 生产、特性标志等）。

## 核心问题

当 AI 编写代码并随后评审自己的工作时，它会在两个步骤中携带相同的假设。这会产生一种可预测的失败模式：

```
AI 编写修复代码 → AI 评审修复代码 → AI 说“看起来正确” → 缺陷仍然存在
```

**真实案例**（在生产环境中观察到）：

```
修复 1：在 API 响应中添加了 notification_settings
  → 忘记将其添加到 SELECT 查询中
  → AI 进行了评审但未能发现（相同的盲区）

修复 2：将其添加到了 SELECT 查询中
  → 出现 TypeScript 构建错误（生成的类型中没有该列）
  → AI 评审了修复 1，但未捕捉到 SELECT 问题

修复 3：更改为 SELECT *
  → 修复了生产路径，但忘记了沙盒路径
  → AI 再次评审并再次遗漏（第 4 次发生）

修复 4：测试在第一次运行时立即捕捉到了问题：通过 (PASS)！
```

该模式：**沙盒/生产路径的不一致** 是 AI 引入的头号回归问题。

## 沙盒模式 API 测试

大多数具有“AI 友好”架构的项目都有沙盒/模拟模式。这是实现快速、无数据库 API 测试的关键。

### 配置 (Vitest + Next.js App Router)

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  test: {
    environment: "node",
    globals: true,
    include: ["__tests__/**/*.test.ts"],
    setupFiles: ["__tests__/setup.ts"],
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "."),
    },
  },
});
```

```typescript
// __tests__/setup.ts
// 强制开启沙盒模式 —— 无需数据库
process.env.SANDBOX_MODE = "true";
process.env.NEXT_PUBLIC_SUPABASE_URL = "";
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = "";
```

### Next.js API 路由测试辅助函数

```typescript
// __tests__/helpers.ts
import { NextRequest } from "next/server";

export function createTestRequest(
  url: string,
  options?: {
    method?: string;
    body?: Record<string, unknown>;
    headers?: Record<string, string>;
    sandboxUserId?: string;
  },
): NextRequest {
  const { method = "GET", body, headers = {}, sandboxUserId } = options || {};
  const fullUrl = url.startsWith("http") ? url : `http://localhost:3000${url}`;
  const reqHeaders: Record<string, string> = { ...headers };

  if (sandboxUserId) {
    reqHeaders["x-sandbox-user-id"] = sandboxUserId;
  }

  const init: { method: string; headers: Record<string, string>; body?: string } = {
    method,
    headers: reqHeaders,
  };

  if (body) {
    init.body = JSON.stringify(body);
    reqHeaders["content-type"] = "application/json";
  }

  return new NextRequest(fullUrl, init);
}

export async function parseResponse(response: Response) {
  const json = await response.json();
  return { status: response.status, json };
}
```

### 编写回归测试

核心原则：**为已发现的缺陷编写测试，而不是为正常工作的代码编写测试**。

```typescript
// __tests__/api/user/profile.test.ts
import { describe, it, expect } from "vitest";
import { createTestRequest, parseResponse } from "../../helpers";
import { GET, PATCH } from "@/app/api/user/profile/route";

// 定义契约 —— 响应中必须包含哪些字段
const REQUIRED_FIELDS = [
  "id",
  "email",
  "full_name",
  "phone",
  "role",
  "created_at",
  "avatar_url",
  "notification_settings",  // ← 在发现该字段缺失的缺陷后添加
];

describe("GET /api/user/profile", () => {
  it("返回所有必填字段", async () => {
    const req = createTestRequest("/api/user/profile");
    const res = await GET(req);
    const { status, json } = await parseResponse(res);

    expect(status).toBe(200);
    for (const field of REQUIRED_FIELDS) {
      expect(json.data).toHaveProperty(field);
    }
  });

  // 回归测试 —— AI 曾先后 4 次引入这个确切的缺陷
  it("notification_settings 不是 undefined (BUG-R1 回归测试)", async () => {
    const req = createTestRequest("/api/user/profile");
    const res = await GET(req);
    const { json } = await parseResponse(res);

    expect("notification_settings" in json.data).toBe(true);
    const ns = json.data.notification_settings;
    expect(ns === null || typeof ns === "object").toBe(true);
  });
});
```

### 测试沙盒/生产环境的一致性

最常见的 AI 回归问题：修复了生产路径但忘记了沙盒路径（或反之亦然）。

```typescript
// 测试沙盒响应是否符合预期契约
describe("GET /api/user/messages (会话列表)", () => {
  it("在沙盒模式下包含 partner_name", async () => {
    const req = createTestRequest("/api/user/messages", {
      sandboxUserId: "user-001",
    });
    const res = await GET(req);
    const { json } = await parseResponse(res);

    // 捕捉到了 partner_name 被添加到生产路径
    // 但未被添加到沙盒路径的缺陷
    if (json.data.length > 0) {
      for (const conv of json.data) {
        expect("partner_name" in conv).toBe(true);
      }
    }
  });
});
```

## 将测试集成到缺陷检查 (Bug-Check) 工作流中

### 自定义命令定义

```markdown
<!-- .claude/commands/bug-check.md -->
# 缺陷检查 (Bug Check)

## 第一步：自动化测试（强制执行，不可跳过）

在进行任何代码评审之前，先运行以下命令：

    npm run test       # Vitest 测试套件
    npm run build      # TypeScript 类型检查 + 构建

- 如果测试失败 → 将其作为最高优先级的缺陷进行报告。
- 如果构建失败 → 将类型错误作为最高优先级的缺陷进行报告。
- 只有在两者都通过的情况下，才进入第二步。

## 第二步：代码评审（AI 评审）

重点关注：
1. 沙盒 / 生产路径的一致性
2. API 响应结构是否匹配前端预期
3. SELECT 子句的完整性
4. 带有回滚机制的错误处理
5. 乐观更新 (Optimistic Update) 的竞态条件

## 第三步：针对修复的每个缺陷，提出回归测试方案
```

### 工作流示例

```
用户：“帮我检查一下缺陷” (或输入 /bug-check)
  │
  ├─ 第一步：运行 npm run test
  │   ├─ 失败 → 通过机械检查发现缺陷（无需 AI 判断）
  │   └─ 通过 → 继续
  │
  ├─ 第二步：运行 npm run build
  │   ├─ 失败 → 通过机械检查发现类型错误
  │   └─ 通过 → 继续
  │
  ├─ 第三步：AI 代码评审（时刻警惕已知的 AI 盲区）
  │   └─ 报告发现的问题
  │
  └─ 第四步：针对每个修复，编写回归测试
      └─ 下次执行缺陷检查时，若修复失效将被捕捉
```

## 常见的 AI 回归模式

### 模式 1：沙盒/生产路径不匹配

**频率**：最常见（在 4 分之 3 的回归案例中被观察到）

```typescript
// 失败：AI 仅在生产路径添加了字段
if (isSandboxMode()) {
  return { data: { id, email, name } };  // 缺失新字段
}
// 生产路径
return { data: { id, email, name, notification_settings } };

// 通过：两个路径必须返回相同的结构
if (isSandboxMode()) {
  return { data: { id, email, name, notification_settings: null } };
}
return { data: { id, email, name, notification_settings } };
```

**捕捉该问题的测试**：

```typescript
it("沙盒与生产环境返回相同的字段", async () => {
  // 在测试环境中，沙盒模式被强制开启
  const res = await GET(createTestRequest("/api/user/profile"));
  const { json } = await parseResponse(res);

  for (const field of REQUIRED_FIELDS) {
    expect(json.data).toHaveProperty(field);
  }
});
```

### 模式 2：SELECT 子句遗漏

**频率**：在使用 Supabase/Prisma 添加新列时很常见

```typescript
// 失败：新列被添加到响应中，但未添加到 SELECT 语句
const { data } = await supabase
  .from("users")
  .select("id, email, name")  // 此处缺失 notification_settings
  .single();

return { data: { ...data, notification_settings: data.notification_settings } };
// → notification_settings 始终为 undefined

// 通过：使用 SELECT * 或显式包含新列
const { data } = await supabase
  .from("users")
  .select("*")
  .single();
```

### 模式 3：错误状态泄漏

**频率**：中等 —— 常发生在为现有组件添加错误处理时

```typescript
// 失败：设置了错误状态但未清除旧数据
catch (err) {
  setError("加载失败");
  // reservations 仍然显示上一个标签页的数据！
}

// 通过：发生错误时清除相关状态
catch (err) {
  setReservations([]);  // 清除陈旧数据
  setError("加载失败");
}
```

### 模式 4：无适当回滚机制的乐观更新

```typescript
// 失败：操作失败时没有回滚
const handleRemove = async (id: string) => {
  setItems(prev => prev.filter(i => i.id !== id));
  await fetch(`/api/items/${id}`, { method: "DELETE" });
  // 如果 API 调用失败，项在 UI 上消失了，但仍然存在于数据库中
};

// 通过：捕捉上一个状态并在失败时回滚
const handleRemove = async (id: string) => {
  const prevItems = [...items];
  setItems(prev => prev.filter(i => i.id !== id));
  try {
    const res = await fetch(`/api/items/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error("API 错误");
  } catch {
    setItems(prevItems);  // 回滚
    alert("删除失败");
  }
};
```

## 策略：在发现缺陷的地方编写测试

不要追求 100% 的覆盖率。相反：

```
在 /api/user/profile 发现缺陷     → 为 profile API 编写测试
在 /api/user/messages 发现缺陷    → 为 messages API 编写测试
在 /api/user/favorites 发现缺陷   → 为 favorites API 编写测试
/api/user/notifications 没有缺陷  → （暂时）不编写测试
```

**为什么这在 AI 开发中有效**：

1. AI 倾向于反复犯**同一类错误**。
2. 缺陷往往聚集在复杂区域（认证、多路径逻辑、状态管理）。
3. 一旦编写了测试，那个确切的回归**将不再发生**。
4. 测试用例随着缺陷修复有机增长 —— 绝无无用功。

## 快速参考

| AI 回归模式 | 测试策略 | 优先级 |
|---|---|---|
| 沙盒/生产环境不匹配 | 断言沙盒模式下的响应结构一致 | 高 |
| SELECT 子句遗漏 | 断言响应中包含所有必填字段 | 高 |
| 错误状态泄漏 | 断言发生错误时状态已清理 | 中 |
| 缺失回滚机制 | 断言 API 失败时状态已恢复 | 中 |
| 类型转换掩盖 null 值 | 断言字段不为 undefined | 中 |

## 建议做法 (DO) / 禁止做法 (DON'T)

**建议做法 (DO)：**
- 发现缺陷后立即编写测试（如果可能，在修复之前编写）。
- 测试 API 的响应结构，而不是其内部实现。
- 将运行测试作为每次缺陷检查的第一步。
- 保持测试运行飞快（配合沙盒模式，总耗时应 < 1 秒）。
- 根据所防范的缺陷为测试命名（例如：“BUG-R1 回归测试”）。

**禁止做法 (DON'T)：**
- 为从未出过缺陷的代码编写测试。
- 相信 AI 的自我评审可以替代自动化测试。
- 因为“只是模拟数据”而跳过对沙盒路径的测试。
- 当单元测试足够时编写集成测试。
- 追求覆盖率百分比 —— 目标应是防止回归。
