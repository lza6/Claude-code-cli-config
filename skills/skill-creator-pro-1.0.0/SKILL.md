---
name: skill-creator-pro
description: "创建新技能 (Skill)、修改和改进现有技能，并通过评估驱动的迭代来衡量技能性能。在用户希望从头创建技能、编辑或优化现有技能、运行评估测试技能、通过方差分析对技能性能进行基准测试，或优化技能描述以提高触发准确性时使用。也适用于用户说‘把它变成技能’、‘为 X 创建技能’、‘改进这个技能’、‘测试这个技能’、‘对这个技能运行评估’，或提及技能描述、技能触发、技能质量时。"
---

# 技能创建者专业版 (Skill Creator Pro)

> 受到 Anthropic 的 Claude Code 技能创建者的启发和改编
> (https://github.com/anthropics/skills/tree/main/skills/skill-creator)。
> 根据 Apache 2.0 获得许可。

用于创建新的 OpenClaw 技能并通过评估驱动的开发迭代改进它们的技能。

## 高级流程

- 决定该技能应该做什么以及它应该如何发挥作用
- 编写技能草案
- 创建测试提示词 (Prompt) 并在其上运行具有技能的代理 (通过子代理)
- 定性和定量评估结果
  - 当运行在后台进行时，如果没有则起草定量评估
  - 使用 "eval-viewer/generate_review.py" 向用户显示结果
- 根据反馈重写技能
- 重复直到满意为止
- 扩大测试集并在更大范围内重试

您的工作是找出用户在此过程中的位置并帮助他们进步。也许他们想从头开始创建一项新技能，或者他们可能已经有了草案并想要迭代。保持灵活性 —— 如果用户说“只是和我一起交流”，请跳过正式的评估循环。

技能完成后，还可以运行描述优化器来提高触发精度。

## 与用户沟通

根据用户的技术水平调整您的沟通方式。留意上下文线索：

- “评估 (Eval)”和“基准 (Benchmark)”对于大多数用户来说都很好
- 对于 “JSON” 和 “断言 (Assertions)”，请确保用户在自由使用它们之前对这些术语感到满意
- 如果有疑问，请简要解释术语

---

## 创建技能

### 捕获意图

首先了解用户的意图。当前对话可能已经包含要捕获的工作流程（例如，“将其转化为技能”）。如果是这样，请首先从对话历史记录中提取答案 —— 使用的工具、步骤顺序、所做的更正、输入/输出格式。用户可能需要填补空白，并应在继续之前确认。

1. 这项技能应该让代理能够做什么？
2. 这个技能什么时候触发？ (什么用户短语/上下文)
3. 预期的输出格式是什么？
4. 我们应该设置测试用例吗？具有客观可验证输出的技能受益于测试。具有主观输出的技能（写作风格、艺术）通常不会。建议适当的默认值，但让用户决定。

### 采访与研究

主动询问边缘情况、输入/输出格式、示例文件、成功标准和依赖性。解决这些问题后再编写测试提示词 (Prompt)。

### 编写 SKILL.md

根据访谈内容，填写：

- **名称 (name)**：技能标识符（短横线命名法，kebab-case）
- **描述 (description)**：何时触发，它的作用。这是主要的触发机制。让它变得“主动” —— 包括该技能的作用和具体背景。不要写“仪表板构建器”，而是写“构建仪表板。每当用户提到仪表板、数据可视化、指标显示或想要以可视方式显示任何数据时使用，即使他们没有说‘仪表板’。”
- **其余技能说明**

### 技能写作指南

有关整个评估系统中使用的详细 JSON 模式，请参阅 "references/schemas.md"。

#### 技能剖析

```
skill-name/
├── SKILL.md (必填)
│   ├── YAML frontmatter (必填：name, description)
│   └── Markdown 指令
└── 捆绑资源 (可选)
    ├── scripts/    - 可执行代码
    ├── references/ - 根据需要加载到上下文的文档
    └── assets/     - 输出中使用的文件 (模板、图标、字体)
```

#### 渐进式披露

技能采用三级加载系统：
1. **元数据** (名称 + 描述) —— 始终在上下文中 (约 100 个字)
2. **SKILL.md 正文** —— 技能触发时的上下文 (理想情况下 < 500 行)
3. **捆绑资源** —— 根据需要加载 (无限制)

将 SKILL.md 控制在 500 行以内；使用 `references/` 来存放溢出的内容。

#### 写作模式

在指令中使用命令式。解释**为什么**事情很重要 —— 今天的 LLM 很聪明，并且比严格的“必须”更能对推理做出反应。包含有帮助的示例。使技能具有普遍性，而不是局限于特定示例。

### 测试用例

写完技能草稿后，创建 2-3 个真实的测试提示词 (Prompt)。与用户分享以供审阅。保存到 "evals/evals.json"：

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "用户任务提示词 (Prompt)",
      "expected_output": "预期结果描述",
      "files": []
    }
  ]
}
```

## 运行和评估测试用例

将结果放入 `<skill-name>-workspace/` 中，作为技能目录的同级目录。按迭代 (`iteration-1/`, `iteration-2/` 等) 组织 `eval-0/`, `eval-1/` 等中的每个测试用例。

### 第 1 步：生成所有运行

对于每个测试用例，生成两个子代理 —— 一个具有技能，一个没有 (基线)。立即启动所有内容，以便它们大约在同一时间完成。

**带技能运行** —— 生成一个子代理，其指令如下：
```
执行此任务：
- 技能路径: <path-to-skill>
- 任务: <eval prompt>
- 输入文件: <eval files if any>
- 保存输出至: <workspace>/iteration-N/eval-ID/with_skill/outputs/
```

**基线运行** —— 没有技能的相同提示词 (Prompt)，保存到 `without_skill/outputs/`。

为每个测试用例编写一个 `eval_metadata.json`：
```json
{
  "eval_id": 0,
  "eval_name": "此处填写描述性名称",
  "prompt": "用户任务提示词 (Prompt)",
  "assertions": []
}
```

### 步骤 2：在运行过程中草拟断言 (Assertions)

为每个测试用例起草定量断言。好的断言是客观可验证的，并且有描述性的名称。使用断言更新 `eval_metadata.json` 和 `evals/evals.json`。

### 步骤 3：捕获耗时数据

当每个子代理完成时，将耗时数据保存到 `timing.json`：
```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

