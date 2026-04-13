---
title: "设置适当的连接限制"
impact: "批判的"
impactDescription: "防止数据库崩溃和内存耗尽"
tags: "连接数、最大连接数、限制、稳定性"
---

## 设置适当的连接限制

连接过多会耗尽内存并降低性能。根据可用资源设置限制。

**不正确（无限或过多的连接）：**

```sql
-- Default max_connections = 100, but often increased blindly
show max_connections;  -- 500 (way too high for 4GB RAM)

-- Each connection uses 1-3MB RAM
-- 500 connections * 2MB = 1GB just for connections!
-- Out of memory errors under load
```

**正确（根据资源计算）：**

```sql
-- Formula: max_connections = (RAM in MB / 5MB per connection) - reserved
-- For 4GB RAM: (4096 / 5) - 10 = ~800 theoretical max
-- But practically, 100-200 is better for query performance

-- Recommended settings for 4GB RAM
alter system set max_connections = 100;

-- Also set work_mem appropriately
-- work_mem * max_connections should not exceed 25% of RAM
alter system set work_mem = '8MB';  -- 8MB * 100 = 800MB max
```

监控连接使用情况：

```sql
select count(*), state from pg_stat_activity group by state;
```

参考：[数据库连接](https://supabase.com/docs/guides/platform/performance#connection-management)
