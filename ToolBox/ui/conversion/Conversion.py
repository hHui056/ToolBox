from ui.conversion.ConversionPanel import ConversionPanel
from ui.conversion.dateFormat.DateFormat import DateFormat
from ui.conversion.image.Image import Image
from ui.conversion.json.Json import Json
from ui.conversion.tts.TTS import TTS


class Conversion(ConversionPanel):
    def __init__(self, parent):
        ConversionPanel.__init__(self, parent)
        self.__init_view()

    def __init_view(self):
        self.conversion_note_book.AddPage(Json(self.conversion_note_book), "JSON格式化")
        self.conversion_note_book.AddPage(DateFormat(self.conversion_note_book), "日期时间")
        self.conversion_note_book.AddPage(TTS(self.conversion_note_book), "语音合成")
        self.conversion_note_book.AddPage(Image(self.conversion_note_book), "图片处理")
