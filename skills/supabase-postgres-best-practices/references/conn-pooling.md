---
title: "对所有应用程序使用连接池"
impact: "批判的"
impactDescription: "处理 10-100 倍的并发用户数"
tags: "连接池、pgbouncer、性能、可扩展性"
---

## 对所有应用程序使用连接池

Postgres 连接很昂贵（每个 1-3MB RAM）。如果没有池化，应用程序会在负载下耗尽连接。

**不正确（每个请求的新连接）：**

```sql
-- Each request creates a new connection
-- Application code: db.connect() per request
-- Result: 500 concurrent users = 500 connections = crashed database

-- Check current connections
select count(*) from pg_stat_activity;  -- 487 connections!
```

**正确（连接池）：**

```sql
-- Use a pooler like PgBouncer between app and database
-- Application connects to pooler, pooler reuses a small pool to Postgres

-- Configure pool_size based on: (CPU cores * 2) + spindle_count
-- Example for 4 cores: pool_size = 10

-- Result: 500 concurrent users share 10 actual connections
select count(*) from pg_stat_activity;  -- 10 connections
```

池模式：

- **交易模式**：每次交易后返回连接（最适合大多数应用程序）
- **会话模式**：整个会话保持连接（准备好的语句、临时表需要）

参考：[连接池](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)
