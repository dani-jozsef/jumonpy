#!/usr/bin/env python3
# coding: utf-8

# This module implements a password generator based on pbkdf2, and the
# totugane64 encoding

import hashlib

from . import stringutils as su
from . import totugane64

_separator = b'_'

def gen_hash(input, salt, iterations):
  """Generates a pbkdf2 hash from a plaintext byte string"""
  h = hashlib.pbkdf2_hmac(
      hash_name='sha256',
      password=input,
      salt=salt,
      iterations=iterations)
  return h

def _gen_account_string(service, account, secret):
  service = su.cook_inputstring(service)
  account = su.cook_inputstring(account)
  if secret is None:
    return _separator.join([service, account])
  secret = su.cook_inputstring(secret, lowercase=False)
  return _separator.join([service, account, secret])

def gen_spellstring(service, account, passphrase, iterations, secret):
  account_string = _gen_account_string(service, account, secret)
  passphrase = su.cook_inputstring(passphrase)
  h = gen_hash(
    input=account_string,
    salt=passphrase,
    iterations=iterations
  )
  return totugane64.totugane64_encode(h)
