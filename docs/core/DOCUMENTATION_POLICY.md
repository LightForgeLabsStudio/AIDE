# Documentation Policy

Keep docs lean, consistent, and authoritative.

## Sources of Truth

Define your project's documentation hierarchy:

- **README.md**: User/player-facing basics (install, run, key features)
- **{{PROJECT_SUMMARY_DOC}}**: High-level project overview and current state
- **{{DEVELOPMENT_DOC}}**: Architecture and how to extend/debug
- **{{CONTRIBUTING_DOC}}**: Workflow, specs, testing, review process
- **{{SPECS_DIRECTORY}}**: Feature or debugging specs for larger changes

Customize this list to match your project's structure.

## Update Rules

- Update only the relevant sources; avoid duplicating the same details across multiple files
- When behavior changes, touch the single best place (README for users, {{DEVELOPMENT_DOC}} for developers)
- Do not remove or rewrite existing tests without explicit approval
- Confirm with the requester before initiating large refactors or cross-cutting doc reorganizations
- Align on intent and testing scope before commits/PRs (no surprise changes)

## Changelog Policy

During active development, git commits serve as the technical changelog. Commit messages should be descriptive and include what was tested.

A formal `CHANGELOG.md` is optional and should be added when preparing for public releases or when the project reaches a stable milestone. If created, changelog entries should include:
- Version number and date
- Summary of changes (new features, fixes, breaking changes)
- Tests run or manual verification performed

## Adding/Editing Docs

- Add a brief feature summary and implementation approach in specs/PRs before coding
- Prefer links/references to existing sections instead of copy/pasting content
- Note known gaps or future work where applicable

## Allowed Exceptions to No-Duplication Policy

In rare cases, duplication is permitted when there is a clear operational benefit that outweighs the maintenance cost:

### Token Optimization for Agents

**Exception:** Quick reference documents (e.g., `DESIGN_QUICK_REFERENCE.md`, `API_QUICK_REFERENCE.md`)

- **Purpose:** Condensed summaries for agent token efficiency
- **Justification:** Reading full docs (10,000+ tokens) vs quick reference (500 tokens) = 95%+ reduction
- **Requirements:**
  - Must clearly state it is NOT authoritative
  - Must link to authoritative sources
  - Must be kept synchronized when source docs change
  - Must cover ALL relevant topics (not selective)

**Agent Token Economy Best Practices:**

All agent primer files should prioritize token efficiency to maximize context budget for code analysis and implementation. See `.aide/docs/agents/AGENT_TOKEN_ECONOMY.md` for comprehensive strategies.

- **Prefer concise directives over verbose explanations**
- **Use bullet points and checklists instead of paragraphs**
- **Reference authoritative docs instead of duplicating content**
- **Front-load critical information (most important rules first)**
- **Use quick reference documents when available**
- **Avoid redundant examples (one clear example > three similar ones)**

### ~~Implementation State Tracking~~ (DEPRECATED)

**Former Exception:** `IMPLEMENTATION_STATUS.md` (deprecated as of AIDE v1.1)

- **Replaced by:** GitHub Issues/PRs/Epics (query via `gh` CLI)
- **Rationale:** Static markdown files fall out of sync. GitHub is the actual canonical state and auto-updates on PR merge.
- **Migration:** Use GitHub CLI queries instead of reading stale markdown:
  ```bash
  gh issue list --label "status:in-progress" --state open  # Current work
  gh pr list --state open                                   # Active PRs
  gh issue list --label "status:ready" --state open        # Ready to implement
  ```
- **See:** [GITHUB_QUERIES.md](../agents/GITHUB_QUERIES.md) for comprehensive query reference

**Recommendation:** Use GitHub as single source of truth for implementation state. Agents query current state dynamically rather than reading snapshot documents.

**When to add new exceptions:**
- Operational benefit must be significant and measurable
- Exception must be explicitly documented here
- Must include synchronization requirements
- Prefer references over duplication whenever possible

## Customization for Your Project

Replace these placeholders with your actual documentation structure:

- `{{PROJECT_SUMMARY_DOC}}` → `docs/PROJECT_SUMMARY.md` or `docs/OVERVIEW.md`
- `{{DEVELOPMENT_DOC}}` → `docs/DEVELOPMENT.md` or `docs/ARCHITECTURE.md`
- `{{CONTRIBUTING_DOC}}` → `docs/CONTRIBUTING.md` or `CONTRIBUTING.md`
- `{{SPECS_DIRECTORY}}` → `docs/specs/`, `docs/rfcs/`, `docs/adr/`
- `{{IMPLEMENTATION_STATUS_QUERY}}` → `gh issue list --label "status:in-progress"` (see [GITHUB_QUERIES.md](../agents/GITHUB_QUERIES.md))
- `{{PROJECT_DESIGN_DOCS}}` → `docs/design/`, `docs/specs/`, `docs/architecture/`
