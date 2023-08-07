#!/usr/bin/env python3
# coding: utf-8

import string


def cook_inputstring(input, lowercase=True):
  """Converts a string to a bytes object after trimming and ASCIIfying, w/ optional conversion to lowercase"""
  if lowercase:
    input = input.casefold()
  return input.strip().encode(
    encoding='ascii',
    errors='replace')


class _SliceFormatter(string.Formatter):

  def get_value(self, key, args, kwds):
    if '|' in key:
      try:
        key, indexes = key.split('|')
        indexes = map(int, indexes.split(','))
        if key.isdigit():
          return args[int(key)][slice(*indexes)]
        return kwds[key][slice(*indexes)]
      except KeyError:
        return kwds[key]
    return super(_SliceFormatter, self).get_value(key, args, kwds)

slice_formatter = _SliceFormatter()