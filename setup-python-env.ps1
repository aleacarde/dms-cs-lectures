# Check if pyenv is installed, if not, install it
if (-not (Get-Command pyenv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing pyenv..."
    Invoke-Expression (Invoke-WebRequest -Uri https://pyenv-win.github.io/pyenv-win/install-pyenv-win.ps1 -UseBasicParsing).Content
    $env:PATH += ";$HOME\.pyenv\pyenv-win\bin;$HOME\.pyenv\pyenv-win\shims"
    Write-Host "pyenv installed successfully."
} else {
    Write-Host "pyenv is already installed."
}

# Navigate to the root of the project directory (assuming this script is run from there)
$projectRoot = Get-Location

# Read the .python-version file to determine the desired Python version
$pythonVersionFile = Join-Path -Path $projectRoot -ChildPath ".python-version"
if (Test-Path $pythonVersionFile) {
    $pythonVersion = Get-Content $pythonVersionFile | Select-Object -First 1
    Write-Host "Setting Python version to $pythonVersion using pyenv..."
    pyenv install -s $pythonVersion  # Install the version if not already installed
    pyenv local $pythonVersion       # Set the local version
    Write-Host "Python version set to $pythonVersion."
} else {
    Write-Host ".python-version file not found. Please ensure it exists in the project root."
    exit 1
}

# Check if poetry is installed, if not, install it
if (-not (Get-Command poetry -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Poetry..."
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
    $env:PATH += ";$HOME\.local\bin"
    Write-Host "Poetry installed successfully."
} else {
    Write-Host "Poetry is already installed."
}

# Configure Poetry to create a .venv directory in the project root
Write-Host "Configuring Poetry to create a local .venv directory..."
poetry config virtualenvs.in-project true

# Install dependencies using Poetry
Write-Host "Installing dependencies with Poetry..."
if (Test-Path "$projectRoot\pyproject.toml") {
    poetry install
    Write-Host "Dependencies installed successfully."
} else {
    Write-Host "pyproject.toml not found. Please ensure it exists in the project root."
    exit 1
}

Write-Host "Setup complete. Python environment and dependencies are ready."