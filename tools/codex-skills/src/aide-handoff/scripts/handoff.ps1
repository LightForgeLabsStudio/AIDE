param(
    [string]$StartPath = (Get-Location).Path,
    [string]$Pr,
    [string]$Issue,
    [string]$Repo,
    [switch]$Post
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

function Get-Template {
    param([string]$RepoRoot)
    if ($RepoRoot) {
        $path = Join-Path $RepoRoot ".aide\\docs\\core\\SESSION_HANDOFF.template.md"
        if (Test-Path $path) {
            return Get-Content -Raw $path
        }
    }
    return @"
# Session State Handoff

**Current Stage:** (Implementation Step X: Name)
**Branch:** (e.g. `feature/my-branch`)
**PR:** (link or "not created yet")
**Issue:** (link/number or "n/a")

---

## Completed

- [ ] ...

## In Progress

- [ ] ... (blocked on: ...)

## Blockers / Unknowns

- ...

## Next Actions (Most Important First)

1. ...
2. ...
3. ...

## Context Notes (Decisions + Rationale)

- ...

## Validation

- Lint: (command + result)
- Tests: (command + result)
- Other: ...
"@
}

$repoRoot = Find-RepoRoot -Path $StartPath
$template = Get-Template -RepoRoot $repoRoot

if (-not $Post) {
    Write-Output $template
    exit 0
}

if (($Pr -and $Issue) -or (-not $Pr -and -not $Issue)) {
    Write-Error "Provide exactly one of -Pr or -Issue when using -Post."
    exit 2
}

$targetArgs = @()
if ($Repo) { $targetArgs += @("--repo", $Repo) }

if ($Pr) {
    $cmd = @("gh", "pr", "comment", $Pr, "-F", "-") + $targetArgs
} else {
    $cmd = @("gh", "issue", "comment", $Issue, "-F", "-") + $targetArgs
}

try {
    $template | & $cmd[0] @($cmd[1..($cmd.Length-1)])
    exit $LASTEXITCODE
} catch {
    Write-Error "Failed to post comment. Ensure gh is installed and authenticated."
    exit 1
}

