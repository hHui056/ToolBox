from ui.codec.CodecPanel import CodecPanel
from ui.codec.base64.Base64Panel import Base64Panel


class Codec(CodecPanel):
    def __init__(self, parent):
        CodecPanel.__init__(self, parent)
        self.__init_view()

    def __init_view(self):
        self.codec_note_book.AddPage(Base64Panel(self.codec_note_book), "base64")
