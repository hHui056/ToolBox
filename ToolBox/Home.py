from ui.codec.Codec import Codec
from ui.encryAndDecry.EncryAndDecry import EncryAndDecry
from HomeFrame import HomeFrame
from ui.conversion.Conversion import Conversion
from ui.generate.GeneratePanel import GeneratePanel


class Home(HomeFrame):
    def __init__(self, parent) -> None:
        HomeFrame.__init__(self, parent)
        self.Centre()
        self.__init_view()

    def __init_view(self):
        self.m_notebook2.AddPage(Conversion(self.m_notebook2), u"转换", True)
        self.m_notebook2.AddPage(EncryAndDecry(self.m_notebook2), u"加解密", True)
        self.m_notebook2.AddPage(Codec(self.m_notebook2), u"编解码", True)
        self.m_notebook2.AddPage(GeneratePanel(self.m_notebook2), u"生成", True)
        self.m_notebook2.SetSelection(0)
