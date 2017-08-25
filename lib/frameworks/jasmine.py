import json

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
