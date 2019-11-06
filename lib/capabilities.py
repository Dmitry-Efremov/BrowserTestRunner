from selenium import webdriver

def get( w3cBeta, browser, browserVersion, platform, enableTestLogs, screenResolution, maxDuration, tunnelId, idleTimeout, prerunScriptUrl, avoidProxy, chromeOptions ):

    browser_name = browser.upper()
    capabilities = getattr( webdriver.DesiredCapabilities, browser_name ).copy()
    if enableTestLogs:
        capabilities[ "loggingPrefs"] = { "performance": "ALL", "browser": "ALL", "driver": "ALL" }

    if w3cBeta:

        if "platform" in capabilities:
            capabilities[ "platformName" ] = capabilities[ "platform" ]
            del capabilities[ "platform" ]

        if "version" in capabilities:
            del capabilities[ "version" ]

        if browser_name == "CHROME":
            capabilities[ "browserName" ] = "googlechrome"
            options = { "w3c": True }
            capabilities[ webdriver.ChromeOptions.KEY ] = options
            if chromeOptions:
                options[ "args" ] = chromeOptions.split( "," )

        if not ( browserVersion is None ):
            capabilities[ "browserVersion" ] = browserVersion
        else:
            capabilities[ "browserVersion" ] = "latest"

        if not ( platform is None ):
            capabilities[ "platformName" ] = platform

        sauce_options = { "seleniumVersion": "3.11.0" }

        if browser_name == "INTERNETEXPLORER":
            sauce_options[ "iedriverVersion" ] = "3.12.0"

        set_sauce_specific_capabilities(
            sauce_options,
            screenResolution,
            maxDuration,
            tunnelId,
            idleTimeout,
            prerunScriptUrl,
            avoidProxy)

        capabilities[ "sauce:options" ] = sauce_options
    else:

        if chromeOptions:
            opts = chromeOptions.split( "," )
            capabilities[ "chromeOptions" ] = { "args": opts }

        if not ( browserVersion is None ):
            capabilities[ "version" ] = browserVersion

        if not ( platform is None ):
            capabilities[ "platform" ] = platform

        set_sauce_specific_capabilities(
            capabilities,
            screenResolution,
            maxDuration,
            tunnelId,
            idleTimeout,
            prerunScriptUrl,
            avoidProxy)

    return capabilities

def set_sauce_specific_capabilities(
        capabilities,
        screenResolution,
        maxDuration,
        tunnelId,
        idleTimeout,
        prerunScriptUrl,
        avoidProxy):

    if not ( screenResolution is None ):
        capabilities[ "screenResolution" ] = screenResolution

    if not ( maxDuration is None ):
        capabilities[ "maxDuration" ] = maxDuration

    if not ( tunnelId is None ):
        capabilities[ "tunnelIdentifier" ] = tunnelId

    if not ( idleTimeout is None ):
        capabilities[ "idleTimeout" ] = idleTimeout

    if not ( prerunScriptUrl is None ):
        capabilities[ "prerun" ] = { "executable": prerunScriptUrl, "background": "false" }

    if avoidProxy:
        capabilities[ "avoidProxy" ] = True
