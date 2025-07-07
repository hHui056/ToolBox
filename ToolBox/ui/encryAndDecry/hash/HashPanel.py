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
## Class HashPanel
###########################################################################

class HashPanel(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(1000, 400), style=wx.TAB_TRAVERSAL,
                 name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        bSizer13 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer14 = wx.BoxSizer(wx.VERTICAL)

        bSizer14.SetMinSize(wx.Size(500, -1))
        bSizer16 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, _(u"输入"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)

        bSizer16.Add(self.m_staticText8, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        input_type_choiceChoices = [_(u"文本"), _(u"文件")]
        self.input_type_choice = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           input_type_choiceChoices, 0)
        self.input_type_choice.SetSelection(0)
        bSizer16.Add(self.input_type_choice, 1, wx.ALL, 5)

        bSizer14.Add(bSizer16, 0, wx.EXPAND, 5)

        choice_file_layout = wx.BoxSizer(wx.HORIZONTAL)

        self.edit_file_path = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.edit_file_path.Enable(False)

        choice_file_layout.Add(self.edit_file_path, 1, wx.ALL, 5)

        self.choice_file_btn = wx.Button(self, wx.ID_ANY, _(u"选择文件"), wx.DefaultPosition, wx.DefaultSize, 0)
        choice_file_layout.Add(self.choice_file_btn, 0, wx.ALL, 5)

        bSizer14.Add(choice_file_layout, 0, wx.EXPAND, 5)

        self.edit_content = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_MULTILINE)
        bSizer14.Add(self.edit_content, 1, wx.ALL | wx.EXPAND, 5)

        self.m_button9 = wx.Button(self, wx.ID_ANY, _(u"清空"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer14.Add(self.m_button9, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer13.Add(bSizer14, 0, wx.EXPAND, 5)

        bSizer15 = wx.BoxSizer(wx.VERTICAL)

        bSizer15.SetMinSize(wx.Size(500, -1))
        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, _(u"哈希值"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)

        self.m_staticText9.SetFont(
            wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                    False, wx.EmptyString))

        bSizer15.Add(self.m_staticText9, 0, wx.ALL, 5)

        bSizer17 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText11 = wx.StaticText(self, wx.ID_ANY, _(u"MD5"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)

        bSizer17.Add(self.m_staticText11, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText12 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)

        bSizer17.Add(self.m_staticText12, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_button10 = wx.Button(self, wx.ID_ANY, _(u"复制"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer17.Add(self.m_button10, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer15.Add(bSizer17, 0, wx.EXPAND, 5)

        self.md5_result = wx.TextCtrl(self, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE)
        self.md5_result.Enable(False)

        bSizer15.Add(self.md5_result, 1, wx.ALL | wx.EXPAND, 5)

        bSizer171 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText111 = wx.StaticText(self, wx.ID_ANY, _(u"SHA1"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText111.Wrap(-1)

        bSizer171.Add(self.m_staticText111, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText121 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText121.Wrap(-1)

        bSizer171.Add(self.m_staticText121, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_button101 = wx.Button(self, wx.ID_ANY, _(u"复制"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer171.Add(self.m_button101, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer15.Add(bSizer171, 0, wx.EXPAND, 5)

        self.sha1_result = wx.TextCtrl(self, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE)
        self.sha1_result.Enable(False)

        bSizer15.Add(self.sha1_result, 1, wx.ALL | wx.EXPAND, 5)

        bSizer1711 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1111 = wx.StaticText(self, wx.ID_ANY, _(u"SHA256"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1111.Wrap(-1)

        bSizer1711.Add(self.m_staticText1111, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText1211 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1211.Wrap(-1)

        bSizer1711.Add(self.m_staticText1211, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_button1011 = wx.Button(self, wx.ID_ANY, _(u"复制"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1711.Add(self.m_button1011, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer15.Add(bSizer1711, 0, wx.EXPAND, 5)

        self.sha256_result = wx.TextCtrl(self, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE)
        self.sha256_result.Enable(False)

        bSizer15.Add(self.sha256_result, 1, wx.ALL | wx.EXPAND, 5)

        bSizer17111 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText11111 = wx.StaticText(self, wx.ID_ANY, _(u"SHA512"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11111.Wrap(-1)

        bSizer17111.Add(self.m_staticText11111, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText12111 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText12111.Wrap(-1)

        bSizer17111.Add(self.m_staticText12111, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_button10111 = wx.Button(self, wx.ID_ANY, _(u"复制"), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer17111.Add(self.m_button10111, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer15.Add(bSizer17111, 0, wx.EXPAND, 5)

        self.sha512_result = wx.TextCtrl(self, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE)
        self.sha512_result.Enable(False)

        bSizer15.Add(self.sha512_result, 1, wx.ALL | wx.EXPAND, 5)

        bSizer13.Add(bSizer15, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer13)
        self.Layout()

        # Connect Events
        self.input_type_choice.Bind(wx.EVT_CHOICE, self.on_choice_type)
        self.choice_file_btn.Bind(wx.EVT_BUTTON, self.show_choice_file_dialog)
        self.edit_content.Bind(wx.EVT_TEXT, self.on_text_change)
        self.m_button9.Bind(wx.EVT_BUTTON, self.clear_input)
        self.m_button10.Bind(wx.EVT_BUTTON, self.copy_md5)
        self.m_button101.Bind(wx.EVT_BUTTON, self.copy_sha1)
        self.m_button1011.Bind(wx.EVT_BUTTON, self.copy_sha256)
        self.m_button10111.Bind(wx.EVT_BUTTON, self.copy_sha512)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def on_choice_type(self, event):
        event.Skip()

    def show_choice_file_dialog(self, event):
        event.Skip()

    def on_text_change(self, event):
        event.Skip()

    def clear_input(self, event):
        event.Skip()

    def copy_md5(self, event):
        event.Skip()

    def copy_sha1(self, event):
        event.Skip()

    def copy_sha256(self, event):
        event.Skip()

    def copy_sha512(self, event):
        event.Skip()
