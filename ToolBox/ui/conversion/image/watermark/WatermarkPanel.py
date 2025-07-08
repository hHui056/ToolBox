import wx
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
import os
import io
import sys
import platform
import math


class WatermarkPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # 初始化变量
        self.image_path = ""
        self.watermark_path = ""
        self.watermark_type = "text"  # "text" 或 "image"
        self.watermark_text = "水印文字"
        self.font_size = 56  # 默认字体大小改为56
        self.font_color = (0, 0, 0, 180)  # RGBA - 黑色半透明
        self.watermark_opacity = 0.7  # 透明度
        self.watermark_position = "center"  # 位置
        self.watermark_scale = 0.3  # 图片水印缩放比例
        self.font_file = self.get_default_font()  # 默认字体文件
        self.rotation_angle = 0  # 旋转角度

        # 创建UI
        self.init_ui()
        self.SetMinSize((900, 600))

    def get_default_font(self):
        """获取系统中文字体路径"""
        try:
            # Windows系统
            if sys.platform.startswith('win'):
                # 尝试获取微软雅黑字体
                win_dir = os.environ.get('SystemRoot', 'C:\\Windows')
                fonts_dir = os.path.join(win_dir, 'Fonts')
                font_path = os.path.join(fonts_dir, 'msyh.ttc')

                if os.path.exists(font_path):
                    return font_path

                # 尝试获取宋体
                font_path = os.path.join(fonts_dir, 'simsun.ttc')
                if os.path.exists(font_path):
                    return font_path

                # 尝试获取微软正黑体
                font_path = os.path.join(fonts_dir, 'msjh.ttc')
                if os.path.exists(font_path):
                    return font_path

            # macOS系统
            elif sys.platform.startswith('darwin'):
                # 尝试苹方字体
                font_path = '/System/Library/Fonts/PingFang.ttc'
                if os.path.exists(font_path):
                    return font_path

                # 尝试华文黑体
                font_path = '/System/Library/Fonts/STHeiti Light.ttc'
                if os.path.exists(font_path):
                    return font_path

            # Linux系统
            elif sys.platform.startswith('linux'):
                # 尝试Droid Sans字体
                font_path = '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf'
                if os.path.exists(font_path):
                    return font_path

                # 尝试Noto Sans字体
                font_path = '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc'
                if os.path.exists(font_path):
                    return font_path

        except:
            pass

        # 默认返回None，将在后续处理
        return None

    def init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        # 控制面板
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 按钮区域
        btn_open = wx.Button(self, label="选择图片")
        btn_open.Bind(wx.EVT_BUTTON, self.on_open_image)

        self.btn_apply = wx.Button(self, label="应用水印")
        self.btn_apply.Bind(wx.EVT_BUTTON, self.on_apply_watermark)
        self.btn_apply.Disable()

        self.btn_save = wx.Button(self, label="保存图片")
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        self.btn_save.Disable()

        btn_clear = wx.Button(self, label="清空")
        btn_clear.Bind(wx.EVT_BUTTON, self.on_clear)

        # 添加到控制面板
        control_sizer.Add(btn_open, 0, wx.ALL | wx.EXPAND, 5)
        control_sizer.Add(self.btn_apply, 0, wx.ALL | wx.EXPAND, 5)
        control_sizer.Add(self.btn_save, 0, wx.ALL | wx.EXPAND, 5)
        control_sizer.Add(btn_clear, 0, wx.ALL | wx.EXPAND, 5)

        # ====== 水印设置区域 - 重新组织布局 ======
        settings_box = wx.StaticBox(self, label="水印设置")
        settings_sizer = wx.StaticBoxSizer(settings_box, wx.VERTICAL)

        # 第一行：水印类型、水印文字、文字大小
        row1_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 水印类型
        type_sizer = wx.BoxSizer(wx.VERTICAL)
        type_sizer.Add(wx.StaticText(self, label="水印类型:"), 0, wx.ALIGN_LEFT)
        self.type_choice = wx.Choice(self, choices=["文字水印", "图片水印"])
        self.type_choice.SetSelection(0)
        self.type_choice.Bind(wx.EVT_CHOICE, self.on_watermark_type_change)
        type_sizer.Add(self.type_choice, 0, wx.EXPAND)
        row1_sizer.Add(type_sizer, 1, wx.ALL | wx.EXPAND, 5)

        # 水印文字
        text_sizer = wx.BoxSizer(wx.VERTICAL)
        text_sizer.Add(wx.StaticText(self, label="水印文字:"), 0, wx.ALIGN_LEFT)
        self.text_ctrl = wx.TextCtrl(self, value="水印文字")
        self.text_ctrl.Bind(wx.EVT_TEXT, self.on_text_change)
        text_sizer.Add(self.text_ctrl, 0, wx.EXPAND)
        row1_sizer.Add(text_sizer, 2, wx.ALL | wx.EXPAND, 5)

        # 字体大小
        size_sizer = wx.BoxSizer(wx.VERTICAL)
        size_sizer.Add(wx.StaticText(self, label="字体大小:"), 0, wx.ALIGN_LEFT)
        self.font_size_ctrl = wx.SpinCtrl(self, min=10, max=200, initial=56)  # 默认56
        self.font_size_ctrl.Bind(wx.EVT_SPINCTRL, self.on_font_size_change)
        size_sizer.Add(self.font_size_ctrl, 0, wx.EXPAND)
        row1_sizer.Add(size_sizer, 1, wx.ALL | wx.EXPAND, 5)

        # 第二行：透明度、位置、文字颜色、旋转角度
        row2_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 透明度 - 使用输入框
        opacity_sizer = wx.BoxSizer(wx.VERTICAL)
        opacity_sizer.Add(wx.StaticText(self, label="透明度(%):"), 0, wx.ALIGN_LEFT)

        # 创建输入框
        opacity_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.opacity_ctrl = wx.SpinCtrl(self, min=10, max=100, initial=70)
        self.opacity_ctrl.Bind(wx.EVT_SPINCTRL, self.on_opacity_change)
        opacity_input_sizer.Add(self.opacity_ctrl, 1, wx.ALIGN_CENTER_VERTICAL)
        opacity_input_sizer.Add(wx.StaticText(self, label="%"), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)

        opacity_sizer.Add(opacity_input_sizer, 0, wx.EXPAND)
        row2_sizer.Add(opacity_sizer, 1, wx.ALL | wx.EXPAND, 5)

        # 位置
        position_sizer = wx.BoxSizer(wx.VERTICAL)
        position_sizer.Add(wx.StaticText(self, label="位置:"), 0, wx.ALIGN_LEFT)
        position_choices = ["左上", "中上", "右上", "左中", "中心", "右中", "左下", "中下", "右下", "铺满"]
        self.position_choice = wx.Choice(self, choices=position_choices)
        self.position_choice.SetSelection(4)  # 默认中心
        self.position_choice.Bind(wx.EVT_CHOICE, self.on_position_change)
        position_sizer.Add(self.position_choice, 0, wx.EXPAND)
        row2_sizer.Add(position_sizer, 1, wx.ALL | wx.EXPAND, 5)

        # 文字颜色
        color_sizer = wx.BoxSizer(wx.VERTICAL)
        color_sizer.Add(wx.StaticText(self, label="文字颜色:"), 0, wx.ALIGN_LEFT)
        self.color_picker = wx.ColourPickerCtrl(self, colour=wx.Colour(0, 0, 0))  # 默认黑色
        self.color_picker.Bind(wx.EVT_COLOURPICKER_CHANGED, self.on_color_change)
        color_sizer.Add(self.color_picker, 0, wx.EXPAND)
        row2_sizer.Add(color_sizer, 1, wx.ALL | wx.EXPAND, 5)

        # 旋转角度
        rotation_sizer = wx.BoxSizer(wx.VERTICAL)
        rotation_sizer.Add(wx.StaticText(self, label="旋转角度:"), 0, wx.ALIGN_LEFT)
        self.rotation_ctrl = wx.SpinCtrl(self, min=-180, max=180, initial=0)
        self.rotation_ctrl.Bind(wx.EVT_SPINCTRL, self.on_rotation_change)
        rotation_sizer.Add(self.rotation_ctrl, 0, wx.EXPAND)
        row2_sizer.Add(rotation_sizer, 1, wx.ALL | wx.EXPAND, 5)

        # 字体文件选择
        row3_sizer = wx.BoxSizer(wx.HORIZONTAL)
        font_sizer = wx.BoxSizer(wx.VERTICAL)
        font_sizer.Add(wx.StaticText(self, label="字体文件:"), 0, wx.ALIGN_LEFT)

        font_file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.font_path_ctrl = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.font_path_ctrl.SetValue(self.font_file if self.font_file else "系统默认字体")
        btn_select_font = wx.Button(self, label="选择...")
        btn_select_font.Bind(wx.EVT_BUTTON, self.on_select_font)
        font_file_sizer.Add(self.font_path_ctrl, 1, wx.EXPAND | wx.RIGHT, 5)
        font_file_sizer.Add(btn_select_font, 0, wx.EXPAND)
        font_sizer.Add(font_file_sizer, 0, wx.EXPAND)
        row3_sizer.Add(font_sizer, 1, wx.ALL | wx.EXPAND, 5)

        # 图片水印设置
        image_watermark_sizer = wx.BoxSizer(wx.VERTICAL)
        image_watermark_sizer.Add(wx.StaticText(self, label="水印图片:"), 0, wx.ALIGN_LEFT)

        img_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.watermark_path_ctrl = wx.TextCtrl(self, style=wx.TE_READONLY)
        btn_select_watermark = wx.Button(self, label="选择...")
        btn_select_watermark.Bind(wx.EVT_BUTTON, self.on_select_watermark)
        img_sizer.Add(self.watermark_path_ctrl, 1, wx.EXPAND | wx.RIGHT, 5)
        img_sizer.Add(btn_select_watermark, 0, wx.EXPAND)
        image_watermark_sizer.Add(img_sizer, 0, wx.EXPAND)
        row3_sizer.Add(image_watermark_sizer, 1, wx.ALL | wx.EXPAND, 5)

        # 缩放比例
        scale_sizer = wx.BoxSizer(wx.VERTICAL)
        scale_sizer.Add(wx.StaticText(self, label="缩放比例:"), 0, wx.ALIGN_LEFT)
        self.scale_slider = wx.Slider(self, value=30, minValue=5, maxValue=100)
        self.scale_slider.Bind(wx.EVT_SLIDER, self.on_scale_change)
        scale_sizer.Add(self.scale_slider, 0, wx.EXPAND)
        row3_sizer.Add(scale_sizer, 1, wx.ALL | wx.EXPAND, 5)

        # 添加到设置区域
        settings_sizer.Add(row1_sizer, 0, wx.EXPAND | wx.ALL, 5)
        settings_sizer.Add(row2_sizer, 0, wx.EXPAND | wx.ALL, 5)
        settings_sizer.Add(row3_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # 图片显示区域
        img_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 左侧面板 - 原始图片
        left_panel = wx.Panel(self)
        left_box = wx.StaticBox(left_panel, label="原始图片")
        left_sizer = wx.StaticBoxSizer(left_box, wx.VERTICAL)

        self.lbl_image_path = wx.StaticText(left_panel, label="未选择图片", style=wx.ALIGN_LEFT)
        self.lbl_image_path.Wrap(350)  # 允许换行

        # 创建空位图
        empty_bitmap = self.create_empty_bitmap(400, 300)

        self.image_display = wx.StaticBitmap(left_panel, bitmap=empty_bitmap)
        self.lbl_image_info = wx.StaticText(left_panel, label="等待选择图片", style=wx.ALIGN_CENTER)

        left_sizer.Add(self.lbl_image_path, 0, wx.ALL | wx.EXPAND, 5)
        left_sizer.Add(self.image_display, 1, wx.EXPAND | wx.ALL, 5)
        left_sizer.Add(self.lbl_image_info, 0, wx.EXPAND | wx.ALL, 5)

        left_panel.SetSizer(left_sizer)

        # 右侧面板 - 水印效果
        right_panel = wx.Panel(self)
        right_box = wx.StaticBox(right_panel, label="水印效果 - 双击预览")
        right_sizer = wx.StaticBoxSizer(right_box, wx.VERTICAL)

        self.watermark_display = wx.StaticBitmap(right_panel, bitmap=empty_bitmap)
        self.watermark_display.Bind(wx.EVT_LEFT_DCLICK, self.on_preview_watermark)
        self.lbl_watermark_info = wx.StaticText(right_panel, label="等待添加水印", style=wx.ALIGN_CENTER)

        right_sizer.Add(self.watermark_display, 1, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(self.lbl_watermark_info, 0, wx.EXPAND | wx.ALL, 5)

        right_panel.SetSizer(right_sizer)

        # 添加到主布局
        img_sizer.Add(left_panel, 1, wx.EXPAND | wx.ALL, 5)
        img_sizer.Add(right_panel, 1, wx.EXPAND | wx.ALL, 5)

        # 将所有控件添加到主sizer
        main_sizer.Add(control_sizer, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(settings_sizer, 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(img_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)

        # 保存空位图用于重置
        self.empty_bitmap = empty_bitmap
        self.watermarked_image = None
        self.original_image = None

        # 更新UI状态
        self.update_ui_for_watermark_type()

    def create_empty_bitmap(self, width, height):
        """创建空白的位图"""
        bitmap = wx.Bitmap(width, height)
        dc = wx.MemoryDC()
        dc.SelectObject(bitmap)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.SelectObject(wx.NullBitmap)
        return bitmap

    def on_open_image(self, event):
        with wx.FileDialog(self, "选择图片",
                           wildcard="图片文件 (*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp)|*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.image_path = dlg.GetPath()
                self.load_image()

    def load_image(self):
        if not self.image_path:
            return

        try:
            # 获取文件信息
            img = Image.open(self.image_path)
            self.original_image = img.copy()  # 保存原始图像副本
            width, height = img.size
            file_size = os.path.getsize(self.image_path)
            size_kb = file_size / 1024

            # 显示图片信息
            self.lbl_image_path.SetLabel(self.image_path)
            self.lbl_image_info.SetLabel(f"尺寸: {width}×{height} | 大小: {size_kb:.1f}KB")

            # 显示图片
            wx_img = self.pil_to_wx_image(img)
            display_size = self.image_display.GetSize()

            # 缩放图片
            scaled_img = self.scale_image(wx_img, display_size[0], display_size[1])
            self.image_display.SetBitmap(wx.Bitmap(scaled_img))

            # 启用应用水印按钮
            self.btn_apply.Enable()

            # 清空右侧预览
            self.watermark_display.SetBitmap(self.empty_bitmap)
            self.lbl_watermark_info.SetLabel("等待添加水印")

            self.Layout()
        except Exception as e:
            wx.MessageBox(f"加载图片失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def pil_to_wx_image(self, pil_image):
        """将PIL图像转换为wx.Image"""
        if pil_image.mode == 'RGBA':
            # 处理透明通道
            alpha = pil_image.split()[3]
            image = wx.Image(pil_image.size[0], pil_image.size[1])
            image.SetData(pil_image.convert("RGB").tobytes())
            image.SetAlpha(alpha.tobytes())
            return image
        else:
            return wx.Image(pil_image.size[0], pil_image.size[1], pil_image.convert("RGB").tobytes())

    def scale_image(self, img, max_width, max_height):
        """缩放图片以适应给定的最大宽度和高度"""
        if not img.IsOk():
            return None

        w, h = img.GetWidth(), img.GetHeight()

        if w == 0 or h == 0:
            return img

        # 计算缩放比例
        ratio_width = max_width / w
        ratio_height = max_height / h
        scale = min(ratio_width, ratio_height) * 0.95  # 留出一些空白

        # 应用缩放，确保结果为整数
        new_w = int(w * scale)
        new_h = int(h * scale)

        # 确保尺寸至少为1
        new_w = max(new_w, 1)
        new_h = max(new_h, 1)

        return img.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)

    def on_watermark_type_change(self, event):
        """水印类型改变事件"""
        self.watermark_type = "text" if self.type_choice.GetSelection() == 0 else "image"
        self.update_ui_for_watermark_type()

    def update_ui_for_watermark_type(self):
        """根据水印类型更新UI状态"""
        is_text = self.watermark_type == "text"

        # 显示/隐藏相关控件
        self.text_ctrl.Show(is_text)
        self.font_size_ctrl.Show(is_text)
        self.font_path_ctrl.Show(is_text)
        self.color_picker.Show(is_text)

        # 图片水印设置
        self.watermark_path_ctrl.Show(not is_text)
        self.scale_slider.Show(not is_text)

        # 查找相关标签
        for child in self.GetChildren():
            if isinstance(child, wx.StaticText):
                label = child.GetLabel()
                if label == "水印文字:":
                    child.Show(is_text)
                elif label == "字体大小:":
                    child.Show(is_text)
                elif label == "字体文件:":
                    child.Show(is_text)
                elif label == "文字颜色:":
                    child.Show(is_text)
                elif label == "水印图片:":
                    child.Show(not is_text)
                elif label == "缩放比例:":
                    child.Show(not is_text)

        self.Layout()

    def on_text_change(self, event):
        """水印文字改变事件"""
        self.watermark_text = self.text_ctrl.GetValue()

    def on_font_size_change(self, event):
        """字体大小改变事件"""
        self.font_size = self.font_size_ctrl.GetValue()

    def on_select_font(self, event):
        """选择字体文件"""
        with wx.FileDialog(self, "选择字体文件",
                           wildcard="字体文件 (*.ttf;*.ttc;*.otf)|*.ttf;*.ttc;*.otf") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.font_file = dlg.GetPath()
                self.font_path_ctrl.SetValue(self.font_file)

    def on_select_watermark(self, event):
        """选择水印图片"""
        with wx.FileDialog(self, "选择水印图片",
                           wildcard="图片文件 (*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp)|*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.watermark_path = dlg.GetPath()
                self.watermark_path_ctrl.SetValue(self.watermark_path)

    def on_scale_change(self, event):
        """水印缩放比例改变事件"""
        self.watermark_scale = self.scale_slider.GetValue() / 100.0

    def on_opacity_change(self, event):
        """透明度改变事件"""
        self.watermark_opacity = self.opacity_ctrl.GetValue() / 100.0
        # 同时更新文字颜色的透明度
        color = self.color_picker.GetColour()
        self.font_color = (color.Red(), color.Green(), color.Blue(), int(255 * self.watermark_opacity))

    def on_position_change(self, event):
        """位置改变事件"""
        positions = ["top-left", "top-center", "top-right",
                     "middle-left", "center", "middle-right",
                     "bottom-left", "bottom-center", "bottom-right", "tiled"]
        idx = self.position_choice.GetSelection()
        self.watermark_position = positions[idx]

        # 如果选择铺满，设置默认旋转角度为-30度
        if idx == 9:  # 铺满位置
            self.rotation_angle = -30
            self.rotation_ctrl.SetValue(-30)
        else:
            # 非铺满位置，重置旋转角度为0
            self.rotation_angle = 0
            self.rotation_ctrl.SetValue(0)

    def on_rotation_change(self, event):
        """旋转角度改变事件"""
        self.rotation_angle = self.rotation_ctrl.GetValue()

    def on_color_change(self, event):
        """颜色改变事件"""
        color = self.color_picker.GetColour()
        self.font_color = (color.Red(), color.Green(), color.Blue(), int(255 * self.watermark_opacity))

    def on_apply_watermark(self, event):
        """应用水印"""
        if not self.image_path:
            wx.MessageBox("请先选择图片", "提示", wx.OK | wx.ICON_INFORMATION)
            return

        try:
            # 使用保存的原始图像
            img = self.original_image.copy() if self.original_image else Image.open(self.image_path)

            # 添加水印
            if self.watermark_type == "text":
                watermarked = self.add_text_watermark(img)
            else:
                if not self.watermark_path:
                    wx.MessageBox("请先选择水印图片", "提示", wx.OK | wx.ICON_INFORMATION)
                    return
                watermarked = self.add_image_watermark(img)

            # 保存水印图片
            self.watermarked_image = watermarked

            # 显示水印效果
            wx_img = self.pil_to_wx_image(watermarked)
            display_size = self.watermark_display.GetSize()

            # 缩放图片
            scaled_img = self.scale_image(wx_img, display_size[0], display_size[1])
            if scaled_img and scaled_img.IsOk():
                self.watermark_display.SetBitmap(wx.Bitmap(scaled_img))

            # 更新信息
            if self.watermark_type == "text":
                font_name = "系统默认字体"
                if self.font_file and os.path.exists(self.font_file):
                    font_name = os.path.basename(self.font_file)
                self.lbl_watermark_info.SetLabel(f"水印已添加 (字体: {font_name}, 旋转: {self.rotation_angle}度)")
            else:
                wm_size = watermarked.size
                self.lbl_watermark_info.SetLabel(
                    f"水印已添加 (尺寸: {wm_size[0]}x{wm_size[1]}px, 旋转: {self.rotation_angle}度)")

            # 启用保存按钮
            self.btn_save.Enable()

            self.Layout()
        except Exception as e:
            wx.MessageBox(f"添加水印失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def on_preview_watermark(self, event):
        """双击预览水印效果"""
        if not self.watermarked_image:
            return

        try:
            # 创建预览对话框
            dlg = wx.Dialog(self, title="水印效果预览", size=(800, 600),
                            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

            # 创建面板
            panel = wx.Panel(dlg)
            sizer = wx.BoxSizer(wx.VERTICAL)

            # 创建图像显示区域
            self.preview_bitmap = wx.StaticBitmap(panel)
            self.preview_bitmap.SetMinSize((600, 400))

            # 添加信息
            info_text = wx.StaticText(panel,
                                      label=f"图片尺寸: {self.watermarked_image.width}×{self.watermarked_image.height}")
            close_btn = wx.Button(panel, label="关闭")
            close_btn.Bind(wx.EVT_BUTTON, lambda e: dlg.Close())

            sizer.Add(self.preview_bitmap, 1, wx.EXPAND | wx.ALL, 10)
            sizer.Add(info_text, 0, wx.ALL, 10)
            sizer.Add(close_btn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

            panel.SetSizer(sizer)

            # 绑定大小改变事件
            dlg.Bind(wx.EVT_SIZE, self.on_preview_resize)

            # 初始显示图片
            self.update_preview_image(dlg)

            dlg.ShowModal()

        except Exception as e:
            wx.MessageBox(f"预览失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def on_preview_resize(self, event):
        """预览窗口大小改变事件"""
        dlg = event.GetEventObject()
        self.update_preview_image(dlg)
        event.Skip()

    def update_preview_image(self, dlg):
        """更新预览图像"""
        if not self.watermarked_image:
            return

        try:
            # 获取对话框客户区大小
            client_size = dlg.GetClientSize()
            max_width = client_size.width - 20  # 减去边距
            max_height = client_size.height - 100  # 减去标题栏和信息区域

            # 将PIL图像转换为wx.Image
            wx_img = self.pil_to_wx_image(self.watermarked_image)

            # 缩放图像以适应对话框
            scaled_img = self.scale_image(wx_img, max_width, max_height)
            if scaled_img and scaled_img.IsOk():
                self.preview_bitmap.SetBitmap(wx.Bitmap(scaled_img))

            # 更新布局
            dlg.Layout()
        except Exception as e:
            print(f"更新预览图像失败: {str(e)}")

    def add_text_watermark(self, image):
        """添加文字水印"""
        # 确保图像是RGBA模式
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # 创建水印图层
        watermark = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)

        # 尝试加载字体
        font = None

        # 尝试用户指定的字体
        if self.font_file and os.path.exists(self.font_file):
            try:
                font = ImageFont.truetype(self.font_file, self.font_size)
            except Exception as e:
                print(f"加载字体文件失败: {e}")

        # 尝试默认字体
        if font is None and self.get_default_font():
            try:
                font = ImageFont.truetype(self.get_default_font(), self.font_size)
            except:
                pass

        # 尝试系统常见中文字体
        if font is None:
            try:
                # Windows 系统
                if platform.system() == "Windows":
                    font = ImageFont.truetype("msyh.ttc", self.font_size)  # 微软雅黑
                # macOS 系统
                elif platform.system() == "Darwin":
                    font = ImageFont.truetype("PingFang.ttc", self.font_size)  # 苹方
                # Linux 系统
                else:
                    font = ImageFont.truetype("NotoSansCJK-Regular.ttc", self.font_size)  # Noto Sans
            except:
                pass

        # 如果还不行，尝试系统字体
        if font is None:
            try:
                font = ImageFont.truetype("arial.ttf", self.font_size)
            except:
                pass

        # 最后尝试加载默认字体
        if font is None:
            try:
                font = ImageFont.load_default()
                self.font_size = min(self.font_size, 20)  # 默认字体通常较小
            except:
                # 创建空字体对象避免崩溃
                font = ImageFont.load_default()
                self.font_size = min(self.font_size, 20)

        # 处理铺满水印
        if self.watermark_position == "tiled":
            # 计算文本位置
            bbox = draw.textbbox((0, 0), self.watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # 创建单个水印文本
            single_text = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
            single_draw = ImageDraw.Draw(single_text)
            # 修复文字底部被截断的问题 - 调整绘制位置
            single_draw.text((0, 0), self.watermark_text, font=font, fill=self.font_color)

            # 旋转水印文本
            if self.rotation_angle:
                single_text = single_text.rotate(self.rotation_angle, expand=True, fillcolor=(0, 0, 0, 0))

            # 平铺水印
            rotated_width, rotated_height = single_text.size

            # 计算水平和垂直间距
            horizontal_spacing = int(rotated_width * 1.5)
            vertical_spacing = int(rotated_height * 1.5)

            # 计算行列数
            cols = int(image.width / horizontal_spacing) + 2
            rows = int(image.height / vertical_spacing) + 2

            # 在透明层上平铺水印
            for i in range(cols):
                for j in range(rows):
                    x = (i * horizontal_spacing) - int(rotated_width * 0.25)
                    y = (j * vertical_spacing) - int(rotated_height * 0.25)
                    watermark.paste(single_text, (x, y), single_text)
        else:
            # 非铺满位置
            bbox = draw.textbbox((0, 0), self.watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # 创建临时文本图像 - 修复文字底部被截断的问题
            # 增加额外高度以容纳文本的下降部分
            extra_height = int(text_height * 0.2)  # 增加20%的高度
            text_height += extra_height

            text_layer = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
            draw_text = ImageDraw.Draw(text_layer)
            # 调整绘制位置，确保文本完整显示
            draw_text.text((0, 0), self.watermark_text, font=font, fill=self.font_color)

            # 旋转水印文本
            if self.rotation_angle:
                text_layer = text_layer.rotate(self.rotation_angle, expand=True, fillcolor=(0, 0, 0, 0))

            # 计算位置
            rotated_width, rotated_height = text_layer.size
            position = self.calculate_position(image.size, (rotated_width, rotated_height))

            # 将旋转后的文本贴到水印层
            watermark.paste(text_layer, position, text_layer)

        # 合并图层
        return Image.alpha_composite(image, watermark)

    def add_image_watermark(self, image):
        """添加图片水印"""
        # 打开水印图片
        watermark_img = Image.open(self.watermark_path)

        # 转换为RGBA模式
        if watermark_img.mode != "RGBA":
            watermark_img = watermark_img.convert("RGBA")

        # 调整水印大小
        base_width, base_height = image.size
        watermark_width = int(base_width * self.watermark_scale)
        watermark_height = int(watermark_img.height * (watermark_width / watermark_img.width))
        watermark_img = watermark_img.resize((watermark_width, watermark_height), Image.LANCZOS)

        # 调整透明度
        alpha = watermark_img.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(self.watermark_opacity)
        watermark_img.putalpha(alpha)

        # 旋转水印
        if self.rotation_angle:
            watermark_img = watermark_img.rotate(self.rotation_angle, expand=True, fillcolor=(0, 0, 0, 0))

        # 处理铺满水印
        if self.watermark_position == "tiled":
            # 计算平铺水印
            wm_width, wm_height = watermark_img.size

            # 计算水平和垂直间距
            horizontal_spacing = int(wm_width * 1.5)
            vertical_spacing = int(wm_height * 1.5)

            # 创建水印图层
            watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))

            # 计算行列
            cols = int(image.width / horizontal_spacing) + 2
            rows = int(image.height / vertical_spacing) + 2

            # 平铺水印
            for i in range(cols):
                for j in range(rows):
                    x = (i * horizontal_spacing) - int(wm_width * 0.25)
                    y = (j * vertical_spacing) - int(wm_height * 0.25)
                    watermark_layer.paste(watermark_img, (x, y), watermark_img)
        else:
            # 单个水印位置
            watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
            wm_width, wm_height = watermark_img.size
            position = self.calculate_position(image.size, (wm_width, wm_height))
            watermark_layer.paste(watermark_img, position, watermark_img)

        # 确保原始图像是RGBA模式
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        # 合并图层
        return Image.alpha_composite(image, watermark_layer)

    def calculate_position(self, base_size, watermark_size):
        """计算水印位置"""
        base_width, base_height = base_size
        wm_width, wm_height = watermark_size

        if self.watermark_position == "top-left":
            return (10, 10)
        elif self.watermark_position == "top-center":
            return ((base_width - wm_width) // 2, 10)
        elif self.watermark_position == "top-right":
            return (base_width - wm_width - 10, 10)
        elif self.watermark_position == "middle-left":
            return (10, (base_height - wm_height) // 2)
        elif self.watermark_position == "center":
            return ((base_width - wm_width) // 2, (base_height - wm_height) // 2)
        elif self.watermark_position == "middle-right":
            return (base_width - wm_width - 10, (base_height - wm_height) // 2)
        elif self.watermark_position == "bottom-left":
            return (10, base_height - wm_height - 10)
        elif self.watermark_position == "bottom-center":
            return ((base_width - wm_width) // 2, base_height - wm_height - 10)
        elif self.watermark_position == "bottom-right":
            return (base_width - wm_width - 10, base_height - wm_height - 10)
        else:
            return (10, 10)  # 默认左上角

    def on_save(self, event):
        """保存添加水印后的图片"""
        if not self.watermarked_image:
            wx.MessageBox("请先添加水印", "提示", wx.OK | wx.ICON_INFORMATION)
            return

        # 生成默认文件名
        base_name = os.path.basename(self.image_path)
        name, ext = os.path.splitext(base_name)
        default_filename = f"{name}_watermarked{ext}"

        with wx.FileDialog(
                self, "保存图片",
                defaultFile=default_filename,
                wildcard="PNG 图片 (*.png)|*.png|JPG 图片 (*.jpg)|*.jpg",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                save_path = dlg.GetPath()

                # 确保文件扩展名
                if not save_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    format = dlg.GetFilterIndex()
                    if format == 0:  # PNG
                        save_path += '.png'
                    else:  # JPG
                        save_path += '.jpg'

                try:
                    # 保存图片
                    if save_path.lower().endswith('.jpg') or save_path.lower().endswith('.jpeg'):
                        self.watermarked_image.convert("RGB").save(save_path, "JPEG", quality=95)
                    else:
                        self.watermarked_image.save(save_path, "PNG")

                    # 显示成功消息
                    wx.MessageBox(f"图片已保存到:\n{save_path}", "保存成功", wx.OK | wx.ICON_INFORMATION)
                except Exception as e:
                    wx.MessageBox(f"保存失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def on_clear(self, event):
        """清空所有内容"""
        # 重置变量
        self.image_path = ""
        self.watermark_path = ""
        self.watermark_text = "水印文字"
        self.font_size = 56  # 默认56
        self.font_color = (0, 0, 0, 180)  # 黑色半透明
        self.watermark_opacity = 0.7
        self.watermark_position = "center"
        self.watermark_scale = 0.3
        self.font_file = self.get_default_font()  # 重置字体
        self.original_image = None  # 清空原始图像
        self.rotation_angle = 0

        # 重置UI状态
        self.lbl_image_path.SetLabel("未选择图片")
        self.lbl_image_info.SetLabel("等待选择图片")
        self.image_display.SetBitmap(self.empty_bitmap)

        self.watermark_display.SetBitmap(self.empty_bitmap)
        self.lbl_watermark_info.SetLabel("等待添加水印")

        # 重置控件
        self.text_ctrl.SetValue("水印文字")
        self.font_size_ctrl.SetValue(56)  # 默认56
        self.color_picker.SetColour(wx.Colour(0, 0, 0))  # 黑色
        self.watermark_path_ctrl.SetValue("")
        self.font_path_ctrl.SetValue(self.font_file if self.font_file else "系统默认字体")
        self.scale_slider.SetValue(30)
        self.opacity_ctrl.SetValue(70)
        self.position_choice.SetSelection(4)
        self.type_choice.SetSelection(0)
        self.rotation_ctrl.SetValue(0)

        # 禁用按钮
        self.btn_apply.Disable()
        self.btn_save.Disable()
