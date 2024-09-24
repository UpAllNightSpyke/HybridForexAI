# Check if .venv directory exists
if (Test-Path -Path ".venv") {
    # Activate the virtual environment
    .\.venv\Scripts\Activate.ps1
    Write-Output "Virtual environment activated."
} else {
    Write-Output ".venv directory not found. Please create the virtual environment first."
}