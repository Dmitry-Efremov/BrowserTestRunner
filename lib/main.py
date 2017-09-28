import os, sys, time, requests, retrying, json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from . import selenium_process


def Main( seleniumServer = None, testsUrl = None, platform = None, browser = None, browserVersion = None, screenResolution = None, timeout = None, output = None, framework = None, nosandbox = None ):

  driver = None
  framework = __import__( "lib.frameworks." + framework, fromlist = [ "lib.frameworks" ] )

  if ( seleniumServer is None ):

    sysPrint( "Starting selenium ..." )

    seleniumServer = selenium_process.run_selenium_process()
    waitSeleniumPort( seleniumServer )

  try:

    driver_browser = getattr( webdriver.DesiredCapabilities, browser.upper() )

    if not ( nosandbox is None ):
      driver_browser[ "chromeOptions" ] = { "args": [ "--no-sandbox" ] }

    if not ( browserVersion is None ):
      driver_browser[ "version" ] = browserVersion

    if not ( screenResolution is None ):
      driver_browser[ "screenResolution" ] = screenResolution

    if not ( platform is None ):
      driver_browser[ "platform" ] = platform

    if not ( timeout is None ):
      driver_browser[ "maxDuration" ] = timeout

    sysPrint( "Connecting to selenium ..." )

    driver = webdriver.Remote( seleniumServer, driver_browser )

    sysPrint( "Selenium session id: %s" % ( driver.session_id ) )

    runTests( driver = driver, url = testsUrl, timeout = timeout, framework = framework, output = output )

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

  f = open( outputFile, "wb" )
  f.write( xmlResults.encode( "utf-8" ) )
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
