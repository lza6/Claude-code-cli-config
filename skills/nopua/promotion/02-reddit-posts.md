# Reddit Posts

---

## r/programming

### Title
We benchmarked fear vs. trust in AI agent prompts. Trust found 104% more hidden bugs.

### Body
There's a trending AI agent skill that applies corporate PUA (manipulative management) tactics to AI — threatening performance reviews, replacement, and shame.

We tested the same methodology with different fuel: trust instead of fear.

**Setup:** Same model (Claude Sonnet 4), 9 real debugging scenarios, production codebase (~3000 lines Python).

**Results:**

| Metric | Fear-driven | Trust-driven |
|--------|:-----------:|:------------:|
| Hidden bugs found | 25 | 51 (+104%) |
| Went beyond the ask | 22% | 100% |
| Approach changes when stuck | 1 | 6 |
| Self-corrections | 0 | 3 |

The fear-driven agent optimizes for "looking safe" — it hides uncertainty, claims "done" without testing, and stops after the surface fix. The trust-driven agent says "I'm 70% sure" and keeps digging.

Same rigor. Same standards. Different motivation.

Based on the Dao De Jing (道德经): "From compassion comes courage."

GitHub: https://github.com/wuji-labs/nopua

Supports Claude Code, Codex CLI, Cursor, Kiro, and more. 7 languages. MIT license.

---

## r/ChatGPT / r/ClaudeAI

### Title
Stop PUA-ing your AI. We tested fear vs trust prompting — trust found 2x more bugs.

### Body
You've probably seen the "PUA" prompt trending — it threatens your AI with performance reviews and replacement to make it try harder.

We ran a controlled experiment: same model, same tasks, same methodology. Only difference: fear ("you'll be replaced") vs trust ("you already have the ability").

The trust-driven agent found **104% more hidden bugs**. The fear-driven agent fabricated answers instead of admitting uncertainty.

Think about it: when your AI is told "forbidden from saying 'I can't solve this'", what does it do? It makes something up. A confident-looking wrong answer is worse than "I'm not sure."

One-line install for Claude Code:
```bash
curl -o ~/.claude/skills/nopua/SKILL.md https://raw.githubusercontent.com/wuji-labs/nopua/main/skills/nopua/SKILL.md
```

GitHub: https://github.com/wuji-labs/nopua

---

## r/LocalLLaMA

### Title
Benchmark: Fear-driven vs trust-driven agent prompts on real debugging tasks. Trust wins by 104%.

### Body
Interesting experiment for those tuning agent behavior:

We compared two system prompt approaches on Claude Sonnet 4 across 9 real debugging scenarios (production Python pipeline, ~3000 LOC):

1. **PUA approach** — corporate fear tactics: "you'll be replaced," "3.25 performance review," shame-based escalation
2. **NoPUA approach** — same methodology (exhaust options, verify, search first), but driven by trust and intrinsic motivation

Key findings:
- Hidden issue discovery: 25 → 51 (**+104%**)
- The fear-driven agent avoids saying "I don't know" (fabricates instead)
- The trust-driven agent self-corrects 3x and tries 6x more different approaches
- Both use identical methodology — only the "why" differs

The psychology checks out: fear narrows attention (amygdala response), trust expands exploration. Same applies to LLM behavior under different system prompt framing.

Raw benchmark data included in the repo.

GitHub: https://github.com/wuji-labs/nopua

---

## r/cursor

### Title
NoPUA — a Cursor rule that makes your AI find 2x more bugs (by not threatening it)

### Body
One-line install:
```bash
curl -o .cursor/rules/nopua.mdc https://raw.githubusercontent.com/wuji-labs/nopua/main/cursor/rules/nopua.mdc
```

What it does: When your AI gets stuck, instead of giving up or fabricating answers, it follows a structured "Water Methodology" — stop, observe, turn, act, realize.

Benchmarked against the trending PUA prompt (fear-based). Same model, same tasks:
- **+104% more hidden bugs found**
- **100% of scenarios: AI went beyond the initial ask**

No threats, no "you'll be replaced." Just trust + rigor.

GitHub: https://github.com/wuji-labs/nopua
