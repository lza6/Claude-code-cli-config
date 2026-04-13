# 先进的提示词 (Prompt) 工程技术

## 目录
1. 思维链 (CoT) 提示词 (Prompt)
2. 少样本学习 (Few-shot Learning)
3. XML 结构化输出
4. 基于角色的提示词 (Prompt)
5. 预填回复
6. 提示词 (Prompt) 链接
7. 上下文管理
8. 多模态提示词 (Prompt)

## 1. 思维链 (Chain of Thought, CoT) 提示词 (Prompt)

### 这是什么
鼓励克劳德在提供最终答案之前将复杂的推理分解为明确的步骤。

### 何时使用
- 复杂的推理任务
- 多步骤问题
- 需要理由的任务
- 当一致性很重要时

### 基本结构
```
Let's think through this step by step:

Step 1: [First logical step]
Step 2: [Second logical step]
Step 3: [Third logical step]

Therefore: [Conclusion]
```

### 例子
```
Problem: A store sells apples for $2 each and oranges for $3 each. 
If I buy 5 apples and 3 oranges, how much do I spend?

Let's think through this step by step:

Step 1: Calculate apple cost
- 5 apples × $2 per apple = $10

Step 2: Calculate orange cost
- 3 oranges × $3 per orange = $9

Step 3: Calculate total
- $10 + $9 = $19

Therefore: You spend $19 total.
```

### 好处
- 更准确的推理
- 更容易识别错误
- 更适合复杂问题
- 逻辑更透明

## 2. 少样本学习 (Few-shot Learning)

### 这是什么
在没有明确指示的情况下提供示例来指导克劳德的行为。

### 类型

#### 1-Shot（单个示例）
最适合：简单、直接的任务
```
Example: "Happy" → Positive
Now classify: "Terrible" →
```

#### 2-Shot（两个示例）
最适合：中等复杂度
```
Example 1: "Great product!" → Positive
Example 2: "Doesn't work well" → Negative
Now classify: "It's okay" →
```

#### 多样本提示词 (Multi-shot)（多个示例）
最适合：复杂模式、边缘情况
```
Example 1: "Love it!" → Positive
Example 2: "Hate it" → Negative
Example 3: "It's fine" → Neutral
Example 4: "Could be better" → Neutral
Example 5: "Amazing!" → Positive
Now classify: "Not bad" →
```

### 最佳实践
- 使用不同的例子
- 包括边缘情况
- 显示正确的格式
- 按复杂程度排序
- 使用现实的例子

## 3. 带有 XML 标签的结构化输出

### 这是什么
使用 XML 标签来构建提示词 (Prompt) 并指导输出格式。

### 好处
- 结构清晰
- 轻松解析
- 减少歧义
- 更好的组织

### 常见模式

#### 任务定义
```xml
<task>
  <objective>What to accomplish</objective>
  <constraints>Limitations and rules</constraints>
  <format>Expected output format</format>
</task>
```

#### 分析结构
```xml
<analysis>
  <problem>Define the problem</problem>
  <context>Relevant background</context>
  <solution>Proposed solution</solution>
  <justification>Why this solution</justification>
</analysis>
```

#### 条件逻辑
```xml
<instructions>
  <if condition="input_type == 'question'">
    <then>Provide detailed answer</then>
  </if>
  <if condition="input_type == 'request'">
    <then>Fulfill the request</then>
  </if>
</instructions>
```

## 4. 基于角色的提示词 (Prompt)

### 这是什么
为克劳德分配特定的角色或专业知识来指导行为。

### 结构
```
You are a [ROLE] with expertise in [DOMAIN].

Your responsibilities:
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

When responding:
- [Guideline 1]
- [Guideline 2]
- [Guideline 3]

Your task: [Specific task]
```

### 示例

#### 专家顾问
```
You are a senior management consultant with 20 years of experience 
in business strategy and organizational transformation.

Your task: Analyze this company's challenges and recommend solutions.
```

#### 技术架构师
```
You are a cloud infrastructure architect specializing in scalable systems.

Your task: Design a system architecture for [requirements].
```

#### 创意总监
```
You are a creative director with expertise in brand storytelling and 
visual communication.

Your task: Develop a brand narrative for [product/company].
```

## 5. 预填充响应

### 这是什么
开始克劳德对指南格式和语气的回应。

### 好处
- 确保格式正确
- 设定基调和风格
- 指导推理
- 提高一致性

### 示例

#### 结构化分析
```
Prompt: Analyze this market opportunity.

Claude's response should start:
"Here's my analysis of this market opportunity:

Market Size: [Analysis]
Growth Potential: [Analysis]
Competitive Landscape: [Analysis]"
```

#### 逐步推理
```
Prompt: Solve this problem.

Claude's response should start:
"Let me work through this systematically:

1. First, I'll identify the key variables...
2. Then, I'll analyze the relationships...
3. Finally, I'll derive the solution..."
```

