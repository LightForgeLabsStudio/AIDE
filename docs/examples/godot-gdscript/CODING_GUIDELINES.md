# Coding Guidelines

NOTE: Ported from the Pygame prototype and updated for a Godot 4 (2D, GDScript) codebase.

Standards to keep the Godot version of Lightborn Exile consistent and predictable. See [CONTRIBUTING.md](CONTRIBUTING.md) for workflow; this file focuses on style and architecture.

## Core Principles
- **Deterministic behavior:** Keep core simulation logic deterministic and reproducible; avoid unseeded randomness in gameplay systems.
- **Follow design specifications:** Implement systems according to design pillars (see [design/](../design/)); movement, combat, logistics must match documented behavior.
- **System-appropriate AI:** Use the appropriate control system for each entity type (JobSystem for logistics, combat AI for fleet units, etc.).
- **Engine separation:** Keep simulation logic engine-agnostic where possible (pure scripts without scene references); UI/input/rendering stay in scene scripts.
- **Single sources of truth:** Use authoritative autoloads (`ResourceManager`, `JobSystem`) for shared state/configs; avoid duplicating state across scenes.
- **Small, focused changes:** Prefer minimal diffs with matching test hooks and doc updates.

## GDScript Style
- Use snake_case for functions/variables, PascalCase for classes/resources, and ALL_CAPS for constants.
- Add concise docstrings/comments for non-obvious logic or data flow; avoid noisy narration.
- Prefer guard clauses and short methods to keep state handling readable.
- Keep data structures simple (dictionaries/arrays/enums). Use enums for states/types (e.g., JobType, DroneState).
- Avoid new plugins/dependencies unless agreed; base stack is Godot 4, 2D renderer, GDScript.

## Scene & Script Boundaries

For detailed architecture patterns, see [DEVELOPMENT.md](DEVELOPMENT.md).

**Key Boundaries:**
- **Autoloads are UI-free:** No rendering, input handling, or scene-tree coupling in autoloads.
- **Scenes expose signals/methods:** Use public APIs (`request_dock()`, `deliver_resource()`) instead of internal property access.
- **UI decoupled from logic:** UI scenes subscribe to signals/callbacks; avoid tight coupling to autoload internals.
- **Simulation logic in scripts:** Keep gameplay rules in scripts, not editor-only node configurations.
- **FX/Helpers are visual-only:** Effects scenes should not contain gameplay logic.

## Movement & Physics

All movement implementation must follow the movement models documented in [design/pillar_6_combat.md](../design/pillar_6_combat.md). Movement must be deterministic and reproducible.

**Implementation Standards:**
- Docking/interaction points should be explicit nodes/markers; avoid magic offsets in code.
- Route new behaviors through state handlers or dedicated methods instead of ad hoc updates inside `_physics_process`.
- Maintain clear thresholds for arrival radii/interaction ranges in config, not literals.

## Testing & Verification
- Add deterministic tests for simulation logic where feasible (e.g., gdUnit or headless script checks) and keep them engine-agnostic.
- Prefer unit-style checks for job assignment, resource flow, and inventory math.
- Avoid visual-only verification; expose small helpers that can be tested without a running scene.

## Git Commits
- Keep commits small and single-purpose; one concern per commit/branch.
- Use imperative subjects (e.g., "Tighten drone docking radius"); note tests run in the body when applicable.
- Commit code, tests, and doc updates together so expectations match behavior.
- Avoid committing generated assets or debug spam; gate logs behind config flags.

## Documentation & Changelog

Follow [DOCUMENTATION_POLICY.md](DOCUMENTATION_POLICY.md) for all documentation updates:
- Update player-facing docs for behavior/balance changes
- Update `DEVELOPMENT.md` for architecture/extension notes
- Avoid duplicating the same detail across files; use references instead

## Logging & Debugging
- Prefer structured debug helpers (job id, target, path length, inventory deltas) over ad hoc prints.
- Make debug logging opt-in via config flags or debug builds; avoid shipping noisy output.

---

## Reference Docs

**Related Standards:**
- [CONTRIBUTING.md](CONTRIBUTING.md) - Workflow and collaboration process
- [DEVELOPMENT.md](DEVELOPMENT.md) - Architecture patterns and component details
- [TESTING_POLICY.md](TESTING_POLICY.md) - Testing requirements and practices
- [DOCUMENTATION_POLICY.md](DOCUMENTATION_POLICY.md) - Documentation standards

**Design References:**
- [design/pillar_6_combat.md](../design/pillar_6_combat.md) - Movement models and combat systems
- [design/pillar_2_sector_logistics.md](../design/pillar_2_sector_logistics.md) - Drone and logistics systems
