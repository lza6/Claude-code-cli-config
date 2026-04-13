---
title: "批量数据的批量 INSERT 语句"
impact: "中等的"
impactDescription: 10-50x faster bulk inserts
tags: "批处理、插入、批量、性能、复制"
---

## 大容量数据的批量 INSERT 语句

单个 INSERT 语句的开销很高。在单个语句中批量处理多行或使用 COPY。

**不正确（个别插入）：**

```sql
-- Each insert is a separate transaction and round trip
insert into events (user_id, action) values (1, 'click');
insert into events (user_id, action) values (1, 'view');
insert into events (user_id, action) values (2, 'click');
-- ... 1000 more individual inserts

-- 1000 inserts = 1000 round trips = slow
```

**正确（批量插入）：**

```sql
-- Multiple rows in single statement
insert into events (user_id, action) values
  (1, 'click'),
  (1, 'view'),
  (2, 'click'),
  -- ... up to ~1000 rows per batch
  (999, 'view');

-- One round trip for 1000 rows
```

对于大量导入，请使用 COPY：

```sql
-- COPY is fastest for bulk loading
copy events (user_id, action, created_at)
from '/path/to/data.csv'
with (format csv, header true);

-- Or from stdin in application
copy events (user_id, action) from stdin with (format csv);
1,click
1,view
2,click
\.
```

参考：[复制](https://www.postgresql.org/docs/current/sql-copy.html)