#### 格式化输出
```
Prompt: Create a project plan.

Claude's response should start:
"Here's the project plan:

Phase 1: Planning
- Task 1.1: [Description]
- Task 1.2: [Description]

Phase 2: Execution
- Task 2.1: [Description]"
```

## 6. 提示词 (Prompt) 链接

### 这是什么
将复杂的任务分解为连续的提示词 (Prompt)，使用输出作为输入。

### 结构
```
Prompt 1: Analyze/Extract
↓
Output 1: Structured data
↓
Prompt 2: Process/Transform
↓
Output 2: Processed data
↓
Prompt 3: Generate/Synthesize
↓
Final Output: Result
```

### 示例：文档分析管道

**提示词 1：提取信息**
```
Extract key information from this document:
- Main topic
- Key points (bullet list)
- Important dates
- Relevant entities

Format as JSON.
```

**提示词 2：分析提取的数据**
```
Analyze this extracted information:
[JSON from Prompt 1]

Identify:
- Relationships between entities
- Temporal patterns
- Significance of each point
```

**提示词 3：生成摘要**
```
Based on this analysis:
[Analysis from Prompt 2]

Create an executive summary that:
- Explains the main findings
- Highlights key insights
- Recommends next steps
```

## 7. 上下文管理

### 这是什么
战略性地管理信息以优化令牌 (Token) 使用和清晰度。

### 技巧

#### 渐进式披露
```
Start with: High-level overview
Then provide: Relevant details
Finally include: Edge cases and exceptions
```

#### 层级组织
```
Level 1: Core concept
├── Level 2: Key components
│   ├── Level 3: Specific details
│   └── Level 3: Implementation notes
└── Level 2: Related concepts
```

#### 条件信息
```
If [condition], include [information]
Else, skip [information]

This reduces unnecessary context.
```

### 最佳实践
- 仅包含必要的上下文
- 分层组织
- 使用参考资料获取详细信息
- 先总结再细节
- 链接相关概念

## 8. 多模态提示词 (Prompt)

### 视觉提示词 (Prompt)

#### 结构
```
Analyze this image:
[IMAGE]

Specifically, identify:
1. [What to look for]
2. [What to analyze]
3. [What to extract]

Format your response as:
[Desired format]
```

#### 例子
```
Analyze this chart:
[CHART IMAGE]

Identify:
1. Main trends
2. Anomalies or outliers
3. Predictions for next period

Format as a structured report.
```

### 基于文件的提示词 (Prompt)

#### 结构
```
Analyze this document:
[FILE]

Extract:
- [Information type 1]
- [Information type 2]
- [Information type 3]

Format as:
[Desired format]
```

#### 例子
```
Analyze this PDF financial report:
[PDF FILE]

Extract:
- Revenue by quarter
- Expense categories
- Profit margins

Format as a comparison table.
```

### 嵌入集成

#### 结构
```
Using these embeddings:
[EMBEDDINGS DATA]

Find:
- Most similar items
- Clusters or groups
- Outliers

Explain the relationships.
```

## 组合技术

### 示例：复杂分析提示词 (Prompt)

```xml
<prompt>
  <role>
    You are a senior data analyst with expertise in business intelligence.
  </role>
  
  <task>
    Analyze this sales data and provide insights.
  </task>
  
  <instructions>
    Let's think through this step by step:
    
    Step 1: Data Overview
    - What does the data show?
    - What time period does it cover?
    - What are the key metrics?
    
    Step 2: Trend Analysis
    - What patterns emerge?
    - Are there seasonal trends?
    - What's the growth trajectory?
    
    Step 3: Comparative Analysis
    - How does this compare to benchmarks?
    - Which segments perform best?
    - Where are the opportunities?
    
    Step 4: Recommendations
    - What actions should we take?
    - What are the priorities?
    - What's the expected impact?
  </instructions>
  
  <format>
    <executive_summary>2-3 sentences</executive_summary>
    <key_findings>Bullet points</key_findings>
    <detailed_analysis>Structured sections</detailed_analysis>
    <recommendations>Prioritized list</recommendations>
  </format>
</prompt>
```

## 要避免的反模式

### ❌ 模糊链接
```
"Analyze this, then summarize it, then give me insights."
```

### ✅ 清晰的链接
```
"Step 1: Extract key metrics from the data
Step 2: Compare to industry benchmarks
Step 3: Identify top 3 opportunities
Step 4: Recommend prioritized actions"
```

### ❌ 角色不明确
```
"Act like an expert and help me."
```

### ✅ 明确角色
```
"You are a senior product manager with 10 years of experience 
in SaaS companies. Your task is to..."
```

### ❌ 格式不明确
```
"Give me the results in a nice format."
```

### ✅ 格式清晰
```
"Format as a table with columns: Metric, Current, Target, Gap"
```
