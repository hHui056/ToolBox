import wx
import datetime


class DateFormatPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # 创建布局
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 当前时间显示
        time_box = wx.StaticBox(self, label="当前时间")
        time_sizer = wx.StaticBoxSizer(time_box, wx.VERTICAL)

        # 格式化时间显示行
        time_row = wx.BoxSizer(wx.HORIZONTAL)
        self.time_label = wx.StaticText(self, label="格式时间: ")
        self.copy_time_btn = wx.Button(self, label="📋", size=(30, -1))
        self.copy_time_btn.Bind(wx.EVT_BUTTON,
                                lambda e: self.copy_to_clipboard(self.time_label.GetLabel().split(": ")[1]))
        time_row.Add(self.time_label, 1, wx.ALL | wx.EXPAND, 5)
        time_row.Add(self.copy_time_btn, 0, wx.ALL | wx.EXPAND, 5)

        # 毫秒时间戳显示行
        millis_row = wx.BoxSizer(wx.HORIZONTAL)
        self.millis_label = wx.StaticText(self, label="毫秒时间戳: ")
        self.copy_millis_btn = wx.Button(self, label="📋", size=(30, -1))
        self.copy_millis_btn.Bind(wx.EVT_BUTTON,
                                  lambda e: self.copy_to_clipboard(self.millis_label.GetLabel().split(": ")[1]))
        millis_row.Add(self.millis_label, 1, wx.ALL | wx.EXPAND, 5)
        millis_row.Add(self.copy_millis_btn, 0, wx.ALL | wx.EXPAND, 5)

        # 秒时间戳显示行
        seconds_row = wx.BoxSizer(wx.HORIZONTAL)
        self.seconds_label = wx.StaticText(self, label="秒时间戳: ")
        self.copy_seconds_btn = wx.Button(self, label="📋", size=(30, -1))
        self.copy_seconds_btn.Bind(wx.EVT_BUTTON,
                                   lambda e: self.copy_to_clipboard(self.seconds_label.GetLabel().split(": ")[1]))
        seconds_row.Add(self.seconds_label, 1, wx.ALL | wx.EXPAND, 5)
        seconds_row.Add(self.copy_seconds_btn, 0, wx.ALL | wx.EXPAND, 5)

        time_sizer.Add(time_row, 0, wx.EXPAND)
        time_sizer.Add(millis_row, 0, wx.EXPAND)
        time_sizer.Add(seconds_row, 0, wx.EXPAND)

        # 时间戳转换区域
        convert_box = wx.StaticBox(self, label="时间转换工具")
        convert_sizer = wx.StaticBoxSizer(convert_box, wx.VERTICAL)

        # 时间字符串转时间戳
        str_to_ts_sizer = wx.BoxSizer(wx.HORIZONTAL)
        str_to_ts_label = wx.StaticText(self, label="时间字符串 (YYYY-MM-dd HH:mm:ss):")
        self.time_str_input = wx.TextCtrl(self)
        self.convert_to_ts_btn = wx.Button(self, label="转为时间戳")
        self.convert_to_ts_btn.Bind(wx.EVT_BUTTON, self.on_convert_str_to_ts)
        self.result_ts = wx.StaticText(self, label="")

        str_to_ts_sizer.Add(str_to_ts_label, 0, wx.ALL | wx.CENTER, 5)
        str_to_ts_sizer.Add(self.time_str_input, 1, wx.ALL | wx.EXPAND, 5)

        convert_sizer.Add(str_to_ts_sizer, 0, wx.EXPAND)
        convert_sizer.Add(self.convert_to_ts_btn, 0, wx.ALL, 5)

        # 添加复制按钮到转换结果
        result_ts_row = wx.BoxSizer(wx.HORIZONTAL)
        self.copy_ts_btn = wx.Button(self, label="📋", size=(30, -1))
        self.copy_ts_btn.Bind(wx.EVT_BUTTON, lambda e: self.copy_to_clipboard(self.result_ts.GetLabel()))
        result_ts_row.Add(self.result_ts, 1, wx.ALL | wx.EXPAND, 5)
        result_ts_row.Add(self.copy_ts_btn, 0, wx.ALL | wx.EXPAND, 5)
        convert_sizer.Add(result_ts_row, 0, wx.EXPAND)

        # 分隔线
        convert_sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.ALL, 5)

        # 时间戳转时间字符串
        ts_to_str_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ts_to_str_label = wx.StaticText(self, label="时间戳:")
        self.ts_input = wx.TextCtrl(self)
        self.ts_type = wx.RadioBox(
            self,
            choices=["秒", "毫秒"],
            style=wx.RA_HORIZONTAL,
            label="时间戳类型"
        )
        self.convert_to_str_btn = wx.Button(self, label="转为时间字符串")
        self.convert_to_str_btn.Bind(wx.EVT_BUTTON, self.on_convert_ts_to_str)
        self.result_str = wx.StaticText(self, label="")

        ts_to_str_sizer.Add(ts_to_str_label, 0, wx.ALL | wx.CENTER, 5)
        ts_to_str_sizer.Add(self.ts_input, 1, wx.ALL | wx.EXPAND, 5)
        ts_to_str_sizer.Add(self.ts_type, 0, wx.ALL, 5)

        convert_sizer.Add(ts_to_str_sizer, 0, wx.EXPAND)
        convert_sizer.Add(self.convert_to_str_btn, 0, wx.ALL, 5)

        # 添加复制按钮到转换结果
        result_str_row = wx.BoxSizer(wx.HORIZONTAL)
        self.copy_str_btn = wx.Button(self, label="📋", size=(30, -1))
        self.copy_str_btn.Bind(wx.EVT_BUTTON,
                               lambda e: self.copy_to_clipboard(self.result_str.GetLabel().split(": ")[1]))
        result_str_row.Add(self.result_str, 1, wx.ALL | wx.EXPAND, 5)
        result_str_row.Add(self.copy_str_btn, 0, wx.ALL | wx.EXPAND, 5)
        convert_sizer.Add(result_str_row, 0, wx.EXPAND)

        # 组装主布局
        main_sizer.Add(time_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(convert_sizer, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(main_sizer)

        # 创建定时器
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_time, self.timer)
        self.timer.Start(1000)  # 每秒刷新一次
        self.update_time()  # 立即更新显示

    def update_time(self, event=None):
        """更新时间显示"""
        # 获取当前时间
        now = datetime.datetime.now()

        # 格式化时间字符串
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        # 毫秒级时间戳
        millis_timestamp = int(now.timestamp() * 1000)
        # 秒级时间戳
        seconds_timestamp = int(now.timestamp())

        # 更新UI显示
        self.time_label.SetLabel(f"格式时间: {current_time}")
        self.millis_label.SetLabel(f"毫秒时间戳: {millis_timestamp}")
        self.seconds_label.SetLabel(f"秒时间戳: {seconds_timestamp}")

        # 调整窗口大小适应新内容
        self.GetParent().Layout()

    def copy_to_clipboard(self, text):
        """复制文本到剪贴板"""
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(text))
            wx.TheClipboard.Close()
            # 显示复制成功的提示
            wx.MessageBox(f"已复制到剪贴板: {text}", "成功", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("无法访问剪贴板", "错误", wx.OK | wx.ICON_ERROR)

    def on_convert_str_to_ts(self, event):
        """将时间字符串转换为时间戳"""
        time_str = self.time_str_input.GetValue().strip()
        try:
            # 解析时间字符串
            dt = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            # 转换为时间戳（秒）
            timestamp = dt.timestamp()

            # 显示结果（同时显示秒和毫秒）
            self.result_ts.SetLabel(
                f"秒: {int(timestamp)} | 毫秒: {int(timestamp * 1000)}"
            )
            self.Layout()
        except ValueError:
            self.result_ts.SetLabel("时间格式无效!")
            self.Layout()

    def on_convert_ts_to_str(self, event):
        """将时间戳转换为时间字符串"""
        ts_str = self.ts_input.GetValue().strip()
        if not ts_str.isdigit():
            self.result_str.SetLabel("时间戳无效!")
            self.Layout()
            return

        ts_val = float(ts_str)

        # 根据选择调整时间戳类型
        if self.ts_type.GetSelection() == 1:  # 毫秒
            ts_val /= 1000.0

        try:
            # 将时间戳转换为datetime对象
            dt = datetime.datetime.fromtimestamp(ts_val)
            # 格式化为字符串
            time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            self.result_str.SetLabel(f"格式时间: {time_str}")
            self.Layout()
        except (ValueError, OSError):
            self.result_str.SetLabel("时间戳超出范围!")
            self.Layout()

