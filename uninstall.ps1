param([switch]$Elevated)

function Test-Admin {
    $currentUser = New-Object Security.Principal.WindowsPrincipal $([Security.Principal.WindowsIdentity]::GetCurrent())
    $isAdmin = $currentUser.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
    return $isAdmin
}

if ((Test-Admin) -eq $false)  {
    if ($elevated) {
        # tried to elevate, did not work, aborting
        Write-Output "Tried to elevate but did not work. Aborting."
        exit 1
    } else {
        Start-Process powershell.exe -Verb RunAs -ArgumentList ('-noprofile -noexit -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition))
        exit
    }
}

'running with full privileges'

# Change working directory to script directory
Set-Location -Path $PSScriptRoot

# Check if Chocolatey is installed
if ((Get-Command choco.exe -ErrorAction SilentlyContinue) -eq $null) {
    Write-Output "Chocolatey is not installed. Exiting."
    exit 1
}

# List all installed Chocolatey packages
$chocoPackages = choco list --local-only

# If there are no packages installed, exit
if (!$chocoPackages) {
    Write-Output "No Chocolatey packages are installed. Exiting."
    exit
}

# Uninstall each package
$chocoPackages | ForEach-Object {
    Write-Output "Uninstalling $_..."
    choco uninstall $_ -y
}

Write-Output "All Chocolatey packages have been uninstalled."