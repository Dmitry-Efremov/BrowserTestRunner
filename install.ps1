if ( -not (Test-Path .\BrowserTestRunner) ) {
	aws s3 cp s3://ODME/BrowserTestRunner/BrowserTestRunner.zip .\BrowserTestRunner.zip
	unzip .\BrowserTestRunner.zip
	rm .\BrowserTestRunner.zip
	
	if ((Get-Command "python.exe" -ErrorAction SilentlyContinue) -eq $null) {
		$pythonpath = ".\BrowserTestRunner\vendors\python"
	    #$python = "$pythonpath\python.exe"	
	    $pip = "$pythonpath\Scripts\pip.exe"
	    #$pip = Join-Path (Split-Path (get-command python).Path) "Scripts\pip.exe"
	} else {
	    $pythonpath = "python.exe"
		$pip = "pip.exe"
	}
	iex "$pip install -r BrowserTestRunner\requirements.txt"
} else {
	"Already installed"
}