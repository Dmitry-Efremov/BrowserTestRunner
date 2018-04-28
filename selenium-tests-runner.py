#!/usr/bin/python
# coding: utf-8

import argparse


argsParser = argparse.ArgumentParser( description = "Run selenium tests in specified browser", formatter_class = argparse.RawTextHelpFormatter )

argsParser.add_argument( "--selenium-server", help = "URL of a selenium server. A selenium server will be started locally if this argument is not specified." )
argsParser.add_argument( "--tests-url", help = "URL where tests are served", required = True )
argsParser.add_argument( "--platform", help = "Platform to run browser, default: \"Windows 7\"", default = "Windows 7" )
argsParser.add_argument( "--browser", help = "Browser to run, e.g. \"chrome\", \"firefox\", \"internetexplorer\", \"edge\"", required = True )
argsParser.add_argument( "--browser-version", help = "Version of browser" )
argsParser.add_argument( "--screen-resolution", help = "Screen resolution, default: 1024x768", default = "1024x768" )
argsParser.add_argument( "--framework", help = "Javascript test framework used", required = True, choices = [ "jasmine", "qunit" ] )
argsParser.add_argument( "--max-duration", help = "Maximum tests duration in seconds, default: 300.", type = int, default = 300 )
argsParser.add_argument( "--tunnel-id", help = "SauceLabs tunnel identifier." )
argsParser.add_argument( "--idle-timeout", help = "SauceLabs idle test timeout, default: 90.", type = int, default = 90 )
argsParser.add_argument( "--output", help = "Filename to store JUnit xml results." )
argsParser.add_argument( "--chrome-options", help = "Options for Chrome webdriver separated by commas, example: --chrome-options=\"--js-flags=--expose-gc,--enable-precise-memory-info\"" )
argsParser.add_argument( "--prerun-script-url", help = "Url of the script executed before run." )
argsParser.add_argument( "--one-by-one", action = "store_true", help = "Run tests one by one." )
argsParser.add_argument( "--avoid-proxy", action = "store_true", help = "Configures Sauce Labs to avoid using the  Selenium HTTP proxy server and have browsers communicate directly with your servers. Firefox and Google Chrome under WebDriver aren't affected by this flag." )
argsParser.add_argument( "--tests-urls", help = "URLs where tests are served for parallel runs.",  nargs='+' )
argsParser.add_argument( "--enable-test-logs", action = "store_true", help = "Print to console browser, performance and driver logs after running tests for debug purposes")
argsParser.add_argument( "--browsers-count", help = "Number of selenium servers to run tests")

args = argsParser.parse_args()

print "Arguments:"
print args

from lib.main import Main

Main(

  testsUrl = args.tests_url,
  browser = args.browser,
  framework = args.framework,
  seleniumServer = args.selenium_server,
  platform = args.platform,
  browserVersion = args.browser_version,
  screenResolution = args.screen_resolution,
  maxDuration = args.max_duration,
  tunnelId = args.tunnel_id,
  idleTimeout = args.idle_timeout,
  output = args.output,
  chromeOptions = args.chrome_options,
  prerunScriptUrl = args.prerun_script_url,
  oneByOne = args.one_by_one,
  avoidProxy = args.avoid_proxy,
  testsUrls = args.tests_urls,
  enableTestLogs = args.enable_test_logs,
  browsersCount = args.browsers_count
)
