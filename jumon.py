#!/usr/bin/env python3
# coding: utf-8

import dbm
import json
import time
import passgen
import stringutils as su


dbname = 'jumon'
default_fmt_string = '{spell|0,20}.{password_iteration}'
iterations = 200000


def save_record(key, value):
	try:
		with dbm.open(file=dbname, flag='c') as db:
			dbkey = su.cook_inputstring(key)
			dbvalue = json.dumps(value)
			db[dbkey] = dbvalue
	except:
		print('Db access failed on save')


def load_record(key):
	try:
		with dbm.open(file=dbname, flag='r') as db:
			dbkey = su.cook_inputstring(key)
			value = db.get(dbkey)
			return json.loads(value)
	except:
		return None


def clear_record(key):
	try:
		with dbm.open(file=dbname, flag='w') as db:
			db.pop(key)
	except:
		print('No such record or db access failed on delete')


def get_record_with_init(index):
	meta = load_record(index)
	if not meta:
		meta = { 'firstused': time.time() }
		save_record(index, meta)
	return meta


def get_password_iteration(meta):
	return meta.get('password_iteration', 0)


class Jumon(object):

	def __init__(self, salt, secret, fmt_string=default_fmt_string):
		self.passgen = passgen.Passgen(salt, secret, iterations)
		self.fmt_string = fmt_string

	def __call__(self, service, account=''):
		index = self.passgen.gen_spellstring(service, account, -1)
		meta = get_record_with_init(index)
		return self.gen_password(service, account, meta)	

	def next_password(self, service, account):
		index = self.passgen.gen_spellstring(service, account, -1)
		meta = get_record_with_init(index)
		meta['password_iteration'] = get_password_iteration(meta) + 1
		save_record(index, meta)
		return self.gen_password(service, account, meta)

	def set_fmt_string(self, service, account, fmt_string):
		index = self.passgen.gen_spellstring(service, account, -1)
		meta = get_record_with_init(index)
		meta['fmt_string'] = fmt_string
		save_record(index, meta)
		return self.gen_password(service, account, meta)

	def clear_meta(self, service, account):
		index = self.passgen.gen_spellstring(service, account, -1)
		clear_record(index)
		print('Done.')

	def gen_password(self, service, account, meta):
		return self.passgen.gen_password(
			service=service,
			account=account,
			password_iteration=get_password_iteration(meta),
			fmt_string=self.__get_fmt_string(meta)
		)
	
	def __get_fmt_string(self, meta):
		return meta.get('fmt_string', self.fmt_string)