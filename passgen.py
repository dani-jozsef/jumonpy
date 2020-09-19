#!/usr/bin/env python3
# coding: utf-8

import totugane64
import hashgen
import stringutils as su


encoding = totugane64.Encoding()


fmt = su.SliceFormatter()


class Passgen(object):

	def __init__(self, salt, secret, iterations):
		self.hashgen = hashgen.Hashgen(salt, secret)
		self.iterations = iterations

	def gen_spellstring(self, service, account, password_iteration):
		h = self.hashgen.gen_hash(
			service = service,
			account = account,
			iterations = self.iterations - password_iteration
		)
		return encoding.encode(h)

	def gen_password(self, service, account, password_iteration, fmt_string):
		spell = self.gen_spellstring(
			service = service,
			account = account,
			password_iteration = password_iteration
		)
		return fmt.format(
			fmt_string,
			spell = spell,
			password_iteration = password_iteration
		)
