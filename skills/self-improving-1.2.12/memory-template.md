# 内存模板

Copy this structure to `~/self-improving/memory.md` on first use.

```markdown
# Self-Improving Memory

## Confirmed Preferences
<!-- Patterns confirmed by user, never decay -->

## Active Patterns
<!-- Patterns observed 3+ times, subject to decay -->

## Recent (last 7 days)
<!-- New corrections pending confirmation -->
```

## 初始目录结构

首次激活时创建：

```bash
mkdir -p ~/self-improving/{projects,domains,archive}
touch ~/self-improving/{memory.md,index.md,corrections.md}
```

## 索引模板

For `~/self-improving/index.md`:

```markdown
# Memory Index

## HOT
- memory.md: 0 lines

## WARM
- (no namespaces yet)

## COLD
- (no archives yet)

Last compaction: never
```

## 更正日志模板

For `~/self-improving/corrections.md`:

```markdown
# Corrections Log

<!-- Format:
## YYYY-MM-DD
- [HH:MM] Changed X → Y
  Type: format|technical|communication|project
  Context: where correction happened
  Confirmed: pending (N/3) | yes | no
-->
```
