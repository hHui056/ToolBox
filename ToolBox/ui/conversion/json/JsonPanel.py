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
## Class JSONPanel
###########################################################################

class JsonPanel(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(1000, 400), style=wx.TAB_TRAVERSAL,
                 name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        bSizer7 = wx.BoxSizer(wx.VERTICAL)

        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer8.SetMinSize(wx.Size(-1, 20))
        self.btn_format = wx.Button(self, wx.ID_ANY, u"格式化", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.btn_format, 0, wx.ALL, 5)

        self.btn_clean = wx.Button(self, wx.ID_ANY, u"清空", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.btn_clean, 0, wx.ALL, 5)

        bSizer7.Add(bSizer8, 0, wx.EXPAND, 5)

        bSizer9 = wx.BoxSizer(wx.HORIZONTAL)

        self.txt_format_result = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(500, -1),
                                             wx.TE_MULTILINE)
        bSizer9.Add(self.txt_format_result, 0, wx.ALL | wx.EXPAND, 5)

        self.tree_ctrl = wx.TreeCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE)
        bSizer9.Add(self.tree_ctrl, 1, wx.ALL | wx.EXPAND, 5)

        bSizer7.Add(bSizer9, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer7)
        self.Layout()

        # Connect Events
        self.btn_format.Bind(wx.EVT_BUTTON, self.doFormat)
        self.btn_clean.Bind(wx.EVT_BUTTON, self.doClear)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def doFormat(self, event):
        event.Skip()

    def doClear(self, event):
        event.Skip()
