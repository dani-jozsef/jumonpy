#!/usr/bin/env python3
# coding: utf-8

import dbm
import json
from jumon import metadata_fields
import jumonconfig

class MetadataDb(object):
	
  def __init__(self, dbpath=None):
    self.dbpath = dbpath if dbpath is not None else jumonconfig.metadata_db_path
    dbm.open(file=self.dbpath, flag='c').close()

  def _save_record(self, key, value):
    with dbm.open(file=self.dbpath, flag='c') as db:
      dbvalue = json.dumps(value)
      db[key] = dbvalue

  def load_record(self, key):
    with dbm.open(file=self.dbpath, flag='r') as db:
      value = db.get(key, b'{}')
      return json.loads(value)

  def clear_record(self, key):
    with dbm.open(file=self.dbpath, flag='w') as db:
      try:
        del db[key]
      except KeyError:
        print('WARNING: No such metadata record')

  def increment_iteration(self, key):
    metadata = self.load_record(key)
    current_iteration = metadata.get(metadata_fields.PASSWORD_ITERATION, 0)
    metadata[metadata_fields.PASSWORD_ITERATION] = current_iteration + 1
    self._save_record(key, metadata)

  def set_fmt_string(self, key, fmt_string):
    metadata = self.load_record(key)
    metadata[metadata_fields.FMT_STRING] = fmt_string
    self._save_record(key, metadata)
