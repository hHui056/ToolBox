from pysm4 import sm4
import wx

from ui.encryAndDecry.sm4.SM4Panel import SM4Panel


class SM4(SM4Panel):
    def __init__(self, parent):
        SM4Panel.__init__(self, parent)
        # 0-CBC 1-ECB
        self.encrypt_model = 0

    def choice_cbc(self, event):
        self.encrypt_model = 0

    def choice_ecb(self, event):
        self.encrypt_model = 1

    def doEncrypt(self, event):
        data = self.edit_plain.GetValue()
        if data == '':
            wx.MessageDialog(self, '待加密数据不能为空', '操作提醒', wx.OK).ShowModal()
            return
        key = self.edit_secret_key.GetValue()
        iv = self.edit_iv.GetValue()
        if len(key) != 16:
            wx.MessageDialog(self, 'SecretKey必须为16位', '操作提醒', wx.OK).ShowModal()
            return
        if len(iv) != 16 and self.encrypt_model == 0:
            wx.MessageDialog(self, 'iv必须为16位', '操作提醒', wx.OK).ShowModal()
            return
        result = ''
        if self.encrypt_model == 0:
            result = self.encryptCBC(data, key, iv)
        elif self.encrypt_model == 1:
            result = self.encryECB(data, key)

        self.edit_cipher.SetValue(result)

    def doDecrypt(self, event):
        cipherText = self.edit_cipher.GetValue()
        if cipherText == '':
            wx.MessageDialog(self, '密文不能为空', '操作提醒', wx.OK).ShowModal()
            return
        key = self.edit_secret_key.GetValue()
        iv = self.edit_iv.GetValue()
        if len(key) != 16:
            wx.MessageDialog(self, 'SecretKey必须为16位', '操作提醒', wx.OK).ShowModal()
            return
        if len(iv) != 16 and self.encrypt_model == 0:
            wx.MessageDialog(self, 'iv必须为16位', '操作提醒', wx.OK).ShowModal()
            return
        result = ''
        if self.encrypt_model == 0:
            result = self.decryptCBC(cipherText, key, iv)
        elif self.encrypt_model == 1:
            result = self.decryptECB(cipherText, key)

        self.edit_plain.SetValue(result)

    def doClear(self, event):
        self.edit_plain.SetValue('')
        self.edit_cipher.SetValue('')

    def encryptCBC(self, plain_text, key, iv):
        return sm4.encrypt_cbc(plain_text, key, iv)

    def encryECB(self, plain_text, key):
        return sm4.encrypt_ecb(plain_text, key)

    def decryptCBC(self, cipher_text, key, iv):
        return sm4.decrypt_cbc(cipher_text, key, iv)

    def decryptECB(self, cipher_text, key):
        return sm4.decrypt_ecb(cipher_text, key)
