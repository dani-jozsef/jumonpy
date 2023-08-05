#!/usr/bin/env python3
# coding: utf-8

import stringutils as su
import jumon
import jumonconfig
import metadata_db

# iOS Pythonista specific imports
import keychain
import clipboard
import dialogs

def _passphrase_dialog():
  salt_dialog = dialogs.form_dialog(
    title = 'New Jumon Instance',
    fields = [{
      'key':'passphrase',
      'placeholder':'passphrase',
      'type':'password'
    }])
  if salt_dialog is None:
    return ''
  return salt_dialog['passphrase']

_keychain_service = 'jumon'

class KeychainSecretStore_iOS(object):

  def __init__(self, keychain_account=None):
    self.keychain_account = keychain_account if keychain_account is not None else jumonconfig.ios_keychain_account

  def clear_secret(self):
    keychain.delete_password(_keychain_service, self.keychain_account)
    print('Done.')

  def set_secret(self, secret):
    keychain.set_password(_keychain_service, self.keychain_account, secret)
    print('Done.')

  def get_secret(self):
    secret = keychain.get_password(_keychain_service, self.keychain_account)
    if secret is None:
      raise KeyError(f'No secret is set in the keychain under {_keychain_service}:{self.keychain_account}')
    return secret

class JumonApp_iOS(jumon.JumonApp):
  
  def __init__(self,
      iterations=None,
      fmt_string=None,
      keychain_account=None,
      metadata_dbpath=None):
    passphrase = _passphrase_dialog()
    secret_store = KeychainSecretStore_iOS(keychain_account)
    metadata_store = metadata_db.MetadataDb(metadata_dbpath)
    super().__init__(passphrase, iterations, fmt_string, secret_store, metadata_store)

  def gen_password(self, service, account='', password_iteration=None, fmt_string=None, copy=True):
    password = super().gen_password(service, account, password_iteration, fmt_string)
    if copy:
      clipboard.set(password)
      print("Password copied to clipboard...")
    return password
