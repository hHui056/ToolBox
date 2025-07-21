# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from ui.generate.uuid.UuidGeneratorPanel import UuidGeneratorPanel
from ui.generate.qrcode.QRCodeMainPanel import QRCodeMainPanel


###########################################################################
## Class GeneratePanel
###########################################################################

class GeneratePanel(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(1000, -1), style=wx.TAB_TRAVERSAL,
                 name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        self.generate_note_book = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        bSizer10.Add(self.generate_note_book, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer10)
        self.Layout()

        # Connect Events
        self.generate_note_book.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onChoose)
        self.generate_note_book.AddPage(UuidGeneratorPanel(self.generate_note_book), "UUID")
        self.generate_note_book.AddPage(QRCodeMainPanel(self.generate_note_book), "二维码")

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def onChoose(self, event):
        event