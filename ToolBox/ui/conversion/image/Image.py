from ui.conversion.image.ImagePanel import ImagePanel
from ui.conversion.image.compression.ImageCompressPanel import ImageCompressorPanel
from ui.conversion.image.ico.ImageToIconConverterPanel import ImageToIconConverterPanel
from ui.conversion.image.watermark.WatermarkPanel import WatermarkPanel


class Image(ImagePanel):
    def __init__(self, parent):
        ImagePanel.__init__(self, parent)
        self.__init_view()

    def __init_view(self):
        self.image_note_book.AddPage(ImageCompressorPanel(self.image_note_book), "压缩")
        self.image_note_book.AddPage(ImageToIconConverterPanel(self.image_note_book), "转ico")
        self.image_note_book.AddPage(WatermarkPanel(self.image_note_book), "加水印")
