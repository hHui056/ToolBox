import wx


class TTSFileDialog(wx.Dialog):
    def __init__(self, parent):
        super(TTSFileDialog, self).__init__(parent, title="用户登录", size=(300, 200))
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 用户名
        user_sizer = wx.BoxSizer(wx.HORIZONTAL)
        user_sizer.Add(wx.StaticText(panel, label="用户名:"), 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.username = wx.TextCtrl(panel)
        user_sizer.Add(self.username, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(user_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 密码
        pwd_sizer = wx.BoxSizer(wx.HORIZONTAL)
        pwd_sizer.Add(wx.StaticText(panel, label="密码:"), 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.password = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        pwd_sizer.Add(self.password, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(pwd_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, id=wx.ID_OK, label="登录")
        btn_ok.Bind(wx.EVT_BUTTON, self.on_ok)
        btn_cancel = wx.Button(panel, id=wx.ID_CANCEL, label="取消")
        btn_sizer.Add(btn_ok, 0, wx.ALL, 5)
        btn_sizer.Add(btn_cancel, 0, wx.ALL, 5)
        sizer.Add(btn_sizer, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        panel.SetSizer(sizer)

    def on_ok(self, event):
        if self.username.GetValue().strip() == "":
            wx.MessageBox("用户名不能为空！", "错误", wx.ICON_ERROR)
            return
        if self.password.GetValue().strip() == "":
            wx.MessageBox("密码不能为空！", "错误", wx.ICON_ERROR)
            return

        # 在此处添加验证逻辑...
        event.Skip()  # 继续关闭对话框
