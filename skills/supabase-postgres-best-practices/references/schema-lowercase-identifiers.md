---
title: "使用小写标识符以实现兼容性"
impact: "中等的"
impactDescription: "使用工具、ORM 和 AI 助手避免区分大小写的错误"
tags: "命名、标识符、区分大小写、模式、约定"
---

## 使用小写标识符以实现兼容性

PostgreSQL 将未加引号的标识符折叠为小写。带引号的混合大小写标识符永远需要引号，并会导致工具、ORM 和 AI 助手可能无法识别它们的问题。

**不正确（混合大小写标识符）：**

```sql
-- Quoted identifiers preserve case but require quotes everywhere
CREATE TABLE "Users" (
  "userId" bigint PRIMARY KEY,
  "firstName" text,
  "lastName" text
);

-- Must always quote or queries fail
SELECT "firstName" FROM "Users" WHERE "userId" = 1;

-- This fails - Users becomes users without quotes
SELECT firstName FROM Users;
-- ERROR: relation "users" does not exist
```

**正确（小写snake_case）：**

```sql
-- Unquoted lowercase identifiers are portable and tool-friendly
CREATE TABLE users (
  user_id bigint PRIMARY KEY,
  first_name text,
  last_name text
);

-- Works without quotes, recognized by all tools
SELECT first_name FROM users WHERE user_id = 1;
```

混合大小写标识符的常见来源：

```sql
-- ORMs often generate quoted camelCase - configure them to use snake_case
-- Migrations from other databases may preserve original casing
-- Some GUI tools quote identifiers by default - disable this

-- If stuck with mixed-case, create views as a compatibility layer
CREATE VIEW users AS SELECT "userId" AS user_id, "firstName" AS first_name FROM "Users";
```

参考：[标识符和关键词](https://www.postgresql.org/docs/current/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS)
