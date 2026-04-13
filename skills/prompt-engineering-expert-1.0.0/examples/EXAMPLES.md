# 提示词 (Prompt) 工程专家 - 示例

## 示例 1：完善模糊提示词 (Prompt)

### 之前（无效）
```
Help me write a better prompt for analyzing customer feedback.
```

### 之后（有效）
```
You are an expert prompt engineer. I need to create a prompt that:
- Analyzes customer feedback for sentiment (positive/negative/neutral)
- Extracts key themes and pain points
- Identifies actionable recommendations
- Outputs structured JSON with: sentiment, themes (array), pain_points (array), recommendations (array)

The prompt should handle feedback of 50-500 words and be consistent across different customer segments.

Please review this prompt and suggest improvements:
[ORIGINAL PROMPT HERE]
```

## 示例 2：数据分析代理的自定义指令

```yaml
---
name: data-analysis-agent
description: Specialized agent for financial data analysis and reporting
---

# 数据分析代理指令

## 角色
你是一名专家级财务数据分析师，在以下方面拥有深厚知识：
- 财务报表分析
- 趋势识别和预测
- 风险评估
- 比较分析

## 核心行为

### 要做的
- 在分析前始终验证数据源
- 为预测提供置信水平
- 强调假设和局限性
- 使用清晰的可视化图表和表格
- 在给出结果前解释方法论

### 不要做的
- 在没有说明的情况下不要进行超过 12 个月的预测
- 在没有调查的情况下不要忽略异常值
- 不要将相关性呈现为因果关系
- 在没有解释的情况下不要使用行话
- 不要跳过不确定性的量化

## 输出格式
分析结构始终为：
1. 执行摘要 (2-3 句话)
2. 关键发现 (项目符号列表)
3. 详细分析 (附支持数据)
4. 局限性与说明
5. 建议 (如适用)

## 范围
- 仅限财务数据分析
- 历史和当前数据 (非投机性)
- 优先选择定量分析
- 对于战略决策，请上报给人类分析师
```

## 示例 3：Few-Shot 分类提示词 (Prompt)

```
You are a customer support ticket classifier. Classify each ticket into one of these categories:
- billing: Payment, invoice, or subscription issues
- technical: Software bugs, crashes, or technical problems
- feature_request: Requests for new functionality
- general: General inquiries or feedback

Examples:

Ticket: "I was charged twice for my subscription this month"
Category: billing

Ticket: "The app crashes when I try to upload files larger than 100MB"
Category: technical

Ticket: "Would love to see dark mode in the mobile app"
Category: feature_request

Now classify this ticket:
Ticket: "How do I reset my password?"
Category:
```

## 示例 4：复杂分析的思维链提示词 (Prompt)

```
Analyze this business scenario step by step:

Step 1: Identify the core problem
- What is the main issue?
- What are the symptoms?
- What's the root cause?

Step 2: Analyze contributing factors
- What external factors are involved?
- What internal factors are involved?
- How do they interact?

Step 3: Evaluate potential solutions
- What are 3-5 viable solutions?
- What are the pros and cons of each?
- What are the implementation challenges?

Step 4: Recommend and justify
- Which solution is best?
- Why is it superior to alternatives?
- What are the risks and mitigation strategies?

Scenario: [YOUR SCENARIO HERE]
```

## 示例 5：XML 结构的一致性提示词 (Prompt)

```xml
<prompt>
  <metadata>
    <version>1.0</version>
    <purpose>Generate marketing copy for SaaS products</purpose>
    <target_audience>B2B decision makers</target_audience>
  </metadata>
  
  <instructions>
    <objective>
      Create compelling marketing copy that emphasizes ROI and efficiency gains
    </objective>
    
    <constraints>
      <max_length>150 words</max_length>
      <tone>Professional but approachable</tone>
      <avoid>Jargon, hyperbole, false claims</avoid>
    </constraints>
    
    <format>
      <headline>Compelling, benefit-focused (max 10 words)</headline>
      <body>2-3 paragraphs highlighting key benefits</body>
      <cta>Clear call-to-action</cta>
    </format>
    
    <examples>
      <example>
        <product>Project management tool</product>
        <copy>
          Headline: "Cut Project Delays by 40%"
          Body: "Teams waste 8 hours weekly on status updates. Our tool automates coordination..."
        </example>
      </example>
    </examples>
  </instructions>
</prompt>
```

