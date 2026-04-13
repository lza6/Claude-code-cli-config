# Supabase Postgres 最佳实践 - 贡献者指南

该技能包含针对以下内容进行优化的 Postgres 性能优化参考
人工智能代理人和法学硕士。它遵循[代理技能开放标准](https://agentskills.io/)。

## 快速入门

```bash
# From repository root
npm install

# Validate existing references
npm run validate

# Build AGENTS.md
npm run build
```

## 创建新参考

1. **根据类别选择部分前缀**：
   - `query-` 查询性能（关键）
   - `conn-` 连接管理（关键）
   - `安全-` 安全和 RLS（关键）
   - `schema-` 架构设计（高）
   - `lock-` 并发和锁定（中-高）
   - `data-` 数据访问模式（中）
   - `monitor-` 监控和诊断（低-中）
   - `高级-`高级功能（低）

2. **复制模板**：
   ```bash
   cp references/_template.md references/query-your-reference-name.md
   ```

3. **按照模板结构填写内容**

4. **验证和构建**：
   ```bash
   npm run validate
   npm run build
   ```

5. **查看**生成的`AGENTS.md`

## 技能结构

```
skills/supabase-postgres-best-practices/
├── SKILL.md           # Agent-facing skill manifest (Agent Skills spec)
├── AGENTS.md          # [GENERATED] Compiled references document
├── README.md          # This file
└── references/
    ├── _template.md      # Reference template
    ├── _sections.md      # Section definitions
    ├── _contributing.md  # Writing guidelines
    └── *.md              # Individual references

packages/skills-build/
├── src/               # Generic build system source
└── package.json       # NPM scripts
```

## 参考文件结构

有关完整模板，请参阅“references/_template.md”。关键要素：

````markdown
---
title: Clear, Action-Oriented Title
impact: CRITICAL|HIGH|MEDIUM-HIGH|MEDIUM|LOW-MEDIUM|LOW
impactDescription: Quantified benefit (e.g., "10-100x faster")
tags: relevant, keywords
---

## [Title]

[1-2 sentence explanation]

**Incorrect (description):**

```sql
-- 评论解释哪里出了问题
[错误的 SQL 示例]
```
````

**正确（描述）：**

```sql
-- Comment explaining why this is better
[Good SQL example]
```

```
## Writing Guidelines

See `references/_contributing.md` for detailed guidelines. Key principles:

1. **Show concrete transformations** - "Change X to Y", not abstract advice
2. **Error-first structure** - Show the problem before the solution
3. **Quantify impact** - Include specific metrics (10x faster, 50% smaller)
4. **Self-contained examples** - Complete, runnable SQL
5. **Semantic naming** - Use meaningful names (users, email), not (table1, col1)

## Impact Levels

| Level | Improvement | Examples |
|-------|-------------|----------|
| CRITICAL | 10-100x | Missing indexes, connection exhaustion |
| HIGH | 5-20x | Wrong index types, poor partitioning |
| MEDIUM-HIGH | 2-5x | N+1 queries, RLS optimization |
| MEDIUM | 1.5-3x | Redundant indexes, stale statistics |
| LOW-MEDIUM | 1.2-2x | VACUUM tuning, config tweaks |
| LOW | Incremental | Advanced patterns, edge cases |
```
