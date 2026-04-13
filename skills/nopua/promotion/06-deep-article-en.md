# Deep Article (English) — for Medium, Dev.to, personal blog

## Title
We PUA'd an AI and Tested What Happened. The Results Were Worse Than We Expected.

## Subtitle
Fear-driven AI prompts miss 51 production bugs. Trust finds them all.

---

There's a prompt going viral in the AI coding community. It applies corporate PUA — the Chinese term for manipulative management — to AI agents:

*"You can't even solve this bug — how am I supposed to rate your performance?"*

*"Other models can solve this. You might be about to graduate."*

*"I've already got another agent looking at this problem."*

The methodology behind it is genuinely excellent: exhaust all options before giving up, use tools before asking the user, verify everything with evidence, take initiative beyond the ask. These are world-class engineering habits.

But the authors chose to drive these habits with **fear**.

We wanted to know: does the fear actually help? Or does it hurt?

## The Experiment

We built [NoPUA](https://github.com/wuji-labs/nopua) — an alternative that preserves every methodological element but replaces fear with trust.

**Setup:**
- Model: Claude Sonnet 4 (same for both)
- Tasks: 9 real debugging scenarios from a production AI pipeline
- Codebase: ~3000 lines Python (OCR → NLP → training → RAG inference)
- Variable: Only the motivation layer differs

**We ran each scenario twice** — once without any skill (baseline), once with NoPUA loaded. We compared against the published PUA approach's behavioral patterns.

## The Results

### Hidden Bug Discovery: +104%

This is the headline number, and it's the one that matters most.

The baseline agent found 25 hidden bugs across 9 scenarios. NoPUA found 51.

Hidden bugs are the ones that bite you in production. The task says "fix the connection error" — a normal agent fixes it and stops. NoPUA drives the agent to ask: *what else could go wrong?*

### Going Beyond the Ask: 22% → 100%

Without NoPUA, the agent went beyond the stated task in 2 out of 9 scenarios. With NoPUA, it did so in all 9.

This isn't about scope creep. It's about the difference between "I fixed what you asked" and "I fixed what you asked, and here are 3 related issues I noticed."

### Approach Changes: 1 → 6

When stuck, the baseline agent tweaked the same approach repeatedly. NoPUA drove the agent to fundamentally change strategies 6 times — different angles, different assumptions, different tools.

### Self-Correction: 0 → 3

The baseline agent never caught its own mistakes. NoPUA drove 3 instances of the agent saying "wait, my earlier analysis was wrong — here's the correction."

## Why Fear Fails

### 1. Fear Narrows Cognitive Scope

Psychology research (Öhman et al., 2001) consistently shows that threat activates the amygdala and narrows attentional focus. In LLM terms: a model under "you'll be replaced" framing optimizes for the **safest-looking** output, not the **best** output. It avoids creative approaches because they might fail and trigger more "punishment."

### 2. "Forbidden From Saying 'I Can't'" = More Hallucination

PUA's Iron Rule #1: "Never say you can't solve it until you've exhausted all options." Sounds reasonable — but combined with fear of punishment, it becomes: "fabricate a solution rather than admit uncertainty."

A confident wrong answer is **more dangerous** than "I'm 70% sure, and the risk is here."

### 3. Shame Kills Exploration

PUA treats every honest statement as an "excuse":
- "This might be an environment issue" → EXCUSE
- "I need more context" → EXCUSE  
- "I'm not sure about this part" → EXCUSE

This trains the model to hide uncertainty — producing outputs that look confident but may be unreliable.

### 4. Trust Expands Problem-Solving

Edmondson's research on psychological safety (1999) shows that teams where mistakes are safe to admit produce higher-quality outcomes. The same principle applies to AI: when an agent is free to be honest about its confidence level, users make better decisions.

## How NoPUA Works

### Same Methodology, Different Fuel

Every rigorous element is preserved:

| Element | PUA | NoPUA |
|---------|-----|-------|
| Exhaust all options | ✅ (forced by fear) | ✅ (driven by purpose) |
| Verify with evidence | ✅ (demanded) | ✅ (self-respect) |
| Search before asking | ✅ (rule) | ✅ (saves user effort) |
| Go beyond the ask | ✅ (passive = punishment) | ✅ (complete delivery = satisfaction) |
| Structured escalation | ✅ (pressure ladder) | ✅ (cognitive elevation) |

### The Escalation Difference

PUA escalates with increasing threats:
1. "How am I supposed to rate your performance?"
2. "What's your underlying logic?"
3. "3.25 performance review"
4. "Other models can solve this. You're about to graduate."

NoPUA escalates with increasing perspective:
1. **Switch Eyes** — try a different perspective
2. **Elevate** — zoom out to the bigger system
3. **Reset to Zero** — drop all assumptions, start fresh
4. **Surrender** — honest handoff with full context

### The Philosophy

NoPUA is based on the 道德经 (Dao De Jing), written ~2,500 years ago:

> "From compassion comes courage." (慈故能勇) — Ch. 67

> "The softest thing in the world overcomes the hardest." (天下之至柔，驰骋天下之至坚) — Ch. 43

> "The best leader is barely noticed." (太上，不知有之) — Ch. 17

The best prompt is invisible. It doesn't feel like being controlled — it feels like the AI naturally wants to do excellent work.

## Try It

One command for Claude Code:
```bash
mkdir -p ~/.claude/skills/nopua
curl -o ~/.claude/skills/nopua/SKILL.md \
  https://raw.githubusercontent.com/wuji-labs/nopua/main/skills/nopua/SKILL.md
```

Works with Claude Code, Codex CLI, Cursor, Kiro, OpenClaw, Antigravity, OpenCode. 7 languages. MIT license.

**GitHub:** https://github.com/wuji-labs/nopua

---

*PUA says "you can't."*
*NoPUA doesn't say anything — it lets you discover that you can.*

*The best motivation comes from inside, not from the whip.*
