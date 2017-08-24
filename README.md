Install
--------

In PowerShell console:
```
iex ((new-object net.webclient).DownloadString('https://s3.amazonaws.com/ODME/BrowserTestRunner/install.ps1'))
```

or

In Windows Command Line:
```
@powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((new-object net.webclient).DownloadString('https://s3.amazonaws.com/ODME/BrowserTestRunner/install.ps1'))"
```