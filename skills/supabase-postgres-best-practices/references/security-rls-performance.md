---
title: "优化 RLS 策略以提高性能"
impact: "高的"
impactDescription: 5-10x faster RLS queries with proper patterns
tags: "rls、性能、安全、优化"
---

## 优化 RLS 策略以提高性能

编写不当的 RLS 策略可能会导致严重的性能问题。有策略地使用子查询和索引。

**不正确（为每一行调用函数）：**

```sql
create policy orders_policy on orders
  using (auth.uid() = user_id);  -- auth.uid() called per row!

-- With 1M rows, auth.uid() is called 1M times
```

**正确（在 SELECT 中包装函数）：**

```sql
create policy orders_policy on orders
  using ((select auth.uid()) = user_id);  -- Called once, cached

-- 100x+ faster on large tables
```

使用安全定义器函数进行复杂检查：

```sql
-- Create helper function (runs as definer, bypasses RLS)
create or replace function is_team_member(team_id bigint)
returns boolean
language sql
security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.team_members
    where team_id = $1 and user_id = (select auth.uid())
  );
$$;

-- Use in policy (indexed lookup, not per-row check)
create policy team_orders_policy on orders
  using ((select is_team_member(team_id)));
```

始终在 RLS 策略中使用的列上添加索引：

```sql
create index orders_user_id_idx on orders (user_id);
```

参考：[RLS性能](https://supabase.com/docs/guides/database/postgres/row-level-security#rls-performance-recommendations)
