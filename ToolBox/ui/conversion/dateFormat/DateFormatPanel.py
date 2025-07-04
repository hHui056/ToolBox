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
## Class DateFormatPanel
###########################################################################

class DateFormatPanel(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(1000, 400), style=wx.TAB_TRAVERSAL,
                 name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, _(u"当前时间"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)

        self.m_staticText1.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                    False, wx.EmptyString))

        bSizer3.Add(self.m_staticText1, 0, wx.ALL, 5)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, _(u"时间字符串："), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)

        bSizer4.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)

        bSizer4.Add(self.m_staticText3, 0, wx.ALL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, _(u"复制"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.m_button1, 0, wx.ALL, 5)

        bSizer3.Add(bSizer4, 0, wx.EXPAND, 5)

        bSizer41 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText21 = wx.StaticText(self, wx.ID_ANY, _(u"毫秒时间戳"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText21.Wrap(-1)

        bSizer41.Add(self.m_staticText21, 0, wx.ALL, 5)

        self.m_staticText31 = wx.StaticText(self, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText31.Wrap(-1)

        bSizer41.Add(self.m_staticText31, 0, wx.ALL, 5)

        self.m_button11 = wx.Button(self, wx.ID_ANY, _(u"复制"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer41.Add(self.m_button11, 0, wx.ALL, 5)

        bSizer3.Add(bSizer41, 1, wx.EXPAND, 5)

        bSizer1.Add(bSizer3, 0, wx.EXPAND, 5)

        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer9 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, _(u"时间字符串转时间戳"), wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)

        self.m_staticText9.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                    False, wx.EmptyString))

        bSizer9.Add(self.m_staticText9, 0, wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        bSizer9.Add(self.m_textCtrl1, 0, wx.ALL, 5)

        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button4 = wx.Button(self, wx.ID_ANY, _(u"转换"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer10.Add(self.m_button4, 0, wx.ALL, 5)

        self.m_button5 = wx.Button(self, wx.ID_ANY, _(u"清空"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer10.Add(self.m_button5, 0, wx.ALL, 5)

        bSizer9.Add(bSizer10, 1, wx.EXPAND, 5)

        bSizer8.Add(bSizer9, 0, 0, 5)

        bSizer91 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText91 = wx.StaticText(self, wx.ID_ANY, _(u"时间戳转时间字符串"), wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText91.Wrap(-1)

        self.m_staticText91.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                    False, wx.EmptyString))

        bSizer91.Add(self.m_staticText91, 0, wx.ALL, 5)

        self.m_textCtrl11 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(300, -1), 0)
        bSizer91.Add(self.m_textCtrl11, 0, wx.ALL, 5)

        bSizer101 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button41 = wx.Button(self, wx.ID_ANY, _(u"转换"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer101.Add(self.m_button41, 0, wx.ALL, 5)

        self.m_button51 = wx.Button(self, wx.ID_ANY, _(u"清空"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer101.Add(self.m_button51, 0, wx.ALL, 5)

        bSizer91.Add(bSizer101, 1, wx.EXPAND, 5)

        bSizer8.Add(bSizer91, 0, 0, 5)

        bSizer1.Add(bSizer8, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        # Connect Events
        self.m_button1.Bind(wx.EVT_BUTTON, self.copy_time_string)
        self.m_button11.Bind(wx.EVT_BUTTON, self.copy_time_ms)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def copy_time_string(self, event):
        event.Skip()

    def copy_time_ms(self, event):
        event.Skip()
