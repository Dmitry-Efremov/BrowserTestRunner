#!/usr/bin/python
# coding: utf-8

# © 2015 Dell Inc.
# ALL RIGHTS RESERVED.

import sys
sys.path.append('env')

import argparse

parser = argparse.ArgumentParser(description='Run selenium tests locally in specified browser')
parser.add_argument('--selenium-server', help='URL of a selenium server. A selenium serve will be started locally if the argument not specified.')
parser.add_argument('--tests-url', help='an URL where tests are served', required=True)
parser.add_argument('--browser', help='A browser to run', required=True, choices=['chrome', 'firefox', 'internetexplorer'])
parser.add_argument('--framework', help='A js test framework used', required=True, choices=['jasmine-1.3', 'jasmine-2', 'qunit'])
parser.add_argument('--timeout', type=int, default=60, help='Tests timeout in seconds')
parser.add_argument('--output', help='XML filename to store results. Default: stdout.')
parser.add_argument('nosandbox', help='Options for chrome webdriver disables sandbox.')

args = parser.parse_args(sys.argv[1:])
print(args)

from lib.main import Main

Main(
	selenium=args.selenium_server,
	url=args.tests_url,
	browser=args.browser,
	timeout=args.timeout,
	output=args.output,
	framework=args.framework,
	nosandbox=args.nosandbox
)