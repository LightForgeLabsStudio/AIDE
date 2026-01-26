param(
    [string]$StartPath = (Get-Location).Path
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

function Get-QuickConstraints {
    param([string]$AgentsPath)
    if (-not (Test-Path $AgentsPath)) {
        return "Constraints: project-defined (AGENTS.md missing)"
    }

    $lines = Get-Content $AgentsPath
    $inSection = $false
    $items = @()
    foreach ($line in $lines) {
        if ($line -match '^##\\s+Quick Constraints') {
            $inSection = $true
            continue
        }
        if ($inSection) {
            if ($line -match '^##\\s+') { break }
            if ($line -match '^\\s*-\\s+(.*)$') {
                $items += $Matches[1].Trim()
            }
        }
    }

    if ($items.Count -gt 0) {
        return "Constraints: " + ($items -join "; ")
    }
    return "Constraints: project-defined (see AGENTS.md)"
}

$repoRoot = Find-RepoRoot -Path $StartPath
if (-not $repoRoot) {
    Write-Output "Primed: AGENT_ORIENTATION.md: no AGENTS.md: no"
    Write-Output "Constraints: project-defined (AGENTS.md missing)"
    Write-Output "Next input needed: authoritative AGENTS.md path"
    Write-Output "If resuming work: provide handoff or PR link"
    exit 1
}

$agentOrientationPath = Join-Path $repoRoot "AGENT_ORIENTATION.md"
$agentsPath = Join-Path $repoRoot "AGENTS.md"

$hasOrientation = Test-Path $agentOrientationPath
$hasAgents = Test-Path $agentsPath

if ($hasOrientation) {
    Get-Content $agentOrientationPath | Out-Null
}
if ($hasAgents) {
    Get-Content $agentsPath | Out-Null
}

Write-Output ("Primed: AGENT_ORIENTATION.md: {0} AGENTS.md: {1}" -f ($(if ($hasOrientation) {'yes'} else {'no'}), $(if ($hasAgents) {'yes'} else {'no'})))
Write-Output (Get-QuickConstraints -AgentsPath $agentsPath)
Write-Output "Next input needed: task spec or PR/issue link"
Write-Output "If resuming work: provide handoff or PR link"

