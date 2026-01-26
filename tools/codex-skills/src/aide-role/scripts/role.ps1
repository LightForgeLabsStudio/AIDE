param(
    [string]$StartPath = (Get-Location).Path,
    [string]$Text = "",
    [string]$PrUrl = "",
    [ValidateSet("implementation","pr-review","codebase-review","design-spec","design-workshop","doc-review")]
    [string]$Role = ""
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

function Choose-Role {
    param([string]$Text, [string]$PrUrl)
    $t = ($Text + " " + $PrUrl).ToLowerInvariant()
    if (-not [string]::IsNullOrWhiteSpace($PrUrl) -or $t -match "\bpr\b" -or $t -match "review") {
        return "pr-review"
    }
    if ($t -match "doc" -and $t -match "review") {
        return "doc-review"
    }
    if ($t -match "audit" -or $t -match "codebase review" -or $t -match "health check") {
        return "codebase-review"
    }
    if ($t -match "spec" -or $t -match "write.*issue" -or $t -match "scope" -or $t -match "acceptance criteria") {
        return "design-spec"
    }
    if ($t -match "brainstorm" -or $t -match "explore" -or $t -match "options" -or $t -match "workshop") {
        return "design-workshop"
    }
    if ($t -match "implement" -or $t -match "build" -or $t -match "fix" -or $t -match "bug" -or $t -match "feature") {
        return "implementation"
    }
    return "implementation"
}

function Primer-Path {
    param([string]$Role)
    switch ($Role) {
        "implementation" { return ".aide/docs/agents/IMPLEMENTATION_START.md" }
        "pr-review" { return ".aide/docs/agents/PR_REVIEW_START.md" }
        "codebase-review" { return ".aide/docs/agents/CODEBASE_REVIEW_START.md" }
        "design-spec" { return ".aide/docs/agents/DESIGN_SPEC_START.md" }
        "design-workshop" { return ".aide/docs/agents/DESIGN_WORKSHOP_START.md" }
        "doc-review" { return ".aide/docs/agents/DOC_REVIEW_START.md" }
        default { return ".aide/docs/agents/IMPLEMENTATION_START.md" }
    }
}

$repoRoot = Find-RepoRoot -Path $StartPath
if (-not $repoRoot) {
    Write-Output "Repo root not found (AGENTS.md missing)."
    exit 1
}

$agentOrientationPath = Join-Path $repoRoot "AGENT_ORIENTATION.md"
$agentsPath = Join-Path $repoRoot "AGENTS.md"
if (Test-Path $agentOrientationPath) { Get-Content $agentOrientationPath | Out-Null }
if (Test-Path $agentsPath) { Get-Content $agentsPath | Out-Null }

$selected = $Role
if ([string]::IsNullOrWhiteSpace($selected)) {
    $selected = Choose-Role -Text $Text -PrUrl $PrUrl
}

$primer = Primer-Path -Role $selected

$next = "Provide task spec or issue link."
switch ($selected) {
    "pr-review" { $next = "Provide PR link/number to review." }
    "doc-review" { $next = "Provide doc path(s) to review." }
    "codebase-review" { $next = "Provide audit scope (areas) and constraints." }
    "design-spec" { $next = "Provide feature goal(s) and constraints; create a spec." }
    "design-workshop" { $next = "Provide problem statement and what decisions are needed." }
    "implementation" { $next = "Provide issue/spec link and success criteria." }
}

Write-Output "Role: $selected"
Write-Output "Primer: $primer"
Write-Output "Next input: $next"

