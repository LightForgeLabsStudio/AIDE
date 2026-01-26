param(
    [string]$StartPath = (Get-Location).Path,
    [string]$Spec = "",
    [string]$Issue,
    [string]$Repo,
    [switch]$Fetch
)

function Find-RepoRoot {
    param([string]$Path)
    $current = Resolve-Path $Path
    while ($true) {
        $agentsPath = Join-Path $current "AGENTS.md"
        if (Test-Path $agentsPath) {
            return $current
        }
        $parent = Split-Path $current -Parent
        if ($parent -eq $current -or [string]::IsNullOrWhiteSpace($parent)) {
            return $null
        }
        $current = $parent
    }
}

function Get-CommandValue {
    param([string]$Content, [string]$Placeholder)
    $pattern = [regex]::Escape($Placeholder) + "\s*\|\s*`?([^`\r\n]+)`?\s*\|"
    $match = [regex]::Match($Content, $pattern)
    if ($match.Success) { return $match.Groups[1].Value.Trim() }
    return $null
}

function Fetch-IssueBody {
    param([string]$Issue, [string]$Repo)
    if (-not $Issue) { return $null }
    $args = @("issue", "view", $Issue, "--json", "title,body")
    if ($Repo) { $args += @("--repo", $Repo) }
    $json = & gh @args 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $json) { return $null }
    try {
        $obj = $json | ConvertFrom-Json
        return ("# " + $obj.title + "`n`n" + $obj.body)
    } catch {
        return $null
    }
}

$repoRoot = Find-RepoRoot -Path $StartPath
if (-not $repoRoot) {
    Write-Output "Repo root not found (AGENTS.md missing)."
    exit 1
}

$agentsPath = Join-Path $repoRoot "AGENTS.md"
$agentsContent = Get-Content -Raw $agentsPath

$lint = Get-CommandValue $agentsContent "{{LINT_COMMAND}}"
$format = Get-CommandValue $agentsContent "{{FORMAT_COMMAND}}"
$unit = Get-CommandValue $agentsContent "{{RUN_UNIT_TESTS_COMMAND}}"
$all = Get-CommandValue $agentsContent "{{RUN_ALL_TESTS_COMMAND}}"
$smoke = Get-CommandValue $agentsContent "{{SMOKE_TEST_COMMAND}}"

$specText = $Spec
if ($Fetch -and -not $specText -and $Issue) {
    $specText = Fetch-IssueBody -Issue $Issue -Repo $Repo
}

if (-not $specText) {
    $specText = "(spec not provided - paste issue/PR description here)"
}

Write-Output "## Layer 1: Constraints"
Write-Output "- Extend, don't replace; no test modifications; never work on main; deterministic simulation; InventoryService/JobSystem authoritative; autoloads UI-free"
Write-Output "- Quality gates (from AGENTS.md):"
if ($lint) { Write-Output "  - Lint: $lint" }
if ($format) { Write-Output "  - Format: $format" }
if ($unit) { Write-Output "  - Unit tests: $unit" }
if ($all) { Write-Output "  - All tests: $all" }
if ($smoke) { Write-Output "  - Smoke: $smoke" }
Write-Output ""
Write-Output "## Layer 2: Plan (Draft)"
Write-Output "**Spec:**"
Write-Output $specText
Write-Output ""
Write-Output "**Plan:**"
Write-Output "1. (Task 1) - (exit criteria)"
Write-Output "2. (Task 2) - (exit criteria)"
Write-Output "3. (Task 3) - (exit criteria)"
Write-Output ""
Write-Output "**Files touched:** (list)"
Write-Output "**Validation:**"
Write-Output "- Lint: (run)"
Write-Output "- Tests: (run)"
Write-Output ""
Write-Output "----"
Write-Output "## Draft PR Body (Checklist)"
Write-Output "## Summary"
Write-Output "(1-2 sentences)"
if ($Issue) { Write-Output ""; Write-Output "**Implements:** #$Issue" }
Write-Output ""
Write-Output "## Implementation Plan"
Write-Output "- [ ] Task 1"
Write-Output "- [ ] Task 2"
Write-Output "- [ ] Task 3"
Write-Output ""
Write-Output "## Validation"
Write-Output "- [ ] Lint"
Write-Output "- [ ] Unit tests"
Write-Output "- [ ] All tests (before ready)"

