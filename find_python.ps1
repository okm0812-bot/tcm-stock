Get-ChildItem 'C:\Users\user\AppData\Local\Programs' -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "python*" } | Select-Object -First 5 FullName
Get-ChildItem 'C:\Users\user\AppData\Local\Programs' -ErrorAction SilentlyContinue | Select-Object Name
