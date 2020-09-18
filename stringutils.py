#!/usr/bin/env python3
# coding: utf-8

import string


# Converts a string to a bytes object after trimming, ASCIIfying
# and optional conversion to lowercase
def cook_inputstring(input, lowercase=True):
	if lowercase:
		input = input.casefold()
	return input.strip().encode(
		encoding='ascii',
		errors='replace')


class SliceFormatter(string.Formatter):

    def get_value(self, key, args, kwds):
        if '|' in key:
            try:
                key, indexes = key.split('|')
                indexes = map(int, indexes.split(','))
                if key.isdigit():
                    return args[int(key)][slice(*indexes)]
                return kwds[key][slice(*indexes)]
            except KeyError:
                return kwds.get(key, 'Missing')
        return super(SliceFormatter, self).get_value(key, args, kwds)