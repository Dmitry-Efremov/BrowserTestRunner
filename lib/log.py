import sys

def writeln( message = "" ):

    write( message + "\n" )

def write( message = "" ):

    sys.stdout.flush()
    sys.stdout.write( message )
    sys.stdout.flush()
