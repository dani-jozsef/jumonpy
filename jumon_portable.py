
import jumon
import metadata_db
import getpass

class InmemorySecretstore(object):

  def __init__(self, secret):
    self.secret = secret
  
  def get_secret(self):
    return self.secret


class JumonApp_portable(jumon.JumonApp):

  def __init__(self, iterations=None, fmt_string=None, secret=None, metadata_dbpath=None):
    if secret is not None:
      secret_store = InmemorySecretstore(secret)
    else:
      secret_store = None
    metadata_store = metadata_db.MetadataDb(metadata_dbpath)
    passphrase = getpass.getpass("Passphrase: ")
    super().__init__(passphrase, iterations, fmt_string, secret_store, metadata_store)
