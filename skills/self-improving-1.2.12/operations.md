# 内存操作

## 用户命令

|命令 |行动|
|---------|--------|
| “你对X了解多少？” |搜索所有层，返回与源匹配的内容 |
| “展示我的记忆力” |显示内存.md 内容 |
| “显示[项目]模式”|加载并显示特定命名空间 |
| “忘记X”|从所有层中删除，确认删除 |
| “忘记一切”|具有导出选项的完全擦除 |
| “最近有什么变化吗？” |显示最近 20 条更正 |
| “导出内存”|生成可下载的存档 |
| “内存状态”|显示层大小、最后压实、健康状况 |

## 自动操作

### 会话开始时
1.加载内存.md（HOT层）
2.检查index.md中的上下文提示
3. 如果检测到项目→预加载相关命名空间

### 收到更正
```
1. Parse correction type (preference, pattern, override)
2. Check if duplicate (exists in any tier)
3. If new:
   - Add to corrections.md with timestamp
   - Increment correction counter
4. If duplicate:
   - Bump counter, update timestamp
   - If counter >= 3: ask to confirm as rule
5. Determine namespace (global, domain, project)
6. Write to appropriate file
7. Update index.md line counts
```

### 关于模式匹配
应用学习模式时：
```
1. Find pattern source (file:line)
2. Apply pattern
3. Cite source: "Using X (from memory.md:15)"
4. Log usage for decay tracking
```

### 每周维护（Cron）
```
1. Scan all files for decay candidates
2. Move unused >30 days to WARM
3. Archive unused >90 days to COLD
4. Run compaction if any file >limit
5. Update index.md
6. Generate weekly digest (optional)
```

## 文件格式

###内存.md（热门）
```markdown
# Self-Improving Memory

## Confirmed Preferences
- format: bullet points over prose (confirmed 2026-01)
- tone: direct, no hedging (confirmed 2026-01)

## Active Patterns
- "looks good" = approval to proceed (used 15x)
- single emoji = acknowledged (used 8x)

## Recent (last 7 days)
- prefer SQLite for MVPs (corrected 02-14)
```

###更正.md
```markdown
# Corrections Log

## 2026-02-15
- [14:32] Changed verbose explanation → bullet summary
  Type: communication
  Context: Telegram response
  Confirmed: pending (1/3)

## 2026-02-14
- [09:15] Use SQLite not Postgres for MVP
  Type: technical
  Context: database discussion
  Confirmed: yes (said "always")
```

### 项目/{名称}.md
```markdown
# Project: my-app

Inherits: global, domains/code

## Patterns
- Use Tailwind (project standard)
- No Prettier (eslint only)
- Deploy via GitLab CI

## Overrides
- semicolons: yes (overrides global no-semi)

## History
- Created: 2026-01-15
- Last active: 2026-02-15
- Corrections: 12
```

## 边缘情况处理

### 检测到矛盾
```
Pattern A: "Use tabs" (global, confirmed)
Pattern B: "Use spaces" (project, corrected today)

Resolution:
1. Project overrides global → use spaces for this project
2. Log conflict in corrections.md
3. Ask: "Should spaces apply only to this project or everywhere?"
```

### 用户改变主意
```
Old: "Always use formal tone"
New: "Actually, casual is fine"

Action:
1. Archive old pattern with timestamp
2. Add new pattern as tentative
3. Keep archived for reference ("You previously preferred formal")
```

### 上下文歧义
```
User says: "Remember I like X"

But which namespace?
1. Check current context (project? domain?)
2. If unclear, ask: "Should this apply globally or just here?"
3. Default to most specific active context
```
