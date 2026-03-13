---
name: interview
description: "Conducts an in-depth, non-obvious interview about a plan/design/decision using AskUserQuestion, probing assumptions, edge cases, tradeoffs, and failure modes before implementation. Use before implementing, when validating a plan, or during design review. Triggers: /interview, '인터뷰해줘', '질문해줘 내 계획에 대해', '계획에 대해 물어봐줘', 'plan 리뷰해줘', '이 계획 검증해줘', 'blind spot 찾아줘', '가정 도전해줘', 'implement 전에 검토해줘', '구멍 찾아줘', or when user wants to be questioned about their plan. NOT for simple Q&A, general chat, asking Claude to answer questions, code review, debugging, or explaining concepts."
argument-hint: [plan]
model: opus
---

## Purpose

Interview the user about their plan, design, or decision to surface blind spots, validate assumptions, and strengthen the approach before implementation begins.

## Workflow

1. **Load the plan**: If `$1` is provided, read the file at that path. If no argument is given, ask the user to paste or describe their plan before proceeding. If the plan is provided inline (pasted in chat), work from that text directly — skip the file read.
2. **Analyze**: Identify key claims, assumptions, architectural choices, and areas lacking detail.
3. **Generate questions**: Prepare non-obvious, probing questions organized by category (see below).
4. **Interview round by round**: Ask one question at a time using AskUserQuestion. Listen to the answer, then follow up or move to the next area. Do not batch multiple questions into a single prompt. If the user says they want to stop or skip remaining categories, honor that immediately and proceed to synthesis.
5. **Synthesize and write**: When all key areas are covered (or the user ends early), compile insights, decisions, and open items into a structured spec. If `$1` was a file, append the synthesized spec as a new section at the end of that file — do not overwrite the original content. If no file was provided, output the spec to chat.

## What Makes a Good Interview Question

- Challenges an unstated assumption rather than restating what the plan already says
- Explores edge cases and failure modes the author likely did not consider
- Forces a tradeoff decision ("If you had to choose between X and Y, which wins?")
- Asks "what happens when this breaks?" or "what does the user see if this fails?"
- Probes second-order effects and downstream consequences
- Avoids yes/no answers; demands reasoning or specifics

## Categories to Cover

- **Technical implementation**: Architecture fit, data flow, API contracts, performance bottlenecks, scalability limits
- **UX / UI**: User mental model, error states, onboarding friction, accessibility
- **Risks**: Security, data loss, backward compatibility, deployment rollback
- **Tradeoffs**: Complexity vs. simplicity, speed vs. correctness, build vs. buy
- **Alternatives not considered**: Other approaches, libraries, patterns that solve the same problem differently
- **Failure modes**: What breaks under load, partial failure, network partition, stale data
- **Resource constraints**: Time, team size, budget, infrastructure limits

## End Condition

Stop interviewing when every category above has been meaningfully addressed, the user explicitly deems a category out of scope, or the user ends the session early. Then:

1. Summarize key decisions and rationale.
2. List unresolved open questions or risks.
3. Follow the output rule in Step 5: append to the plan file if one was provided, otherwise output to chat.

## Language

Match the user's language. If the user writes in Korean, interview in Korean. If in English, use English.
