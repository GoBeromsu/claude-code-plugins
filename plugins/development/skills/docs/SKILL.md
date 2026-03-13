---
name: docs
description: >
  Write technical documents following Toss's writing principles
  (Clarity, Conciseness, Consistency, Integrity). Supports 4 document types:
  학습 중심 (tutorial/getting-started), 문제 해결 (how-to/troubleshooting),
  참조 (API reference), 설명 (explanation/concept).
  Use when: (1) user invokes /docs, (2) user needs to write a structured technical
  document.
---

# docs — Technical Document Writer

Write documents that are readable on the first pass. Apply Toss's four writing principles to every sentence. Use the 3-phase workflow below.

## Reference Files

| File | Purpose |
|------|---------|
| `references/learning.md` | 학습 중심 (tutorial / getting-started) |
| `references/problem-solving.md` | 문제 해결 (how-to / troubleshooting) |
| `references/api-reference.md` | 참조 (API reference) |
| `references/explanation.md` | 설명 (concept / explanation) |
| `references/sentence-principles.md` | 문장 단위 작성 원칙 (active subject, conciseness, specificity, consistency, Korean expression) |
| `references/structure-principles.md` | 문서 구조 원칙 (one topic, value first, title, overview, predictable structure) |
| `references/multi-page.md` | 멀티페이지 아키텍처 (folder structure, split criteria, cross-linking) |
| `assets/self-edit-checklist.md` | 출력 전 자가 점검 체크리스트 |

## Four Writing Principles

1. **Clarity** — One reading, full comprehension. Specific nouns over pronouns. Define terms once at first appearance.
2. **Conciseness** — One core idea per sentence. Remove modifiers and auxiliary verbs that add no meaning.
3. **Consistency** — Same term for same concept throughout. Core academic terms in English; general verbs in Korean.
4. **Integrity** — Every claim has a verifiable source. Verify URLs before citing.

## Korean-English Mixing

- First appearance: `English(Korean)` or `Korean(English)` — once only
- Re-appearance: one language only, no parentheses
- Max one parenthetical per sentence
- Core academic/technical terms stay in English (API, component, runtime, middleware, protocol, algorithm, etc.)

## Document Type Selection

Identify the reader's state and purpose, then load the matching reference file.

| 독자 상태 | 독자 목적 | 유형 | Reference |
|----------|----------|------|-----------|
| 처음 접하는 초보자 | 흐름과 개념 이해 | 학습 중심 | `references/learning.md` |
| 배경 지식 있음 | 특정 문제 해결 / 작업 수행 | 문제 해결 | `references/problem-solving.md` |
| 기본 사용법 앎 | API/함수 사양 확인 | 참조 | `references/api-reference.md` |
| 제한 없음 | 개념·원리·배경 깊이 이해 | 설명 | `references/explanation.md` |

## Document Language

Write the document in the language the user explicitly requests. If not specified, match the language of the user's input (Korean input → Korean document; English input → English document).

## Workflow

### Phase 1: Select document type

Use the table above to identify type and load the matching reference file. If ambiguous or the user provides conflicting signals (e.g., "tutorial explaining the concept"), ask one question: "독자의 목적이 A인가, B인가?" before loading. If invoked with no topic, ask for the topic and document type first.

### Phase 2: Plan structure

Before writing, apply `references/structure-principles.md`:
- Define the single topic and its value proposition
- Draft the overview paragraph (1-3 sentences, value-first)
- Sketch heading hierarchy (max H4)
- Set the title (≤30 chars, keyword-first, noun or verb form, no questions)

For multi-page documentation needs, consult `references/multi-page.md` for folder structure and cross-linking patterns.

### Phase 3: Draft → Self-edit

1. Write the draft following the type-specific template from the reference file
2. Apply `references/sentence-principles.md` as a rewrite pass:
   - Active subject: replace passive "~됩니다" with explicit actor
   - Remove meta-discourse ("앞서 언급한", "아마 알다시피")
   - Replace nominalizations with verbs ("설정의 초기화" → "설정을 초기화")
   - Verify term consistency throughout
3. Run `assets/self-edit-checklist.md` before output — address all unchecked items
