#!/usr/bin/env python3
# coding: utf-8

import math

# iOS specific imports
import keychain
import ui
import dialogs

import totugane64
import passgen

appname = 'spellGen'
mysalt = b'totugane'  # change this value!


class spellGenGui(ui.View):

    def did_load(self):
        self.encoding = totugane64.Encoding()

        self.txt_service = self['txt_service']
        self.txt_account = self['txt_account']
        self.sld_iter = self['sld_iter']
        self.lbl_iter = self['lbl_iterdisp']
        self.btn_hash = self['btn_hash']
        self.btn_secret = self['btn_secret']
        self.txv_spell = self['txv_spell']

        self.sld_iter.action = self.sld_iter_update
        self.btn_hash.action = self.btn_hash_push
        self.btn_secret.action = self.btn_secret_push

        self.iter = 0

        secret = keychain.get_password(appname, appname)
        if secret is not None:
            self.passgen = passgen.Passgen(mysalt, secret)
            self.activate_button()

    def mypresent(self):
        if ui.get_screen_size()[1] >= 768:
            # iPad
            self.present('sheet')
        else:
            # iPhone
            self.present()

    def activate_button(self):
        self.btn_hash.enabled = True
        self.btn_hash.title = '✏️'

    def deactivate_button(self):
        self.btn_hash.enabled = False
        self.btn_hash.title = '⛔️'

    def sld_iter_update(self, sender):
        self.iter = math.floor(self.sld_iter.value * 10)
        if self.iter == 10:
            self.iter = 9
        self.lbl_iter.text = str(self.iter)

    def btn_hash_push(self, sender):
        service = self.passgen.cook_inputstring(
            self.txt_service.text).decode(encoding='utf-8')
        account = self.passgen.cook_inputstring(
            self.txt_account.text).decode(encoding='utf-8')
        self.txt_service.text = service
        self.txt_account.text = account
        if service:
            h = self.passgen.generate(service, account, self.iter)
            spell = self.encoding.encode(h)
            self.txv_spell.text = spell
        else:
            self.txv_spell.text = ''

    def btn_secret_push(self, sender):
        tmpsecret = self.secret
        if tmpsecret is None:
            tmpsecret = ''
        tmpsecret = dialogs.text_dialog(
            title='Set secret',
            text=tmpsecret,
            autocorrection=False,
            autocapitalization=ui.AUTOCAPITALIZE_NONE,
            spellchecking=False)
        if tmpsecret is None:
            return
        if tmpsecret:
            tmpsecret = self.passgen.setSecret(tmpsecret)
            keychain.set_password(appname, appname, tmpsecret)
            self.activate_button()
        else:
            self.deactivate_button()
            keychain.delete_password(appname, appname)
            self.passgen = None


gui = ui.load_view(appname)
gui.mypresent()
