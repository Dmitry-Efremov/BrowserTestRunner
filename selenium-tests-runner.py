#!/usr/bin/python
# coding: utf-8

import sys, argparse
sys.path.append( "env" ) # ???

argsParser = argparse.ArgumentParser( description = "Run selenium tests in specified browser" )
argsParser.add_argument( "--selenium-server", help = "URL of a selenium server. A selenium server will be started locally if this argument is not specified." )
argsParser.add_argument( "--tests-url", help = "URL where tests are served", required = True )
argsParser.add_argument( "--platform", help = "Platform to run browser, default: 'Windows 7'", default = "Windows 7" )
argsParser.add_argument( "--browser", help = "Browser to run", required = True, choices = [ "chrome", "firefox", "internetexplorer" ] )
argsParser.add_argument( "--browser-version", help = "Version of browser" )
argsParser.add_argument( "--screen-resolution", help = "Screen resolution, default: 1024x768", default = "1024x768" )
argsParser.add_argument( "--framework", help = "Javascript test framework used", required = True, choices = [ "jasmine", "qunit" ] )
argsParser.add_argument( "--timeout", type = int, default = 60, help = "Tests timeout in seconds, default: 60." )
argsParser.add_argument( "--output", help = "Filename to store JUnit xml results." )
argsParser.add_argument( "--nosandbox", help = "Option for Chrome webdriver: disables sandbox." )

args = argsParser.parse_args()

print "Arguments:"
print args

from lib.main import Main

Main(

  selenium = args.selenium_server,
  url = args.tests_url,
  platform = args.platform,
  browser = args.browser,
  browserVersion = args.browser_version,
  screenResolution = args.screen_resolution,
  timeout = args.timeout,
  output = args.output,
  framework = args.framework,
  nosandbox = args.nosandbox
)
