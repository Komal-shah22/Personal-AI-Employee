# Ralph Wiggum Loop - "I'm helping!" (Windows PowerShell)
# Wrapper script to start Claude Code with the stop hook enabled

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Prompt,

    [Parameter(Mandatory=$false)]
    [int]$MaxIterations = 10,

    [switch]$Help
)

# Show help
if ($Help) {
    Write-Host @"
Ralph Wiggum Loop - I'm helping!

Usage: .\scripts\ralph-loop.ps1 [OPTIONS] "prompt"

Options:
  -MaxIterations N    Maximum iterations (default: 10)
  -Help              Show this help message

Examples:
  .\scripts\ralph-loop.ps1 "Process all pending tasks"
  .\scripts\ralph-loop.ps1 -MaxIterations 20 "Process all emails and invoices"

How it works:
  1. Starts Claude Code with your prompt
  2. Stop hook checks for unprocessed files in Needs_Action/
  3. If files exist: continues working (up to max iterations)
  4. If no files or max reached: stops

"@
    exit 0
}

# Get project directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

# Colors
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Print banner
Write-ColorOutput "==========================================" "Cyan"
Write-ColorOutput "RALPH WIGGUM LOOP - I'M HELPING!" "Cyan"
Write-ColorOutput "==========================================" "Cyan"
Write-Host ""

# Validate prompt
if ([string]::IsNullOrWhiteSpace($Prompt)) {
    Write-ColorOutput "ERROR: No prompt provided" "Red"
    Write-Host "Usage: .\scripts\ralph-loop.ps1 `"your prompt here`""
    Write-Host "Run with -Help for more information"
    exit 1
}

# Check if stop hook exists
$StopHook = Join-Path $ProjectDir ".claude\hooks\stop_hook.py"
if (-not (Test-Path $StopHook)) {
    Write-ColorOutput "ERROR: Stop hook not found at $StopHook" "Red"
    exit 1
}

# Check if Python is available
$PythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $PythonCmd = "python3"
} else {
    Write-ColorOutput "ERROR: Python not found" "Red"
    Write-Host "Please install Python first"
    exit 1
}

# Check if Claude CLI is installed
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    Write-ColorOutput "ERROR: Claude CLI not found" "Red"
    Write-Host "Install with: npm install -g @anthropic-ai/claude-cli"
    exit 1
}

# Initialize loop status
$PlansDir = Join-Path $ProjectDir "AI_Employee_Vault\Plans"
if (-not (Test-Path $PlansDir)) {
    New-Item -ItemType Directory -Path $PlansDir -Force | Out-Null
}

$LoopStatus = Join-Path $PlansDir "loop_status.md"
$Timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

$StatusContent = @"
---
iteration: 0
max_iterations: $MaxIterations
started: $Timestamp
last_updated: $Timestamp
status: running
---

# Ralph Wiggum Loop Status

**Current Status**: RUNNING

## Progress

- **Iteration**: 0 of $MaxIterations
- **Started**: $Timestamp

## Initial Prompt

``````
$Prompt
``````

---

*Loop initialized by ralph-loop.ps1*
"@

Set-Content -Path $LoopStatus -Value $StatusContent -Encoding UTF8

Write-ColorOutput "✓ Loop status initialized" "Green"
Write-Host "  Max iterations: " -NoNewline
Write-ColorOutput $MaxIterations "Yellow"
Write-Host "  Status file: $LoopStatus"
Write-Host ""

# Set environment variable for stop hook
$env:RALPH_MAX_ITERATIONS = $MaxIterations

# Change to project directory
Set-Location $ProjectDir

Write-ColorOutput "Starting Claude Code with stop hook..." "Cyan"
Write-Host "Prompt: " -NoNewline
Write-ColorOutput $Prompt "Yellow"
Write-Host ""
Write-ColorOutput "==========================================" "Cyan"
Write-Host ""

# Start Claude with the prompt
# The stop hook will automatically trigger when Claude tries to exit
try {
    claude -p $Prompt
} catch {
    Write-ColorOutput "ERROR: Claude execution failed: $_" "Red"
    exit 1
}

# After Claude exits, show final status
Write-Host ""
Write-ColorOutput "==========================================" "Cyan"
Write-ColorOutput "RALPH LOOP COMPLETE" "Cyan"
Write-ColorOutput "==========================================" "Cyan"
Write-Host ""

# Read final status
if (Test-Path $LoopStatus) {
    $StatusLines = Get-Content $LoopStatus

    $FinalIteration = ($StatusLines | Select-String "^iteration:" | ForEach-Object { $_ -replace "iteration:\s*", "" }).Trim()
    $FinalStatus = ($StatusLines | Select-String "^status:" | ForEach-Object { $_ -replace "status:\s*", "" }).Trim()

    Write-Host "Final Status: " -NoNewline
    Write-ColorOutput $FinalStatus "Yellow"
    Write-Host "Iterations: " -NoNewline
    Write-ColorOutput "$FinalIteration of $MaxIterations" "Yellow"
    Write-Host ""

    # Check for remaining files
    $NeedsActionDir = Join-Path $ProjectDir "AI_Employee_Vault\Needs_Action"
    if (Test-Path $NeedsActionDir) {
        $RemainingFiles = Get-ChildItem $NeedsActionDir -Filter "*.md" | Where-Object { -not $_.Name.StartsWith("_") }
        $Remaining = $RemainingFiles.Count

        if ($Remaining -gt 0) {
            Write-ColorOutput "⚠ $Remaining files remain in Needs_Action/" "Yellow"
            Write-Host ""
            Write-Host "To continue processing:"
            Write-Host "  .\scripts\ralph-loop.ps1 -MaxIterations $MaxIterations `"Continue processing remaining tasks`""
        } else {
            Write-ColorOutput "✓ All files processed!" "Green"
        }
    }
}

Write-Host ""
