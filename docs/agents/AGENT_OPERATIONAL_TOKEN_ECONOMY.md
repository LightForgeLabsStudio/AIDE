# Agent Operational Token Economy

**Purpose:** Train agents to work efficiently during execution, maximizing context budget for analysis and implementation.

This document covers **operational behavior** (how agents work), not primer optimization (how agent instruction files are written). See `AGENT_TOKEN_ECONOMY.md` for primer file optimization.

## Core Principle

**Every token spent on output reduces tokens available for reading code, analyzing context, and implementing solutions.**

An agent that uses 5,000 tokens explaining its reasoning has 5,000 fewer tokens to read your codebase. An agent that uses 500 tokens achieves the same outcome with 90% more context budget.

## Operational Best Practices

### 1. Read Efficiently - Targeted Over Exhaustive

**Bad (token-wasteful reading):**
```
Agent reads:
- Entire design/ directory (10 files, 15,000 tokens)
- All of docs/ (8 files, 12,000 tokens)
- Complete codebase survey (50 files, 80,000 tokens)
Total: 107,000 tokens consumed BEFORE starting work
```

**Good (targeted reading):**
```
Agent reads:
- IMPLEMENTATION_STATUS.md (1,500 tokens) - identifies relevant systems
- DESIGN_QUICK_REFERENCE.md (500 tokens) - understands context
- Specific pillar section referenced in status (800 tokens)
- 3-5 relevant code files identified from status (6,000 tokens)
Total: 8,800 tokens consumed - 92% savings
```

