from ui.encryAndDecry.EncryAndDecryPanel import EncryAndDecryPanel
from ui.encryAndDecry.aes.AESPanel import AESPanel
from ui.encryAndDecry.hash.Hash import Hash
from ui.encryAndDecry.sm4.SM4 import SM4


class EncryAndDecry(EncryAndDecryPanel):
    def __init__(self, parent):
        EncryAndDecryPanel.__init__(self, parent)
        self.__init_view()

    def __init_view(self):
        self.encry_and_decry_note_book.AddPage(Hash(self.encry_and_decry_note_book), "HASH")
        self.encry_and_decry_note_book.AddPage(AESPanel(self.encry_and_decry_note_book), "AES")
        self.encry_and_decry_note_book.AddPage(SM4(self.encry_and_decry_note_book), "SM4")
