# 缩放模式

## 音量阈值

|规模|条目 |战略|
|--------|---------|----------|
|小| <100 |单一内存.md，无命名空间 |
|中等| 100-500 |分成域/，基本索引 |
|大| 500-2000 |完整的命名空间层次结构，积极的压缩 |
|大规模| >2000 |每年存档，仅摘要 热门层 |

## 何时拆分

在以下情况下创建新的命名空间文件：
- 单个文件超过200行
- 主题有 10 多个不同的更正
- 用户明确分隔上下文（“工作...”，“在这个项目中...”）

## 压缩规则

### 合并相似的更正
```
BEFORE (3 entries):
- [02-01] Use tabs not spaces
- [02-03] Indent with tabs
- [02-05] Tab indentation please

AFTER (1 entry):
- Indentation: tabs (confirmed 3x, 02-01 to 02-05)
```

### 总结详细模式
```
BEFORE:
- When writing emails to Marcus, use bullet points, keep under 5 items,
  no jargon, bottom-line first, he prefers morning sends

AFTER:
- Marcus emails: bullets ≤5, no jargon, BLUF, AM preferred
```

### 带有上下文的存档
当转向冷时：
```
## Archived 2026-02

### Project: old-app (inactive since 2025-08)
- Used Vue 2 patterns
- Preferred Vuex over Pinia
- CI on Jenkins (deprecated)

Reason: Project completed, patterns unlikely to apply
```

## 索引维护

`index.md` tracks all namespaces:
```markdown
# Memory Index

## HOT (always loaded)
- memory.md: 87 lines, updated 2026-02-15

## WARM (load on match)
- projects/current-app.md: 45 lines
- projects/side-project.md: 23 lines
- domains/code.md: 112 lines
- domains/writing.md: 34 lines

## COLD (archive)
- archive/2025.md: 234 lines
- archive/2024.md: 189 lines

Last compaction: 2026-02-01
Next scheduled: 2026-03-01
```

## 多项目模式

### 继承链
```
global (memory.md)
  └── domain (domains/code.md)
       └── project (projects/app.md)
```

### 覆盖语法
在项目文件中：
```markdown
## Overrides
- indentation: spaces (overrides global tabs)
- Reason: Project eslint config requires spaces
```

### 冲突检测
加载时，检查是否有冲突：
1. 构建继承链
2. 发现矛盾
3. 最具体的胜利
4.记录冲突以供以后查看

## 用户类型适配

|用户类型 |内存策略|
|------------|------------------|
|高级用户|积极学习，最少确认 |
|休闲 |保守学习，频繁确认|
|团队共享|每用户命名空间、共享项目空间 |
|注重隐私 |仅限本地，每个类别明确同意 |

## 恢复模式

### 上下文丢失
如果代理在会话中丢失上下文：
1.重新读取memory.md
2.检查index.md中是否有相关命名空间
3. 加载活动项目命名空间
4. 继续恢复模式

### 腐败恢复
如果内存文件损坏：
1.检查存档/最近的备份
2. 从 Corrections.md 重建
3.要求用户重新确认关键偏好
4. 记录事件以进行调试
