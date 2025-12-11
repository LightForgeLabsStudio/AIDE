# Development Guide

NOTE: Ported from the prototype and refocused for a Godot 4 (2D, GDScript) project.

Technical reference for extending and debugging the Godot implementation.

## Architecture Overview

**Scene-Driven Composition**
- **World/Root Scene**: Hosts the play area, spawns resource nodes/enemies, owns the camera, and instantiates child scenes.
- **Entities as Scenes**: `Mothership`, `Drone`, `Building` variants (Refinery, Turret, etc.), `OreNode`, `Enemy`. Each exposes signals/public methods for interaction and keeps visuals separated from logic helpers where possible.
- **Autoloads**: `JobSystem` (job queue/assignment), `ResourceManager` (inventories, recipes), `PressureSystem` (future), `WaveSpawner` (future). Keep autoloads UI-free and deterministic.

## Core Components

### 1. Configuration
- Centralize tunables (movement speeds, interaction radii, docking offsets, inventory caps, production timers) in a shared config script or `ProjectSettings` block consumed by autoloads and scenes.

### 2. ResourceManager (autoload)
- Tracks resources (Ore, Alloy, Ammo, Components, Flux) and worker counts.
- Provides helpers for `has_resources`, `consume_resources`, `add_resource`, and per-entity inventory checks.
- Acts as the single source of truth for crafting/production recipes.

### 3. JobSystem (autoload)
- Owns job creation/queues for mining, delivery, collection, crafting triggers, and refuel/ammo runs.
- Handles reservations, timeouts, and reassignment.
- Publishes jobs to idle drones; drones pull jobs rather than being commanded directly.

### 4. Buildings (scenes)
- Base building script holds name, cost, input/output inventories, production timers, docking markers, and signal hooks.
- Building types emit jobs via the JobSystem instead of directly commanding drones.
- Example variants: `Refinery` (Ore → Alloy), `Turret` (consumes Ammo), `Assembler`/`DroneBay` (future).

### 5. Resource Nodes (scenes)
- Represent Ore/Mineral nodes with occupancy limits and mining timers.
- Expose reservation/mine methods for drones; avoid embedding job logic directly in the node.

### 6. Drones (scenes)
- FSM/stateful script that consumes jobs from JobSystem.
- Movement follows design specifications (see [design/pillar_2_sector_logistics.md](../design/pillar_2_sector_logistics.md) for logistics drones, [design/pillar_6_combat.md](../design/pillar_6_combat.md) for combat units).
- Cargo capacity and docking/interaction flows are data-driven (configurable radii/offsets).

### 7. Enemies (scenes)
- Simple pursuit toward the mothership or nearest building.
- Health/damage kept in the enemy script; combat resolves via signals or method calls from turrets.

### 8. UI
- HUD/overlays live in their own scenes; subscribe to signals from autoloads/entities instead of polling scene internals.

## World & Grid Notes
- Keep coordinates world-space friendly; if a grid is used for placement/pathing, centralize cell size and conversions in a helper script.
- Avoid hardcoding pixel offsets; expose markers/points in scenes for docking/interaction instead.

## Testing
- Prefer small, deterministic tests for autoload logic (job assignment, inventory math, pressure curves).
- Use gdUnit or lightweight headless scripts; keep logic decoupled from nodes when feasible to ease testing.
- Avoid modifying existing tests without approval; add new cases alongside new functionality.

## Common Tasks

| Task | How To |
|------|--------|
| Change balance | Adjust config constants or resource definitions in the autoload/shared config. |
| Add building | Create a new Building scene + script, set costs/inventories, implement production tick, and publish jobs via JobSystem. |
| Add resource | Update ResourceManager definitions, UI displays, and any crafting recipes that produce/consume it. |
| Debug drones | Add structured logs or debug draw helpers; simulate jobs in a headless test where possible. |
| Add enemy type | Create a new Enemy scene with movement/targeting parameters; ensure Turret targeting handles it. |

## Reference Docs

- [CONTRIBUTING.md](CONTRIBUTING.md) - Full workflow
- [CODING_GUIDELINES.md](CODING_GUIDELINES.md) - Code standards
- [PROJECT_SUMMARY.md](../design/PROJECT_SUMMARY.md) - Project overview
- [PR_REVIEW_START.md](agents/PR_REVIEW_START.md) - Review checklist
