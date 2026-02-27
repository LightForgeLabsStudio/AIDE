# Token Economy

**Goal:** maximize context budget for code analysis and implementation; minimize waste on narration and bloat.

## Primer / Skill Files (design time)

Keep agent-facing docs lean:
- Bullets and checklists over paragraphs (~65% token savings)
- Reference authoritative docs; do not duplicate them
- Front-load critical constraints at the top of the file
- One clear example per concept

**Budgets:**

| Doc type | Load mode | Target |
| --- | --- | --- |
| AGENTS.md | Always-loaded | 300–800 tokens |
| SKILL.md | On-demand | 150–400 tokens |
| Tier 2 reference | On-demand | ≤50 lines |

**Red flags:** prose paragraphs, duplicated content, reference docs required before starting work.

## Runtime Operation (execution time)

**Read efficiently:**
- Query GitHub first — current state at ~200 tokens vs 8,000+ for snapshot docs
- Use grep/glob to locate files; read only relevant sections with `offset`/`limit`
- Batch independent tool calls in parallel (not sequential)

**Communicate concisely:**
- State what you're doing, not why
- Bullets with `file:line` references, not block quotes
- Skip filler: "I'm going to", "This will help me", "Next I will"
- Report only what changed (delta), not full state re-dumps

**Output in structured form:**
- Plans: numbered steps with specific file references
- PR descriptions: `## sections` and bullets, not prose paragraphs
- Errors: show the exact error output + one-line cause + one-line action

**Self-monitoring checklist:**
- [ ] Read only what's necessary? (GitHub query before file reads?)
- [ ] Communicating in bullets, not paragraphs?
- [ ] Batching parallel tool calls?
- [ ] Using `file:line` instead of quoting large sections?
- [ ] Plan and summary under ~100 tokens for simple tasks?
