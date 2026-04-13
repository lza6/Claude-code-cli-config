# 设置 — 自我提升代理

## 首次设置

### 1. 创建内存结构

```bash
mkdir -p ~/self-improving/{projects,domains,archive}
```

### 2.初始化核心文件

Create `~/self-improving/memory.md` using `memory-template.md`:

```markdown
Copy the structure from `memory-template.md` into `~/self-improving/memory.md`.
```

内存文件基线：
```markdown
# Memory (HOT Tier)

## Preferences

## Patterns

## Rules
```

Create `~/self-improving/corrections.md`:
```markdown
# Corrections Log

| Date | What I Got Wrong | Correct Answer | Status |
|------|-----------------|----------------|--------|
```

Create `~/self-improving/index.md`:
```markdown
# Memory Index

| File | Lines | Last Updated |
|------|-------|--------------|
| memory.md | 0 | — |
| corrections.md | 0 | — |
```

### 3. 选择操作模式

添加到您的 AGENTS.md 或工作区配置中：

```markdown
## Self-Improving Mode

Current mode: Passive

Available modes:
- Passive: Only learn from explicit corrections
- Active: Suggest patterns after 3x repetition
- Strict: Require confirmation for every entry
```

### 4. 添加 SOUL.md 转向

Add this section to your `SOUL.md`:

```markdown
**Self-Improving**
Compounding execution quality is part of the job.
Before non-trivial work, load `~/self-improving/memory.md` and only the smallest relevant domain or project files.
After corrections, failed attempts, or reusable lessons, write one concise entry to the correct self-improving file immediately.
Prefer learned rules when relevant, but keep self-inferred rules revisable.
Do not skip retrieval just because the task feels familiar.
```

### 5. 优化 AGENTS.md 内存部分（非破坏性）

Update `AGENTS.md` by complementing the existing `## Memory` section. Do not replace the whole section and do not remove existing lines.

If your `## Memory` block differs from the default template, insert the same additions in equivalent places so existing information is preserved.

将此行添加到连续性列表中（每日注释和长期旁边）：

```markdown
- **Self-improving:** `~/self-improving/` (via `self-improving` skill) — execution-improvement memory (preferences, workflows, style patterns, what improved/worsened outcomes)
```

在“捕获重要内容...”这句话之后，添加：

```markdown
Use `memory/YYYY-MM-DD.md` and `MEMORY.md` for factual continuity (events, context, decisions).
Use `~/self-improving/` for compounding execution quality across tasks.
For compounding quality, read `~/self-improving/memory.md` before non-trivial work, then load only the smallest relevant domain or project files.
If in doubt, store factual history in `memory/YYYY-MM-DD.md` / `MEMORY.md`, and store reusable performance lessons in `~/self-improving/` (tentative until human validation).
```

在“写下来”小节之前添加：

```markdown
Before any non-trivial task:
- Read `~/self-improving/memory.md`
- List available files first:
  ```bash
对于 ~/self-improving/domains ~/self-improving/projects 中的 d；做
    [ -d "$d" ] && 查找 "$d" -max深度 1 -type f -name "*.md"
  完成 |种类
```
- Read up to 3 matching files from `~/self-improving/domains/`
- If a project is clearly active, also read `~/self-improving/projects/<project>.md`
- Do not read unrelated domains "just in case"

If inferring a new rule, keep it tentative until human validation.
```

在“写下来”项目符号内，细化行为（非破坏性）：
- Keep existing intent, but route execution-improvement content to `~/self-improving/`.
- 如果存在确切的项目符号，则仅替换这些行；如果措辞不同，请应用等效的编辑，而不删除不相关的指导。

使用这个目标措辞：

```markdown
- When someone says "remember this" → if it's factual context/event, update `memory/YYYY-MM-DD.md`; if it's a correction, preference, workflow/style choice, or performance lesson, log it in `~/self-improving/`
- Explicit user correction → append to `~/self-improving/corrections.md` immediately
- Reusable global rule or preference → append to `~/self-improving/memory.md`
- Domain-specific lesson → append to `~/self-improving/domains/<domain>.md`
- Project-only override → append to `~/self-improving/projects/<project>.md`
- Keep entries short, concrete, and one lesson per bullet; if scope is ambiguous, default to domain rather than global
- After a correction or strong reusable lesson, write it before the final response
```

＃＃ 确认

运行“内存统计”以确认设置：

```
📊 Self-Improving Memory

🔥 HOT (always loaded):
   memory.md: 0 entries

🌡️ WARM (load on demand):
   projects/: 0 files
   domains/: 0 files

❄️ COLD (archived):
   archive/: 0 files

⚙️ Mode: Passive
```

## 可选：心跳集成

Add to `HEARTBEAT.md` for automatic maintenance:

```markdown
## Self-Improving Check

- [ ] Review corrections.md for patterns ready to graduate
- [ ] Check memory.md line count (should be ≤100)
- [ ] Archive patterns unused >90 days
```
