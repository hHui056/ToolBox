import wx
import base64
import os
import mimetypes
import time
import threading
import queue


class Base64Panel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # 初始化MIME类型库
        mimetypes.init()

        # 创建主布局
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 创建标签页
        self.notebook = wx.Notebook(self)
        text_tab = wx.Panel(self.notebook)
        file_tab = wx.Panel(self.notebook)
        self.notebook.AddPage(text_tab, "文本编解码")
        self.notebook.AddPage(file_tab, "文件编解码")

        # 文本编解码标签页布局
        self.setup_text_tab(text_tab)

        # 文件编解码标签页布局
        self.setup_file_tab(file_tab)

        # 添加标签页到主布局
        main_sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(main_sizer)

        # 初始化线程相关变量
        self.encoding_thread = None
        self.cancel_encoding = False
        self.progress_queue = queue.Queue()

        # 启动进度更新定时器
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_progress, self.timer)
        self.timer.Start(100)  # 每100毫秒检查一次进度

    def setup_text_tab(self, tab):
        """设置文本编解码标签页"""
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 输入区域
        input_sizer = wx.BoxSizer(wx.VERTICAL)
        input_label = wx.StaticText(tab, label="输入文本:")
        input_sizer.Add(input_label, 0, wx.ALL, 5)

        self.input_text = wx.TextCtrl(tab, style=wx.TE_MULTILINE, size=(-1, 150))
        input_sizer.Add(self.input_text, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(input_sizer, 1, wx.EXPAND)

        # 按钮区域
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text_encode_btn = wx.Button(tab, label="编码文本")
        self.text_decode_btn = wx.Button(tab, label="解码文本")
        btn_sizer.Add(self.text_encode_btn, 1, wx.ALL | wx.EXPAND, 5)
        btn_sizer.Add(self.text_decode_btn, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(btn_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # 输出区域
        output_sizer = wx.BoxSizer(wx.VERTICAL)
        output_label = wx.StaticText(tab, label="输出结果:")
        output_sizer.Add(output_label, 0, wx.ALL, 5)

        self.output_text = wx.TextCtrl(tab, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(-1, 150))
        output_sizer.Add(self.output_text, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(output_sizer, 1, wx.EXPAND)

        tab.SetSizer(sizer)

        # 绑定事件
        self.text_encode_btn.Bind(wx.EVT_BUTTON, self.on_encode_text)
        self.text_decode_btn.Bind(wx.EVT_BUTTON, self.on_decode_text)

    def setup_file_tab(self, tab):
        """设置文件编解码标签页"""
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 文件选择区域
        file_sel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        file_label = wx.StaticText(tab, label="选择文件:")
        file_sel_sizer.Add(file_label, 0, wx.ALL | wx.CENTER, 5)

        self.file_path = wx.TextCtrl(tab)
        file_sel_sizer.Add(self.file_path, 1, wx.ALL | wx.EXPAND, 5)

        self.browse_btn = wx.Button(tab, label="浏览...")
        file_sel_sizer.Add(self.browse_btn, 0, wx.ALL, 5)
        sizer.Add(file_sel_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 文件信息区域
        info_sizer = wx.FlexGridSizer(cols=4, vgap=10, hgap=15)
        info_sizer.AddGrowableCol(1)
        info_sizer.AddGrowableCol(3)

        # 文件名
        name_label = wx.StaticText(tab, label="文件名:")
        self.file_name = wx.StaticText(tab, label="")
        info_sizer.Add(name_label, 0, wx.ALIGN_CENTER_VERTICAL)
        info_sizer.Add(self.file_name, 0, wx.ALIGN_CENTER_VERTICAL)

        # 文件大小
        size_label = wx.StaticText(tab, label="文件大小:")
        self.file_size = wx.StaticText(tab, label="")
        info_sizer.Add(size_label, 0, wx.ALIGN_CENTER_VERTICAL)
        info_sizer.Add(self.file_size, 0, wx.ALIGN_CENTER_VERTICAL)

        # 文件类型
        type_label = wx.StaticText(tab, label="文件类型:")
        self.file_type = wx.StaticText(tab, label="")
        info_sizer.Add(type_label, 0, wx.ALIGN_CENTER_VERTICAL)
        info_sizer.Add(self.file_type, 0, wx.ALIGN_CENTER_VERTICAL)

        # MIME类型
        mime_label = wx.StaticText(tab, label="MIME类型:")
        self.mime_type = wx.StaticText(tab, label="")
        info_sizer.Add(mime_label, 0, wx.ALIGN_CENTER_VERTICAL)
        info_sizer.Add(self.mime_type, 0, wx.ALIGN_CENTER_VERTICAL)

        sizer.Add(info_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # 编码选项
        options_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.include_header = wx.CheckBox(tab, label="包含头部信息 (MIME类型)")
        self.include_header.SetValue(True)
        options_sizer.Add(self.include_header, 0, wx.ALL | wx.CENTER, 5)

        self.file_encode_btn = wx.Button(tab, label="编码文件")
        options_sizer.Add(self.file_encode_btn, 0, wx.ALL | wx.CENTER, 5)

        sizer.Add(options_sizer, 0, wx.ALL | wx.CENTER, 5)

        # 进度区域
        progress_sizer = wx.BoxSizer(wx.VERTICAL)

        # 进度条
        self.loading_indicator = wx.Gauge(tab, range=100, size=(-1, 20))
        self.loading_indicator.Hide()
        progress_sizer.Add(self.loading_indicator, 0, wx.EXPAND | wx.ALL, 5)

        # 进度文本
        progress_text_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.progress_label = wx.StaticText(tab, label="进度:")
        progress_text_sizer.Add(self.progress_label, 0, wx.ALIGN_CENTER_VERTICAL)

        self.progress_text = wx.StaticText(tab, label="0%")
        progress_text_sizer.Add(self.progress_text, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 5)

        progress_sizer.Add(progress_text_sizer, 0, wx.ALL, 5)

        # 状态信息
        self.status_info = wx.StaticText(tab, label="就绪")
        self.status_info.SetForegroundColour(wx.Colour(100, 100, 100))
        progress_sizer.Add(self.status_info, 0, wx.ALL | wx.CENTER, 5)

        # 取消按钮
        self.cancel_btn = wx.Button(tab, label="取消编码")
        self.cancel_btn.Hide()
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel_encoding)
        progress_sizer.Add(self.cancel_btn, 0, wx.ALL | wx.CENTER, 5)

        sizer.Add(progress_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 输出区域
        output_sizer = wx.BoxSizer(wx.VERTICAL)
        output_label = wx.StaticText(tab, label="编码结果:")
        output_sizer.Add(output_label, 0, wx.ALL, 5)

        self.file_output_text = wx.TextCtrl(tab, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(-1, 150))
        output_sizer.Add(self.file_output_text, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(output_sizer, 1, wx.EXPAND)

        # 操作按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.copy_btn = wx.Button(tab, label="复制结果")
        self.save_btn = wx.Button(tab, label="保存结果")
        self.file_decode_btn = wx.Button(tab, label="解码结果")

        btn_sizer.Add(self.copy_btn, 1, wx.ALL | wx.EXPAND, 5)
        btn_sizer.Add(self.save_btn, 1, wx.ALL | wx.EXPAND, 5)
        btn_sizer.Add(self.file_decode_btn, 1, wx.ALL | wx.EXPAND, 5)

        sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 5)

        tab.SetSizer(sizer)

        # 绑定事件
        self.browse_btn.Bind(wx.EVT_BUTTON, self.on_browse_file)
        self.file_encode_btn.Bind(wx.EVT_BUTTON, self.on_encode_file)
        self.file_decode_btn.Bind(wx.EVT_BUTTON, self.on_decode_file)
        self.save_btn.Bind(wx.EVT_BUTTON, self.on_save_file)
        self.copy_btn.Bind(wx.EVT_BUTTON, self.on_copy_result)

    def on_encode_text(self, event):
        """文本编码"""
        text = self.input_text.GetValue()
        if not text:
            wx.MessageBox("请输入要编码的文本", "提示", wx.OK | wx.ICON_INFORMATION, self)
            return

        try:
            # 添加头部信息
            if self.include_header.GetValue():
                header = "data:text/plain;base64,"
                encoded = header + base64.b64encode(text.encode('utf-8')).decode('utf-8')
            else:
                encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')

            self.output_text.SetValue(encoded)
        except Exception as e:
            wx.MessageBox(f"编码错误: {str(e)}", "错误", wx.OK | wx.ICON_ERROR, self)

    def on_decode_text(self, event):
        """文本解码"""
        text = self.input_text.GetValue()
        if not text:
            wx.MessageBox("请输入要解码的文本", "提示", wx.OK | wx.ICON_INFORMATION, self)
            return

        try:
            # 尝试解析头部信息
            header_end = text.find(",")
            if text.startswith("data:") and header_end != -1:
                base64_content = text[header_end + 1:]
                decoded = base64.b64decode(base64_content).decode('utf-8')
            else:
                decoded = base64.b64decode(text.encode('utf-8')).decode('utf-8')

            self.output_text.SetValue(decoded)
        except Exception as e:
            wx.MessageBox(f"解码错误: {str(e)}", "错误", wx.OK | wx.ICON_ERROR, self)

    def on_browse_file(self, event):
        """浏览文件"""
        with wx.FileDialog(self, "选择文件", wildcard="所有文件 (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                self.file_path.SetValue(path)
                self.update_file_details(path)

    def update_file_details(self, path):
        """更新文件详情"""
        if not path or not os.path.exists(path):
            return

        try:
            # 获取文件信息
            size = os.path.getsize(path)
            filename = os.path.basename(path)
            _, ext = os.path.splitext(filename)

            # 文件类型描述
            file_type = ext[1:].upper() + "文件" if ext else "未知类型文件"

            # MIME类型
            mime_type, _ = mimetypes.guess_type(path)
            mime_type = mime_type or "application/octet-stream"

            # 更新UI
            self.file_name.SetLabel(filename)
            self.file_size.SetLabel(self.format_file_size(size))
            self.file_type.SetLabel(file_type)
            self.mime_type.SetLabel(mime_type)

            # 重置状态
            self.file_output_text.SetValue("")
            self.status_info.SetLabel("已选择文件")
            self.status_info.SetForegroundColour(wx.Colour(100, 100, 100))

        except Exception as e:
            self.status_info.SetLabel(f"读取文件信息出错: {str(e)}")
            self.status_info.SetForegroundColour(wx.RED)

    def on_encode_file(self, event):
        """文件编码"""
        file_path = self.file_path.GetValue()

        if not file_path or not os.path.exists(file_path):
            wx.MessageBox("请选择有效的文件路径", "错误", wx.OK | wx.ICON_ERROR, self)
            return

        # 检查是否已有线程在运行
        if self.encoding_thread and self.encoding_thread.is_alive():
            wx.MessageBox("当前已有编码任务在进行中", "提示", wx.OK | wx.ICON_INFORMATION, self)
            return

        try:
            file_size = os.path.getsize(file_path)
            filename = os.path.basename(file_path)

            # 处理大文件警告
            if file_size > 1024 * 1024:  # 大于1MB
                dlg = wx.MessageDialog(
                    self,
                    f"您选择了一个较大的文件 ({self.format_file_size(file_size)})。Base64编码后的内容会很大，可能会降低程序性能。是否继续？",
                    "警告",
                    wx.YES_NO | wx.ICON_WARNING
                )
                result = dlg.ShowModal()
                dlg.Destroy()
                if result != wx.ID_YES:
                    return

            # 获取MIME类型
            mime_type, _ = mimetypes.guess_type(file_path)
            mime_type = mime_type or "application/octet-stream"

            # 添加头部信息
            header = f"data:{mime_type};base64," if self.include_header.GetValue() else ""

            # 禁用按钮
            self.toggle_buttons(False)

            # 显示加载状态
            self.status_info.SetLabel(f"正在编码文件: {filename}...")
            self.status_info.SetForegroundColour(wx.BLUE)
            self.loading_indicator.SetValue(0)
            self.loading_indicator.Show()
            self.progress_text.SetLabel("0%")
            self.cancel_btn.Show()
            self.Layout()

            # 重置取消标志
            self.cancel_encoding = False

            # 创建并启动编码线程
            self.encoding_thread = threading.Thread(
                target=self.encode_file_thread,
                args=(file_path, header, file_size)
            )
            self.encoding_thread.daemon = True
            self.encoding_thread.start()

        except Exception as e:
            self.status_info.SetLabel(f"文件编码出错: {str(e)}")
            self.status_info.SetForegroundColour(wx.RED)
            self.reset_encoding_ui()

    def encode_file_thread(self, file_path, header, file_size):
        """文件编码线程"""
        try:
            base64_str = ""
            processed_bytes = 0
            chunk_size = 1024 * 1024  # 每次读取1MB

            with open(file_path, "rb") as f:
                while not self.cancel_encoding:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break

                    processed_bytes += len(chunk)
                    base64_str += base64.b64encode(chunk).decode('utf-8')

                    # 更新进度
                    percent = int((processed_bytes / file_size) * 100)
                    self.progress_queue.put((processed_bytes, file_size, percent))

            if self.cancel_encoding:
                self.progress_queue.put(("cancelled",))
                return

            # 组合完整结果
            full_result = header + base64_str

            # 更新UI
            self.progress_queue.put(("completed", full_result, file_size))

        except Exception as e:
            self.progress_queue.put(("failed", str(e)))

    def update_progress(self, event):
        """更新进度"""
        try:
            while not self.progress_queue.empty():
                data = self.progress_queue.get_nowait()

                if data[0] == "completed":
                    self.encoding_completed(data[1], data[2])
                elif data[0] == "failed":
                    self.encoding_failed(data[1])
                elif data[0] == "cancelled":
                    self.encoding_cancelled()
                else:
                    processed_bytes, file_size, percent = data
                    self.loading_indicator.SetValue(percent)
                    self.progress_text.SetLabel(f"{percent}%")
                    self.status_info.SetLabel(
                        f"编码中: {self.format_file_size(processed_bytes)} / {self.format_file_size(file_size)}"
                    )
        except queue.Empty:
            pass

    def encoding_completed(self, full_result, file_size):
        """编码完成"""
        self.file_output_text.SetValue(full_result)
        self.status_info.SetLabel(
            f"文件编码成功! 大小: {self.format_file_size(file_size)} → "
            f"Base64: {self.format_file_size(len(full_result))} "
            f"({len(full_result) * 100 // file_size}%)"
        )
        self.status_info.SetForegroundColour(wx.BLACK)
        self.reset_encoding_ui()

    def encoding_failed(self, error_message):
        """编码失败"""
        self.status_info.SetLabel(f"文件编码出错: {error_message}")
        self.status_info.SetForegroundColour(wx.RED)
        self.reset_encoding_ui()

    def encoding_cancelled(self):
        """编码取消"""
        self.status_info.SetLabel("编码已取消")
        self.status_info.SetForegroundColour(wx.BLACK)
        self.reset_encoding_ui()

    def on_cancel_encoding(self, event):
        """取消编码"""
        self.cancel_encoding = True
        self.status_info.SetLabel("正在取消编码...")
        self.status_info.SetForegroundColour(wx.BLUE)

    def reset_encoding_ui(self):
        """重置编码UI状态"""
        self.loading_indicator.Hide()
        self.cancel_btn.Hide()
        self.Layout()
        self.toggle_buttons(True)
        self.encoding_thread = None

    def toggle_buttons(self, enable):
        """切换按钮状态"""
        buttons = [
            self.file_encode_btn,
            self.browse_btn,
            self.file_decode_btn,
            self.copy_btn,
            self.save_btn
        ]

        for btn in buttons:
            btn.Enable(enable)

    def on_decode_file(self, event):
        """文件解码"""
        base64_str = self.file_output_text.GetValue().strip()

        if not base64_str:
            wx.MessageBox("请先对文件进行编码或粘贴有效的Base64字符串", "提示", wx.OK | wx.ICON_INFORMATION, self)
            return

        try:
            # 显示状态
            self.status_info.SetLabel("开始解码Base64内容...")
            self.status_info.SetForegroundColour(wx.BLUE)
            wx.Yield()  # 刷新界面

            # 检查并移除头部信息
            is_data_uri = False
            header_end = base64_str.find(",")
            if base64_str.startswith("data:") and header_end != -1:
                header = base64_str[:header_end + 1]
                base64_content = base64_str[header_end + 1:]
                is_data_uri = True

                # 提取MIME类型
                mime_type = header.split(";")[0][5:]
            else:
                base64_content = base64_str
                mime_type = "application/octet-stream"

            # 检查内容长度
            content_length = len(base64_content)
            if content_length > 10 * 1024 * 1024:  # 大于10MB
                dlg = wx.MessageDialog(
                    self,
                    f"Base64内容很大 ({self.format_file_size(content_length)})。解码可能会消耗较多资源。是否继续？",
                    "警告",
                    wx.YES_NO | wx.ICON_WARNING
                )
                result = dlg.ShowModal()
                dlg.Destroy()
                if result != wx.ID_YES:
                    self.status_info.SetLabel("解码已取消")
                    self.status_info.SetForegroundColour(wx.BLACK)
                    return

            # 解码文件
            start_time = time.time()
            decoded_data = base64.b64decode(base64_content)

            # 文件选择对话框让用户保存解码结果
            with wx.FileDialog(self, "保存解码文件", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
                if is_data_uri:
                    # 尝试从头部提取文件扩展名
                    ext = mimetypes.guess_extension(mime_type) or ".bin"
                    dlg.SetFilename("decoded_file" + ext)
                else:
                    dlg.SetFilename("decoded_file.bin")

                if dlg.ShowModal() == wx.ID_OK:
                    save_path = dlg.GetPath()

                    # 写入文件
                    with open(save_path, "wb") as f:
                        f.write(decoded_data)

                    elapsed = time.time() - start_time
                    self.status_info.SetLabel(
                        f"文件解码成功! 保存到: {os.path.basename(save_path)} "
                        f"- 大小: {self.format_file_size(len(decoded_data))} "
                        f"- 耗时: {self.format_elapsed_time(elapsed)}"
                    )
                    self.status_info.SetForegroundColour(wx.BLACK)

        except Exception as e:
            self.status_info.SetLabel(f"文件解码出错: {str(e)}\n请确保这是有效的Base64编码")
            self.status_info.SetForegroundColour(wx.RED)

    def on_save_file(self, event):
        """保存结果到文件"""
        base64_str = self.file_output_text.GetValue().strip()

        if not base64_str:
            wx.MessageBox("没有内容可保存", "提示", wx.OK | wx.ICON_INFORMATION, self)
            return

        try:
            with wx.FileDialog(self, "保存Base64编码", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
                dlg.SetFilename("base64_encoded.txt")
                if dlg.ShowModal() == wx.ID_OK:
                    save_path = dlg.GetPath()
                    with open(save_path, "w", encoding="utf-8") as f:
                        f.write(base64_str)
                    self.status_info.SetLabel(f"Base64编码已保存: {os.path.basename(save_path)}")
                    self.status_info.SetForegroundColour(wx.BLACK)
        except Exception as e:
            self.status_info.SetLabel(f"保存失败: {str(e)}")
            self.status_info.SetForegroundColour(wx.RED)

    def on_copy_result(self, event):
        """复制结果到剪贴板"""
        base64_str = self.file_output_text.GetValue().strip()

        if not base64_str:
            return

        try:
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(wx.TextDataObject(base64_str))
                wx.TheClipboard.Close()
                self.status_info.SetLabel("Base64编码已复制到剪贴板")
                self.status_info.SetForegroundColour(wx.Colour(0, 128, 0))  # 深绿色
        except Exception as e:
            self.status_info.SetLabel(f"复制失败: {str(e)}")
            self.status_info.SetForegroundColour(wx.RED)

    def format_file_size(self, size):
        """格式化文件大小显示"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0 or unit == 'GB':
                break
            size /= 1024.0
        return f"{size:.2f} {unit}"

    def format_elapsed_time(self, seconds):
        """格式化时间显示"""
        if seconds < 1:
            return f"{seconds * 1000:.0f}毫秒"
        elif seconds < 60:
            return f"{seconds:.2f}秒"
        else:
            minutes = int(seconds / 60)
            seconds = seconds % 60
            return f"{minutes}分{seconds:.0f}秒"
