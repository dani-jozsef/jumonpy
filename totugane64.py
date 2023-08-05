#!/usr/bin/env python3
# coding: utf-8

import base64
import binascii

totugane64_glyphs = (
  [b'ka', b'ki', b'ku', b'ke', b'ko'] +
  [b'ga', b'gi', b'gu', b'ge', b'go'] +
  [b'sa', b'si', b'su', b'se', b'so'] +
  [b'za', b'zi', b'zu', b'ze', b'zo'] +
  [b'ta', b'ti', b'tu', b'te', b'to'] +
  [b'da', b'di', b'du', b'de', b'do'] +
  [b'na', b'ni', b'nu', b'ne', b'no'] +
  [b'ha', b'hi', b'hu', b'he', b'ho'] +
  [b'ba', b'bi', b'bu', b'be', b'bo'] +
  [b'pa', b'pi', b'pu', b'pe', b'po'] +
  [b'ma', b'mi', b'mu', b'me', b'mo'] +
  [b'ya', b'yu', b'yo'] +
  [b'ra', b'ri', b'ru', b're', b'ro'] +
  [b'wa', b'wo'])

_b64_glyph_decode_table = bytes([
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255,  62,  63,  62, 255,  63,  52,  53,  54,  55,
   56,  57,  58,  59,  60,  61, 255, 255, 255,  64, 255, 255, 255,
   0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,
   13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,
  255, 255, 255, 255,  63, 255,  26,  27,  28,  29,  30,  31,  32,
   33,  34,  35,  36,  37,  38,  39,  40,  41,  42,  43,  44,  45,
   46,  47,  48,  49,  50,  51, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255
])

_b64_glyph_encode_table = bytes([
   65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,
   78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,
   97,  98,  99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
  110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122,
   48,  49,  50,  51,  52,  53,  54,  55,  56,  57,  43,  47,  61,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
  255, 255, 255, 255, 255, 255, 255, 255, 255
])

_whitespace_characters = b'\t\n\v\f\r '

def base64_to_totugane64(input):
  indexes = input.translate(_b64_glyph_decode_table, delete=_whitespace_characters)
  try:
    output = b''.join(map(
      lambda value: totugane64_glyphs[value],
      indexes
    ))
    return output
  except IndexError as e:
    raise ValueError("Not a valid base64 byte string") from e

def totugane64_to_base64(input):
  clean_input = input.translate(None, delete=_whitespace_characters)
  glyphs = [clean_input[i:i+2] for i in range(0, len(clean_input), 2)]
  try:
    indexes = bytes(map(
      lambda glyph: totugane64_glyphs.index(glyph),
      glyphs
    ))
    output = indexes.translate(_b64_glyph_encode_table)
    return output
  except (ValueError, binascii.Error) as e:
    raise ValueError("Not a valid totugane64 byte string") from e

def totugane64_encode(input):
  b64_bytes = base64.standard_b64encode(input)
  totugane_bytes = base64_to_totugane64(b64_bytes)
  return totugane_bytes

def totugane64_decode(input):
  b64_bytes = totugane64_to_base64(input)
  plaintext_bytes = base64.standard_b64decode(b64_bytes)
  return plaintext_bytes