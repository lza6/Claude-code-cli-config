---
name: supabase-postgres-best-practices
description: "Supabase 的 Postgres 性能优化和最佳实践。在编写、审查或优化 Postgres 查询、模式设计或数据库配置时使用此技能。"
license: "麻省理工学院"
metadata:
  author: supabase
  version: "1.1.0"
  organization: Supabase
  date: January 2026
  abstract: Comprehensive Postgres performance optimization guide for developers using Supabase and Postgres. Contains performance rules across 8 categories, prioritized by impact from critical (query performance, connection management) to incremental (advanced features). Each rule includes detailed explanations, incorrect vs. correct SQL examples, query plan analysis, and specific performance metrics to guide automated optimization and code generation.
---

# Supabase Postgres 最佳实践

Postgres 综合性能优化指南，由 Supabase 维护。包含跨 8 个类别的规则，按影响进行优先级排序，以指导自动查询优化和架构设计。

## 何时申请

在以下情况下请参考这些指南：
- 编写 SQL 查询或设计模式
- 实施索引或查询优化
- 审查数据库性能问题
- 配置连接池或扩展
- 针对 Postgres 特定功能进行优化
- 使用行级安全性 (RLS)

## 按优先级规则类别

|优先|类别 |影响 |前缀|
|----------|----------|--------|--------|
| 1 |查询性能 |关键 | `查询-` |
| 2 |连接管理|关键 | `conn-` |
| 3 |安全与 RLS |关键 | `安全-` |
| 4 |架构设计|高| `模式-` |
| 5 |并发与锁定 |中高| `锁-` |
| 6 |数据访问模式|中 | `数据-` |
| 7 |监控与诊断|低-中| `监视器-` |
| 8 |高级功能 |低| `高级-` |

## 如何使用

阅读各个规则文件以获取详细说明和 SQL 示例：

```
references/query-missing-indexes.md
references/schema-partial-indexes.md
references/_sections.md
```

每个规则文件包含：
- 简要解释为什么它很重要
- 不正确的 SQL 示例及解释
- 带有解释的正确 SQL 示例
- 可选的 EXPLAIN 输出或指标
- 其他上下文和参考资料
- Supabase 特定注释（如适用）

## 参考

- https://www.postgresql.org/docs/current/
- https://supabase.com/docs
- https://wiki.postgresql.org/wiki/Performance_Optimization
- https://supabase.com/docs/guides/database/overview
- https://supabase.com/docs/guides/auth/row-level-security
