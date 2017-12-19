import os, sys, requests, retrying, json

from concurrent import futures

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from . import selenium_process


def Main( seleniumServer = None, testsUrl = None, platform = None, browser = None, browserVersion = None, screenResolution = None,
          framework = None, maxDuration = None, tunnelId = None, output = None, nosandbox = None, prerunScriptUrl = None ):

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

    if not ( maxDuration is None ):
      driver_browser[ "maxDuration" ] = maxDuration

    if not ( tunnelId is None ):
      driver_browser[ "tunnelIdentifier" ] = tunnelId

    if not ( prerunScriptUrl is None ):
      driver_browser[ "prerun" ] = { "executable": prerunScriptUrl, "background": "false" }
    driver_browser[ "idleTimeout" ] = 300

    sysPrint( "Connecting to selenium ..." )

    def getDriver( seleniumServer, driver_browser ):
      return webdriver.Remote( seleniumServer, driver_browser )

    drivers = []
    with futures.ThreadPoolExecutor(max_workers=5) as executor:
      executions = []
      for i in range(0, 5):
        executions.append( executor.submit( getDriver, seleniumServer, driver_browser ) )
      for execution in executions:
        drivers.append( execution.result() )

    #sysPrint( "Selenium session id: %s" % ( driver.session_id ) )

    runTests( drivers = drivers, url = testsUrl, timeout = maxDuration, framework = framework, output = output )

  finally:

    for driver in drivers:
      driver.quit()

    selenium_process.stop_selenium_process()

@retrying.retry( stop_max_attempt_number = 2, wait_fixed = 1000, retry_on_result = lambda status: status != 200 )
def waitSeleniumPort( url ):

  return requests.get( url ).status_code

def runTests( drivers = None, url = None, timeout = None, framework = None, output = None ):

  sysPrint( "Running tests ..." )

  results = framework.runTests( drivers, url, timeout )

  printResults( results )

  if ( output ):

    #results = framework.GetXmlResults( driver )
    saveResults( json.dumps( results, indent=4 ), output )
    sysPrint( "JUnit xml saved to: " + output )

def saveResults( xmlResults, outputFile ):

  outputPath = os.path.dirname( outputFile )

  if not os.path.exists( outputPath ):
    os.makedirs( outputPath )

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