### 步骤 4：评分、聚合和启动查看器

全部运行完成后：

1. **对每次运行进行评分** —— 阅读 `agents/grader.md` 并根据输出评估断言。保存到 `grading.json`。`grading.json` 的期望数组必须使用字段 `"text"`、`"passed"` 和 `"evidence"`。对于可通过编程检查的断言，编写并运行脚本。

2. **聚合到基准测试** —— 从该技能的目录运行：
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```

3. **分析师阶段** —— 阅读 `agents/analyzer.md` 并了解聚合统计数据可能隐藏的表面模式。

4. **启动查看器** —— 在 OpenClaw 中始终使用 `--static` 模式：
   ```bash
   python <skill-creator-pro-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     --static <workspace>/iteration-N/review.html
   ```
对于迭代 2+，还传递 `--previous-workspace <workspace>/iteration-<N-1>`。

然后将 HTML 文件发送给用户：
   ```
   message(action=send, filePath="<workspace>/iteration-N/review.html")
   ```
或者通过 Canvas 工具（如果可用）呈现它。

*在*自己评估结果之前*生成评估查看器。尽快将它们呈现在用户面前！

5. **告诉用户**：“我已经生成了结果查看器。‘输出’选项卡可让您查看每个测试用例并留下反馈。‘基准’选项卡显示定量比较。完成后，请回来告诉我。”

### 第 5 步：阅读反馈

查看器的“提交所有评论”按钮会下载 `feedback.json`。当用户提供它时阅读它：

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "图表缺少轴标签", "timestamp": "..."}
  ],
  "status": "complete"
}
```

空反馈意味着用户认为没问题。将改进重点放在具有具体建议的测试用例上。

---

## 改进技能

### 如何思考改进

1. **根据反馈进行概括。** 不要过度拟合具体示例。该技能将在不同的提示词 (Prompt) 中多次使用。尝试不同的隐喻或模式，而不是繁琐的改变或压抑的“必须”。

2. **保持精简。** 删除那些不起作用的东西。阅读执行记录 —— 如果该技能导致工作效率低下，请修剪这些部分。

3. **解释原因。** LLM 对推理的反应比对严格规则的反应更好。如果您发现自己用大写字母写“总是”或“从不”，请重新解释并说明原因。

4. **寻找重复的工作。** 如果所有测试用例独立编写类似的辅助脚本，则将该脚本捆绑在 `scripts/` 中，以节省将来的调用，避免重复造轮子。

