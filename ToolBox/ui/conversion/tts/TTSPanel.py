# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext

_ = gettext.gettext


###########################################################################
## Class TTSPanel
###########################################################################

class TTSPanel(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(1000, 400), style=wx.TAB_TRAVERSAL,
                 name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)

        self.tts_content = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(600, -1), 0)
        bSizer10.Add(self.tts_content, 0, wx.ALL | wx.EXPAND, 5)

        bSizer11 = wx.BoxSizer(wx.VERTICAL)

        voice_choicesChoices = []
        self.voice_choices = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, voice_choicesChoices, 0)
        bSizer11.Add(self.voice_choices, 1, wx.ALL | wx.EXPAND, 5)

        bSizer12 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button7 = wx.Button(self, wx.ID_ANY, _(u"语音合成"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer12.Add(self.m_button7, 1, wx.ALL, 5)

        self.m_button71 = wx.Button(self, wx.ID_ANY, _(u"语音文件"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer12.Add(self.m_button71, 1, wx.ALL, 5)

        bSizer11.Add(bSizer12, 0, wx.EXPAND, 5)

        bSizer10.Add(bSizer11, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer10)
        self.Layout()

        # Connect Events
        self.voice_choices.Bind(wx.EVT_LISTBOX, self.list_box_click)
        self.m_button7.Bind(wx.EVT_BUTTON, self.start_tts)
        self.m_button71.Bind(wx.EVT_BUTTON, self.show_tts_dialog)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def list_box_click(self, event):
        event.Skip()

    def start_tts(self, event):
        event.Skip()

    def show_tts_dialog(self, event):
        event.Skip()
