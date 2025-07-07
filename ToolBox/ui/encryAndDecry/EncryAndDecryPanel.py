# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class EncryAndDecryPanel
###########################################################################

class EncryAndDecryPanel(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(1000, -1), style=wx.TAB_TRAVERSAL,
                 name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        self.encry_and_decry_note_book = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        bSizer10.Add(self.encry_and_decry_note_book, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer10)
        self.Layout()

        # Connect Events
        self.encry_and_decry_note_book.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onChoose)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def onChoose(self, event):
        event.Skip()
