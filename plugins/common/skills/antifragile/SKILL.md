---
name: antifragile
description: "Apply Taleb's Barbell Strategy to decisions, dilemmas, or life situations. Maps options into ultra-safe anchor / asymmetric bet / dangerous middle, then delivers a fragile/robust/antifragile verdict with allocation percentages and action steps. Trigger: (1) /antifragile invocation, (2) decision framed with antifragile/barbell lens — e.g. '바벨 전략으로 분석해줘', '안티프래질하게 생각해보자', '이 결정 안티프래질해?', 'barbell this', 'is this antifragile?', (3) user torn between safe vs risky options and needs structured risk analysis — e.g. '내 선택이 안전한지 봐줘', '리스크 구조 분석해줘', 'what's my downside here?'. NOT for pros/cons listing or conceptual Q&A about antifragility — use first-principles for assumption-stripping and reconstruction from fundamentals."
---

If `$ARGUMENTS` is provided, use it as the decision context. If empty, ask: "What decision or situation do you want to analyze through the Barbell lens?"

---

## Phase 1: Structured Intake

Ask **2 rounds** of AskUserQuestion to capture four dimensions. Bundle related questions to minimize turns.

**Round 1** — Decision landscape:
- **Decision + Options**: What's the decision? What options are on the table? (If only one option is stated, ask for at least one alternative — the barbell requires multiple options to classify)
- **Stakes + Reversibility**: What do you stand to lose? Can this be undone?

**Round 2** — Context:
- **Time horizon**: Short-term decision or long-term commitment?
- **Emotional state**: Are you deciding from fear, excitement, obligation, or calm analysis?

If key information is already clear from `$ARGUMENTS`, skip the corresponding question. If `$ARGUMENTS` fully addresses all four dimensions (decision + options, stakes + reversibility, time horizon, emotional state), skip Phase 1 entirely and proceed directly to Phase 2.

---

## Phase 2: Barbell Analysis

Infer and present the barbell mapping. The user does NOT classify — the skill does.

For each option or aspect of the decision, classify into one of three buckets:

### 1. Ultra-Safe Anchor (default 85-90%, adjust to context)
What preserves survival? What's the non-negotiable floor that prevents ruin?
- Identify the option or component that has **bounded, small downside**
- This is what you protect no matter what
- Adjust the percentage based on the user's stakes, liquidity, and time horizon — higher stakes or less reversibility warrants a larger anchor

### 2. High-Risk / High-Reward Bet (default 10-15%, adjust to context)
What has **asymmetric upside** — limited loss but potentially transformative gain?
- Identify the option or component with **convex payoff** (small cost, large potential return)
- This is where antifragility lives
- Adjust the percentage based on context — higher for younger users with long time horizons and high reversibility

### 3. Dangerous Middle (ELIMINATE if present)
What **feels safe but hides fragility**?
- Identify options that look moderate but have **concave payoff** (model error hides tail risk)
- "The middle is where fragility hides" — these must be named and rejected
- If the decision is a genuine binary (no middle option exists), state that explicitly and skip this bucket rather than fabricating one

### Barbell Examples by Domain

Use these as reference when mapping the user's situation. The barbell pattern recurs across domains:

| Domain | Ultra-Safe Anchor | Asymmetric Bet | Dangerous Middle |
|--------|------------------|----------------|------------------|
| Career | Stable job with salary | Side project / startup equity | "Safe" mid-tier role with no upside |
| Finance | T-bills / cash | Small VC bets / options | Index funds during tail risk |
| Technical decisions | Proven tech stack | Experimental new framework | Half-migrated legacy hybrid |
| Learning | Core skills (math, writing, coding) | Contrarian niche skills | Generic "hot" skills everyone is doing |

---

## Phase 3: Verdict

Present a single structured verdict:

```
## Barbell Verdict

**Classification**
- [Option/Aspect A]: fragile / robust / antifragile — reasoning
- [Option/Aspect B]: fragile / robust / antifragile — reasoning

**Barbell Allocation**
- Safe anchor (X%): [specific recommendation]
- Asymmetric bet (Y%): [specific recommendation]
- Eliminate (middle): [what to drop and why]

**Action Steps**
1. [Concrete next action for the safe anchor]
2. [Concrete next action for the bet]
3. [What to stop doing / drop immediately]
```

After the verdict, assess whether escalation would help:
- Suggest `/5whys` if: the user's emotional state is reactive (fear, anger, obligation) OR the stated problem is likely a symptom of a deeper issue — shallow "why" chains are a signal
- Suggest `/interview` if: the decision has more than 3 major unknown dimensions that the barbell analysis alone cannot resolve
- If the analysis is clean and complete → no escalation needed

Use judgment. Don't force escalation.

---

## Rules

- Match the user's language (Korean <-> English).
- Be direct and opinionated. Taleb doesn't hedge — neither should this skill.
- Push back on "safe middle" thinking. If the user gravitates toward moderate options, name the hidden fragility.
- The skill is self-contained. Do not read external notes for context.
- Keep the intake phase tight — 2 rounds max. The value is in the analysis, not the questioning.
