---
name: writing-plans
description: "当您在接触代码之前对多步骤任务有规范或要求时使用"
---

# 写作计划

## 概述

假设工程师对我们的代码库的背景为零并且品味有问题，则编写全面的实施计划。记录他们需要知道的一切：每个任务需要修改哪些文件、代码、测试、文档，以及如何测试。将整个计划拆分为小任务交给他们。DRY。YAGNI。测试驱动。频繁提交。

假设他们是一位熟练的开发人员，但对我们的工具集或问题领域几乎一无所知。假设他们不太了解良好的测试设计。

**开始时宣布：**“我正在使用写作计划技能来创建实施计划。”

**上下文：** 这应该在专用工作树中运行（通过头脑风暴技能创建）。

**将计划保存到：** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## 小任务粒度

**每一步都是一个动作（2-5 分钟）：**
- “编写失败的测试” - 步骤
- “运行它以确保它失败” - 步骤
- “实现最少的代码以使测试通过” - 步骤
- “运行测试并确保它们通过” - 步骤
-“提交”-步骤

## 计划文档标题

**每个计划必须以此标题开头：**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** 必需子 Skill：使用 superpowers:executing-plans 逐步实施此计划。

**Goal：** [一句话描述构建内容]

**Architecture：** [2-3 句话说明方法]

**Tech Stack：** [关键技术/库]

---
```

## 任务结构

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: 编写失败的测试**

```python
def test_specific_behavior():
    结果 = 函数（输入）
    断言结果==预期
```

**Step 2: 运行测试以验证它失败**

运行：`pytest tests/path/test.py::test_name -v`
预期：FAIL 并显示 "function not defined"

**Step 3: 编写最小实现**

```python
def 函数（输入）：
    预期回报
```

**Step 4: 运行测试以验证它通过**

运行：`pytest tests/path/test.py::test_name -v`
预期：PASS

**Step 5: 提交**

```bash
git add 测试/路径/test.py src/path/file.py
git commit -m“壮举：添加特定功能”
```
```

## 记住
- 始终使用精确文件路径
- 计划中包含完整代码（不是"添加验证"）
- 具有预期输出的精确命令
- 使用 @ 语法引用相关 Skill
- DRY、YAGNI、TDD、频繁提交

## 执行交接

保存计划后，提供执行选择：

**"计划已完成并保存到 `docs/plans/<filename>.md`。两个执行选项：**

**1. 子代理驱动（本次会议）** - 我为每个任务分配新的子代理，在任务之间进行审查，快速迭代

**2. 并行会话（单独）** - 打开新会话使用执行计划，使用检查点批量执行

**哪种方法？"**

**如果选择子代理驱动：**
- **所需子 Skill：** 使用超能力：子代理驱动开发
- 留在本次会议中
- 每个任务使用新的子代理 + 代码审查

**如果选择并行会话：**
- 指导他们在工作树中打开新会话
- **所需子 Skill：** 新会话使用超能力：执行计划
