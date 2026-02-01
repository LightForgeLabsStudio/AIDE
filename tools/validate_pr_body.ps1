param(
    [string]$Body = ""
)

function Get-PrBodyFromEvent {
    $eventPath = $env:GITHUB_EVENT_PATH
    if (-not $eventPath -or -not (Test-Path $eventPath)) {
        return ""
    }
    try {
        $json = Get-Content -Raw $eventPath | ConvertFrom-Json
        if ($json.pull_request -and $json.pull_request.body) {
            return [string]$json.pull_request.body
        }
    } catch {
        return ""
    }
    return ""
}

function Is-InlineCode {
    param(
        [string]$Line,
        [int]$Index
    )
    $prefix = $Line.Substring(0, $Index)
    $tickCount = ($prefix.ToCharArray() | Where-Object { $_ -eq '`' }).Count
    return ($tickCount % 2 -eq 1)
}

if (-not $Body) {
    $Body = Get-PrBodyFromEvent
}

if (-not $Body) {
    Write-Output "No PR body found to validate."
    exit 0
}

$errors = @()
$lines = $Body -split "`n"
$inCodeBlock = $false

$filePathRegexes = @(
    # Repo-relative file paths (require a file extension to reduce false positives like "docs/")
    [regex]::new('(?:^|\s)(?<path>(?:tools|docs|scripts|\.aide|\.github)/[^\s`\)]+?\.[A-Za-z0-9]{1,8}(?:#[^\s`\)]*)?)'),

    # Windows absolute paths
    [regex]::new('(?:^|\s)(?<path>[A-Za-z]:\\[^\s`]+)')
)

$backslashPathRegex = [regex]::new('(?:^|\s)(?<path>\\[A-Za-z0-9._-]+(?:\\[^\s`]+)*)')

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    if ($line -match '^\s*```') {
        $inCodeBlock = -not $inCodeBlock
        continue
    }
    if ($inCodeBlock) {
        continue
    }

    # Disallow stray control characters (excluding tab)
    if ($line -match "[\u0000-\u0008\u000B\u000C\u000E-\u001F]") {
        $errors += "Line $($i+1): contains control characters."
        continue
    }

    foreach ($re in $filePathRegexes) {
        $matches = $re.Matches($line)
        foreach ($m in $matches) {
            $path = $m.Groups['path'].Value.Trim()
            if (-not $path) {
                continue
            }
            $pathIndex = $m.Groups['path'].Index
            if (-not (Is-InlineCode -Line $line -Index $pathIndex)) {
                $errors += "Line $($i+1): file path appears outside backticks -> '$path'"
            }
        }
    }

    # Disallow escaped leading backslash paths like \tools (require backticks)
    $matches = $backslashPathRegex.Matches($line)
    foreach ($m in $matches) {
        $path = $m.Groups['path'].Value.Trim()
        if (-not $path) {
            continue
        }
        $pathIndex = $m.Groups['path'].Index
        if (-not (Is-InlineCode -Line $line -Index $pathIndex)) {
            $errors += "Line $($i+1): backslash path appears outside backticks -> '$path'"
        }
    }
}

if ($errors.Count -gt 0) {
    Write-Output "PR body formatting check failed:"
    $errors | ForEach-Object { Write-Output "- $_" }
    Write-Output ""
    Write-Output "Guidance: wrap file paths in backticks and avoid stray backslash paths."
    exit 1
}

Write-Output "PR body formatting check passed."
