#!/usr/bin/env python3
# coding: utf-8

import dbm
import json
import time
import passgen
import stringutils as su


dbname = 'jumon'
default_fmt_string = '{spell|0,20}.{password_iteration}'
iterations = 100000


def saverec(key, value):
	try:
		with dbm.open(file=dbname, flag='c') as db:
			dbkey = su.cook_inputstring(key)
			dbvalue = json.dumps(value)
			db[dbkey] = dbvalue
	except:
		print('Db access failed on save')


def loadrec(key):
	try:
		with dbm.open(file=dbname, flag='r') as db:
			dbkey = su.cook_inputstring(key)
			value = db.get(dbkey)
			return json.loads(value)
	except:
		return None


def clearrec(key):
	try:
		with dbm.open(file=dbname, flag='w') as db:
			db.pop(key)
	except:
		print('No such record or db access failed on delete')


def getrecord(index):
	meta = loadrec(index)
	if not meta:
		meta = { 'firstused': time.time() }
		saverec(index, meta)
	return meta


def get_fmt_string(meta):
	return meta.get('fmt_string', default_fmt_string)


def get_password_iteration(meta):
	return meta.get('password_iteration', 0)


class Jumon(object):

	def __init__(self, salt, secret):
		self.passgen = passgen.Passgen(salt, secret, iterations)

	def __call__(self, service, account):
		index = self.passgen.gen_spellstring(service, account, -1)
		meta = getrecord(index)
		return self.gen_password(service, account, meta)	

	def next_password(self, service, account):
		index = self.passgen.gen_spellstring(service, account, -1)
		meta = getrecord(index)
		meta['password_iteration'] = get_password_iteration(meta) + 1
		saverec(index, meta)
		return self.gen_password(service, account, meta)

	def set_fmt_string(self, service, account, fmt_string):
		index = self.passgen.gen_spellstring(service, account, -1)
		meta = getrecord(index)
		meta['fmt_string'] = fmt_string
		saverec(index, meta)
		return self.gen_password(service, account, meta)

	def clear_meta(self, service, account):
		index = self.passgen.gen_spellstring(service, account, -1)
		clearrec(index)
		print('Done.')

	def gen_password(self, service, account, meta):
		return self.passgen.gen_password(
			service=service,
			account=account,
			password_iteration=get_password_iteration(meta),
			fmt_string=get_fmt_string(meta)
		)