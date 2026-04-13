---
title: "配置空闲连接超时"
impact: "高的"
impactDescription: "从空闲客户端回收 30-50% 的连接时隙"
tags: "连接、超时、空闲、资源管理"
---

## 配置空闲连接超时

空闲连接浪费资源。配置超时以自动回收它们。

**不正确（无限期保持连接）：**

```sql
-- No timeout configured
show idle_in_transaction_session_timeout;  -- 0 (disabled)

-- Connections stay open forever, even when idle
select pid, state, state_change, query
from pg_stat_activity
where state = 'idle in transaction';
-- Shows transactions idle for hours, holding locks
```

**正确（自动清理空闲连接）：**

```sql
-- Terminate connections idle in transaction after 30 seconds
alter system set idle_in_transaction_session_timeout = '30s';

-- Terminate completely idle connections after 10 minutes
alter system set idle_session_timeout = '10min';

-- Reload configuration
select pg_reload_conf();
```

对于池化连接，请在池化器级别进行配置：

```ini
# pgbouncer.ini
server_idle_timeout = 60
client_idle_timeout = 300
```

参考：[连接超时](https://www.postgresql.org/docs/current/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT)
