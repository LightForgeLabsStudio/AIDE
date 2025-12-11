# Testing Policy

NOTE: Ported from the prototype; adapted for Godot 4 (2D, GDScript).

Keep test runs aligned with change scope and release expectations.

## Testing Approach

This project uses a **hybrid testing strategy**:

- **GUT (Godot Unit Test)**: For fast, isolated unit tests of pure logic (autoloads, utility functions, data structures)
- **SceneTree Integration Tests**: For integration tests that require full scene loading and runtime behavior

This approach combines the speed and isolation of unit tests with the realism of integration tests.

## Required Before PR

Run the unified test suite to ensure all tests pass:

```bash
# Windows
run_tests.bat

# Linux/Mac
./run_tests.sh
```

At minimum, run the fast unit tests:

```bash
# Run GUT unit tests only
Godot_v4.5.1_console.exe --headless -s addons/gut/gut_cmdln.gd -gdir=res://tests/unit -gexit
```

If no automated tests exist yet, provide a short, repeatable manual checklist (steps + expected outcome) in the PR.

### Current Test Suites

**GUT Unit Tests** (fast, isolated):
- `tests/unit/test_resource_manager.gd` - ResourceManager autoload logic
- `tests/unit/test_config.gd` - Config constants and helpers

**Integration Tests** (SceneTree-based, headless):
- `tests/smoke/smoke_world.gd` - Load World.tscn and run for 3s
- `tests/logistics/test_job_and_refinery.gd` - Deliver ore to refinery and verify alloy output
- `tests/logistics/test_placement_anchor_rotation.gd` - Footprint anchor rotation and placement
- Additional tests in `tests/combat/` and `tests/logistics/`

### Running Individual Tests

**GUT Unit Tests:**
```bash
# Run all unit tests
Godot_v4.5.1_console.exe --headless -s addons/gut/gut_cmdln.gd -gdir=res://tests/unit -gexit

# Run specific unit test file
Godot_v4.5.1_console.exe --headless -s addons/gut/gut_cmdln.gd -gtest=res://tests/unit/test_resource_manager.gd -gexit

# Run from Godot Editor: Project → Tools → GUT
```

**Integration Tests:**
```bash
# Deliver ore to refinery and verify alloy output
Godot_v4.5.1_console.exe --headless -s tests/logistics/test_job_and_refinery.gd

# Load World.tscn and run a short smoke
Godot_v4.5.1_console.exe --headless -s tests/smoke/smoke_world.gd

# Placement anchor rotation test
Godot_v4.5.1_console.exe --headless -s tests/logistics/test_placement_anchor_rotation.gd
```

### Notes for Godot 4 Test Runs

- Warnings-as-errors are enabled; add explicit type annotations in scripts/tests to avoid load failures.
- SceneTree-based integration tests should wait at least one frame before accessing node paths or autoloads.
- GUT unit tests run in isolation and don't require scene loading (faster).

## Run When Relevant
- Logistics changes: job assignment, drone docking/movement, delivery/collection flows.
- Building production changes: input/output inventory rules, crafting timers.
- Combat changes: turret targeting/firing, enemy health/damage interactions.
- Pressure/evacuation changes (once implemented): wave pacing, pressure curves, evacuation gating.

## Release/Pre-merge Sweep
- Run all available automated suites and smoke-test the core gameplay loop in-editor.
- Include commands/logs of the runs in the PR/commit description.

## Writing New Tests

### When to Write Unit Tests (GUT)

Write GUT unit tests for:
- Pure logic functions (math, data transformations)
- Autoload singletons (ResourceManager, Config, JobSystem logic)
- Utility classes without scene dependencies
- Recipe/crafting logic
- State machines and FSM transitions
- Inventory and resource calculations

**Example structure:**
```gdscript
extends GutTest

var resource_manager: Node

func before_each() -> void:
	resource_manager = get_node("/root/ResourceManager")
	resource_manager.inventories.clear()

func after_each() -> void:
	resource_manager.inventories.clear()

func test_add_resource_increases_amount() -> void:
	resource_manager.add_resource("entity", Config.RESOURCE_IDS.ORE, 10)
	var amount := resource_manager.get_amount("entity", Config.RESOURCE_IDS.ORE)
	assert_eq(amount, 10, "Amount should be 10")
```

Place unit tests in: `tests/unit/test_<module_name>.gd`

### When to Write Integration Tests (SceneTree)

Write SceneTree integration tests for:
- Scene loading and node hierarchy
- Drone movement and pathfinding
- Building placement and collision
- Full gameplay loops (job assignment → drone movement → delivery)
- UI interactions
- Combat and enemy spawning

**Example structure:**
```gdscript
extends SceneTree

func _initialize() -> void:
	var world_scene: PackedScene = load("res://scenes/World.tscn")
	var world: Node = world_scene.instantiate()
	get_root().add_child(world)
	await process_frame

	# Test logic here

	print("test_name: PASS")
	quit(0)
```

Place integration tests in: `tests/logistics/`, `tests/combat/`, or `tests/smoke/`

### Test Guidelines

- Don't alter existing tests without explicit approval and rationale.
- Add new targeted tests alongside new features/fixes; keep them deterministic.
- Prefer unit tests (GUT) for fast feedback; use integration tests for end-to-end validation.
- All tests should run headless/offscreen to avoid coupling to editor state.
- Use descriptive test names: `test_<action>_<expected_result>`
- Keep tests focused: one concept per test function.
