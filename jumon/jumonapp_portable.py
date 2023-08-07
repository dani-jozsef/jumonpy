#!/usr/bin/env python3
# coding: utf-8

from getpass import getpass

from .jumonapp import JumonApp
from .metadata_db import MetadataDb

class InmemorySecretstore(object):

  def __init__(self, secret):
    self.secret = secret
  
  def get_secret(self):
    return self.secret


class JumonApp_portable(JumonApp):

  def __init__(self, iterations=None, fmt_string=None, secret=None, metadata_dbpath=None):
    if secret is not None:
      secret_store = InmemorySecretstore(secret)
    else:
      secret_store = None
    metadata_store = MetadataDb(metadata_dbpath)
    passphrase = getpass("Passphrase: ")
    super().__init__(passphrase, iterations, fmt_string, secret_store, metadata_store)
