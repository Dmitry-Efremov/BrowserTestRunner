import os, sys, traceback
import log
from azure.storage.blob import BlockBlobService

def getService(  ):

  azureAccount = os.getenv( "AZURE_STORAGE_ACCOUNT" )
  azureKey = os.getenv( "AZURE_STORAGE_ACCOUNT_KEY" )

  if azureAccount and azureKey:

    blobService = BlockBlobService( account_name = azureAccount, account_key = azureKey )

  else:

    log.writeln( "WARNING: Azure Storage credentials not found." )


def main():

  service = getService()

try:

  main()

except Exception as err:

  log.writeln( "ERROR: %s" % err )
  traceback.print_exc()