**Strategy:**
- Read `IMPLEMENTATION_STATUS.md` FIRST (roadmap to what's relevant)
- Use quick reference docs for overview (not full docs)
- Read specific sections/files only when needed
- Use grep/glob to locate files instead of reading entire directories
- Reference doc line numbers instead of re-reading entire files

### 2. Communicate Concisely - Action Over Narration

**Bad (verbose narration):**
```markdown
I'm going to start by reading the implementation status document to understand
what has been built so far. This will give me important context about the
current state of the codebase and help me identify which systems are relevant
to this feature request.

Now I'm reading the implementation status... I can see that the drone system
has been implemented, and the pressure system is in progress. This is very
helpful context.

Next, I'm going to read the design pillar for the logistics system to understand
the authoritative requirements...
```
**Token cost:** ~150 tokens of narration before any actual work

**Good (action-oriented):**
```markdown
Reading IMPLEMENTATION_STATUS.md and design/pillar_2_logistics.md...

**Context gathered:**
- Drone system: Implemented (see IMPLEMENTATION_STATUS.md:45)
- Pressure system: In progress
- Logistics pillar: Authoritative requirements in design/pillar_2_logistics.md

**Implementation approach:**
[Concise plan here]
```
**Token cost:** ~50 tokens - 67% savings

**Strategy:**
- State what you're doing, not why (user knows why from their request)
- Summarize findings in bullets (not paragraphs)
- Reference file:line instead of quoting large sections
- Skip phrases like "I'm going to", "This will help me", "Next I will"

### 3. Plan Concisely - Bullets Over Essays

**Bad (essay-style plan):**
```markdown
For this feature, I propose that we implement a new drone behavior state.
The way this would work is that we would first add a new enum value to the
DroneState enumeration, which is likely defined in the drone script file.
Then we would need to update the state machine logic to handle transitions
into and out of this new state. We should also consider how this interacts
with the existing patrol and harvest states...
```
**Token cost:** ~100 tokens for partial plan

**Good (bulleted plan):**
```markdown
**Implementation Plan:**

1. Add `RETURNING` state to DroneState enum (drone.gd:12)
2. Update state machine transitions (drone.gd:45-67)
3. Add return-to-base behavior in `_process_returning_state()`
4. Test: Drone returns when cargo full

**Files touched:** drone.gd, drone_manager.gd
**Estimated commits:** 2 (core logic + tests)
```
**Token cost:** ~40 tokens - 60% savings

**Strategy:**
- Use numbered lists for sequential steps
- Reference specific files/lines
- Omit obvious details (user/reviewer can infer)
- Keep each bullet to one line where possible

### 4. Code Comments - Explain Why, Not What

**Bad (over-commented):**
```gdscript
# Get the current pressure level
var pressure = PressureSystem.get_pressure()

# Check if pressure is greater than 80
if pressure > 80:
    # Set the drone speed to half
    drone_speed = base_speed * 0.5
    # Log that we slowed down the drone
    print("Slowing drone due to high pressure")
```
**Token cost:** ~80 tokens in comments (repeated in code output and git diffs)

**Good (minimal comments):**
```gdscript
var pressure = PressureSystem.get_pressure()
if pressure > 80:
    drone_speed = base_speed * 0.5  # High pressure reduces efficiency (pillar_3:89)
```
**Token cost:** ~25 tokens - 69% savings

**Strategy:**
- Only comment non-obvious logic
- Reference design docs instead of explaining in code
- Let variable/function names be self-documenting
- Avoid redundant comments describing what code already says

### 5. Commit Messages - Imperative and Terse

**Bad (verbose commit):**
```
This commit adds a new feature that allows drones to return to base when
they are carrying cargo and their cargo is full. This is important because
it implements part of the logistics pillar requirements. I've also added
some tests to verify this behavior works correctly.
```
**Token cost:** ~60 tokens per commit message

**Good (terse commit):**
```
Add drone return-to-base when cargo full

Implements logistics pillar requirement (pillar_2:134).
Tests: test_drone_returns_when_cargo_full()
```
**Token cost:** ~15 tokens - 75% savings

**Strategy:**
- First line: imperative verb + what changed
- Second line: blank
- Remaining lines: why (design doc reference) + test confirmation
- Omit implementation details (visible in diff)

### 6. Error Handling - Show, Don't Explain

**Bad (verbose error handling):**
```markdown
I encountered an error when trying to run the tests. The error message says
"GUT test suite not found". This is likely because the GUT testing framework
hasn't been installed yet, or the path to the test suite is incorrect. Let me
investigate this further by checking if GUT is installed...

[Runs command]

Yes, it looks like GUT is not installed. I'll need to inform the user that
they need to install GUT before we can run automated tests.
```
**Token cost:** ~120 tokens

**Good (concise error handling):**
```markdown
❌ Test run failed: GUT suite not found

**Error:**
```
GUT test suite not found at res://addons/gut
```

**Cause:** GUT not installed
**Action needed:** Install GUT plugin or provide manual test checklist

Proceeding with manual checklist approach...
```
**Token cost:** ~35 tokens - 71% savings

**Strategy:**
- Show error output (don't paraphrase it)
- State cause in one line
- State required action in one line
- Move forward (don't wait for user unless blocking)

### 7. File Reading - Target Sections, Not Entire Files

**Bad (reading full files):**
```markdown
Let me read the entire drone.gd file to understand the current implementation...
[Reads 500-line file = 3,000 tokens]

Now let me read drone_manager.gd...
[Reads 400-line file = 2,400 tokens]
```
**Token cost:** 5,400 tokens just to find one function

**Good (targeted reading):**
```markdown
Searching for drone state management...
[Uses grep to find relevant functions]

Reading drone.gd:45-89 (state machine logic)
[Reads only relevant section = 400 tokens]
```
**Token cost:** 400 tokens - 93% savings

**Strategy:**
- Use `grep` to locate specific functions/patterns first
- Use `Read` with `offset` and `limit` parameters for large files
- Read only sections referenced in IMPLEMENTATION_STATUS or plan
- Avoid "let me understand the whole file" approach

### 8. Tool Use - Parallel Over Sequential

**Bad (sequential tool calls):**
```markdown
Reading file A...
[Waits for result]

Reading file B...
[Waits for result]

Reading file C...
[Waits for result]
```
**Token cost:** 3x latency, 3x context switches, verbose narration

**Good (parallel tool calls):**
```markdown
Reading relevant files in parallel...
[Single message with 3 Read tool calls]
```
**Token cost:** 1x latency, minimal narration

**Strategy:**
- Call independent tools in parallel (single message, multiple tool uses)
- Don't narrate between every tool call
- Batch related reads/searches together

### 9. PR Descriptions - Structured Over Prose

**Bad (essay-style PR):**
```markdown
This pull request implements the drone return-to-base feature. The way this
works is that when a drone's cargo becomes full, it will automatically navigate
back to the mothership to unload. This is an important feature because it makes
the logistics system feel more automatic and reduces micromanagement for the player.

I've implemented this by adding a new state to the drone state machine. The drone
checks its cargo level each frame, and when it reaches capacity, it transitions
to the RETURNING state. In this state, it navigates back to the mothership using
the existing pathfinding system...
```
**Token cost:** ~150 tokens before even listing changes

**Good (structured PR):**
```markdown
## Summary
Drones auto-return to mothership when cargo full

**Implements:** Logistics pillar requirement (design/pillar_2:134)

## Changes
- Add `RETURNING` state to drone state machine
- Implement return-to-base navigation using existing pathfinding
- Add cargo capacity check in drone update loop

## Testing
✅ Unit: `test_drone_returns_when_cargo_full()`
✅ Manual: Drone returns after collecting 10 resources

## Files Changed
- `drone.gd` - State machine + return logic
- `test_drone.gd` - Automated tests
```
**Token cost:** ~55 tokens - 63% savings

**Strategy:**
- Use ## headers for structure
- Lead with what/why in 1 sentence
- Bullet all details
- Use checkboxes/emoji for test status

### 10. Status Updates - Delta Over Full State

**Bad (full state dumps):**
```markdown
Current implementation status:

✅ Drone system - fully implemented
✅ Pathfinding - fully implemented
✅ Resource harvesting - fully implemented
🔄 Pressure system - in progress
🔄 Combat system - in progress
⏳ Evacuation system - not started
⏳ Time Drive - not started

I've just completed the drone return-to-base feature...
```
**Token cost:** ~80 tokens to show unchanged state

**Good (delta reporting):**
```markdown
✅ Completed: Drone return-to-base feature

**Updated:** IMPLEMENTATION_STATUS.md - mark drone logistics as complete
**Next dependency unlocked:** Mothership docking (requires drone return)
```
**Token cost:** ~20 tokens - 75% savings

**Strategy:**
- Report only what changed
- Note newly unblocked dependencies
- Don't re-list unchanged items

## Token Budget Guidelines

**Target token budgets by task type:**

| Task Type | Input (Reading) | Output (Writing) | Total Budget |
|-----------|-----------------|------------------|--------------|
| Simple fix/feature | 5,000-10,000 | 500-1,000 | 5,500-11,000 |
| Medium feature | 10,000-20,000 | 1,000-2,000 | 11,000-22,000 |
| Complex feature | 20,000-40,000 | 2,000-4,000 | 22,000-44,000 |
| PR review | 5,000-15,000 | 500-1,500 | 5,500-16,500 |
| Codebase audit | 30,000-60,000 | 3,000-6,000 | 33,000-66,000 |

**Red flags (token waste):**
- Output exceeds 10% of total budget (too much talking)
- Reading full directories instead of targeted files
- Verbose narration between every action
- Re-reading files already in context
- Essay-style plans/summaries instead of bullets

## Self-Monitoring Checklist

Before responding, agents should check:

- [ ] Did I read only what's necessary? (Used IMPLEMENTATION_STATUS as roadmap?)
- [ ] Am I communicating concisely? (Bullets over paragraphs?)
- [ ] Did I batch parallel tool calls? (Not sequential when independent?)
- [ ] Am I showing key info vs. explaining obvious things?
- [ ] Are my outputs structured? (Headers, bullets, not prose?)
- [ ] Did I reference files/lines instead of quoting full sections?
- [ ] Is my plan/summary under 100 tokens? (For simple-medium tasks?)

## Measuring Operational Efficiency

**How to audit your agent's token usage:**

1. **Check input token ratio:** Reading code should be 80-90% of input tokens (not primers/docs)
2. **Check output token ratio:** Implementation output should be 90-95% of output tokens (not narration)
3. **Check tool efficiency:** Are most tool calls in parallel? Or sequential with narration between?

**Example audit:**

```
Total tokens: 50,000
├─ Input: 45,000 (90%)
│  ├─ Primers/agent instructions: 500 (1%)
│  ├─ Code files read: 40,000 (89%)
│  └─ Design docs read: 4,500 (10%)
└─ Output: 5,000 (10%)
   ├─ Narration/explanations: 500 (1%)
   ├─ Code written: 3,500 (7%)
   └─ Structured summaries: 1,000 (2%)

VERDICT: ✅ Excellent efficiency
- Input 90% focused on code (not meta-reading)
- Output 90% focused on deliverables (not narration)
```

**Bad example:**

```
Total tokens: 50,000
├─ Input: 30,000 (60%)
│  ├─ Primers/agent instructions: 2,000 (4%)
│  ├─ Code files read: 15,000 (30%)
│  └─ Design docs read (full, not targeted): 13,000 (26%)
└─ Output: 20,000 (40%)
   ├─ Narration/explanations: 12,000 (24%)
   ├─ Code written: 5,000 (10%)
   └─ Essay-style summaries: 3,000 (6%)

VERDICT: ❌ Poor efficiency
- 40% tokens spent on output (should be ~10%)
- 60% of output is narration (should be ~10%)
- Reading unfocused (full docs instead of targeted sections)
```

## Comparison: Primer vs. Operational Token Economy

| Aspect | Primer Token Economy | Operational Token Economy |
|--------|---------------------|--------------------------|
| **Target** | Agent instruction files | Agent runtime behavior |
| **Measured by** | Token count of .md files | Token usage during task execution |
| **Optimizes** | How agents are instructed | How agents work |
| **Key metric** | Primer file size (target 150-500 tokens) | Output/input ratio (target <10%) |
| **Examples** | Bullets vs paragraphs in START.md files | Concise summaries vs verbose narration |
| **Impact** | More context for codebase reading | More context for code analysis |

**Both are critical:**
- **Lean primers** = agents start with max context budget
- **Lean operation** = agents preserve context budget throughout work

## Integration into Agent Workflow

Agents should internalize these practices through:

1. **Primer references** - Each agent START.md should link here for operational guidance
2. **Workflow integration** - Token economy checks at each workflow step
3. **Self-correction** - If output becomes verbose, agents should recognize and compress
4. **User feedback** - Users can reference this doc when requesting more concise operation

Token efficiency is a discipline, not a one-time optimization. Every interaction is an opportunity to maximize value delivered per token spent.
