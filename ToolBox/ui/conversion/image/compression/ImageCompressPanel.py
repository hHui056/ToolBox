import wx
import os
import math
from PIL import Image
import io
import wx.lib.agw.genericmessagedialog as gmd
from wx.lib.agw.floatspin import FloatSpin


class ImageCompressorPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # 初始化变量
        self.original_path = ""
        self.compressed_path = ""

        # 创建UI
        self.init_ui()

    def init_ui(self):
        # 创建主布局
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 控制面板
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 添加按钮
        btn_open = wx.Button(self, label="选择图片")
        btn_open.Bind(wx.EVT_BUTTON, self.on_open_image)

        btn_compress = wx.Button(self, label="压缩图片")
        btn_compress.Bind(wx.EVT_BUTTON, self.on_compress)

        btn_save = wx.Button(self, label="保存图片")
        btn_save.Bind(wx.EVT_BUTTON, self.on_save)

        # 增加清空按钮
        btn_clear = wx.Button(self, label="清空")
        btn_clear.Bind(wx.EVT_BUTTON, self.on_clear)

        # 参数控件
        self.spn_quality = FloatSpin(self, value=80, min_val=1, max_val=100, increment=1)

        self.spn_max_width = wx.SpinCtrl(self, value="1200", min=100, max=10000)

        # 添加到控制面板
        control_sizer.Add(btn_open, 0, wx.ALL | wx.EXPAND, 5)
        control_sizer.Add(btn_compress, 0, wx.ALL | wx.EXPAND, 5)
        control_sizer.Add(btn_save, 0, wx.ALL | wx.EXPAND, 5)
        control_sizer.Add(btn_clear, 0, wx.ALL | wx.EXPAND, 5)
        control_sizer.AddStretchSpacer()
        control_sizer.Add(wx.StaticText(self, label="质量:"), 0, wx.ALIGN_CENTER | wx.ALL, 5)
        control_sizer.Add(self.spn_quality, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        control_sizer.Add(wx.StaticText(self, label="最大宽度:"), 0, wx.ALIGN_CENTER | wx.ALL, 5)
        control_sizer.Add(self.spn_max_width, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        # 图片显示区域
        img_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 创建空位图
        empty_bitmap = wx.Bitmap(600, 400)
        dc = wx.MemoryDC()
        dc.SelectObject(empty_bitmap)
        dc.SetBackground(wx.Brush(wx.Colour(240, 240, 240)))
        dc.Clear()
        dc.SelectObject(wx.NullBitmap)

        # 原始图片面板
        original_panel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        original_panel.SetBackgroundColour(wx.Colour(240, 240, 240))
        original_box = wx.StaticBox(original_panel, label="原始图片")
        original_sizer = wx.StaticBoxSizer(original_box, wx.VERTICAL)

        self.original_img = wx.StaticBitmap(original_panel, bitmap=empty_bitmap)
        self.lbl_original = wx.StaticText(original_panel, label="未选择图片", style=wx.ALIGN_CENTER)

        original_sizer.Add(self.original_img, 1, wx.EXPAND | wx.ALL, 5)
        original_sizer.Add(self.lbl_original, 0, wx.EXPAND | wx.ALL, 5)
        original_panel.SetSizer(original_sizer)

        # 压缩后图片面板
        compressed_panel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        compressed_panel.SetBackgroundColour(wx.Colour(240, 240, 240))
        compressed_box = wx.StaticBox(compressed_panel, label="压缩后图片")
        compressed_sizer = wx.StaticBoxSizer(compressed_box, wx.VERTICAL)

        self.compressed_img = wx.StaticBitmap(compressed_panel, bitmap=empty_bitmap)
        self.lbl_compressed = wx.StaticText(compressed_panel, label="等待压缩", style=wx.ALIGN_CENTER)

        compressed_sizer.Add(self.compressed_img, 1, wx.EXPAND | wx.ALL, 5)
        compressed_sizer.Add(self.lbl_compressed, 0, wx.EXPAND | wx.ALL, 5)
        compressed_panel.SetSizer(compressed_sizer)

        # 添加图片面板到布局
        img_sizer.Add(original_panel, 1, wx.EXPAND | wx.ALL, 5)
        img_sizer.Add(compressed_panel, 1, wx.EXPAND | wx.ALL, 5)

        # 添加所有控件到主布局
        main_sizer.Add(control_sizer, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(img_sizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(main_sizer)

        # 设置最小尺寸
        self.SetMinSize((800, 500))

        # 保存空位图用于重置
        self.empty_bitmap = empty_bitmap

    def on_open_image(self, event):
        with wx.FileDialog(self, "选择图片",
                           wildcard="图片文件 (*.jpg;*.png;*.jpeg;*.bmp)|*.jpg;*.png;*.jpeg;*.bmp") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.original_path = dlg.GetPath()
                self.load_original_image()

    def load_original_image(self):
        try:
            # 获取文件大小
            size_bytes = os.path.getsize(self.original_path)
            size_kb = size_bytes / 1024

            # 获取图片尺寸
            img = Image.open(self.original_path)
            width, height = img.size

            size_str = f"原始: {size_kb:.1f} KB | 尺寸: {width}×{height}"

            # 显示图片信息
            self.lbl_original.SetLabel(f"{os.path.basename(self.original_path)}\n{size_str}")

            # 显示图片
            wx_img = wx.Image(self.original_path, wx.BITMAP_TYPE_ANY)
            wx_img = self.scale_image(wx_img, self.original_img.GetSize())
            self.original_img.SetBitmap(wx.Bitmap(wx_img))

            # 重置压缩状态
            self.compressed_img.SetBitmap(self.empty_bitmap)
            self.lbl_compressed.SetLabel("等待压缩")

            self.Layout()
        except Exception as e:
            self.show_message(f"加载图片错误: {str(e)}", "错误")

    def on_compress(self, event):
        if not self.original_path:
            self.show_message("请先选择图片!", "错误")
            return

        # 获取压缩参数
        quality = int(self.spn_quality.GetValue())
        max_width = self.spn_max_width.GetValue()

        try:
            # 压缩图片
            original_size = os.path.getsize(self.original_path)
            compressed_path = self.compress_image(self.original_path, quality, max_width)

            if compressed_path:
                self.compressed_path = compressed_path

                # 获取压缩后图片尺寸
                img = Image.open(compressed_path)
                width, height = img.size

                # 显示压缩后的图片
                wx_img = wx.Image(compressed_path, wx.BITMAP_TYPE_ANY)
                wx_img = self.scale_image(wx_img, self.compressed_img.GetSize())
                self.compressed_img.SetBitmap(wx.Bitmap(wx_img))

                # 显示大小信息
                compressed_size = os.path.getsize(compressed_path)
                compression_rate = 100 * (1 - compressed_size / original_size)
                size_kb = compressed_size / 1024

                self.lbl_compressed.SetLabel(
                    f"压缩后: {size_kb:.1f} KB | 尺寸: {width}×{height}\n"
                    f"压缩率: {compression_rate:.1f}% | 质量: {quality}% | 宽度: {max_width}px"
                )

                self.Layout()
        except Exception as e:
            self.show_message(f"压缩错误: {str(e)}", "错误")

    def compress_image(self, input_path, quality=80, max_width=1200):
        # 打开原始图片
        img = Image.open(input_path)
        original_width, original_height = img.size

        # 计算新尺寸
        if max_width and original_width > max_width:
            ratio = max_width / original_width
            new_height = int(original_height * ratio)
            img = img.resize((max_width, new_height), Image.LANCZOS)

        # 创建压缩后文件路径
        base_name, ext = os.path.splitext(os.path.basename(input_path))
        output_dir = wx.StandardPaths.Get().GetTempDir()
        output_path = os.path.join(output_dir, f"{base_name}_compressed{ext.lower()}")

        # 保存压缩后的图片
        img.save(output_path, quality=quality, optimize=True)

        return output_path

    def on_save(self, event):
        if not self.compressed_path:
            self.show_message("请先压缩图片!", "警告")
            return

        # 获取原始文件名并添加"_compressed"后缀
        original_filename = os.path.basename(self.original_path)
        name, ext = os.path.splitext(original_filename)
        default_filename = f"{name}_compressed{ext}"

        with wx.FileDialog(
                self, "保存压缩后的图片",
                defaultFile=default_filename,
                wildcard="JPG 图片 (*.jpg)|*.jpg|PNG 图片 (*.png)|*.png|BMP 图片 (*.bmp)|*.bmp",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                save_path = dlg.GetPath()

                try:
                    # 确保文件扩展名
                    if not os.path.splitext(save_path)[1]:
                        format = dlg.GetFilterIndex()
                        if format == 0:  # JPG
                            save_path += ".jpg"
                        elif format == 1:  # PNG
                            save_path += ".png"
                        else:  # BMP
                            save_path += ".bmp"

                    # 保存文件
                    img = Image.open(self.compressed_path)
                    img.save(save_path)

                    # 显示成功消息
                    wx.MessageBox(f"图片已成功保存到:\n{save_path}", "保存成功", wx.OK | wx.ICON_INFORMATION)
                except Exception as e:
                    wx.MessageBox(f"保存失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def on_clear(self, event):
        """清空所有图片和状态"""
        # 重置变量
        self.original_path = ""
        self.compressed_path = ""

        # 清空图片显示
        self.original_img.SetBitmap(self.empty_bitmap)
        self.compressed_img.SetBitmap(self.empty_bitmap)

        # 重置标签
        self.lbl_original.SetLabel("未选择图片")
        self.lbl_compressed.SetLabel("等待压缩")

        # 提示用户
        wx.MessageBox("已清空所有图片", "清空完成", wx.OK | wx.ICON_INFORMATION)

    def scale_image(self, img, target_size):
        """缩放图片以适应容器"""
        if not img.IsOk():
            return img

        # 计算缩放比例
        w, h = img.GetSize()
        target_w, target_h = target_size

        if w == 0 or h == 0:
            return img

        scale_w = target_w / w
        scale_h = target_h / h
        scale = min(scale_w, scale_h) * 0.9  # 留出一些空白

        # 应用缩放
        new_w = int(w * scale)
        new_h = int(h * scale)

        # 确保不会太小
        new_w = max(new_w, 100)
        new_h = max(new_h, 100)

        return img.Scale(new_w, new_h, wx.IMAGE_QUALITY_HIGH)

    def show_message(self, message, title):
        """显示消息对话框"""
        dlg = wx.MessageDialog(self, message, title, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


# 测试代码 - 可嵌入其他应用
if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, title="图片压缩工具", size=(1000, 600))

    # 创建我们的面板
    panel = ImageCompressorPanel(frame)

    # 设置图标
    if os.path.exists("icon.png"):
        frame.SetIcon(wx.Icon("icon.png", wx.BITMAP_TYPE_PNG))

    # 设置状态栏
    status_bar = frame.CreateStatusBar(2)
    status_bar.SetStatusWidths([-1, 150])
    status_bar.SetStatusText("就绪", 0)

    # 布局
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(panel, 1, wx.EXPAND)
    frame.SetSizer(sizer)

    frame.Centre()
    frame.Show()
    app.MainLoop()
