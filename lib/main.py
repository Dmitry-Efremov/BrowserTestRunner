import os, sys, time, requests, retrying, json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from . import selenium_process

csd = os.path.dirname( os.path.abspath( __file__) )


def Main( selenium = None, url = None, browser = None, timeout = None, output = None, framework = None, nosandbox = None ):

  framework = __import__( "lib.frameworks." + framework, fromlist = [ "lib.frameworks" ] )

  if ( selenium is None ):

    sysPrint( "Starting selenium ..." )

    selenium = selenium_process.run_selenium_process()
    waitSeleniumPort( selenium )

  try:

    driver_browser = getattr( webdriver.DesiredCapabilities, browser.upper() )

    if not ( nosandbox is None ):
      driver_browser[ "chromeOptions" ] = { "args": [ "--no-sandbox" ] }

    sysPrint( "Connecting to selenium ..." )

    driver = webdriver.Remote( selenium, driver_browser )

    runTests( driver = driver, url = url, timeout = timeout, framework = framework, output = output )

  finally:

    if driver:
      driver.quit()

    selenium_process.stop_selenium_process()

@retrying.retry( stop_max_attempt_number = 2, wait_fixed = 1000, retry_on_result = lambda status: status != 200 )
def waitSeleniumPort( url ):

  return requests.get( url ).status_code

def runTests( driver = None, url = None, timeout = None, framework = None, output = None ):

  sysPrint( "Running tests ..." )

  driver.get( url )

  WebDriverWait( driver, timeout ).until( framework.isFinished )

  results = framework.GetResults( driver )
  printResults( results )

  if ( output ):

    results = framework.GetXmlResults( driver )
    saveResults( results, output )
    sysPrint( "JUnit xml saved to: " + output )

def saveResults( xmlResults, outputFile ):

  f = open( outputFile, "w" )
  f.write( xmlResults )
  f.close()

def printResults( results ):

  sysPrint( "Results:" )
  sysPrint( "  Passed: %r" % results[ "passed" ] )
  sysPrint( "  Duration: %f" % results[ "durationSec" ] )
  sysPrint( "  Suites: %d" % len( results[ "suites" ] ) )

def sysPrint( line = "" ):

  sys.stdout.flush()
  sys.stdout.write( line + "\n" )
  sys.stdout.flush()
