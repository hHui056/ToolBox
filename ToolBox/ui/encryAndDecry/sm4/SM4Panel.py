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
## Class SM4Panel
###########################################################################

class SM4Panel(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.TAB_TRAVERSAL,
                 name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        bSizer19 = wx.BoxSizer(wx.VERTICAL)

        bSizer20 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_radioBtn4 = wx.RadioButton(self, wx.ID_ANY, u"CBC", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer20.Add(self.m_radioBtn4, 0, wx.ALL, 5)

        self.m_radioBtn3 = wx.RadioButton(self, wx.ID_ANY, u"ECB", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer20.Add(self.m_radioBtn3, 0, wx.ALL, 5)

        bSizer19.Add(bSizer20, 0, wx.EXPAND, 5)

        layout_secret_key = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, u"SecretKey", wx.DefaultPosition, wx.Size(80, -1), 0)
        self.m_staticText10.Wrap(-1)

        layout_secret_key.Add(self.m_staticText10, 0, wx.ALL, 5)

        self.edit_secret_key = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        layout_secret_key.Add(self.edit_secret_key, 1, wx.ALL, 5)

        bSizer19.Add(layout_secret_key, 0, wx.EXPAND, 5)

        layout_iv = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText11 = wx.StaticText(self, wx.ID_ANY, u"iv", wx.DefaultPosition, wx.Size(80, -1), 0)
        self.m_staticText11.Wrap(-1)

        layout_iv.Add(self.m_staticText11, 0, wx.ALL, 5)

        self.edit_iv = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        layout_iv.Add(self.edit_iv, 1, wx.ALL, 5)

        bSizer19.Add(layout_iv, 0, wx.EXPAND, 5)

        bSizer23 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText12 = wx.StaticText(self, wx.ID_ANY, u"明文", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)

        bSizer23.Add(self.m_staticText12, 0, wx.ALL, 5)

        self.edit_plain = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, 100),
                                      wx.TE_MULTILINE)
        bSizer23.Add(self.edit_plain, 1, wx.ALL, 5)

        bSizer19.Add(bSizer23, 0, wx.EXPAND, 5)

        bSizer24 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText13 = wx.StaticText(self, wx.ID_ANY, u"密文", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText13.Wrap(-1)

        bSizer24.Add(self.m_staticText13, 0, wx.ALL, 5)

        self.edit_cipher = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, 100),
                                       wx.TE_MULTILINE)
        bSizer24.Add(self.edit_cipher, 1, wx.ALL, 5)

        bSizer19.Add(bSizer24, 0, wx.EXPAND, 5)

        bSizer25 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button13 = wx.Button(self, wx.ID_ANY, u"加密", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer25.Add(self.m_button13, 0, wx.ALL, 5)

        self.m_button14 = wx.Button(self, wx.ID_ANY, u"解密", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer25.Add(self.m_button14, 0, wx.ALL, 5)

        self.m_button15 = wx.Button(self, wx.ID_ANY, u"清空", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer25.Add(self.m_button15, 0, wx.ALL, 5)

        bSizer19.Add(bSizer25, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer19)
        self.Layout()
        bSizer19.Fit(self)

        # Connect Events
        self.m_radioBtn4.Bind(wx.EVT_RADIOBUTTON, self.choice_cbc)
        self.m_radioBtn3.Bind(wx.EVT_RADIOBUTTON, self.choice_ecb)
        self.m_button13.Bind(wx.EVT_BUTTON, self.doEncrypt)
        self.m_button14.Bind(wx.EVT_BUTTON, self.doDecrypt)
        self.m_button15.Bind(wx.EVT_BUTTON, self.doClear)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def choice_cbc(self, event):
        event.Skip()

    def choice_ecb(self, event):
        event.Skip()

    def doEncrypt(self, event):
        event.Skip()

    def doDecrypt(self, event):
        event.Skip()

    def doClear(self, event):
        event.Skip()
