# JumonPy

JumonPy is a simple, pbkdf2_hmac-based deterministic password generator utility.

It allows the generation of mnemonic password bases for any number of services and accounts, including the ability to generate different "iterations" of passwords for a single service/account pair in case a password is compromised and needs to be replaced, making use of a reverse hash chain.

The core idea came from old Famicom (Japanese NES) games, which used password systems for 'saving' the game state. Unlike western versions, the Japanese passwords were uncannily mnemonic, thanks to the rather limited syllable set of the Japanese language, and were referred to in Japanese gamer culture as "resurrection spells".

## How it works

Passwords are generated via pbkdf2, using the totugane64 encoding (see below) to generate a human-pronouncable, mnemonic string from them. The plaintext input of the pbkdf2 algorithm is the service, account and secret strings concatenated with separators, and a 'passphrase' which is used as the pbkdf2 salt. The passphrase, expected to be input on each instantiation, should provide short-term protection after the compromise of a device. The purpose of the secret string is to provide entropy and security, so having it be relatively long is a good idea.

To avoid self-harm via similar-looking Unicode characters, all these strings are limited to the ASCII character set (with non-ASCII characters replaced with a placeholder), and the service and account strings are both converted to lowercase.

The generated hash strings are then fed through a simple templating engine to generate passwords in any desired shape, with digits and special characters.

## How to use

The `JumonApp` class can be instantiated directly from `jumon.py`, or inherited from as in the `jumon_iOS.py` or `jumon_portable.py` files. JumonApp provides an interface for generating passwords, and manipulating metadata through the metadata store object (an implementation based on the `dbm` module is included in `metadata_db.py`).

The iOS Pythonista version adds some convenience tools like copying passwords to the clipboard, an iOS dialog for inputting the passphrase, and storing the secret string in the device keychain.

### On password templates

Templating format strings can be used to generate the desired length and shape of password. JumonApp uses a custom subclass of the Python string formatter, included in `stringutils.py`. It adds the ability to specify substrings: `'{mystr|1,5}'` is equivalent to `mystr[slice(1, 5)]`

Its use is relatively straightforward from the example included in `jumonconfig_example.py`. Available fields are `upper` and `lower` for the hash string in upper or lower case, and `iteration` for the password's iteration counter.

**NOTE: Make sure to copy `jumonconfig_example.py` into `jumonconfig.py` and personalize the values before running. `jumonconfig.py` is included in `.gitignore` to prevent accidentally pushing your configuration to a public repository.**

# The "totugane64" encoding

*Totugane64* is a riff on *base64 standard* encoding, replacing the single-character glyphs with two character syllables taken from Japanese syllabic script (romanized according to *ISO 3602 Strict* romanization, and encoded via ASCII). *Totugane64* possesses prefix property, making decoding cheap, is human readable, pronouncable and highly mnemonic. Ever wanted to memorize an ECDSA private key? Well now you can.

The commonly used Japanese syllables, excluding standalone wovels (ん/n is a standalone wovel too), number exactly 65. That is 64 without を/wo, which is exclusively used as a particle in modern Japanese, ie. it's never part of a modern word. This gives us a very natural use for for を/wo, as the totugane64 equivalent of the padding glyph =.

So the encoding alphabet with 64 glyphs, plus the padding glyph, in gojūon ordering, is:

```
ka ki ku ke ko
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
ya    yu    yo
ra ri ru re ro
wa          wo
```

The name "totugane" comes from the fact that the ASCII string 'aaa' encodes into 'totugane,' which sounds kinda cool and could be translated as "metal piercer" (突金) or something similar.

The implementation here focuses on simplicity, brevity and ease of understanding. It would be trivial to construct a more efficient and robust codec in something like Rust or C, but for most purposes, this version should suffice.