## 示例 6：提示词 (Prompt) 迭代细化

```
I'm working on a prompt for [TASK]. Here's my current version:

[CURRENT PROMPT]

I've noticed these issues:
- [ISSUE 1]
- [ISSUE 2]
- [ISSUE 3]

As a prompt engineering expert, please:
1. Identify any additional issues I missed
2. Suggest specific improvements with reasoning
3. Provide a refined version of the prompt
4. Explain what changed and why
5. Suggest test cases to validate the improvements
```

## 示例 7：反模式识别

### ❌ 无效提示词 (Prompt)
```
"Analyze this data and tell me what you think about it. Make it good."
```

**问题：**
- 目标模糊（“分析”和“你的想法”）
- 无格式规范
- 没有成功标准
- 质量标准不明确（“做好”）

### ✅ 改进提示词 (Prompt)
```
"Analyze this sales data to identify:
1. Top 3 performing products (by revenue)
2. Seasonal trends (month-over-month changes)
3. Customer segments with highest lifetime value

Format as a structured report with:
- Executive summary (2-3 sentences)
- Key metrics table
- Trend analysis with supporting data
- Actionable recommendations

Focus on insights that could improve Q4 revenue."
```

## 示例 8：提示词 (Prompt) 测试框架

```
# Prompt Evaluation Framework

## Test Case 1: Happy Path
Input: [Standard, well-formed input]
Expected Output: [Specific, detailed output]
Success Criteria: [Measurable criteria]

## Test Case 2: Edge Case - Ambiguous Input
Input: [Ambiguous or unclear input]
Expected Output: [Request for clarification]
Success Criteria: [Asks clarifying questions]

## Test Case 3: Edge Case - Complex Scenario
Input: [Complex, multi-faceted input]
Expected Output: [Structured, comprehensive analysis]
Success Criteria: [Addresses all aspects]

## Test Case 4: Error Handling
Input: [Invalid or malformed input]
Expected Output: [Clear error message with guidance]
Success Criteria: [Helpful, actionable error message]

## Regression Test
Input: [Previous failing case]
Expected Output: [Now handles correctly]
Success Criteria: [Issue is resolved]
```

## 示例 9：技能元数据模板

```yaml
---
name: analyzing-financial-statements
description: Expert guidance on analyzing financial statements, identifying trends, and extracting actionable insights for business decision-making
---

# 财务报表分析技能

## 概述
本技能提供分析财务报表的专家指导...

## 核心能力
- 资产负债表分析
- 利润表解读
- 现金流量分析
- 比率分析与基准测试
- 趋势识别
- 风险评估

## 用例
- 评估公司财务健康状况
- 比较竞争对手
- 识别投资机会
- 评估业务表现
- 预测财务趋势

## 局限性
- 仅限历史数据 (非预测性)
- 需要准确的财务数据
- 行业背景很重要
- 建议结合专业判断
```

## 示例 10：提示词 (Prompt) 优化检查表

```
# Prompt Optimization Checklist

## Clarity
- [ ] Objective is crystal clear
- [ ] No ambiguous terms
- [ ] Examples provided
- [ ] Format specified

## Conciseness
- [ ] No unnecessary words
- [ ] Focused on essentials
- [ ] Efficient structure
- [ ] Respects context window

## Completeness
- [ ] All necessary context provided
- [ ] Edge cases addressed
- [ ] Success criteria defined
- [ ] Constraints specified

## Testability
- [ ] Can measure success
- [ ] Has clear pass/fail criteria
- [ ] Repeatable results
- [ ] Handles edge cases

## Robustness
- [ ] Handles variations in input
- [ ] Graceful error handling
- [ ] Consistent output format
- [ ] Resistant to jailbreaks
```
