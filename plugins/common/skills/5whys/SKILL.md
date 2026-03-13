---
name: 5whys
description: "Run interactive root-cause analysis: ask one Why at a time via AskUserQuestion, going at least 5 rounds until the irreducible root cause emerges. Works for any domain — business, personal, technical, philosophical. Trigger on: /5whys, 5why, 5 why, 'why does this keep happening?', 'drill into why', 'root cause analysis', 'why is this a problem?', '왜 이런 거야?', '이게 왜 반복돼?', '왜 이게 문제야?', '근본 원인 찾고 싶어', '왜 그런지 파고들자', or when the user wants to recursively drill down into why something is the way it is. NOT for structured problem decomposition — use first-principles instead. NOT for open-ended question interviews — use interview instead."
---

If `$ARGUMENTS` is a file path, read it first. If it's a topic or description, use it directly. If empty, use AskUserQuestion to ask: "무엇에 대해 Why를 파고들까요?"

Then immediately ask **Why #1** using the `AskUserQuestion` tool. No preamble.

> **Note:** If the user already provided both the problem and its first-level cause in their initial message (e.g., "/5whys 배포가 늦어져 — QA에서 자꾸 막혀": problem = 배포가 늦어져, Why #1 answer = QA에서 자꾸 막혀), treat the stated cause as the answer to Why #1 and proceed directly to Why #2.

---

## Rules

- Use **AskUserQuestion tool** for every Why question — one question per turn.
- Provide 2–3 plausible answer directions as options to spark thinking, but the real answer almost always comes from "Other".
- Go at least 5 rounds. Keep going if the root hasn't emerged yet — stop only when the answer can't be reduced further.
- After each answer: echo the key insight in one line (in your message), then ask the next Why via AskUserQuestion.
- Push back on shallow answers. If the answer is generic or surface-level, probe harder in the next Why. Example: if the user says "커뮤니케이션이 부족해서" (communication was lacking), don't accept it — ask "커뮤니케이션의 어떤 부분이 부족했나요? 정보 공유? 의사결정 과정? 피드백 루프?" to force specificity.
- Match the user's language (Korean ↔ English).
- **When to stop:** Stop drilling when the answer is a clear root cause that cannot be meaningfully reduced further — typically a structural constraint, a missing system/process, a fundamental assumption, or a concrete action gap. If unsure, ask one more Why.
- **Non-answers:** If the user says "I don't know", "모르겠어", or gives no meaningful answer, offer 2–3 more specific framings of the same Why and ask again — do not skip the round or accept silence as an answer.

## After the final Why — Synthesize

Output in one message using headers that match the user's language:

If the session was in Korean:
- **근본 원인 / 핵심 진실** — the root, in one sentence
- **Why 체인** — numbered list showing how each Why led to the next
- **발견한 것** — what this reveals and what to do with it

If the session was in English:
- **Root Cause** — the root, in one sentence
- **Why Chain** — numbered list showing how each Why led to the next
- **Findings** — what this reveals and what to do with it

Then offer to write the result to a file.
