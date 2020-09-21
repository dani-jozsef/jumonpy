#!/usr/bin/env python3
# coding: utf-8

# iOS specific imports
import keychain
import stringutils as su
import jumon

keychain_service = 'jumon'
keychain_account = 'secret'


# Clears saved secret
def clearSecret():
    keychain.delete_password(keychain_service, keychain_account)
    print('Done.')


def updateSecret(secret):
    keychain.set_password(keychain_service, keychain_account, secret)
    print('Done.')


def getSecret():
    return keychain.get_password(keychain_service, keychain_account)


def newJumon(salt, fmt_string=jumon.default_fmt_string):
    secret = getSecret()
    return jumon.Jumon(salt, secret, fmt_string)
