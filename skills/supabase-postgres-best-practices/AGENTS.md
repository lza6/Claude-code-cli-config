# Supabase Postgres 最佳实践

＃＃ 结构

```
supabase-postgres-best-practices/
  SKILL.md       # Main skill file - read this first
  AGENTS.md      # This navigation guide
  CLAUDE.md      # Symlink to AGENTS.md
  references/    # Detailed reference files
```

＃＃ 用法

1.主要技能说明请阅读`SKILL.md`
2. 浏览“references/”以获取有关特定主题的详细文档
3. 参考文件按需加载 - 只读取您需要的内容

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

＃＃ 参考

- https://www.postgresql.org/docs/current/
- https://supabase.com/docs
- https://wiki.postgresql.org/wiki/Performance_Optimization
- https://supabase.com/docs/guides/database/overview
- https://supabase.com/docs/guides/auth/row-level-security
