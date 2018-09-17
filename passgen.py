#!/usr/bin/env python3
# coding: utf-8

import hashlib


class Passgen(object):

    maxiter = 200000
    separator = b'_'

    # Initializes generator with salt
    def __init__(self, salt):
        self.salt = salt
        self.secret = None

    # Sets the input string after trimming& ASCIIfying as secret
    def setSecret(self, secret):
        self.secret = self.cook_inputstring(secret, False)
        return self.secret

    # Generates a deterministic 256 bit key for a service and account string
    def generate(self, service, account, iteration):
        service = self.cook_inputstring(service)
        account = self.cook_inputstring(account)
        plaintext = self.separator.join([service, account, self.secret])
        h = hashlib.pbkdf2_hmac(
            'sha256',
            plaintext,
            self.salt,
            self.maxiter - iteration)
        return h

    # Converts a string to a bytes object after trimming, ASCIIfying
    # and optional conversion to lowercase
    def cook_inputstring(self, input, lowercase=True):
        if lowercase:
            input = input.casefold()
        return input.strip().encode(
            encoding='ascii',
            errors='replace')
