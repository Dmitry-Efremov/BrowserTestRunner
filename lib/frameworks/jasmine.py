import json
import retrying
import sys
from selenium.webdriver.support.ui import WebDriverWait
from itertools import groupby

from concurrent import futures

def runTests( drivers, url, timeout ):

    driver = drivers[0]
    driver.get( url )
    WebDriverWait( driver, 60 ).until( isFinished ) # need to decrease timeout value here
    tests = getTests( driver )

    newDrivers = []
    port = 8081
    for driver in drivers:
        newDrivers.append( {"driver": driver, "port": ":" + str(port) } )
        port = port + 1
    drivers = newDrivers
    testResults = []

    with futures.ThreadPoolExecutor( max_workers=len( drivers ) ) as executor:
        executions = []
        for test in tests:
            executions.append( executor.submit( runTest, drivers, test, 60 ) )
        for execution in executions:
            exception = execution.exception()
            if exception is not None:
                sys.stdout.flush()
                sys.stdout.write( "Got exception that broke everything: " + str( exception ) + "\n" )
                sys.stdout.flush()
            else:
                testResults.append( execution.result() )

    suites = groupTestSuites( testResults )
    testResults = {
        "suites": suites,
        "durationSec": sum( map( lambda x: x[ "durationSec" ], suites ) ),
        "passed": all( map( lambda x: x[ "passed" ], suites ) )
    }
    return testResults

def runTest( driversPool, url, timeout ):

    driver = None
    try:
        driver = driversPool.pop()
        return runTestInternal( driver["driver"], url.replace(":8084", driver["port"]), timeout )
    finally:
        if driver:
            driversPool.append( driver )

@retrying.retry( stop_max_attempt_number = 5, wait_fixed = 1000 )
def runTestInternal( driver, url, timeout ):
    try:
        sys.stdout.flush()
        sys.stdout.write( "Running test " + url + "\n" )
        sys.stdout.flush()

        driver.get( url )

        sys.stdout.flush()
        sys.stdout.write( "Loaded url " + "\n" )
        sys.stdout.flush()

        WebDriverWait( driver, timeout ).until( isFinished ) # need to decrease timeout value here

        sys.stdout.flush()
        sys.stdout.write( "Waited" + "\n" )
        sys.stdout.flush()
        testResult = GetResults( driver )

        sys.stdout.flush()
        sys.stdout.write( "Got results" + "\n" )
        sys.stdout.flush()

        sys.stdout.flush()
        sys.stdout.write( json.dumps( testResult, indent=2 ) + "\n" )
        sys.stdout.flush()

        parentSuite = filterByDuration( testResult[ "suites" ] ).pop()

        sys.stdout.flush()
        sys.stdout.write( "Filtered by duration" + "\n" )
        sys.stdout.flush()

        sys.stdout.flush()
        sys.stdout.write( json.dumps( parentSuite, indent=2 ) + "\n" )
        sys.stdout.flush()

        reduceSuite( parentSuite )

        sys.stdout.flush()
        sys.stdout.write( "Reduced suite" + "\n" )
        sys.stdout.flush()

        sys.stdout.flush()
        sys.stdout.write( json.dumps( parentSuite, indent=2 ) + "\n" )
        sys.stdout.flush()

        return parentSuite
    except Exception as e:
        sys.stdout.flush()
        sys.stdout.write( "Got exception: " + str( e ) + "\n" )
        sys.stdout.flush()
        raise

def groupTestSuites( testSuites ):
    groupedSuites = []
    for description, group in groupby( testSuites, lambda x: x[ "description" ] ):
        group = list( group )
        suites = list( filter( lambda x: x.get( "suites" ), group ) )
        specs = list( filter( lambda x: x.get( "specs" ), group ) )
        childSuites = groupTestSuites( list( map( lambda x: list( x[ "suites" ] ).pop(), suites ) ) )
        childSpecs = list( map( lambda x: list( x["specs" ] ).pop(), specs ) )
        suite = {
            "description": description,
            "durationSec": sum( map( lambda x: x[ "durationSec" ], childSuites + childSpecs ) ),
            "passed": all( map( lambda x: x[ "passed" ], childSuites + childSpecs ) ),
            "suites": childSuites,
            "specs": childSpecs
        }
        groupedSuites.append( suite )
    return groupedSuites

def reduceSuite( parentSuite ):
    parentSuite[ "specs" ] = list( filter( lambda x: x[ "durationSec" ], parentSuite[ "specs" ] ) )
    parentSuite[ "suites" ] = filterByDuration( parentSuite[ "suites" ] )
    for suite in parentSuite[ "suites" ]:
        reduceSuite( suite )

def filterByDuration( items ):
    return list( filter( lambda item: item[ "durationSec" ] != 0, items ) )

def getTests( driver ):
    return driver.execute_script( "return jasmineTests" )

def isFinished( driver ):
  return driver.find_element_by_css_selector( ".duration" ).text.startswith( "finished" )

def GetResults( driver ):
  selector = "return JSON.stringify( jasmine.getJSReport() )"
  results = driver.execute_script( selector )
  return json.loads( results )

def GetXmlResults( driver ):

  selector = 'return jasmine.JUnitXmlReporter.outputXml'
  results = driver.execute_script( selector )
  return results
