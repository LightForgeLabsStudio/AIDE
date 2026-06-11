# Documentation Principles

Authoritative design principles for AIDE documentation. Adapted from [Build-A-Better-Business/docs-template](https://github.com/Build-A-Better-Business/docs-template); pairs with [DOCUMENT_TAXONOMY.md](DOCUMENT_TAXONOMY.md).

**Audience:** primarily AI coding agents, secondarily human contributors. Optimize for reliable agent execution while remaining easy for humans to read.

## Core Principles (priority order)

1. **Speed** — readers reach the canonical source in one or two hops. Put frequently needed content where the reader already is; move rare detail behind on-demand pointers.
2. **Context efficiency** — load only what the task needs. One fact, one home; pointers everywhere else.
3. **Token cost** — verbose reference material lives off the default reading path; pair it with token-efficient summaries when agents need it often.

When principles conflict: speed for common workflows > context efficiency for edge cases > canonical-source discipline over convenience.

## Document Patterns

- **Pointer docs** — link hubs, no normative content (e.g. `START_HERE.md`). Change when navigation changes.
- **Canonical docs** — single source of truth (specs, conventions). Duplicated nowhere, updated in one place.
- **On-demand guides** — workflow narratives off the default path; may repeat small snippets for readability but defer to canonicals for rules.
- **Token-efficient summaries** — condensed agent versions of verbose sources; must state they are non-authoritative, link the source, and stay synchronized.

## Anti-Patterns

- Duplicating facts across files
- **Stub files that defer to the `.aide/` submodule for their substance** — projects instantiate real files from templates instead
- Plan/status documents that duplicate the issue tracker
- Transient work artifacts (session handoffs, PR findings files) filed as documentation
- Living and dated content mixed in one folder — the living set must stay small and obvious
- Restating general engineering knowledge as repo-specific convention
- Orphaned docs with no path from a navigation doc

## Decision Framework

When adding documentation, ask:

1. Is this system truth (→ spec), a hard-to-reverse choice (→ ADR), execution detail (→ issue), or learning (→ evaluation)?
2. Is it already authoritative elsewhere? Link, don't copy.
3. Does it claim to be current? Then it joins the living set — keep that set small.
4. Would a competent agent already do this without being told? Then omit it.

## Preventing Drift

- One fact, one home; link instead of copy.
- Dated records never get content edits after the fact (status lines only).
- The closing step of work that changes invariants is updating the relevant living spec.
- Update navigation docs when files move.
