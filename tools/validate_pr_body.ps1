param(
    [string]$Body = ""
)

function Get-TextFromEvent {
    $eventPath = $env:GITHUB_EVENT_PATH
    if (-not $eventPath -or -not (Test-Path $eventPath)) {
        return @{
            Text = ""
            Kind = ""
        }
    }
    try {
        $json = Get-Content -Raw $eventPath | ConvertFrom-Json
        if ($json.pull_request -and $json.pull_request.body) {
            return @{
                Text = [string]$json.pull_request.body
                Kind = "PR body"
            }
        }

        # PR conversation comments come through issue_comment events, where
        # issue.pull_request is present.
        if ($json.issue -and $json.issue.pull_request -and $json.comment -and $json.comment.body) {
            return @{
                Text = [string]$json.comment.body
                Kind = "PR comment"
            }
        }
    } catch {
        return @{
            Text = ""
            Kind = ""
        }
    }
    return @{
        Text = ""
        Kind = ""
    }
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
    $result = Get-TextFromEvent
    $Body = $result.Text
    $bodyKind = $result.Kind
} else {
    $bodyKind = "PR body"
}

if (-not $Body) {
    Write-Output "No PR body/comment found to validate."
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

$backslashPathRegex = [regex]::new('(?:^|\s)(?<path>\\(?:tools|docs|scripts|\.aide|\.github)(?:\\[^\s`]+)*)')

$literalEscapeRegex = [regex]::new('\\(?:n|r|t|0)|\\u[0-9A-Fa-f]{4}|\\x[0-9A-Fa-f]{2}')
$backslashWordRegex = [regex]::new('\\[A-Za-z]{2,}')

for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    if ($line -match '^\s*```') {
        $inCodeBlock = -not $inCodeBlock
        continue
    }
    if ($inCodeBlock) {
        continue
    }

    $pathMatchByIndex = @{}

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
            $pathMatchByIndex[$pathIndex] = $path
            $errors += "Line $($i+1): backslash path appears outside backticks -> '$path'"
        }
    }

    # Disallow accidental literal escape sequences (common when a JSON-escaped
    # string gets pasted into a PR body), e.g. "\n" or "\t".
    $wordMatches = $backslashWordRegex.Matches($line)
    $wordMatchByIndex = @{}
    foreach ($m in $wordMatches) {
        if (-not (Is-InlineCode -Line $line -Index $m.Index)) {
            if ($pathMatchByIndex.ContainsKey($m.Index)) {
                continue
            }
            $wordMatchByIndex[$m.Index] = $m.Value
            $errors += "Line $($i+1): contains backslash-escaped word outside backticks -> '$($m.Value)'"
        }
    }

    $matches = $literalEscapeRegex.Matches($line)
    foreach ($m in $matches) {
        if (Is-InlineCode -Line $line -Index $m.Index) {
            continue
        }
        # If this escape is the prefix of a longer backslash-word (e.g. "\type"),
        # prefer reporting it as a word-escape rather than "\t".
        if ($wordMatchByIndex.ContainsKey($m.Index)) {
            continue
        }
        # Don't double-report when this is part of a detected backslash-path (e.g. "\tools\...").
        if ($pathMatchByIndex.ContainsKey($m.Index)) {
            continue
        }
        $errors += "Line $($i+1): contains literal escape sequence outside backticks -> '$($m.Value)'"
    }
}

if ($inCodeBlock) {
    $errors += "Unclosed code fence: found ``` without a matching closing ```."
}

if ($errors.Count -gt 0) {
    $kind = if ($bodyKind) { $bodyKind } else { "PR body/comment" }
    Write-Output "$kind formatting check failed:"
    $errors | ForEach-Object { Write-Output "- $_" }
    Write-Output ""
    Write-Output "Guidance: wrap file paths in backticks and avoid stray backslash paths or literal \\n escapes."
    exit 1
}

$kind = if ($bodyKind) { $bodyKind } else { "PR body/comment" }
Write-Output "$kind formatting check passed."
