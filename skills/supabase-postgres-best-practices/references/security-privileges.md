---
title: "应用最小特权原则"
impact: "中等的"
impactDescription: "减少攻击面，更好的审计跟踪"
tags: "特权、安全、角色、权限"
---

## 应用最小权限原则

仅授予所需的最低权限。切勿使用超级用户进行应用程序查询。

**不正确（过于广泛的权限）：**

```sql
-- Application uses superuser connection
-- Or grants ALL to application role
grant all privileges on all tables in schema public to app_user;
grant all privileges on all sequences in schema public to app_user;

-- Any SQL injection becomes catastrophic
-- drop table users; cascades to everything
```

**正确（最低限度，特定拨款）：**

```sql
-- Create role with no default privileges
create role app_readonly nologin;

-- Grant only SELECT on specific tables
grant usage on schema public to app_readonly;
grant select on public.products, public.categories to app_readonly;

-- Create role for writes with limited scope
create role app_writer nologin;
grant usage on schema public to app_writer;
grant select, insert, update on public.orders to app_writer;
grant usage on sequence orders_id_seq to app_writer;
-- No DELETE permission

-- Login role inherits from these
create role app_user login password 'xxx';
grant app_writer to app_user;
```

撤销公共默认设置：

```sql
-- Revoke default public access
revoke all on schema public from public;
revoke all on all tables in schema public from public;
```

参考：[角色和权限](https://supabase.com/blog/postgres-roles-and-privileges)
