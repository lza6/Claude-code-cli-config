# 热内存 — 模板

> This file is created in `~/self-improving/memory.md` when you first use the skill.
> 保持≤100行。最常用的模式都在这里。

## 示例条目

```markdown
## Preferences
- Code style: Prefer explicit over implicit
- Communication: Direct, no fluff
- Time zone: Europe/Madrid

## Patterns (promoted from corrections)
- Always use TypeScript strict mode
- Prefer pnpm over npm
- Format: ISO 8601 for dates

## Project defaults
- Tests: Jest with coverage >80%
- Commits: Conventional commits format
```

＃＃ 用法

代理人将：
1. 在每个会话上加载此文件
2. 当模式在 7 天内使用 3 次时添加条目
3. 30天后将未使用的条目降级为WARM
4. 切勿超过 100 行（自动压缩）
