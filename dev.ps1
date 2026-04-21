param()

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $projectRoot

function Test-CommandExists {
    param([string]$CommandName)

    return $null -ne (Get-Command $CommandName -ErrorAction SilentlyContinue)
}

if (-not (Test-CommandExists -CommandName "uv")) {
    Write-Error "uv is required to run this project. Install uv first, then rerun dev.ps1."
}

Write-Host "Syncing project dependencies with uv..."
uv sync --locked

Write-Host "Starting the Flask development server on http://127.0.0.1:5000 ..."
uv run flask --app run --debug run
