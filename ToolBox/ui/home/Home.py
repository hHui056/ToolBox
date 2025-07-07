from ui.encryAndDecry.EncryAndDecry import EncryAndDecry
from ui.home.HomeFrame import HomeFrame
from ui.conversion.Conversion import Conversion


class Home(HomeFrame):
    def __init__(self, parent) -> None:
        HomeFrame.__init__(self, parent)
        self.Centre()
        self.__init_view()

    def __init_view(self):
        self.m_notebook2.AddPage(Conversion(self.m_notebook2), u"转换", True)
        self.m_notebook2.AddPage(EncryAndDecry(self.m_notebook2), u"加解密", True)
        self.m_notebook2.SetSelection(0)
