# Example Issue Spec

This example demonstrates creating an Epic with child issues, including blocking dependencies and area inference.

> **For complete format documentation, see [SPEC_WRITING_GUIDE.md](../../docs/SPEC_WRITING_GUIDE.md)**

---

## [Epic]: Job System Overhaul

Complete overhaul of the job assignment and priority system to enable more flexible drone behavior and better player control.

### Goals
- Flexible priority system for jobs
- Better drone assignment logic
- Cancellation support for in-progress jobs
- UI indicators for job status

### Success Criteria
- All child issues completed
- Performance maintained (no regression in job assignment speed)
- Backward compatible with existing save files

### Pillar References
- Pillar 2: Sector Logistics (job management is core to logistics)

---

## Issue: Job Priority System
type: feature
priority: high
area: job-system

### Goals
- Drones prioritize high-priority jobs over low-priority ones
- Buildings can mark jobs as urgent
- Priority visible in UI

### Scope
- Add `priority` enum field to Job struct (LOW, NORMAL, HIGH, URGENT)
- Update `Drone._select_next_job()` to sort by priority
- Add priority icons to job queue UI
- Update JobSystem.post_job() to accept priority parameter

### Non-Goals
- No changes to pathfinding logic
- No changes to resource requirements

### Success Criteria
- Drones claim highest priority job first when multiple available
- Priority UI indicators show correct priority level
- Tests verify priority sorting logic
- Manual test: High priority job claimed before low priority job

---

## Issue: Job Cancellation
type: feature
priority: medium
area: job-system
blocked_by: Issue: Job Priority System

### Goals
- Cancel jobs that are in progress
- Refund partial resources for cancelled jobs
- Update drone state appropriately

### Scope
- Add `Job.cancel()` method
- Add "Cancel" button to job UI panel
- Handle drone state cleanup when job cancelled mid-execution
- Refund logic: full refund if not started, partial if in progress

### Non-Goals
- No mass-cancel functionality (single job only)
- No cancel history/logging

### Success Criteria
- Jobs can be cancelled at any stage (queued, in-progress)
- Resources properly refunded (full or partial)
- Drones reassigned to new jobs immediately
- Tests verify refund calculations
- Manual test: Cancel job mid-execution, verify drone picks new job

---

## Issue: Job Queue UI Improvements
type: feature
priority: medium
area: job-system, ui

### Goals
- Visual feedback for job status (queued, in-progress, blocked)
- Priority indicators
- Worker assignment display

### Scope
- Update JobQueuePanel scene with status icons
- Add priority badges (color-coded)
- Show assigned drone ID for in-progress jobs
- Hover tooltip shows full job details

### Non-Goals
- No job queue reordering (manual priority override)
- No filtering/search functionality

### Success Criteria
- Job status clearly visible at a glance
- Priority color coding intuitive
- Assigned drone shown for in-progress jobs
- Tooltip shows complete job info on hover

---

## Issue: Job System Performance Optimization
type: feature
priority: low
area: job-system

### Goals
- Reduce job assignment overhead for large job queues
- Profile and optimize hot paths

### Scope
- Profile JobSystem.assign_jobs() with 100+ jobs
- Cache sorted job list instead of re-sorting every frame
- Only recalculate assignments when jobs or drones change

### Non-Goals
- No algorithmic changes to assignment logic
- No changes to job data structures

### Success Criteria
- 50% reduction in time spent in assign_jobs() for 100+ job queues
- No regressions in assignment correctness
- Performance tests verify improvements
