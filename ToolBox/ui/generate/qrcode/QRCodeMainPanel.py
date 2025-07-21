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
## Class QRCodeMainPanel
###########################################################################

class QRCodeMainPanel(wx.Panel):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(1000, -1), style=wx.TAB_TRAVERSAL,
                 name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        self.qrcode_note_book = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        bSizer10.Add(self.qrcode_note_book, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer10)
        self.Layout()

        # Connect Events
        self.qrcode_note_book.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onChoose)
        self.qrcode_note_book.AddPage(QRCodeGeneratePanel(self.qrcode_note_book), "生成二维码")
        self.qrcode_note_book.AddPage(QRDecoderPanel(self.qrcode_note_book), "二维码识别")

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def onChoose(self, event):
        event.Skip()


import wx
import qrcode


class QRCodeGeneratePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # 初始化变量
        self.logo_path = None
        self.qr_image = None

        # 创建UI控件
        self.create_controls()

        # 设置布局
        self.setup_layout()

    def create_controls(self):
        """创建所有UI控件"""
        # 文本输入
        self.input_label = wx.StaticText(self, label="输入文本或URL:")
        self.text_entry = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(300, -1))
        self.text_entry.Bind(wx.EVT_TEXT_ENTER, self.on_generate)

        # 按钮
        self.generate_btn = wx.Button(self, label="生成二维码")
        self.generate_btn.Bind(wx.EVT_BUTTON, self.on_generate)

        self.logo_btn = wx.Button(self, label="添加Logo")
        self.logo_btn.Bind(wx.EVT_BUTTON, self.on_select_logo)

        self.save_btn = wx.Button(self, label="保存二维码")
        self.save_btn.Bind(wx.EVT_BUTTON, self.on_save_qrcode)
        self.save_btn.Disable()  # 初始禁用

        # 二维码预览区域
        self.bitmap = wx.StaticBitmap(self, size=(300, 300))
        empty_img = wx.Image(300, 300)
        empty_img.SetRGB(wx.Rect(0, 0, 300, 300), 240, 240, 240)  # 浅灰色背景
        self.bitmap.SetBitmap(wx.Bitmap(empty_img))

        # 状态提示
        self.status_label = wx.StaticText(self, label="准备就绪")
        font = self.status_label.GetFont()
        font.SetPointSize(9)
        self.status_label.SetFont(font)
        self.status_label.SetForegroundColour(wx.Colour(100, 100, 100))

    def setup_layout(self):
        """设置面板布局"""
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 输入区域
        input_sizer = wx.FlexGridSizer(cols=2, vgap=10, hgap=10)
        input_sizer.AddGrowableCol(1)

        input_sizer.Add(self.input_label, 0, wx.ALIGN_CENTER_VERTICAL)
        input_sizer.Add(self.text_entry, 0, wx.EXPAND)

        # 按钮区域
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.generate_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.logo_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.save_btn, 0, wx.ALL, 5)

        # 添加到主布局
        main_sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 15)
        main_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        main_sizer.Add(self.bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 15)
        main_sizer.Add(self.status_label, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)

        self.SetSizer(main_sizer)

    def on_generate(self, event):
        """生成二维码"""
        content = self.text_entry.GetValue().strip()
        if not content:
            self.update_status("请输入内容!", wx.RED)
            return

        self.update_status("正在生成二维码...", wx.BLUE)
        wx.Yield()  # 更新UI

        try:
            # 创建二维码
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=2
            )
            qr.add_data(content)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

            # 添加Logo（如果已选择）
            if self.logo_path:
                try:
                    logo = Image.open(self.logo_path).convert("RGBA")

                    # 调整Logo大小（不超过二维码的20%）
                    max_size = min(img.size) // 5
                    logo.thumbnail((max_size, max_size))

                    # 居中放置Logo
                    position = (
                        (img.width - logo.width) // 2,
                        (img.height - logo.height) // 2
                    )

                    # 圆形遮罩
                    mask = Image.new('L', logo.size, 0)
                    mask_draw = Image.new('L', logo.size, 255)
                    mask = Image.composite(mask, mask_draw, logo.split()[3])

                    img.paste(logo, position, mask)
                except Exception as e:
                    self.update_status(f"Logo添加失败: {str(e)}", wx.RED)

            self.qr_image = img
            wx_img = self.pil_to_wx(img.resize((300, 300)))
            self.bitmap.SetBitmap(wx.Bitmap(wx_img))
            self.save_btn.Enable()
            self.update_status("二维码已生成!", wx.Colour(0, 150, 0))

        except Exception as e:
            self.update_status(f"生成失败: {str(e)}", wx.RED)

    def pil_to_wx(self, pil_image):
        """将PIL图像转换为wx.Image"""
        width, height = pil_image.size
        wx_image = wx.Image(width, height)
        wx_image.SetData(pil_image.convert("RGB").tobytes())

        # 处理透明通道
        if pil_image.mode == 'RGBA':
            alpha = pil_image.convert("RGBA").tobytes()[3::4]
            wx_image.SetAlpha(alpha)

        return wx_image

    def on_select_logo(self, event):
        """选择Logo图片"""
        with wx.FileDialog(
                self, "选择Logo",
                wildcard="图片文件 (*.png;*.jpg;*.jpeg)|*.png;*.jpg;*.jpeg",
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.logo_path = dlg.GetPath()
                self.update_status(f"已选择Logo: {self.logo_path.split('/')[-1]}", wx.BLUE)

    def on_save_qrcode(self, event):
        """保存二维码"""
        if not self.qr_image:
            self.update_status("请先生成二维码", wx.RED)
            return

        with wx.FileDialog(
                self, "保存二维码",
                wildcard="PNG 图片 (*.png)|*.png",
                defaultFile="qrcode.png",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                if not path.lower().endswith('.png'):
                    path += '.png'
                try:
                    self.qr_image.save(path)
                    self.update_status(f"二维码已保存到: {path}", wx.Colour(0, 150, 0))
                except Exception as e:
                    self.update_status(f"保存失败: {str(e)}", wx.RED)

    def update_status(self, message, color=None):
        """更新状态标签"""
        self.status_label.SetLabel(message)
        if color:
            self.status_label.SetForegroundColour(color)
        self.Layout()


import wx
import wx.lib.scrolledpanel as scrolled
import pyzbar.pyzbar as pyzbar
from PIL import Image
import os


class QRDecoderPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.VSCROLL)

        # 初始化变量
        self.image_path = None
        self.original_image = None

        # 设置滚动面板
        self.SetupScrolling(scroll_x=True, scroll_y=True)

        # 创建UI控件
        self.create_controls()

        # 设置布局
        self.setup_layout()

        # 设置窗口最小尺寸
        self.SetMinSize(wx.Size(500, 400))

    def create_controls(self):
        """创建所有UI控件"""
        # 选择图片按钮
        self.select_btn = wx.Button(self, label="选择图片")
        self.select_btn.Bind(wx.EVT_BUTTON, self.on_select_image)
        self.select_btn.SetToolTip("选择包含二维码的图片文件")

        # 识别二维码按钮
        self.decode_btn = wx.Button(self, label="识别二维码")
        self.decode_btn.Bind(wx.EVT_BUTTON, self.on_decode)
        self.decode_btn.SetToolTip("识别图片中的二维码内容")
        self.decode_btn.Disable()  # 初始禁用

        # 图片显示控件
        self.image_display = wx.StaticBitmap(self)
        empty_bmp = self.create_empty_bitmap(400, 300)
        self.image_display.SetBitmap(empty_bmp)

        # 识别结果区域
        self.result_label = wx.StaticText(self, label="识别结果:")
        self.result_label.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        self.result_text = wx.TextCtrl(
            self,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH | wx.BORDER_SUNKEN
        )
        self.result_text.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.result_text.SetMinSize(wx.Size(400, 150))  # 设置最小高度

        # 操作按钮
        self.copy_btn = wx.Button(self, label="复制结果")
        self.copy_btn.Bind(wx.EVT_BUTTON, self.on_copy_result)
        self.copy_btn.Disable()  # 初始禁用

        self.clear_btn = wx.Button(self, label="清空")
        self.clear_btn.Bind(wx.EVT_BUTTON, self.on_clear)

        # 状态提示
        self.status_label = wx.StaticText(self, label="请选择包含二维码的图片")
        font = self.status_label.GetFont()
        font.SetPointSize(9)
        self.status_label.SetFont(font)
        self.status_label.SetForegroundColour(wx.Colour(100, 100, 100))

    def setup_layout(self):
        """设置面板布局"""
        # 使用BoxSizer进行布局，使所有控件都在一个垂直容器中
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 按钮区域
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.select_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.decode_btn, 0, wx.ALL, 5)
        button_sizer.AddStretchSpacer(1)  # 添加弹性空间
        button_sizer.Add(self.copy_btn, 0, wx.ALL, 5)
        button_sizer.Add(self.clear_btn, 0, wx.ALL, 5)

        # 图片显示区域
        image_box = wx.StaticBox(self, label="图片预览")
        image_box_sizer = wx.StaticBoxSizer(image_box, wx.VERTICAL)
        image_box_sizer.Add(self.image_display, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # 结果显示区域
        result_box = wx.StaticBox(self, label="识别内容")
        result_box_sizer = wx.StaticBoxSizer(result_box, wx.VERTICAL)
        result_box_sizer.Add(self.result_text, 1, wx.EXPAND | wx.ALL, 5)

        # 添加到主布局
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(image_box_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        main_sizer.Add(result_box_sizer, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(self.status_label, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(main_sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

    def create_empty_bitmap(self, width, height):
        """创建空位图"""
        img = wx.Image(width, height)
        img.SetRGB(wx.Rect(0, 0, width, height), 240, 240, 240)  # 浅灰色背景
        img.SetAlpha(b'\x80' * (width * height))  # 半透明
        return wx.Bitmap(img)

    def update_status(self, message, color=None):
        """更新状态标签"""
        self.status_label.SetLabel(message)
        if color:
            self.status_label.SetForegroundColour(color)
        self.Layout()
        self.SetupScrolling()  # 更新滚动区域

    def display_image(self, image_path):
        """显示选择的图片"""
        try:
            image = Image.open(image_path)
            self.original_image = image.copy()  # 保存原始图片

            # 调整显示大小（最大尺寸400x300）
            max_width, max_height = 400, 300
            width, height = image.size

            # 计算缩放比例
            scale = min(max_width / width, max_height / height)
            new_width = int(width * scale)
            new_height = int(height * scale)

            # 缩放并显示
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            wx_img = self.pil_to_wx(image)
            self.image_display.SetBitmap(wx.Bitmap(wx_img))
            self.decode_btn.Enable()
            self.update_status(f"已选择图片: {os.path.basename(image_path)}", wx.BLUE)

            # 更新滚动区域
            self.Layout()
            self.SetupScrolling()

        except Exception as e:
            wx.MessageBox(f"无法加载图片: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def pil_to_wx(self, pil_image):
        """将PIL图像转换为wx.Image"""
        width, height = pil_image.size
        if pil_image.mode == 'RGB':
            wx_image = wx.Image(width, height, pil_image.tobytes())
        elif pil_image.mode == 'RGBA':
            wx_image = wx.Image(width, height, pil_image.tobytes())
            wx_image.SetAlpha(pil_image.convert("RGBA").tobytes()[3::4])
        else:
            pil_image = pil_image.convert("RGB")
            wx_image = wx.Image(width, height, pil_image.tobytes())
        return wx_image

    def on_select_image(self, event):
        """选择图片文件"""
        wildcard = "图片文件 (*.png;*.jpg;*.jpeg;*.bmp;*.gif)|*.png;*.jpg;*.jpeg;*.bmp;*.gif"
        with wx.FileDialog(
                self, "选择二维码图片",
                wildcard=wildcard,
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.image_path = dlg.GetPath()
                self.display_image(self.image_path)

    def on_decode(self, event):
        """识别二维码"""
        if not self.original_image:
            self.update_status("请先选择图片", wx.RED)
            return

        try:
            # 识别二维码
            decoded_objects = pyzbar.decode(self.original_image)

            if not decoded_objects:
                self.update_status("未识别到二维码", wx.RED)
                self.result_text.SetValue("未在图片中识别到任何二维码")
                self.copy_btn.Disable()
                return

            # 处理识别结果
            results = []
            for i, obj in enumerate(decoded_objects, 1):
                try:
                    data = obj.data.decode("utf-8", errors="replace")
                    results.append(f"二维码 {i} ({obj.type}):\n{data}\n")
                except Exception as e:
                    results.append(f"二维码 {i} ({obj.type}):\n无法解码内容 ({str(e)})\n")

            result_text = "\n".join(results)
            self.result_text.SetValue(result_text)
            self.copy_btn.Enable()
            self.update_status(f"识别成功: 找到 {len(decoded_objects)} 个二维码", wx.Colour(0, 150, 0))

        except Exception as e:
            wx.MessageBox(f"识别失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)
            self.update_status("识别失败", wx.RED)

    def on_copy_result(self, event):
        """复制识别结果到剪贴板"""
        result = self.result_text.GetValue()
        if not result.strip():
            return

        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(result))
            wx.TheClipboard.Close()
            self.update_status("识别结果已复制到剪贴板", wx.Colour(0, 150, 0))

    def on_clear(self, event):
        """清空所有内容"""
        # 清空图片显示
        empty_bmp = self.create_empty_bitmap(400, 300)
        self.image_display.SetBitmap(empty_bmp)

        # 清空结果
        self.result_text.Clear()

        # 重置状态
        self.image_path = None
        self.original_image = None
        self.decode_btn.Disable()
        self.copy_btn.Disable()
        self.update_status("请选择包含二维码的图片", wx.Colour(100, 100, 100))

        # 更新滚动区域
        self.Layout()
        self.SetupScrolling()
