---
title: "在迁移中安全地添加约束"
impact: "高的"
impactDescription: "防止迁移失败并启用幂等架构更改"
tags: "约束、迁移、模式、更改表"
---

## 在迁移中安全地添加约束

PostgreSQL 不支持“ADD CONSTRAINT IF NOT EXISTS”。使用此语法的迁移将会失败。

**不正确（导致语法错误）：**

```sql
-- ERROR: syntax error at or near "not" (SQLSTATE 42601)
alter table public.profiles
add constraint if not exists profiles_birthchart_id_unique unique (birthchart_id);
```

**正确（幂等约束创建）：**

```sql
-- Use DO block to check before adding
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'profiles_birthchart_id_unique'
    and conrelid = 'public.profiles'::regclass
  ) then
    alter table public.profiles
    add constraint profiles_birthchart_id_unique unique (birthchart_id);
  end if;
end $$;
```

对于所有约束类型：

```sql
-- Check constraints
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'check_age_positive'
  ) then
    alter table users add constraint check_age_positive check (age > 0);
  end if;
end $$;

-- Foreign keys
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'profiles_birthchart_id_fkey'
  ) then
    alter table profiles
    add constraint profiles_birthchart_id_fkey
    foreign key (birthchart_id) references birthcharts(id);
  end if;
end $$;
```

检查约束是否存在：

```sql
-- Query to check constraint existence
select conname, contype, pg_get_constraintdef(oid)
from pg_constraint
where conrelid = 'public.profiles'::regclass;

-- contype values:
-- 'p' = PRIMARY KEY
-- 'f' = FOREIGN KEY
-- 'u' = UNIQUE
-- 'c' = CHECK
```

参考：[约束](https://www.postgresql.org/docs/current/ddl-constraints.html)
