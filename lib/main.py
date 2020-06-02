import os, sys, requests, retrying, json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from lib import selenium_process, log, capabilities


def Main( testsUrl, browser, framework, seleniumServer = None, platform = None, browserVersion = None, screenResolution = None,
          maxDuration = 300, tunnelId = None, idleTimeout = None, output = None, chromeOptions = None, prerunScriptUrl = None,
          oneByOne = False, retries = 1, avoidProxy = False, testsUrls = None, browsersCount = None, azureRepository = None,
          enableTestLogs = False, w3cBeta = False):

  driver = None
  drivers = []

  framework = __import__( "lib.frameworks." + framework, fromlist = [ "lib.frameworks" ] )

  if ( seleniumServer is None ):

    log.writeln( "Starting selenium ..." )

    seleniumServer = selenium_process.run_selenium_process()
    waitSeleniumPort( seleniumServer )

  try:

    driver_browser = capabilities.get(
        w3cBeta = w3cBeta,
        browser = browser,
        browserVersion = browserVersion,
        platform = platform,
        enableTestLogs = enableTestLogs,
        screenResolution = screenResolution,
        maxDuration = maxDuration,
        tunnelId = tunnelId,
        idleTimeout = idleTimeout,
        prerunScriptUrl = prerunScriptUrl,
        avoidProxy = avoidProxy,
        chromeOptions = chromeOptions)

    log.writeln( str( driver_browser ) )
    log.writeln( "Connecting to selenium ..." )

    if browsersCount:

      from concurrent import futures

      with futures.ThreadPoolExecutor( max_workers = int( browsersCount ) ) as executor:

        executions = []

        for idx in range( 0, int( browsersCount ) ):
          executions.append( executor.submit( getDriverOptions, seleniumServer.format(idx), driver_browser, testsUrl, maxDuration) )

        for execution in executions:
          drivers.append( execution.result() )

      runTestsInParallel( list( drivers ), timeout = maxDuration, framework = framework, output = output, retries = retries, enableTestLogs = enableTestLogs )

      if not ( azureRepository is None ):

        from azure_storage import publish
        publish( output, azureRepository )

    else:

      if testsUrls:

        from concurrent import futures

        with futures.ThreadPoolExecutor( max_workers=len(testsUrls) ) as executor:

          executions = []

          for testsUrl in testsUrls:
            executions.append( executor.submit( getDriver, seleniumServer, driver_browser, testsUrl, maxDuration ) )

          for execution in executions:
            drivers.append( execution.result() )

        runTestsInParallel( list( drivers ), timeout = maxDuration, framework = framework, output = output, retries = retries, enableTestLogs = enableTestLogs )

      else:

        driver = getDriver( seleniumServer, driver_browser, testsUrl, maxDuration )

        runTests( driver = driver['driver'], url = testsUrl, timeout = maxDuration, framework = framework, output = output, oneByOne = oneByOne, enableTestLogs = enableTestLogs )

  finally:

    if driver:
      driver['driver'].quit()

    if drivers:
      for driver in drivers:
        if "driver" in driver:
          driver["driver"].quit()

    selenium_process.stop_selenium_process()

def getDriver( seleniumServer, driver_browser, testsUrl, timeout):

  driver = webdriver.Remote( seleniumServer, driver_browser )
  driver.set_page_load_timeout( timeout )

  log.writeln( "Selenium session id: %s, browser: %s" % ( driver.session_id, seleniumServer ) )

  return { "driver": driver, "testsUrl": testsUrl }

def getDriverOptions( seleniumServer, driver_browser, testsUrl, timeout):

  waitSeleniumPort( seleniumServer )
  return { "seleniumServer": seleniumServer, "driver_browser":driver_browser, "timeout": timeout, "testsUrl": testsUrl }

@retrying.retry( stop_max_attempt_number = 120, wait_fixed = 3000, retry_on_result = lambda status: status != 200 )
def waitSeleniumPort( url ):

  return requests.get( url ).status_code

def runTestsInParallel( drivers, timeout, framework, output = None, retries = 1, enableTestLogs = False ):

  log.writeln( "Running tests in parallel, drivers count: %i" % ( len(drivers) ) )

  results = framework.runTestsInParallel( drivers, timeout, retries, enableTestLogs )

  jsonResults = results[ "json" ]
  xmlResults = results[ "junit" ]

  if ( output ):

    saveResults( xmlResults, output )
    log.writeln( "JUnit xml saved to: " + output )


def runTests( driver, url, timeout, framework, output = None, oneByOne = False, enableTestLogs = False ):

  if oneByOne:

    log.writeln( "Running tests one by one" )

    results = framework.runTests( driver, url, timeout )

    jsonResults = results[ "json" ]
    xmlResults = results[ "junit" ]

  else:

    log.writeln( "Running tests ..." )

    driver.get( url )
    WebDriverWait( driver, timeout ).until( framework.isFinished )

    if enableTestLogs:
      log.writeTestLogs( driver )

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
