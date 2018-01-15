import json
from selenium.webdriver.support.ui import WebDriverWait

def runTests( driver, url, timeout ):

    driver.get( url )
    WebDriverWait( driver, timeout ).until( isFinished )
    return {
        "json": getResults( driver ),
        "junit": getXmlResults( driver )
    }

def isFinished( driver ):

  return "Tests completed" in driver.find_element_by_id( "qunit-testresult" ).text

def getResults( driver ):

  selector = """
    var results = [];
    $( '#qunit-tests > li' ).each( function( i, el ) {
      results[i] = { 'name': $("> strong", el).clone().find('.counts').remove().end().text(),
             'result': $( el ).hasClass( 'pass' ),
             'error': $( '> ol ', el ).text() };
    });
    return JSON.stringify(results)
  """

  results = driver.execute_script( selector )
  return json.loads( results )

def getXmlResults( driver ):

  results = driver.execute_script( "return QUnit.jUnitReport.xml" )

  if ( not results ):

    import time
    time.sleep( 500 )
    raise Exception( "Please, place xml results into QUnit.jUnitReport.xml variable (https://github.com/JamesMGreene/qunit-reporter-junit)" )

  return results
