# Define the name for the scheduled task
$taskName = "ExecuteScriptAtStartup"

# Path to the PowerShell script
$scriptPath = "C:\path\to\execute.ps1"

# Create a new scheduled task
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Force

Write-Output "Scheduled task created to execute the PowerShell script at startup."
