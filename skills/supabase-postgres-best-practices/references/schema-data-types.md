---
title: "选择适当的数据类型"
impact: "高的"
impactDescription: 50% storage reduction, faster comparisons
tags: "数据类型、模式、存储、性能"
---

## 选择适当的数据类型

使用正确的数据类型可以减少存储、提高查询性能并防止错误。

**不正确（错误的数据类型）：**

```sql
create table users (
  id int,                    -- Will overflow at 2.1 billion
  email varchar(255),        -- Unnecessary length limit
  created_at timestamp,      -- Missing timezone info
  is_active varchar(5),      -- String for boolean
  price varchar(20)          -- String for numeric
);
```

**正确（适当的数据类型）：**

```sql
create table users (
  id bigint generated always as identity primary key,  -- 9 quintillion max
  email text,                     -- No artificial limit, same performance as varchar
  created_at timestamptz,         -- Always store timezone-aware timestamps
  is_active boolean default true, -- 1 byte vs variable string length
  price numeric(10,2)             -- Exact decimal arithmetic
);
```

主要指导方针：

```sql
-- IDs: use bigint, not int (future-proofing)
-- Strings: use text, not varchar(n) unless constraint needed
-- Time: use timestamptz, not timestamp
-- Money: use numeric, not float (precision matters)
-- Enums: use text with check constraint or create enum type
```

参考：[数据类型](https://www.postgresql.org/docs/current/datatype.html)
