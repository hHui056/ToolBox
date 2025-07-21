import wx
import uuid


class UuidGeneratorPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # 创建主布局
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 创建控制面板（生成数量+按钮）
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 数量标签
        count_label = wx.StaticText(self, label="生成数量:")
        control_sizer.Add(count_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # 数量输入框
        self.count_ctrl = wx.SpinCtrl(self, min=1, max=100, initial=5)
        control_sizer.Add(self.count_ctrl, 0, wx.ALL, 5)

        # 生成按钮
        generate_btn = wx.Button(self, label="生成UUID")
        generate_btn.Bind(wx.EVT_BUTTON, self.on_generate)
        control_sizer.Add(generate_btn, 0, wx.ALL, 5)

        main_sizer.Add(control_sizer, 0, wx.ALL, 10)

        # 创建滚动区域用于显示UUID列表
        self.scroll = wx.ScrolledWindow(self)
        self.scroll.SetScrollRate(10, 10)
        self.list_sizer = wx.BoxSizer(wx.VERTICAL)

        self.scroll.SetSizer(self.list_sizer)
        main_sizer.Add(self.scroll, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(main_sizer)

    def generate_uuids(self, count):
        """生成指定数量的UUID并添加到列表"""
        # 清除现有内容
        self.scroll.DestroyChildren()
        self.list_sizer = wx.BoxSizer(wx.VERTICAL)
        self.scroll.SetSizer(self.list_sizer)

        # 生成新UUID
        for i in range(count):
            uuid_value = str(uuid.uuid4())
            item_sizer = wx.BoxSizer(wx.HORIZONTAL)

            # UUID文本显示
            text = wx.TextCtrl(
                self.scroll,
                value=uuid_value,
                style=wx.TE_READONLY | wx.BORDER_SIMPLE
            )
            text.SetBackgroundColour(wx.Colour(240, 240, 240))
            text.SetMinSize((400, -1))
            item_sizer.Add(text, 1, wx.EXPAND | wx.RIGHT, 5)

            # 复制按钮
            copy_btn = wx.Button(self.scroll, label="复制", name=uuid_value)
            copy_btn.Bind(wx.EVT_BUTTON, self.on_copy_uuid)
            item_sizer.Add(copy_btn, 0, wx.EXPAND)

            self.list_sizer.Add(item_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 更新布局
        self.list_sizer.Layout()
        self.scroll.SetVirtualSize(self.list_sizer.GetMinSize())
        self.scroll.Refresh()
        self.Layout()

    def on_generate(self, event):
        """生成按钮事件处理"""
        count = self.count_ctrl.GetValue()
        self.generate_uuids(count)

    def on_copy_uuid(self, event):
        """复制按钮事件处理"""
        btn = event.GetEventObject()
        uuid_value = btn.GetName()

        # 复制到剪贴板
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(uuid_value))
            wx.TheClipboard.Close()
            # 显示成功提示
            wx.MessageBox(
                f"已复制到剪贴板:\n{uuid_value}",
                "复制成功",
                wx.OK | wx.ICON_INFORMATION,
                self
            )
