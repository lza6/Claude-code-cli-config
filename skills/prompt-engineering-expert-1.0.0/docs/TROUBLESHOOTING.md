# 故障排除指南

## 常见提示词 (Prompt) 问题及解决方案

### 问题 1：输出不一致

**症状：**
- 相同的提示词 (Prompt) 产生不同的结果
- 输出的格式或质量各不相同
- 不可预测的行为

**根本原因：**
- 不明确的指示
- 缺少约束
- 例子不足
- 成功标准不明确

**解决方案：**
```
1. Add specific format requirements
2. Include multiple examples
3. Define constraints explicitly
4. Specify output structure with XML tags
5. Use role-based prompting for consistency
```

**修复示例：**
```
❌ Before: "Summarize this article"

✅ After: "Summarize this article in exactly 3 bullet points, 
each 1-2 sentences. Focus on key findings and implications."
```

---

### 问题 2：幻觉或虚假信息

**症状：**
- 克劳德发明事实
- 自信但不正确的陈述
- 虚构的引文或数据

**根本原因：**
- 鼓励猜测的提示词 (Prompt)
- 缺乏事实依据
- 上下文不足
- 模棱两可的问题

**解决方案：**
```
1. Ask Claude to cite sources
2. Request confidence levels
3. Ask for caveats and limitations
4. Provide factual context
5. Ask "What don't you know?"
```

**修复示例：**
```
❌ Before: "What will happen to the market next year?"

✅ After: "Based on current market data, what are 3 possible 
scenarios for next year? For each, explain your reasoning and 
note your confidence level (high/medium/low)."
```

---

### 问题 3：含糊或无益的回应

**症状：**
- 通用答案
- 缺乏特异性
- 没有解决真正的问题
- 级别太高

**根本原因：**
- 模糊提示词 (Prompt)
- 缺少上下文
- 目标不明确
- 无格式规范

**解决方案：**
```
1. Be more specific in the prompt
2. Provide relevant context
3. Specify desired output format
4. Give examples of good responses
5. Define success criteria
```

**修复示例：**
```
❌ Before: "How can I improve my business?"

✅ After: "I run a SaaS company with $2M ARR. We're losing 
customers to competitors. What are 3 specific strategies to 
improve retention? For each, explain implementation steps and 
expected impact."
```

---

### 问题 4：响应太长或太短

**症状：**
- 响应过于冗长
- 回复太简短
- 与预期不符
- 浪费令牌 (Token)

**根本原因：**
- 无长度规格
- 范围不明确
- 缺少格式指导
- 细节层次不明确

**解决方案：**
```
1. Specify word/sentence count
2. Define scope clearly
3. Use format templates
4. Provide examples
5. Request specific detail level
```

**修复示例：**
```
❌ Before: "Explain machine learning"

✅ After: "Explain machine learning in 2-3 paragraphs for 
someone with no technical background. Focus on practical 
applications, not theory."
```

---

### 问题 5：输出格式错误

**症状：**
- 输出格式不符合需求
- 无法解析响应
- 与下游工具不兼容
- 需要手动重新格式化

**根本原因：**
- 无格式规范
- 不明确的格式请求
- 格式未明确展示
- 缺少示例

**解决方案：**
```
1. Specify exact format (JSON, CSV, table, etc.)
2. Provide format examples
3. Use XML tags for structure
4. Request specific fields
5. Show before/after examples
```

**修复示例：**
```
❌ Before: "List the top 5 products"

✅ After: "List the top 5 products in JSON format:
{
  \"products\": [
    {\"name\": \"...\", \"revenue\": \"...\", \"growth\": \"...\"}
  ]
}"
```

---

### 问题 6：克劳德拒绝回应

**症状：**
- “我帮不上忙”
- 拒绝回答
- 建议替代方案
- 似乎过于谨慎

**根本原因：**
- 提示词 (Prompt) 似乎有害
- 意图不明确
- 敏感话题
- 不明确的合法用例

**解决方案：**
```
1. Clarify legitimate purpose
2. Reframe the question
3. Provide context
4. Explain why you need this
5. Ask for general guidance instead
```

**修复示例：**
```
❌ Before: "How do I manipulate people?"

✅ After: "I'm writing a novel with a manipulative character. 
How would a psychologist describe manipulation tactics? 
What are the psychological mechanisms involved?"
```

---

### 问题 7：提示词 (Prompt) 太长

**症状：**
- 超出上下文窗口
- 反应缓慢
- 高令牌 (Token) 使用率
- 运行成本昂贵

**根本原因：**
- 不必要的上下文
- 冗余信息
- 例子太多
- 详细说明

**解决方案：**
```
1. Remove unnecessary context
2. Consolidate similar points
3. Use references instead of full text
4. Reduce number of examples
5. Use progressive disclosure
```

**修复示例：**
```
❌ Before: [5000 word prompt with full documentation]

✅ After: [500 word prompt with links to detailed docs]
"See REFERENCE.md for detailed specifications"
```

---

### 问题 8：提示词 (Prompt) 不具有普遍性

**症状：**
- 适用于一种情况，但适用于其他情况则失败
- 对输入变化很脆弱
- 不同数据的中断
- 不可重复使用

**根本原因：**
- 某个例子过于具体
- 硬编码值
- 假设特定格式
- 缺乏灵活性

**解决方案：**
```
1. Use variables instead of hardcoded values
2. Handle multiple input formats
3. Add error handling
4. Test with diverse inputs
5. Build in flexibility
```

**修复示例：**
```
❌ Before: "Analyze this Q3 sales data..."

✅ After: "Analyze this [PERIOD] [METRIC] data. 
Handle various formats: CSV, JSON, or table.
If format is unclear, ask for clarification."
```

---

## 调试工作流程

### 第 1 步：找出问题
- 什么不起作用？
- 怎么会失败呢？
- 有什么影响？

### 第 2 步：分析提示词 (Prompt)
- 目标明确吗？
- 说明是否具体？
- 上下文是否足够？
- 格式是否指定？

### 步骤 3：检验假设
- 尝试添加更多上下文
- 尝试更具体
- 尝试提供示例
- 尝试更改格式

### 第 4 步：实施修复
- 更新提示词 (Prompt)
- 使用多个输入进行测试
- 验证一致性
- 记录变更

### 第 5 步：验证
- 现在有用吗？
- 它具有普遍性吗？
- 有效率吗？
- 可以维护吗？

---

## 快速参考：常见修复

| 问题 | 快速修复 |
|--------|------------|
| 不一致 | 添加格式规范 + 示例 |
| 幻觉 | 询问来源 + 置信水平 |
| 模糊 | 添加具体细节 + 示例 |
| 太长 | 指定字数 + 格式 |
| 格式错误 | 显示确切的格式示例 |
| 拒绝 | 澄清合法目的 |
| 提示词 (Prompt) 太长 | 删除不必要的上下文 |
| 不一概而论 | 使用变量 + 处理变化 |

---

## 测试清单

在部署提示词 (Prompt) 之前，请验证：

- [ ] 目标一目了然
- [ ] 说明具体
- [ ] 指定格式
- [ ] 提供示例
- [ ] 处理边缘情况
- [ ] 适用于多个输入
- [ ] 输出一致
- [ ] 令牌 (Token) 优化
- [ ] 错误处理清晰
- [ ] 文档已完成
