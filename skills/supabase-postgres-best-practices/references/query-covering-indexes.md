---
title: "使用覆盖索引来避免表查找"
impact: "中高"
impactDescription: 2-5x faster queries by eliminating heap fetches
tags: "索引、覆盖索引、包含、仅索引扫描"
---

## 使用覆盖索引来避免表查找

覆盖索引包括查询所需的所有列，从而实现完全跳过表的仅索引扫描。

**不正确（索引扫描+堆获取）：**

```sql
create index users_email_idx on users (email);

-- Must fetch name and created_at from table heap
select email, name, created_at from users where email = 'user@example.com';
```

**正确（使用 INCLUDE 进行仅索引扫描）：**

```sql
-- Include non-searchable columns in the index
create index users_email_idx on users (email) include (name, created_at);

-- All columns served from index, no table access needed
select email, name, created_at from users where email = 'user@example.com';
```

对您选择但不过滤的列使用 INCLUDE：

```sql
-- Searching by status, but also need customer_id and total
create index orders_status_idx on orders (status) include (customer_id, total);

select status, customer_id, total from orders where status = 'shipped';
```

参考：[仅索引扫描](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)
