# Run with PowerShell: .\scripts\setup.ps1 --targets codex --apply
# No execution-policy changes, downloads, or elevated privileges are required by this script.
$ErrorActionPreference = 'Stop'
$installer = Join-Path $PSScriptRoot 'setup_skills.py'
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $installer @args
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python $installer @args
} else {
    throw 'Python 3.10+ is required. Install Python, then run this script again.'
}
exit $LASTEXITCODE
