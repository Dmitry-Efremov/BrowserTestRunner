import os, sys, requests, retrying, json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from lib import selenium_process, log

webDriverWaitTimeout = 300


def Main( testsUrl, browser, framework, seleniumServer = None, platform = None, browserVersion = None, screenResolution = None,
          maxDuration = None, tunnelId = None, output = None, chromeOptions = None, prerunScriptUrl = None, oneByOne = False, avoidProxy = False, testsUrls = None ):

  driver = None
  drivers = []

  framework = __import__( "lib.frameworks." + framework, fromlist = [ "lib.frameworks" ] )

  if ( seleniumServer is None ):

    log.writeln( "Starting selenium ..." )

    seleniumServer = selenium_process.run_selenium_process()
    waitSeleniumPort( seleniumServer )

  try:

    driver_browser = getattr( webdriver.DesiredCapabilities, browser.upper() )

    if chromeOptions:
      opts = chromeOptions.split( "," )
      driver_browser[ "chromeOptions" ] = { "args": opts }

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

    if avoidProxy:
      driver_browser[ "avoidProxy" ] = True

    log.writeln( "Connecting to selenium ..." )
    
    if testsUrls:  
    
      from concurrent import futures
      
      with futures.ThreadPoolExecutor( max_workers=len(testsUrls) ) as executor:
        executions = []
        for testsUrl in testsUrls:
          executions.append( executor.submit( getDriver, seleniumServer, driver_browser, testsUrl ) )
        for execution in executions:
          drivers.append( execution.result() )
      
      runTestsInParallel( drivers, timeout = maxDuration, framework = framework, output = output )
      
    else:
    
      driver = getDriver( seleniumServer, driver_browser, testsUrl )

      runTests( driver = driver['driver'], url = testsUrl, timeout = maxDuration, framework = framework, output = output, oneByOne = oneByOne )

  finally:

    if driver:
      driver.quit()
      
    if drivers:
      for driver in drivers:
        driver["driver"].quit()
      
    selenium_process.stop_selenium_process()

def getDriver( seleniumServer, driver_browser, testsUrl ):
  
  driver = webdriver.Remote( seleniumServer, driver_browser )
  driver.set_page_load_timeout( webDriverWaitTimeout )
  log.writeln( "Selenium session id: %s" % ( driver.session_id ) )

  return { "driver": driver, "testsUrl": testsUrl }
    
@retrying.retry( stop_max_attempt_number = 2, wait_fixed = 1000, retry_on_result = lambda status: status != 200 )
def waitSeleniumPort( url ):

  return requests.get( url ).status_code
  
def runTestsInParallel( drivers, timeout, framework, output = None ):

  log.writeln( "Running tests in parallel, drivers count: %i" % ( len(drivers) ) )

  results = framework.runTestsInParallel( drivers, timeout )

  jsonResults = results[ "json" ]
  xmlResults = results[ "junit" ]

  if ( output ):

    saveResults( xmlResults, output )
    log.writeln( "JUnit xml saved to: " + output )
  

def runTests( driver, url, timeout, framework, output = None, oneByOne = False ):

  if oneByOne:

    log.writeln( "Running tests one by one" )

    results = framework.runTests( driver, url, timeout )

    jsonResults = results[ "json" ]
    xmlResults = results[ "junit" ]

  else:

    log.writeln( "Running tests ..." )

    driver.get( url )
    WebDriverWait( driver, timeout ).until( framework.isFinished )

    log.writeln( "Retrieving results ..." )

    jsonResults = framework.getResults( driver )

    if ( output ):

      xmlResults = framework.getXmlResults( driver )

  printResults( jsonResults )

  if ( output ):

    saveResults( xmlResults, output )
    log.writeln( "JUnit xml saved to: " + output )

def saveResults( xmlResults, outputFile ):

  outputPath = os.path.dirname( outputFile )

  if outputPath and not os.path.exists( outputPath ):
    os.makedirs( outputPath )

  f = open( outputFile, "wb" )
  f.write( xmlResults.encode( "utf-8" ) )
  f.close()

def printResults( results ):

  log.writeln( "Results:" )
  log.writeln( "  Passed: %r" % results[ "passed" ] )
  log.writeln( "  Duration: %f" % results[ "durationSec" ] )
  log.writeln( "  Suites: %d" % len( results[ "suites" ] ) )
