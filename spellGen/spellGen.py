#!/usr/bin/env python3
# coding: utf-8

import hashlib
import keychain
import math
import ui
import dialogs

appname = 'spellGen'
mysalt = b'123' #change this value!
myiter = 0
mysecret = keychain.get_password(appname,appname)

syllabs = (['N'] +
  ['a','i','u','e','o'] +
  ['ka','ki','ku','ke','ko'] +
  ['ga','gi','gu','ge','go'] +
  ['sa','si','su','se','so'] +
  ['za','zi','zu','ze','zo'] +
  ['ta','ti','tu','te','to'] +
  ['da','di','du','de','do'] +
  ['na','ni','nu','ne','no'] +
  ['ha','hi','hu','he','ho'] +
  ['ba','bi','bu','be','bo'] +
  ['pa','pi','pu','pe','po'] +
  ['ma','mi','mu','me','mo'] +
  ['ra','ri','ru','re','ro'])

def do_magic( basebytes, iteration ):
	num = int.from_bytes(
		hashlib.pbkdf2_hmac('sha256', basebytes, mysalt, 200000 - myiter)
		,byteorder='big'
		,signed=False )
	spell=''
	while num > 0:
		mod = num % 66
		spell = syllabs[mod] + spell
		num = num // 66
	return spell

def collate_basestring( secret, service, account ):
	return ( service + account + secret )

def one_to_nine( fraction ):
	value = math.floor(fraction * 10)
	if value == 10:
		value = 9
	return value

def precook_string( unistring ):
	return unistring.casefold().strip()

def activate_button( button ):
	button.enabled = True
	button.title = '✏️'

def deactivate_button( button ):
	button.enabled = False
	button.title = '⛔️'

def sld_iter_update( sender ):
	global myiter
	lbl_iter = sender.superview['lbl_iterdisp']
	myiter = one_to_nine(sender.value)
	lbl_iter.text = str(myiter)

def btn_hash_push( sender ):
	txv_spell = sender.superview['txv_spell']
	txt_service = sender.superview['txt_service']
	txt_account = sender.superview['txt_account']
	sld_iter = sender.superview['sld_iter']
	
	myservice = precook_string(txt_service.text)
	myaccount = precook_string(txt_account.text)
	myiter = one_to_nine(sld_iter.value)
	myspell = ''
	txt_service.text = myservice
	txt_account.text = myaccount
	if myservice:
		mybytes = collate_basestring(mysecret,myservice,myaccount).\
		  encode(encoding='ascii',errors='replace')
		myspell = do_magic( mybytes, myiter )
	txv_spell.text = myspell

def btn_secret_push( sender ):
	global mysecret
	btn_hash = sender.superview['btn_hash']
	
	tmpsecret = mysecret
	if tmpsecret is None:
		tmpsecret = ''
	tmpsecret = dialogs.text_dialog(
		title='Set secret'
		,text=tmpsecret
		,autocorrection=False
		,autocapitalization=ui.AUTOCAPITALIZE_NONE
		,spellchecking=False)
	
	if tmpsecret is None:
		return
	tmpsecret = tmpsecret.strip()
	if tmpsecret:
		keychain.set_password(appname,appname,tmpsecret)
		mysecret = tmpsecret
		activate_button(btn_hash)
	else:
		keychain.delete_password(appname,appname)
		mysecret = None
		deactivate_button(btn_hash)

mainview = ui.load_view(appname)
if mysecret is not None:
	activate_button(mainview['btn_hash'])

if ui.get_screen_size()[1] >= 768:
	# iPad
	mainview.present('sheet')
else:
	# iPhone
	mainview.present()

