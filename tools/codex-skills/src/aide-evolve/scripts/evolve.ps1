param(
    [string]$StartPath = (Get-Location).Path,
    [string]$Failure = "",
    [string]$Evidence = "",
    [int]$Count = 2
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

function Read-DecisionTree {
    param([string]$RepoRoot)
    $path = Join-Path $RepoRoot ".aide\\docs\\agents\\SYSTEM_EVOLUTION.md"
    if (Test-Path $path) {
        return Get-Content -Raw $path
    }
    return $null
}

$repoRoot = Find-RepoRoot -Path $StartPath
if (-not $repoRoot) {
    Write-Output "Repo root not found (AGENTS.md missing)."
    exit 1
}

$decisionTree = Read-DecisionTree -RepoRoot $repoRoot
if (-not $decisionTree) {
    Write-Output "Missing decision tree: .aide/docs/agents/SYSTEM_EVOLUTION.md"
    exit 1
}

if ([string]::IsNullOrWhiteSpace($Failure)) {
    Write-Output "Provide -Failure describing the repeated mistake."
    exit 2
}

Write-Output "Failure: $Failure"
Write-Output "Count: $Count"
if ($Evidence) { Write-Output "Evidence: $Evidence" }
Write-Output ""
Write-Output "Decision tree: .aide/docs/agents/SYSTEM_EVOLUTION.md"
Write-Output ""
Write-Output "Next: Provide a proposal (automation vs Tier 1 vs Tier 2 vs reference-only) with file + section targets and example wording."

