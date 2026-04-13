# 示例：使用实际文件进行规划

## 示例 1：研究任务

**用户请求：**“研究晨练的好处并写一份总结”

### 循环 1：创建计划
```bash
Write task_plan.md
```

```markdown
# Task Plan: Morning Exercise Benefits Research

## Goal
Create a research summary on the benefits of morning exercise.

## Phases
- [ ] Phase 1: Create this plan ✓
- [ ] Phase 2: Search and gather sources
- [ ] Phase 3: Synthesize findings
- [ ] Phase 4: Deliver summary

## Key Questions
1. What are the physical health benefits?
2. What are the mental health benefits?
3. What scientific studies support this?

## Status
**Currently in Phase 1** - Creating plan
```

### 循环 2：研究
```bash
Read task_plan.md           # Refresh goals
WebSearch "morning exercise benefits"
Write notes.md              # Store findings
Edit task_plan.md           # Mark Phase 2 complete
```

### 循环 3：综合
```bash
Read task_plan.md           # Refresh goals
Read notes.md               # Get findings
Write morning_exercise_summary.md
Edit task_plan.md           # Mark Phase 3 complete
```

### 循环 4：交付
```bash
Read task_plan.md           # Verify complete
Deliver morning_exercise_summary.md
```

---

## 示例 2：错误修复任务

**用户请求：**“修复认证模块中的登录错误”

###任务计划.md
```markdown
# Task Plan: Fix Login Bug

## Goal
Identify and fix the bug preventing successful login.

## Phases
- [x] Phase 1: Understand the bug report ✓
- [x] Phase 2: Locate relevant code ✓
- [ ] Phase 3: Identify root cause (CURRENT)
- [ ] Phase 4: Implement fix
- [ ] Phase 5: Test and verify

## Key Questions
1. What error message appears?
2. Which file handles authentication?
3. What changed recently?

## Decisions Made
- Auth handler is in src/auth/login.ts
- Error occurs in validateToken() function

## Errors Encountered
- [Initial] TypeError: Cannot read property 'token' of undefined
  → Root cause: user object not awaited properly

## Status
**Currently in Phase 3** - Found root cause, preparing fix
```

---

## 示例 3：功能开发

**用户请求：**“在设置页面添加暗模式切换”

### 3 文件模式的实际应用

**任务计划.md：**
```markdown
# Task Plan: Dark Mode Toggle

## Goal
Add functional dark mode toggle to settings.

## Phases
- [x] Phase 1: Research existing theme system ✓
- [x] Phase 2: Design implementation approach ✓
- [ ] Phase 3: Implement toggle component (CURRENT)
- [ ] Phase 4: Add theme switching logic
- [ ] Phase 5: Test and polish

## Decisions Made
- Using CSS custom properties for theme
- Storing preference in localStorage
- Toggle component in SettingsPage.tsx

## Status
**Currently in Phase 3** - Building toggle component
```

**注释.md：**
```markdown
# Notes: Dark Mode Implementation

## Existing Theme System
- Located in: src/styles/theme.ts
- Uses: CSS custom properties
- Current themes: light only

## Files to Modify
1. src/styles/theme.ts - Add dark theme colors
2. src/components/SettingsPage.tsx - Add toggle
3. src/hooks/useTheme.ts - Create new hook
4. src/App.tsx - Wrap with ThemeProvider

## Color Decisions
- Dark background: #1a1a2e
- Dark surface: #16213e
- Dark text: #eaeaea
```

**dark_mode_implementation.md：**（可交付）
```markdown
# Dark Mode Implementation

## Changes Made

### 1. Added dark theme colors
File: src/styles/theme.ts
...

### 2. Created useTheme hook
File: src/hooks/useTheme.ts
...
```

---

## 示例 4：错误恢复模式

当出现问题时，不要隐藏它：

###之前（错误）
```
Action: Read config.json
Error: File not found
Action: Read config.json  # Silent retry
Action: Read config.json  # Another retry
```

### 之后（正确）
```
Action: Read config.json
Error: File not found

# Update task_plan.md:
## Errors Encountered
- config.json not found → Will create default config

Action: Write config.json (default config)
Action: Read config.json
Success!
```

---

## 先读后决定模式

**在做出重大决定之前，请务必阅读您的计划：**

```
[Many tool calls have happened...]
[Context is getting long...]
[Original goal might be forgotten...]

→ Read task_plan.md          # This brings goals back into attention!
→ Now make the decision       # Goals are fresh in context
```

这就是为什么 Manus 可以处理约 50 个工具调用而不会丢失跟踪。计划文件充当“目标刷新”机制。
