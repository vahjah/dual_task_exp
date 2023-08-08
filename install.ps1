param([switch]$Elevated)

function Test-Admin {
    $currentUser = New-Object Security.Principal.WindowsPrincipal $([Security.Principal.WindowsIdentity]::GetCurrent())
    $currentUser.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}

if ((Test-Admin) -eq $false)  {
    if ($elevated) {
        # tried to elevate, did not work, aborting
    } else {
        Start-Process powershell.exe -Verb RunAs -ArgumentList ('-noprofile -noexit -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition))
    }
    exit
}

'running with full privileges'

# Change working directory to script directory
Set-Location -Path $PSScriptRoot

# Check if Chocolatey is installed
if ((Get-Command choco.exe -ErrorAction SilentlyContinue) -eq $null) {
    # Install Chocolatey
    Set-ExecutionPolicy Bypass -Scope Process -Force;
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
}

# Check if Python is installed
if (!(Test-Path "${Env:ProgramData}\chocolatey\lib\python")) {
    # Install Python
    choco install -y python

    # Wait for Python installation to complete
    Start-Sleep -Seconds 60

    # Refresh environment variables after Python installation
    $env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User')
}

# Check if Git is installed
if ((Get-Command git -ErrorAction SilentlyContinue) -eq $null) {
    # Install Git
    choco install -y git
}

# Check if ffmpeg is installed
if ((Get-Command ffmpeg -ErrorAction SilentlyContinue) -eq $null) {
    # Install ffmpeg
    choco install -y ffmpeg
}

# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine')

# Upgrade pip
python -m pip install --upgrade pip

# Check if venv is installed
if ((pip list | Select-String "virtualenv") -eq $null) {
    # Install venv
    python -m pip install virtualenv
}

# Create a virtual environment
if (!(Test-Path ".\venv")) {
    python -m venv venv
}

# Activate the virtual environment
. .\venv\Scripts\activate

# Check if requirements.txt exists
if (Test-Path ".\requirements.txt") {
    # Install packages from requirements.txt
    python -m pip install -r requirements.txt
}
else {
    Write-Output "No requirements.txt found in the current directory."
    exit 1
}

# Run the main.py script
if (Test-Path ".\main.py") {
    python main.py
}
else {
    Write-Output "No main.py found in the current directory."
    exit 1
}