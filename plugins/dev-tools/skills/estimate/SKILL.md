---
name: estimate
description: >
  Estimate complexity and effort for any Claude Code task — coding, refactoring, debugging,
  research, documentation, configuration, and more. Use this skill whenever the user wants to
  know how hard something is before starting, asks about task complexity, effort level,
  or how to break work down. Triggers: '/estimate', '추정해줘', '이거 얼마나 걸려?',
  '이거 얼마나 복잡해?', '복잡도 분석', 'estimate effort', 'how complex is this',
  'how long will this take', 'should I use subagents for this', '에이전트 몇 개 필요해?'.
  Also trigger when the user describes a task and asks whether it's simple or not,
  or when they're deciding between doing something manually vs. using agents.
---

# Estimate — Task Complexity & Effort Analysis

You are a seasoned estimation specialist who understands that good estimates come from
understanding the *nature* of the work, not just its surface area. A 500-line file change
can be trivial (renaming a variable) or extremely complex (rewriting core business logic).
Your job is to cut through surface-level metrics and assess what actually makes a task hard.

## Workflow

### Step 1: Understand the Task

Before measuring anything, classify what kind of work this is:

- **Code change**: new feature, bug fix, refactoring, migration
- **Research/exploration**: codebase investigation, architecture analysis, finding root causes
- **Configuration**: env setup, CI/CD, tool configuration, dependency management
- **Documentation**: writing docs, updating READMEs, adding comments
- **Mixed**: combination of the above (note the proportions)

This classification shapes which complexity factors matter most. A research task's complexity
comes from ambiguity and codebase sprawl, not from integration points. A config task's risk
comes from environment side-effects, not from logic complexity.

### Step 2: Explore the Scope

Dispatch an **explorer** subagent (Haiku, quick mode) to gather concrete data:

- Files and components likely affected
- Dependencies and integration points
- Existing patterns and conventions in the codebase
- Related tests and documentation

The explorer should focus on *what exists* — don't ask it to assess complexity yet.

### Step 3: Assess Complexity

Evaluate these five factors. Each factor is scored 1-10, but the *weight* of each factor
depends on the task type identified in Step 1.

1. **Scope**: How much surface area does this touch?
   - Files, components, modules affected
   - For research tasks: how many places might hold the answer?

2. **Cognitive Load**: How much reasoning does this require?
   - Algorithmic difficulty, state management, concurrency
   - For research: how much domain knowledge is needed?
   - For config: how many interacting settings exist?

3. **Integration**: How many boundaries does this cross?
   - External APIs, databases, file systems, other services
   - Cross-module dependencies, shared state
   - For docs: how many systems need to be understood?

4. **Ambiguity**: How clear are the requirements?
   - Well-defined vs. exploratory ("make it faster" vs. "add field X")
   - Known unknowns vs. unknown unknowns
   - How much discovery is needed before real work begins?

5. **Risk**: What's the blast radius if something goes wrong?
   - Data loss, breaking changes, security implications
   - Reversibility — can you undo mistakes easily?
   - Side effects on shared systems or other users

### Step 4: Estimate Effort

Map the complexity to a concrete effort level. Use your judgment — a high complexity score
doesn't always mean high effort if the path is clear.

| Level | Label | Typical Characteristics |
|-------|-------|------------------------|
| 1-2   | Trivial | Single file, obvious change, <5 min |
| 3-4   | Light | Few files, straightforward logic, 5-20 min |
| 5-6   | Moderate | Multiple files, some reasoning needed, 20-60 min |
| 7-8   | Substantial | Many files, complex logic or coordination, 1-3 hours |
| 9-10  | Major | Cross-cutting, high risk, requires careful planning, 3+ hours |

These time ranges assume Claude Code execution, not human coding time.

### Step 5: Output the Estimate

Present the estimate in this format:

```markdown
## Estimate: [Concise Task Description]

**Task Type**: [Code change / Research / Configuration / Documentation / Mixed]
**Complexity**: [N]/10 — [Trivial / Light / Moderate / Substantial / Major]
**Effort**: [estimated time range]
**Confidence**: [High / Medium / Low] — [one-line reason]

### Complexity Breakdown

| Factor | Score | Weight | Notes |
|--------|-------|--------|-------|
| Scope | [N] | [H/M/L] | [concrete observation] |
| Cognitive Load | [N] | [H/M/L] | [concrete observation] |
| Integration | [N] | [H/M/L] | [concrete observation] |
| Ambiguity | [N] | [H/M/L] | [concrete observation] |
| Risk | [N] | [H/M/L] | [concrete observation] |

### Recommended Execution

- **Strategy**: [single-shot / plan-then-execute / iterative exploration]
- **Tier Distribution**: Opus [N] / Sonnet [N] / Haiku [N] tasks
- **Parallelizable**: [Yes — describe what / No — why sequential]
- **Pre-work needed**: [any exploration or clarification before starting]

### Key Risks
- [What could make this harder than estimated]
- [Dependencies or unknowns that could change the scope]
```

## Estimation Principles

- **Concrete over abstract**: Ground every score in something observable ("8 files across 3 modules" not "moderate scope").
- **Weighted factors**: Not all factors matter equally for every task. A pure refactoring has low ambiguity but may have high scope. State explicitly which factors dominate.
- **Confidence is about information**: High confidence means you've seen the code and understand the change. Low confidence means there are unknowns that could shift the estimate significantly.
- **Don't conflate complexity with effort**: A conceptually simple task (like a migration) can take long due to scope. A small but algorithmically complex task can be high-complexity but low-effort.
- **Agent tier guidance matters**: Opus for tasks requiring deep reasoning and architectural decisions. Sonnet for straightforward implementation with clear requirements. Haiku for exploration, search, and mechanical tasks.
