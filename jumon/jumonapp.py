#!/usr/bin/env python3
# coding: utf-8

from . import jumonconfig
from . import passgen
from . import stringutils as su

class metadata_fields:
  PASSWORD_ITERATION = 'iteration'
  FMT_STRING = 'fmt_string'

def _format_spellstring(spellstring, password_iteration, fmt_string):
  return su.slice_formatter.format(
    fmt_string,
    spell = spellstring,
    lower = spellstring.lower(),
    upper = spellstring.upper(),
    iteration = password_iteration,
    password_iteration = password_iteration
  )

class JumonApp(object):

  def __init__(
      self,
      passphrase,
      iterations=None,
      fmt_string=None,
      secret_store=None,
      metadata_store=None):
    self.passphrase = passphrase
    self.iterations = iterations if iterations is not None else jumonconfig.iterations
    self.fmt_string = fmt_string if fmt_string is not None else jumonconfig.fmt_string
    self.secret_store = secret_store
    self.metadata_store = metadata_store

  def __call__(self, service, account='', password_iteration=None, fmt_string=None):
    return self.gen_password(service, account, password_iteration, fmt_string)

  def gen_password(self, service, account='', password_iteration=None, fmt_string=None):
    if self.secret_store is None:
      print("WARNING: No secret store is available")
    metadata = self.get_metadata(service, account)
    effective_password_iteration = password_iteration if password_iteration is not None else metadata[metadata_fields.PASSWORD_ITERATION]
    effective_fmt_string = fmt_string if fmt_string is not None else metadata[metadata_fields.FMT_STRING]
    return self._gen_password_with_metadata(service, account, effective_password_iteration, effective_fmt_string)

  def get_metadata(self, service, account=''):
    default_metadata = {
        metadata_fields.PASSWORD_ITERATION: 0,
        metadata_fields.FMT_STRING: self.fmt_string
      }
    if self.metadata_store is None:
      print("WARNING: No metadata store is available")
      return default_metadata
    key = self._get_metadata_key(service, account)
    effective_metadata = default_metadata | self.metadata_store.load_record(key)
    return effective_metadata
  
  def next_password(self, service, account=''):
    if self.metadata_store is None:
      print("WARNING: This call requires a metadata store")
      return None
    key = self._get_metadata_key(service, account)
    self.metadata_store.increment_iteration(key)
    return self.gen_password(service, account)

  def set_fmt_string(self, fmt_string, service, account=''):
    if self.metadata_store is None:
      print("WARNING: This call requires a metadata store")
      return None
    key = self._get_metadata_key(service, account)
    self.metadata_store.set_fmt_string(key, fmt_string)
    return self.gen_password(service, account)

  def clear_metadata(self, service, account=''):
    if self.metadata_store is None:
      print("WARNING: This call requires a metadata store")
      return None
    key = self._get_metadata_key(service, account)
    self.metadata_store.clear_record(key)
    return self.gen_password(service, account)

  def _gen_password_with_metadata(self, service, account, password_iteration, fmt_string):
    if password_iteration < 0:
      raise ValueError("Illegal password iteration (must be >= 0)")
    spellstring = str(self._gen_spellstring(service, account, password_iteration), encoding='ascii')
    return _format_spellstring(spellstring, password_iteration, fmt_string)

  def _get_metadata_key(self, service, account):
    return self._gen_spellstring(service, account, -1)

  def _gen_spellstring(self, service, account, password_iteration):
    return passgen.gen_spellstring(
      service,
      account,
      passphrase = self.passphrase,
      iterations = self.iterations - password_iteration,
      secret = self.secret_store.get_secret() if self.secret_store is not None else None
    )
  
