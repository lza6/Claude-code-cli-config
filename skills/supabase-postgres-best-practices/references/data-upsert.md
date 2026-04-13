---
title: "使用 UPSERT 进行插入或更新操作"
impact: "中等的"
impactDescription: "原子操作，消除竞争条件"
tags: "upsert、冲突时、插入、更新"
---

## 使用 UPSERT 进行插入或更新操作

使用单独的 SELECT-then-INSERT/UPDATE 会产生竞争条件。使用 INSERT ... ON CONFLICT 进行原子更新插入。

**不正确（检查然后插入竞争条件）：**

```sql
-- Race condition: two requests check simultaneously
select * from settings where user_id = 123 and key = 'theme';
-- Both find nothing

-- Both try to insert
insert into settings (user_id, key, value) values (123, 'theme', 'dark');
-- One succeeds, one fails with duplicate key error!
```

**正确（原子 UPSERT）：**

```sql
-- Single atomic operation
insert into settings (user_id, key, value)
values (123, 'theme', 'dark')
on conflict (user_id, key)
do update set value = excluded.value, updated_at = now();

-- Returns the inserted/updated row
insert into settings (user_id, key, value)
values (123, 'theme', 'dark')
on conflict (user_id, key)
do update set value = excluded.value
returning *;
```

插入或忽略模式：

```sql
-- Insert only if not exists (no update)
insert into page_views (page_id, user_id)
values (1, 123)
on conflict (page_id, user_id) do nothing;
```

参考：[冲突时插入](https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT)
