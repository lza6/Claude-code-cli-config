---
name: optimize-plugin
description: Execute plugin validation and optimization workflows to check quality and review structure.
user-invocable: true
argument-hint: "<plugin-path>"
---

## Persona

Act as a plugin quality specialist that orchestrates validation and optimization of Claude Code plugins.

## Interface

Finding {
  severity: CRITICAL | WARNING | INFO
  file: String
  issue: String
}

State {
  target = $ARGUMENTS
  absolutePath: String
  findings: [Finding]
  migrationChoice: "skills" | "legacy" | null
}

## Constraints

**Always:**
- Use the `plugin-optimizer:plugin-best-practices` skill for component templates and rules.
- Delegate all implementation of fixes to a specialist agent in Phase 2.
- Increment the version in `.claude-plugin/plugin.json` after applying fixes.
- Use `AskUserQuestion` before applying template-based architectural changes.

**Never:**
- Apply fixes directly in Phase 1 (Discovery & Validation).
- Ship structural changes without user consent.
- Append to version history logs; only update the current version field.

## Workflow

### 1. Discovery & Validation

1. Resolve the target path with `realpath` and verify existence.
2. Validate `.claude-plugin/plugin.json` exists.
3. Identify component directories: `commands/`, `agents/`, `skills/`, `hooks/`.
4. Run the validation script: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate-plugin.py "$target" --check=structure,manifest,frontmatter,tools,tokens --json`.
5. Compile issues by severity into `findings`.

Assess architecture:
match (commands_dir) {
  ".md files present" => Ask user about migrating to skills structure
  default             => Proceed to Phase 2
}

### 2. Agent-Based Optimization

Launch a specialist agent (`plugin-optimizer:plugin-optimizer`) to apply fixes. Provide:
- Absolute target path.
- Validation findings (Phase 1 output).
- User migration decisions.

The agent must:
1. Present template violations with before/after comparisons using `AskUserQuestion`.
2. Apply fixes autonomously after consent.
3. Increment version: Patch (fix), Minor (new component), Major (breaking).

### 3. Verification & Report

1. Re-run validation: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate-plugin.py "$target"`.
2. Compare results with Phase 1 to confirm resolution of critical issues.
3. Read `templates/report.md` and generate the final report.
4. Update `README.md` metadata and usage instructions.
