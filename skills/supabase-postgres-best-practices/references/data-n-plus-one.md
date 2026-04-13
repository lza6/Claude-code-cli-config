---
title: "通过批量加载消除 N+1 查询"
impact: "中高"
impactDescription: 10-100x fewer database round trips
tags: "n 加一、批处理、性能、查询"
---

## 通过批量加载消除 N+1 查询

N+1 查询在循环中对每个项目执行一个查询。使用数组或 JOIN 将它们批处理为单个查询。

**不正确（N+1 查询）：**

```sql
-- First query: get all users
select id from users where active = true;  -- Returns 100 IDs

-- Then N queries, one per user
select * from orders where user_id = 1;
select * from orders where user_id = 2;
select * from orders where user_id = 3;
-- ... 97 more queries!

-- Total: 101 round trips to database
```

**正确（单批查询）：**

```sql
-- Collect IDs and query once with ANY
select * from orders where user_id = any(array[1, 2, 3, ...]);

-- Or use JOIN instead of loop
select u.id, u.name, o.*
from users u
left join orders o on o.user_id = u.id
where u.active = true;

-- Total: 1 round trip
```

应用模式：

```sql
-- Instead of looping in application code:
-- for user in users: db.query("SELECT * FROM orders WHERE user_id = $1", user.id)

-- Pass array parameter:
select * from orders where user_id = any($1::bigint[]);
-- Application passes: [1, 2, 3, 4, 5, ...]
```

参考：【N+1查询问题】(https://supabase.com/docs/guides/database/query-optimization)
