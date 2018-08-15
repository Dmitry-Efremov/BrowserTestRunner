import os, sys, traceback
import log
from azure.storage.blob import BlockBlobService


def publish( results, repository ):

  try:

    log.writeln( "Publish tests results from \"%s\" to azure \"%s\\%s\"" % ( results, repository, results ) )

    azureAccount = os.getenv( "AZURE_STORAGE_ACCOUNT" )
    azureKey = os.getenv( "AZURE_STORAGE_ACCOUNT_KEY" )

    if azureAccount and azureKey:

      blobService = BlockBlobService( account_name = azureAccount, account_key = azureKey )
      blobService.create_container( repository )
      blobService.create_blob_from_path( repository, results, results )

    else:

      log.writeln( "WARNING: Azure Storage credentials not found." )

  except Exception as err:

    log.writeln( "ERROR: %s" % err )
    traceback.print_exc()
