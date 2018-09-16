#!/usr/bin/env python3
# coding: utf-8

import hashlib


class Passgen(object):

    maxiter = 200000

    def __init__(self, salt, secret):
        self.salt = salt
        self.secret = self.cook_inputstring(secret)

    def generate(self, service, account, iteration):
        service = self.cook_inputstring(service)
        account = self.cook_inputstring(account)
        plaintext = service + account + self.secret
        h = hashlib.pbkdf2_hmac(
            'sha256',
            plaintext,
            self.salt,
            self.maxiter - iteration)
        return h

    def cook_inputstring(self, input):
        return input.strip().casefold().encode(
            encoding='ascii',
            errors='replace')
