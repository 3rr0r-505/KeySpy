Set objShell = CreateObject("WScript.Shell")
objShell.Run "powershell.exe -ExecutionPolicy Bypass -File ""C:\Program Files (x86)\winX32\execute.ps1""", 0, True
