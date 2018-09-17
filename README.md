# JumonPy

JumonPy is a simple, pbkdf2-based password generator utility.

It allows the generation of mnemonic password bases for any number of services and accounts, including the ability to generate 9 different "iterations" of passwords for a single service/account pair in case a password is compromised and needs to be replaced.

It stores a user-provided secret to be used in generating the passes in the keychain.

The core idea is from old Famicom (Japanese NES) games, which used password systems for 'saving' the game state. Unlike western versions, the Japanese passwords were uncannily mnemonic, thanks to the rather limited syllable set of the Japanese language.

To achieve similar results, spellGen uses a base64 representation of the hash function's output, with each glyph represented by a syllable. The result is a pronounceable string, a substring of which may be used as a convenient and mnemonic password.

# The "totugane64" encoding

Totugane64 is a riff on standard base64 encoding, replacing the single-character glyphs with two character syllables taken from Japanese syllabic script (encoded via ASCII). Totugane64 possesses prefix property, making decoding cheap, and is human readable, pronouncable and highly mnemonic. Ever wanted to memorize an ECDSA private key? Well now you can.

The commonly used Japanese syllables, excluding standalone wovels (ん is a standalone wovel too), number exactly 65. That is 64 without を, which is exclusively used as a particle in modern Japanese, ie. it's never part of a modern word. So the encoding alphabet with 64 glyphs, in gojūon ordering, is:

( ka ki ku ke ko
ga gi gu ge go
sa si su se so
za zi zu ze zo
ta ti tu te to
da di du de do
na ni nu ne no
ha hi hu he ho
ba bi bu be bo
pa pi pu pe po
ma mi mu me mo
ya yu yo
ra ri ru re ro
wa )

If the last 24bit sequence isn't full, instead of padding as in standard base64, a single terminator character is added to the end of the output to avoid data corruption from concatenating encoded streams. The terminator is the ASCII character =

The name "totugane" comes from the fact that the ASCII string 'aaa' encodes into 'totugane' (突金), which sounds kinda cool and could be translated as "metal piercer" or something similar. ;)
