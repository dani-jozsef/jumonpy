#!/usr/bin/env python3
# coding: utf-8


class Totugane(object):

    glyphs = (
        ['ka', 'ki', 'ku', 'ke', 'ko'] +
        ['ga', 'gi', 'gu', 'ge', 'go'] +
        ['sa', 'si', 'su', 'se', 'so'] +
        ['za', 'zi', 'zu', 'ze', 'zo'] +
        ['ta', 'ti', 'tu', 'te', 'to'] +
        ['da', 'di', 'du', 'de', 'do'] +
        ['na', 'ni', 'nu', 'ne', 'no'] +
        ['ha', 'hi', 'hu', 'he', 'ho'] +
        ['ba', 'bi', 'bu', 'be', 'bo'] +
        ['pa', 'pi', 'pu', 'pe', 'po'] +
        ['ma', 'mi', 'mu', 'me', 'mo'] +
        ['ya', 'yu', 'yo'] +
        ['ra', 'ri', 'ru', 're', 'ro'] +
        ['wa'])

    terminator = '='

    def encode(self, data):
        result = ''
        while len(data) > 0:
            head = data[:3]
            data = data[3:]
            triad = int.from_bytes(
                head + bytes([0] * (3 - len(head))),
                byteorder='big',
                signed=False)
            result += self.glyphs[(triad >> 18 & 0x3f)] + self.glyphs[(triad >> 12 & 0x3f)]
            if len(head) > 1:
                result += self.glyphs[(triad >> 6 & 0x3f)]
            if len(head) > 2:
                result += self.glyphs[(triad & 0x3f)]
            else:
                result += self.terminator
        return result
