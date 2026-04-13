---
title: "为多租户数据启用行级安全性"
impact: "批判的"
impactDescription: "数据库强制租户隔离，防止数据泄露"
tags: "rls、行级安全性、多租户、安全性"
---

## 为多租户数据启用行级安全性

行级安全性 (RLS) 在数据库级别强制执行数据访问，确保用户只能看到自己的数据。

**不正确（仅限应用程序级过滤）：**

```sql
-- Relying only on application to filter
select * from orders where user_id = $current_user_id;

-- Bug or bypass means all data is exposed!
select * from orders;  -- Returns ALL orders
```

**正确（数据库强制 RLS）：**

```sql
-- Enable RLS on the table
alter table orders enable row level security;

-- Create policy for users to see only their orders
create policy orders_user_policy on orders
  for all
  using (user_id = current_setting('app.current_user_id')::bigint);

-- Force RLS even for table owners
alter table orders force row level security;

-- Set user context and query
set app.current_user_id = '123';
select * from orders;  -- Only returns orders for user 123
```

经过身份验证的角色的策略：

```sql
create policy orders_user_policy on orders
  for all
  to authenticated
  using (user_id = auth.uid());
```

参考：[行级安全](https://supabase.com/docs/guides/database/postgres/row-level-security)
