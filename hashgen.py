#!/usr/bin/env python3
# coding: utf-8

import hashlib
import stringutils as su


class Hashgen(object):

    # Separator string for the inputs
    separator = b'_'

    # Initializes generator with salt
    def __init__(self, salt, secret):
        self.salt = su.cook_inputstring(salt)
        self.secret = su.cook_inputstring(secret, False)

    # Generates a deterministic 256 bit key for a service and account string
    def gen_hash(self, service, account, iterations):
        if not self.secret:
            return None
        service = su.cook_inputstring(service)
        account = su.cook_inputstring(account)
        plaintext = self.separator.join([service, account, self.secret])
        h = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=plaintext,
            salt=self.salt,
            iterations=iterations)
        return h

