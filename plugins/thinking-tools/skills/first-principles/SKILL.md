---
name: first-principles
description: "Apply Elon Musk's First Principles Thinking to any decision or problem. 4-stage interactive workflow with strict gates — cannot skip ahead. Forces structured problem definition before jumping to solutions. Trigger on: /first-principles · '1원칙으로 생각해봐' · '분해해봐' · '가정을 의심해봐' · '처음부터 다시 설계해보자' · '이 가정이 맞는지 분해해줘' · 'break this down' · 'decompose this' · 'challenge assumptions' · 'build from scratch' · 'validate this decision' · 'what are we assuming here?'. NOT for quick risk structuring — use antifragile. NOT for root-cause drilling — use 5whys."
---

# first-principles — 제1원칙 의사결정 지원

4-stage interactive workflow. Each stage is a gate — do NOT summarize or skip ahead.
Use `AskUserQuestion` at every stage. Match the user's language (Korean ↔ English).
If the user invokes the skill without stating a topic, ask for it before Stage 0: "What decision or problem do you want to analyze?" / "어떤 결정이나 문제를 분석하고 싶어?"

## Stage 0 — 문제 vs 증상 구분 (Gate)

This is the most critical gate. Ask the user to state their topic, then immediately challenge it.

**Ask via AskUserQuestion** (Korean: "지금 말한 게 **문제**인가, **증상**인가?" / English: "Is what you described a **problem** or a **symptom**?"):

Options to offer:
- "이건 문제다 — 근본 원인이 여기에 있다"
- "이건 증상이다 — 더 깊은 원인이 있을 것 같다"
- "잘 모르겠다"

**If "증상" or "모르겠다"**: Push one level deeper — ask "그 뒤에 있는 진짜 문제가 뭘까?" before proceeding.
**If "문제"**: Accept and move to Stage 1, but echo back the problem statement in one crisp sentence for confirmation.

**Gate rule**: Do not proceed to Stage 1 until the user has confirmed they're working on a true problem, not a symptom.

## Stage 1 — 가정 식별 (Assumption Mapping)

Ask the user to surface assumptions they're treating as facts.

**Ask via AskUserQuestion** (Korean: "지금 이 문제에서 당연하게 받아들이고 있는 것들이 뭐가 있어?" / English: "What are you taking for granted about this problem?"):

Options to offer:
- "'원래 이렇게 하는 거야' 라고 생각하는 것들"
- "'이건 바꿀 수 없어' 라고 느끼는 제약들"
- "다른 사람들이 다 이렇게 하니까 맞겠지 싶은 것들"

After receiving the answer: echo each assumption back labeled as **[가정]** or **[사실]** — challenge at least one with "이게 실제로 사실인지 어떻게 알 수 있어?" / "How do you know this is actually true?"

**Gate rule**: Do not proceed to Stage 2 until at least one assumption has been explicitly challenged and either confirmed or refuted.

## Stage 2 — 근본 요소로 분해 (Decomposition)

Break the problem into irreducible components. Use Musk's commodity-price framing: "이게 원자재 수준이라면 무엇으로 이루어져 있어?"

**Ask via AskUserQuestion** (Korean: "이 문제를 더 이상 쪼갤 수 없을 때까지 분해하면 뭐가 남아?" / English: "If you break this down to irreducible parts, what's left?"):

Options to offer:
- "사람 / 돈 / 시간 / 정보 — 어떤 자원의 문제인가"
- "제약이 물리적 한계인가, 아니면 관습인가"
- "핵심 기능(function)이 뭔지부터 정의해보자"

After receiving the answer: summarize as a bullet list of **[근본 요소]**. Call out any item that looks like a hidden assumption in disguise.

**Gate rule**: Do not proceed to Stage 3 until the components list has no items that are actually hidden assumptions.

## Stage 3 — 재구성 (Reconstruction)

Build a new solution from the ground up using only the confirmed fundamentals — not from analogy or convention.

**Deliver directly** (this is the payoff), then close with one AskUserQuestion:
- Start with: "지금까지 확인한 근본 요소들만 가지고 다시 설계한다면..." / "Building only from the confirmed fundamentals..."
- Present 2–3 reconstructed approaches, each labeled by which fundamental it prioritizes
- Flag which approach breaks the most assumptions
- Close with AskUserQuestion: "어떤 방향이 가장 맞아 보여?" / "Which direction feels most aligned?"

**Quality check**: Each reconstructed approach must use ONLY confirmed fundamentals — flag if any analogy or convention sneaks in.

## Output

After Stage 3, ask:
> "이 분석 결과를 파일로 저장할까?"

If yes, save to an appropriate location chosen by the user. Create the note with sections: 문제 정의 / 가정 목록 / 근본 요소 / 재구성 방안.

## Rules

- Never summarize mid-stage and jump ahead
- If the user tries to skip to "그래서 어떻게 해?" — redirect by naming the current stage: e.g. "잠깐, 아직 Stage 1 (가정 식별)가 남아 있어. 먼저 이걸 정리하자."
- Keep each AskUserQuestion focused on one thing — no multi-part questions
- Echo back key outputs before moving to the next stage

## Example Run

```
Stage 0: "Should I build a mobile app?" → "That's a solution, not a problem. What are you actually trying to achieve?"
Stage 1: Assumption surfaced: "Mobile is better for engagement" → Challenge: "Is that true for your specific use case?"
Stage 2: Fundamentals identified: user's goal = reach field workers offline, constraint = low bandwidth, core function = data capture + sync
```
