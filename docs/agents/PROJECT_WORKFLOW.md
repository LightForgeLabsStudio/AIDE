# Project workflow configuration

Before implementing, validating or reviewing, read the consuming project's root AGENTS.md. If it points to a workflow document, read that document too (convention: `docs/agents/workflow.md`). Project configuration and user instructions override AIDE defaults.

Resolve these values from those sources before dependent work:

| Value | Meaning |
| --- | --- |
| `MAIN_BRANCH` | PR base branch; default `main` |
| `VALIDATE_COMMAND` | Complete project gate, including any lint/smoke checks it owns |
| `LINT_COMMAND` | Separate lint command, only when needed outside the complete gate |
| `RUN_UNIT_TESTS_COMMAND` | Optional focused rules/unit command |
| `REVIEW_MODE` | `external` (default) or `independent-agent` |
| `REVIEWER` | External tool/session or configured independent reviewer |
| `REVIEW_COMMAND` | Project wrapper for submitting a review with decision, body file and reviewed SHA, if supported |

Existing `{{RUN_ALL_TESTS_COMMAND}}` mappings also resolve the full validation command. An unresolved required command is missing configuration, not a reason to guess a command or silently skip a gate. Run an identical resolved command once; do not rerun full validation under a second placeholder name. Focused checks do not replace the complete delivery gate.

**External review:** implementation ends with a draft PR and a head-specific review handoff. Another tool/session reviews and posts on GitHub. Accepted findings return to the implementation workflow. This supports Codex implementation and Claude review without sharing private conversation state or changing the active GitHub account.

**Independent-agent review:** only use separate-agent review when the project or user selects it. Supply the PR, reviewed SHA, requirements and project constraints. Its report and a posted GitHub review are separate artifacts.

Project exceptions are scoped: a rule allowing notes straight to the base branch applies only to the named paths. Keep code on a feature branch unless explicitly authorized otherwise. Implementation does not merge or close tickets; those actions require their own authorized delivery step.