### 迭代循环

1. 对技能进行改进
2. 将所有测试用例重新运行到 `iteration-<N+1>/` 中，包括基线
3. 使用指向上一个迭代的 `--previous-workspace` 启动查看器
4. 等待用户审核
5. 阅读反馈，再次改进，重复

继续下去，直到用户满意、反馈都是空的，或者您没有取得有意义的进展。

---

## 高级：盲测比较 (Blind Comparison)

要严格比较两个技能版本，请阅读 `agents/comparator.md` 和 `agents/analyzer.md`。将两个输出提供给独立的子代理，而不透露哪个是哪个。这是可选的 —— 人工审核通常就足够了。

---

## 描述优化 (Description Optimization)

描述 (Description) 字段是主要的触发机制。创建或改进一项技能后，主动提出对其进行优化。

### 第 1 步：生成触发评估查询 (Trigger Eval Queries)

创建 20 个评估查询 —— 应该触发和不应该触发的混合。保存为 JSON：
```json
[
  {"query": "真实的用户提示词 (Prompt)", "should_trigger": true},
  {"query": "擦肩而过的提示词 (Prompt)", "should_trigger": false}
]
```

查询必须是真实的 —— 包括文件路径、个人上下文、列名称、随意的言语、拼写错误。关注边缘情况，而不是明确的情况。不应该触发的查询应该是“未遂”事件，而不是明显不相关的查询。

### 第 2 步：与用户一起审核

使用 `assets/eval_review.html` 中的 HTML 模板呈现评估集。替换占位符：
- `__EVAL_DATA_PLACEHOLDER__` → JSON 数组
- `__SKILL_NAME_PLACEHOLDER__` → 技能名称
- `__SKILL_DESCRIPTION_PLACEHOLDER__` → 当前描述

写入临时文件并通过 `message(action=send, filePath=...)` 发送或通过 Canvas 呈现。

### 步骤 3：运行优化循环

描述优化循环需要 CLI 访问权限才能运行 eval 查询。在 OpenClaw 中，使用改编的脚本：

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id> \
  --max-iterations 5 \
  --verbose
```

注意：`run_eval.py` 和 `run_loop.py` 脚本使用 `claude -p` 来触发测试。在没有 `claude` CLI 的 OpenClaw 环境中，您可以手动运行描述优化：通过生成子代理来评估每个查询，检查它是否会触发技能，然后使用 `improve_description.py` 的逻辑生成更好的描述。

### 第 4 步：应用结果

从输出中获取 `best_description` 并更新技能的 `SKILL.md` frontmatter。显示优化前后的对比并报告分数。

---

## 打包

打包分发技能：
```bash
python -m scripts.package_skill <path/to/skill-folder>
```

然后通过 `message(action=send, filePath=...)` 将 `.skill` 文件发送给用户。

---

## OpenClaw 特定工作流程

### 基于子代理的测试

OpenClaw 使用子代理来并行测试执行。当生成测试运行时：
- 子代理可以读取技能的 `SKILL.md` 并按照其说明进行操作
- 结果保存到工作区文件中
- 耗时数据来自子代理完成通知

### 展示结果

由于 OpenClaw 可能没有浏览器显示：
- 始终使用 `--static` 模式和 `generate_review.py` 来创建独立的 HTML
- 通过 `message(action=send, filePath=...)` 发送 HTML 文件
- 或通过 Canvas 工具呈现：`canvas(action=present, url="file://...")`

### 反馈收集

在静态模式下，查看器的“提交所有评论”会下载 `feedback.json`。然后，用户可以将此文件提供给您。

---

## 参考文件

- `agents/grader.md` —— 如何根据输出评估断言
- `agents/comparator.md` —— 如何进行盲测 A/B 比较
- `agents/analyzer.md` —— 如何分析基准测试结果
- `references/schemas.md` —— `evals.json`、`grading.json`、`benchmark.json` 等的 JSON 模式。

---

## 核心循环总结

1. 弄清楚技能是什么
2. 起草或编辑技能
3. 根据测试提示词 (Prompt) 运行具有技能的代理 (通过子代理)
4. 与用户一起评估输出：
   - 创建 `benchmark.json` 并运行 `eval-viewer/generate_review.py`
   - 进行定量评估
5. 重复直到满意为止
6. 打包最终技能
