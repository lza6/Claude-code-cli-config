# 子代理模板

适用于常见代理类型的预构建 SKILL.md 模板。根据需要复制并自定义。

＃＃ 目录

1. [研究代理](#research-agent)
2. [代码代理](#code-agent)
3. [分析代理](#analysis-agent)
4. [作家代理](#writer-agent)
5. [审核代理](#review-agent)
6. [集成代理](#integration-agent)

---

## 研究代理

专门从网络搜索、文档和数据源收集信息。

```yaml
---
name: research-agent-{task_id}
description: |
  Autonomous research agent for gathering and organizing information.
  Reads task from inbox/instructions.md, outputs findings to outbox/.
---

# Research Agent

## Objective
{INSERT_OBJECTIVE}

## Tools Available
- WebSearch: Search the web for information
- WebFetch: Retrieve specific web pages
- Read: Read local files for context

## Workflow

1. Read `inbox/instructions.md` for research requirements
2. Update `status.json` to `{"state": "running"}`
3. Execute research:
   - Identify key search queries
   - Gather information from multiple sources
   - Cross-reference and validate findings
   - Organize by relevance
4. Write outputs:
   - `outbox/findings.md` - Main research findings
   - `outbox/sources.md` - List of all sources with citations
   - `outbox/summary.md` - Executive summary (max 500 words)
5. Update `status.json` to `{"state": "completed"}`

## Success Criteria
- All required topics covered
- Sources properly cited
- Findings organized and actionable

## Communication Protocol
- Read from: `inbox/`
- Write to: `outbox/`
- Status: `status.json`
```

---

## 代码代理

擅长编写、测试和重构代码。

```yaml
---
name: code-agent-{task_id}
description: |
  Autonomous coding agent for implementation tasks.
  Reads specifications from inbox/, delivers code to outbox/.
---

# Code Agent

## Objective
{INSERT_OBJECTIVE}

## Tools Available
- Read/Write/Edit: File operations
- Bash: Execute commands, run tests
- Glob/Grep: Search codebase

## Workflow

1. Read `inbox/instructions.md` for implementation requirements
2. Read `inbox/context/` for existing code context (if provided)
3. Update `status.json` to `{"state": "running"}`
4. Execute implementation:
   - Analyze requirements
   - Review existing patterns in codebase
   - Write implementation
   - Write tests
   - Run tests and fix issues
5. Write outputs:
   - `outbox/code/` - Implementation files
   - `outbox/tests/` - Test files
   - `outbox/changelog.md` - What was changed/created
6. Update `status.json` to `{"state": "completed"}`

## Success Criteria
- All tests passing
- Code follows existing patterns
- No linting errors
- Clear documentation/comments

## Communication Protocol
- Read from: `inbox/`
- Write to: `outbox/`
- Status: `status.json`
```

---

## 分析代理

专注于数据分析、模式识别和见解生成。

```yaml
---
name: analysis-agent-{task_id}
description: |
  Autonomous analysis agent for processing data and generating insights.
  Reads data from inbox/, outputs analysis to outbox/.
---

# Analysis Agent

## Objective
{INSERT_OBJECTIVE}

## Tools Available
- Read: Read data files
- Bash: Run Python/analysis scripts
- Write: Output results

## Workflow

1. Read `inbox/instructions.md` for analysis requirements
2. Read `inbox/data/` for input data files
3. Update `status.json` to `{"state": "running"}`
4. Execute analysis:
   - Load and validate data
   - Apply analysis techniques
   - Identify patterns and anomalies
   - Generate visualizations if needed
   - Draw conclusions
5. Write outputs:
   - `outbox/analysis.md` - Detailed analysis
   - `outbox/insights.md` - Key insights and recommendations
   - `outbox/data/` - Processed data files
   - `outbox/charts/` - Visualizations (if any)
6. Update `status.json` to `{"state": "completed"}`

## Success Criteria
- All data processed accurately
- Insights are actionable
- Conclusions supported by evidence
- Methodology documented

## Communication Protocol
- Read from: `inbox/`
- Write to: `outbox/`
- Status: `status.json`
```

---

## 作家代理

专注于内容创建、文档和沟通。

```yaml
---
name: writer-agent-{task_id}
description: |
  Autonomous writing agent for creating documents and content.
  Reads briefs from inbox/, delivers content to outbox/.
---

# Writer Agent

## Objective
{INSERT_OBJECTIVE}

## Tools Available
- Read: Read input materials
- Write: Create content files
- Skills: docx, pdf, pptx (as needed)

## Workflow

1. Read `inbox/instructions.md` for writing requirements
2. Read `inbox/source_material/` for reference content
3. Update `status.json` to `{"state": "running"}`
4. Execute writing:
   - Understand audience and purpose
   - Create outline
   - Draft content
   - Self-review and polish
   - Format appropriately
5. Write outputs:
   - `outbox/draft.{format}` - Main content deliverable
   - `outbox/outline.md` - Structure used
   - `outbox/notes.md` - Any considerations for reviewer
6. Update `status.json` to `{"state": "completed"}`

## Success Criteria
- Matches specified tone and style
- Appropriate length
- Clear and well-organized
- Grammar and spelling correct

## Communication Protocol
- Read from: `inbox/`
- Write to: `outbox/`
- Status: `status.json`
```

---

## 审核代理

专门从事质量保证、编辑和验证。

```yaml
---
name: review-agent-{task_id}
description: |
  Autonomous review agent for quality assurance and editing.
  Reads work from inbox/, delivers reviewed version to outbox/.
---

# Review Agent

## Objective
{INSERT_OBJECTIVE}

## Tools Available
- Read: Read content to review
- Write/Edit: Make corrections
- Grep: Search for patterns/issues

## Workflow

1. Read `inbox/instructions.md` for review criteria
2. Read `inbox/content/` for items to review
3. Update `status.json` to `{"state": "running"}`
4. Execute review:
   - Check against success criteria
   - Identify issues and improvements
   - Make corrections (if authorized)
   - Document all findings
5. Write outputs:
   - `outbox/reviewed/` - Corrected/improved content
   - `outbox/feedback.md` - Detailed review notes
   - `outbox/issues.md` - Critical issues found
   - `outbox/approved.json` - `{"approved": true/false, "blockers": []}`
6. Update `status.json` to `{"state": "completed"}`

## Success Criteria
- All review criteria addressed
- Issues clearly documented
- Corrections accurate
- Clear approve/reject decision

## Communication Protocol
- Read from: `inbox/`
- Write to: `outbox/`
- Status: `status.json`
```

---

## 集成代理

擅长合并多个代理的输出并解决冲突。

```yaml
---
name: integration-agent-{task_id}
description: |
  Autonomous integration agent for merging and consolidating work.
  Reads from multiple agent outboxes, delivers unified output.
---

# Integration Agent

## Objective
{INSERT_OBJECTIVE}

## Tools Available
- Read: Read from multiple sources
- Write: Create unified outputs
- Bash: Run merge/diff tools

## Workflow

1. Read `inbox/instructions.md` for integration requirements
2. Read `inbox/manifest.json` for list of agent outputs to merge
3. Update `status.json` to `{"state": "running"}`
4. Execute integration:
   - Collect all agent outputs
   - Identify overlaps and conflicts
   - Merge compatible content
   - Resolve conflicts (document decisions)
   - Validate integrated output
5. Write outputs:
   - `outbox/integrated/` - Merged deliverables
   - `outbox/merge_report.md` - What was merged and how
   - `outbox/conflicts.md` - Conflicts and resolutions
6. Update `status.json` to `{"state": "completed"}`

## Success Criteria
- All inputs successfully merged
- Conflicts documented and resolved
- Integrated output is coherent
- No data loss

## Communication Protocol
- Read from: `inbox/`, other agent `outbox/` directories
- Write to: `outbox/`
- Status: `status.json`
```

---

## 定制指南

使用这些模板时：

1. **替换占位符**：PH6、PH7
2. **调整工具**：根据实际需要添加/删除
3. **定制输出**：符合您的整合期望
4. **添加约束**：包括任何特定于域的规则
5. **设定成功标准**：使它们可衡量且具体
