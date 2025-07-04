from ui.conversion.ConversionPanel import ConversionPanel
from ui.conversion.dateFormat.DateFormat import DateFormat
from ui.conversion.json.Json import Json


class Conversion(ConversionPanel):
    def __init__(self, parent):
        ConversionPanel.__init__(self, parent)
        self.__init_view()

    def __init_view(self):
        self.conversion_note_book.AddPage(Json(self.conversion_note_book), "JSON格式化")
        self.conversion_note_book.AddPage(DateFormat(self.conversion_note_book), "日期时间")
