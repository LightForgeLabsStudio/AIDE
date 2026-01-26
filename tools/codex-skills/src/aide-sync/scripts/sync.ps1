param(
    [string]$StartPath = (Get-Location).Path,
    [switch]$AllowMain,
    [switch]$DryRun
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

function Require-CleanWorkingTree {
    $porcelain = & git status --porcelain
    if ($LASTEXITCODE -ne 0) { throw "git status failed." }
    if (-not [string]::IsNullOrWhiteSpace($porcelain)) {
        throw "Working tree is not clean. Commit/stash changes before syncing."
    }
}

function Test-CleanWorkingTree {
    $porcelain = & git status --porcelain
    if ($LASTEXITCODE -ne 0) { throw "git status failed." }
    return [string]::IsNullOrWhiteSpace($porcelain)
}

function Get-CurrentBranch {
    $branch = & git rev-parse --abbrev-ref HEAD
    if ($LASTEXITCODE -ne 0) { throw "git rev-parse failed." }
    return $branch.Trim()
}

function Require-Upstream {
    $upstream = & git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>$null
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($upstream)) {
        throw "No upstream configured. Set it with: git push -u origin <branch>"
    }
}

function Test-Upstream {
    $upstream = & git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>$null
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($upstream)) {
        return $false
    }
    return $true
}

function Run-Step {
    param([string]$Cmd)
    Write-Output "Running: $Cmd"
    if ($DryRun) { return }
    & powershell -NoProfile -ExecutionPolicy Bypass -Command $Cmd
    if ($LASTEXITCODE -ne 0) {
        throw "FAILED: $Cmd (exit $LASTEXITCODE)"
    }
}

$repoRoot = Find-RepoRoot -Path $StartPath
if (-not $repoRoot) {
    Write-Error "Repo root not found (AGENTS.md missing)."
    exit 1
}

Push-Location $repoRoot
try {
    $branch = Get-CurrentBranch
    if ($branch -eq "main" -and -not $AllowMain) {
        Write-Error "Refusing to run on main. Re-run with -AllowMain to override."
        exit 2
    }

    if ($DryRun) {
        if (-not (Test-CleanWorkingTree)) {
            Write-Output "Warning: working tree is not clean; a real run would refuse."
        }
        if (-not (Test-Upstream)) {
            Write-Output "Warning: no upstream configured; a real run would refuse."
        }
    } else {
        Require-CleanWorkingTree
        Require-Upstream
    }

    Run-Step "git pull --rebase"
    Run-Step "git push"

    $status = & git status -sb
    if ($LASTEXITCODE -ne 0) { throw "git status -sb failed." }
    $statusText = ($status | Out-String).TrimEnd()

    Write-Output "Final status:"
    Write-Output $statusText

    if ($statusText -match '\[(?:ahead|behind)\b') {
        Write-Error "Branch is not fully synced (ahead/behind remains). Resolve and re-run."
        exit 3
    }

    if ($DryRun) {
        Write-Output "Dry-run complete."
    } else {
        Write-Output "Sync complete."
    }
} catch {
    Write-Error $_.Exception.Message
    exit 1
} finally {
    Pop-Location
}

