from ui.encryAndDecry.EncryAndDecryPanel import EncryAndDecryPanel
from ui.encryAndDecry.hash.Hash import Hash


class EncryAndDecry(EncryAndDecryPanel):
    def __init__(self, parent):
        EncryAndDecryPanel.__init__(self, parent)
        self.__init_view()

    def __init_view(self):
        self.encry_and_decry_note_book.AddPage(Hash(self.encry_and_decry_note_book), "HASH")
        pass
