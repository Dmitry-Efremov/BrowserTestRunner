
import os, sys, time, requests, retrying

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from . import selenium_process

csd = os.path.dirname(os.path.abspath(__file__))


def Main(selenium=None, url=None, browser=None, timeout=None, output=None, framework=None, nosandbox=None):
	
	framework = __import__('lib.frameworks.'+framework, fromlist=['lib.frameworks'])
	
	if (selenium is None):
		selenium = selenium_process.run_selenium_process()
	
	try:
		wait_selenium_port(selenium)
		driver_browser = getattr(webdriver.DesiredCapabilities, browser.upper())
		if not (nosandbox is None):
			driver_browser["chromeOptions"] = {'args': ['--no-sandbox']}

		driver = webdriver.Remote( selenium, driver_browser )
		
		run(driver=driver, url=url, timeout=timeout, framework=framework, output=output)
		
	finally:
		selenium_process.stop_selenium_process()
	
@retrying.retry(stop_max_attempt_number=2, wait_fixed=1000, retry_on_result=lambda status: status != 200)
def wait_selenium_port(url):
	return requests.get(url).status_code
	
def run(driver=None, url=None, timeout=None, framework=None, output=None):
	
	try:
		driver.get( url )
		
		WebDriverWait( driver, timeout ).until( framework.isFinished )
		
		if ( output ):
		
			results = framework.GetXmlResults( driver )
			saveResults( results, output )
			sys_print( "Saved to: " + output )
			
		else:
		
			results = framework.GetResults( driver )
			printResults( results )

	finally:
		driver.close()

def saveResults( xmlResults, outputFile ):
	
	f = open( outputFile, "w" )
	f.write( xmlResults )
	f.close()
	
		
def printResults( results ):

	for obj in results:
		if not obj[ 'result' ]:
			sys_print()
			line = '%s, result: %s' % ( obj[ 'name' ], obj[ 'result' ] )
			line += ', error: %s' % obj[ 'error' ]
			sys_print( line )	

def sys_print( line = '' ):

	sys.stdout.flush()
	sys.stdout.write( line + '\n' )
	sys.stdout.flush()