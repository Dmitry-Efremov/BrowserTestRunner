import sys
from datetime import datetime


def writeln( message = "" ):

    write( message + "\n" )

def write( message = "" ):

    sys.stdout.flush()
    sys.stdout.write( message )
    sys.stdout.flush()

def writeTestLog( driver, log_type ):

    writeln( "Log '%s':" % log_type )

    for entry in driver.get_log( log_type ):

        entry[ u"timestamp" ] = datetime.fromtimestamp( int( entry[ u"timestamp" ] ) / 1000 ).strftime( "%H:%M:%S" )
        writeln( str( entry ) )

def writeTestLogs( driver ):

    for cur_type in [ "browser", "performance", "driver" ]:
        writeTestLog( driver, cur_type )
