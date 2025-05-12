# PowerShell script to build Sphinx documentation for Edge-AI Orchestrator Backend
# Usage: ./build-docs.ps1

Write-Host "Attempting to activate virtual environment..."
# Activate virtual environment
$VenvPath = Join-Path $PSScriptRoot ".venv"
if (Test-Path (Join-Path $VenvPath "Scripts\Activate.ps1")) {
    . (Join-Path $VenvPath "Scripts\Activate.ps1")
    Write-Host "Activated virtual environment from Scripts/Activate.ps1"
} elseif (Test-Path (Join-Path $VenvPath "bin\activate")) {
    # For non-Windows like environments if script is used there
    . (Join-Path $VenvPath "bin\activate")
    Write-Host "Activated virtual environment from bin/activate"
} else {
    Write-Error "Virtual environment activation script not found in .venv/Scripts or .venv/bin. Please ensure the backend virtual environment exists at $VenvPath"
    exit 1
}

Write-Host "Checking Python version and executable..."
python --version
Write-Host "Python executable path:"
python -c "import sys; print(sys.executable)"
Write-Host "sys.path:"
python -c "import sys; print(sys.path)"

$SphinxSourceDir = Join-Path $PSScriptRoot "..\docs\backend\source"
$SphinxBuildDir = Join-Path $PSScriptRoot "..\docs\backend\build\html"
$StdOutLog = Join-Path $PSScriptRoot "sphinx_stdout.log"
$StdErrLog = Join-Path $PSScriptRoot "sphinx_stderr.log"

Write-Host "Running Sphinx build with verbose output (-vvv)..."
Write-Host "Source directory: $SphinxSourceDir"
Write-Host "Build directory: $SphinxBuildDir"
Write-Host "Stdout log: $StdOutLog"
Write-Host "Stderr log: $StdErrLog"

# Run Sphinx build with maximum verbosity and redirect output
python -m sphinx -vvv -b html $SphinxSourceDir $SphinxBuildDir 1> $StdOutLog 2> $StdErrLog
$ExitCode = $LASTEXITCODE

Write-Host "Sphinx build command exited with code: $ExitCode"

if (Test-Path $StdOutLog) {
    Write-Host "--- Sphinx STDOUT ---"
    Get-Content $StdOutLog
    Write-Host "--- End Sphinx STDOUT ---"
} else {
    Write-Host "Sphinx stdout log not found: $StdOutLog"
}

if (Test-Path $StdErrLog) {
    Write-Host "--- Sphinx STDERR ---"
    Get-Content $StdErrLog
    Write-Host "--- End Sphinx STDERR ---"
} else {
    Write-Host "Sphinx stderr log not found: $StdErrLog"
}

if ($ExitCode -eq 0) {
    Write-Host "Sphinx documentation build complete. Output: $SphinxBuildDir\index.html"
} else {
    Write-Error "Sphinx documentation build failed. Exit code: $ExitCode. Check logs above."
}
