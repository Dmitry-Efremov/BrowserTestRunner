import subprocess, os

selenium_proc = None
csd = os.path.dirname(os.path.abspath(__file__))

def run_selenium_process():
	global selenium_proc
	cmd = ['java','-jar', os.path.abspath(os.path.join(csd, '..', 'vendors', 'selenium-server-standalone-2.47.1.jar'))]
	
	selenium_env = os.environ.copy()
	selenium_env["PATH"] = selenium_env["PATH"] + os.pathsep + os.path.abspath(os.path.join(csd, '..', 'vendors'))
	
	selenium_proc = subprocess.Popen(cmd, env=selenium_env)
	return "http://localhost:4444/wd/hub"
	
def stop_selenium_process():
	global selenium_proc
	if ( selenium_proc ):
		selenium_proc.kill()
		selenium_proc = None