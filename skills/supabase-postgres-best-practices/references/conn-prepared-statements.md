---
title: "正确使用准备好的语句和池化"
impact: "高的"
impactDescription: "避免池环境中准备好的语句冲突"
tags: "准备好的语句、连接池、事务模式"
---

## 正确使用准备好的语句和池化

准备好的语句与各个数据库连接相关联。在事务模式池中，连接是共享的，会导致冲突。

**不正确（带有事务池的命名准备语句）：**

```sql
-- Named prepared statement
prepare get_user as select * from users where id = $1;

-- In transaction mode pooling, next request may get different connection
execute get_user(123);
-- ERROR: prepared statement "get_user" does not exist
```

**正确（使用未命名语句或会话模式）：**

```sql
-- Option 1: Use unnamed prepared statements (most ORMs do this automatically)
-- The query is prepared and executed in a single protocol message

-- Option 2: Deallocate after use in transaction mode
prepare get_user as select * from users where id = $1;
execute get_user(123);
deallocate get_user;

-- Option 3: Use session mode pooling (port 5432 vs 6543)
-- Connection is held for entire session, prepared statements persist
```

检查您的驱动程序设置：

```sql
-- Many drivers use prepared statements by default
-- Node.js pg: { prepare: false } to disable
-- JDBC: prepareThreshold=0 to disable
```

参考：[带池的准备语句](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pool-modes)
