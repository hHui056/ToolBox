import wx
from PIL import Image
import os
import io
import math


class ImageToIconConverterPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # 初始化变量
        self.image_path = ""
        self.icon_sizes = [16, 24, 32, 48, 64, 128, 256]
        self.selected_sizes = [32, 48]  # 默认选中的尺寸

        # 创建UI
        self.init_ui()
        self.SetMinSize((700, 500))

    def init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 标题
        title = wx.StaticText(self, label="图片转ICO工具", style=wx.ALIGN_CENTER)
        title_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)

        # 控制面板
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 按钮区域
        btn_open = wx.Button(self, label="选择图片")
        btn_open.Bind(wx.EVT_BUTTON, self.on_open_image)

        self.btn_convert = wx.Button(self, label="转换为ICO")
        self.btn_convert.Bind(wx.EVT_BUTTON, self.on_convert)
        self.btn_convert.Disable()

        self.btn_save = wx.Button(self, label="保存ICO")
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        self.btn_save.Disable()

        btn_clear = wx.Button(self, label="清空")
        btn_clear.Bind(wx.EVT_BUTTON, self.on_clear)

        # 添加到控制面板
        control_sizer.Add(btn_open, 0, wx.ALL | wx.EXPAND, 5)
        control_sizer.Add(self.btn_convert, 0, wx.ALL | wx.EXPAND, 5)
        control_sizer.Add(self.btn_save, 0, wx.ALL | wx.EXPAND, 5)
        control_sizer.Add(btn_clear, 0, wx.ALL | wx.EXPAND, 5)

        # 尺寸选择
        size_box = wx.StaticBox(self, label="选择ICO尺寸 (可多选)")
        size_sizer = wx.StaticBoxSizer(size_box, wx.HORIZONTAL)

        self.size_controls = {}
        for size in self.icon_sizes:
            cb = wx.CheckBox(self, label=f"{size}x{size}")
            cb.SetValue(size in self.selected_sizes)
            cb.Bind(wx.EVT_CHECKBOX, self.on_size_change)
            self.size_controls[size] = cb
            size_sizer.Add(cb, 0, wx.ALL, 5)

        # 图片显示区域
        img_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 左侧面板 - 原始图片
        left_panel = wx.Panel(self)
        left_box = wx.StaticBox(left_panel, label="原始图片")
        left_sizer = wx.StaticBoxSizer(left_box, wx.VERTICAL)

        self.lbl_image_path = wx.StaticText(left_panel, label="未选择图片", style=wx.ALIGN_LEFT)
        self.lbl_image_path.Wrap(350)  # 允许换行

        # 创建空位图
        empty_bitmap = self.create_empty_bitmap(300, 300)

        self.image_display = wx.StaticBitmap(left_panel, bitmap=empty_bitmap)
        self.lbl_image_info = wx.StaticText(left_panel, label="等待选择图片", style=wx.ALIGN_CENTER)

        left_sizer.Add(self.lbl_image_path, 0, wx.ALL | wx.EXPAND, 5)
        left_sizer.Add(self.image_display, 1, wx.EXPAND | wx.ALL, 5)
        left_sizer.Add(self.lbl_image_info, 0, wx.EXPAND | wx.ALL, 5)

        left_panel.SetSizer(left_sizer)

        # 右侧面板 - ICO预览
        right_panel = wx.Panel(self)
        right_box = wx.StaticBox(right_panel, label="ICO预览")
        right_sizer = wx.StaticBoxSizer(right_box, wx.VERTICAL)

        self.icon_display = wx.StaticBitmap(right_panel, bitmap=empty_bitmap)
        self.lbl_icon_info = wx.StaticText(right_panel, label="等待转换ICO", style=wx.ALIGN_CENTER)

        # 添加尺寸预览
        self.size_preview_panel = wx.Panel(right_panel)
        self.size_preview_sizer = wx.FlexGridSizer(cols=4, hgap=5, vgap=5)

        self.size_preview_panel.SetSizer(self.size_preview_sizer)

        right_sizer.Add(self.icon_display, 1, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(self.size_preview_panel, 0, wx.ALL | wx.EXPAND, 5)
        right_sizer.Add(self.lbl_icon_info, 0, wx.EXPAND | wx.ALL, 5)

        right_panel.SetSizer(right_sizer)

        # 添加到主布局
        img_sizer.Add(left_panel, 1, wx.EXPAND | wx.ALL, 5)
        img_sizer.Add(right_panel, 1, wx.EXPAND | wx.ALL, 5)

        # 将所有控件添加到主sizer
        main_sizer.Add(title, 0, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(control_sizer, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(size_sizer, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(img_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)

        # 保存空位图用于重置
        self.empty_bitmap = empty_bitmap
        self.icon_bitmap = None
        self.icon_data = None

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
            width, height = img.size
            file_size = os.path.getsize(self.image_path)
            size_kb = file_size / 1024

            # 显示图片信息
            self.lbl_image_path.SetLabel(self.image_path)
            self.lbl_image_info.SetLabel(f"尺寸: {width}×{height} | 大小: {size_kb:.1f}KB")

            # 显示图片
            wx_img = self.pil_to_wx_image(img)
            display_size = self.image_display.GetSize()

            # 确保尺寸是整数
            scaled_width = int(display_size[0] * 0.95)
            scaled_height = int(display_size[1] * 0.95)

            # 缩放图片
            wx_img = self.scale_image(wx_img, scaled_width, scaled_height)
            self.image_display.SetBitmap(wx.Bitmap(wx_img))

            # 启用转换按钮
            self.btn_convert.Enable()

            # 清空右侧预览
            self.icon_display.SetBitmap(self.empty_bitmap)
            self.lbl_icon_info.SetLabel("等待转换ICO")

            # 清除之前的尺寸预览
            self.clear_size_previews()

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
        scale = min(ratio_width, ratio_height)

        # 应用缩放，确保结果为整数
        new_w = int(w * scale)
        new_h = int(h * scale)

        # 确保尺寸至少为1
        new_w = max(new_w, 1)
        new_h = max(new_h, 1)

        return img.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)

    def on_size_change(self, event):
        """更新选中的尺寸"""
        self.selected_sizes = []
        for size, cb in self.size_controls.items():
            if cb.GetValue():
                self.selected_sizes.append(size)

        # 排序
        self.selected_sizes.sort()

    def on_convert(self, event):
        if not self.image_path or not self.selected_sizes:
            return

        try:
            # 加载图像并转换为ICO
            img = Image.open(self.image_path)

            # 创建图像列表（包含所有选定尺寸）
            images = []
            for size in self.selected_sizes:
                # 处理透明通道
                if img.mode != 'RGBA':
                    img_with_alpha = img.convert("RGBA")
                else:
                    img_with_alpha = img.copy()

                # 创建正方形的缩略图
                resized_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))

                # 计算缩放比例并调整位置
                ratio = min(size / img.width, size / img.height)
                new_width = int(img.width * ratio)
                new_height = int(img.height * ratio)

                resized_original = img_with_alpha.resize((new_width, new_height), Image.LANCZOS)

                # 居中放置图片
                x = (size - new_width) // 2
                y = (size - new_height) // 2

                resized_img.paste(resized_original, (x, y), resized_original)
                images.append(resized_img)

            # 保存到字节流
            with io.BytesIO() as output:
                images[0].save(output, format="ICO", sizes=[(size, size) for size in self.selected_sizes])
                self.icon_data = output.getvalue()

            # 显示最大尺寸的预览
            max_size = max(self.selected_sizes)
            preview_img = next(img for img in images if img.width == max_size)
            wx_img = self.pil_to_wx_image(preview_img)

            # 获取显示区域尺寸
            display_size = self.icon_display.GetSize()

            # 确保尺寸是整数
            scaled_width = int(display_size[0] * 0.9)
            scaled_height = int(display_size[1] * 0.9)

            # 缩放预览图
            scaled_img = self.scale_image(wx_img, scaled_width, scaled_height)

            # 显示预览
            self.icon_display.SetBitmap(wx.Bitmap(scaled_img))

            # 计算ICO大小
            icon_size = len(self.icon_data) / 1024
            self.lbl_icon_info.SetLabel(
                f"ICO大小: {icon_size:.2f}KB | 包含尺寸: {', '.join(map(str, self.selected_sizes))}")

            # 显示尺寸预览
            self.create_size_previews(images)

            # 启用保存按钮
            self.btn_save.Enable()

            self.Layout()
        except Exception as e:
            import traceback
            traceback.print_exc()
            wx.MessageBox(f"转换失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def create_size_previews(self, images):
        """创建不同尺寸的预览图"""
        self.clear_size_previews()

        # 添加尺寸标题
        lbl_title = wx.StaticText(self.size_preview_panel, label="尺寸预览:")
        self.size_preview_sizer.Add(lbl_title, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # 添加每个尺寸的预览
        for img in images:
            size = img.width
            wx_img = self.pil_to_wx_image(img)

            # 创建面板包含预览和标签
            preview_panel = wx.Panel(self.size_preview_panel)
            sizer = wx.BoxSizer(wx.VERTICAL)

            # 创建预览位图
            preview_bitmap = wx.StaticBitmap(preview_panel, bitmap=wx.Bitmap(wx_img.Scale(32, 32)))

            # 添加尺寸标签
            lbl_size = wx.StaticText(preview_panel, label=f"{size}x{size}")

            sizer.Add(preview_bitmap, 0, wx.ALL | wx.CENTER, 2)
            sizer.Add(lbl_size, 0, wx.ALL | wx.CENTER, 2)

            preview_panel.SetSizer(sizer)
            self.size_preview_sizer.Add(preview_panel, 0, wx.ALL | wx.CENTER, 5)

        self.size_preview_panel.Layout()
        self.size_preview_panel.GetParent().Layout()

    def clear_size_previews(self):
        """清除之前的尺寸预览"""
        for child in self.size_preview_panel.GetChildren():
            child.Destroy()

        self.size_preview_sizer = wx.FlexGridSizer(cols=4, hgap=5, vgap=5)
        self.size_preview_panel.SetSizer(self.size_preview_sizer)

    def on_save(self, event):
        if not self.icon_data:
            return

        default_filename = "icon.ico"
        if self.image_path:
            base = os.path.basename(self.image_path)
            name = os.path.splitext(base)[0]
            default_filename = f"{name}.ico"

        with wx.FileDialog(
                self, "保存ICO文件",
                defaultFile=default_filename,
                wildcard="ICO文件 (*.ico)|*.ico",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                save_path = dlg.GetPath()

                # 确保扩展名正确
                if not save_path.lower().endswith('.ico'):
                    save_path += '.ico'

                try:
                    # 保存ICO文件
                    with open(save_path, 'wb') as f:
                        f.write(self.icon_data)

                    # 显示成功消息
                    wx.MessageBox(f"ICO文件已保存到:\n{save_path}", "保存成功", wx.OK | wx.ICON_INFORMATION)
                except Exception as e:
                    wx.MessageBox(f"保存失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def on_clear(self, event):
        """清空所有内容"""
        # 重置变量
        self.image_path = ""
        self.icon_data = None

        # 重置UI状态
        self.lbl_image_path.SetLabel("未选择图片")
        self.lbl_image_info.SetLabel("等待选择图片")
        self.image_display.SetBitmap(self.empty_bitmap)

        self.icon_display.SetBitmap(self.empty_bitmap)
        self.lbl_icon_info.SetLabel("等待转换ICO")

        # 清除尺寸预览
        self.clear_size_previews()

        # 取消选中所有尺寸
        for size in self.size_controls.values():
            size.SetValue(False)

        # 重置选中的尺寸（保留默认值）
        self.selected_sizes = [32, 48]
        self.size_controls[32].SetValue(True)
        self.size_controls[48].SetValue(True)

        # 禁用按钮
        self.btn_convert.Disable()
        self.btn_save.Disable()
