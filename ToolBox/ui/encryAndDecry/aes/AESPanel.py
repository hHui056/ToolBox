import wx
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64


class AESPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.key = None
        self.iv = None

        # 创建布局
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 密钥输入区域
        key_box = wx.StaticBox(self, label="AES密钥")
        key_sizer = wx.StaticBoxSizer(key_box, wx.VERTICAL)
        self.key_text = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        key_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.gen_key_btn = wx.Button(self, label="生成新密钥")
        self.save_key_btn = wx.Button(self, label="保存密钥")

        key_btn_sizer.Add(self.gen_key_btn, 0, wx.ALL, 5)
        key_btn_sizer.Add(self.save_key_btn, 0, wx.ALL, 5)
        key_sizer.Add(self.key_text, 0, wx.EXPAND | wx.ALL, 5)
        key_sizer.Add(key_btn_sizer, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 5)

        # 加解密区域
        input_box = wx.StaticBox(self, label="输入")
        input_sizer = wx.StaticBoxSizer(input_box, wx.VERTICAL)
        self.input_text = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(-1, 100))
        input_sizer.Add(self.input_text, 1, wx.EXPAND | wx.ALL, 5)

        # 操作按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.encrypt_btn = wx.Button(self, label="加密")
        self.decrypt_btn = wx.Button(self, label="解密")
        self.clear_btn = wx.Button(self, label="清除")

        btn_sizer.Add(self.encrypt_btn, 1, wx.ALL, 5)
        btn_sizer.Add(self.decrypt_btn, 1, wx.ALL, 5)
        btn_sizer.Add(self.clear_btn, 1, wx.ALL, 5)

        # 输出区域
        output_box = wx.StaticBox(self, label="输出")
        output_sizer = wx.StaticBoxSizer(output_box, wx.VERTICAL)
        self.output_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(-1, 100))
        output_sizer.Add(self.output_text, 1, wx.EXPAND | wx.ALL, 5)

        # 整合所有组件
        main_sizer.Add(key_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(input_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        main_sizer.Add(btn_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        main_sizer.Add(output_sizer, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(main_sizer)

        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.on_generate_key, self.gen_key_btn)
        self.Bind(wx.EVT_BUTTON, self.on_save_key, self.save_key_btn)
        self.Bind(wx.EVT_BUTTON, self.on_encrypt, self.encrypt_btn)
        self.Bind(wx.EVT_BUTTON, self.on_decrypt, self.decrypt_btn)
        self.Bind(wx.EVT_BUTTON, self.on_clear, self.clear_btn)

        # 生成初始密钥
        self.generate_key()

    def generate_key(self):
        """生成随机的AES密钥和初始化向量(IV)"""
        self.key = get_random_bytes(32)  # AES-256
        self.iv = get_random_bytes(16)
        key_display = base64.b64encode(self.key).decode('utf-8')
        self.key_text.SetValue(key_display)

    def on_generate_key(self, event):
        self.generate_key()

    def on_save_key(self, event):
        """保存密钥到文件"""
        with wx.FileDialog(self, "保存密钥", wildcard="文本文件 (*.txt)|*.txt",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            filename = dlg.GetPath()
            try:
                with open(filename, 'w') as f:
                    f.write(base64.b64encode(self.key).decode('utf-8'))
                wx.MessageBox("密钥已保存！", "成功", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"保存失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def is_key_valid(self, key_str):
        """检查密钥格式是否正确"""
        try:
            # 检查是否是base64格式的32字节密钥
            key_bytes = base64.b64decode(key_str)
            return len(key_bytes) == 32
        except:
            return False

    def on_encrypt(self, event):
        """AES加密处理"""
        key_str = self.key_text.GetValue().strip()

        if not self.is_key_valid(key_str):
            wx.MessageBox("密钥格式无效！应为Base64编码的32字节密钥", "错误", wx.OK | wx.ICON_ERROR)
            return

        plaintext = self.input_text.GetValue().strip()
        if not plaintext:
            wx.MessageBox("请输入要加密的文本", "警告", wx.OK | wx.ICON_WARNING)
            return

        try:
            cipher = AES.new(base64.b64decode(key_str), AES.MODE_CBC, self.iv)
            padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
            ciphertext = cipher.encrypt(padded_data)

            # 组合IV和密文，并进行Base64编码
            encrypted_data = self.iv + ciphertext
            result = base64.b64encode(encrypted_data).decode('utf-8')

            self.output_text.SetValue(result)
        except Exception as e:
            wx.MessageBox(f"加密失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def on_decrypt(self, event):
        """AES解密处理"""
        key_str = self.key_text.GetValue().strip()

        if not self.is_key_valid(key_str):
            wx.MessageBox("密钥格式无效！应为Base64编码的32字节密钥", "错误", wx.OK | wx.ICON_ERROR)
            return

        ciphertext = self.input_text.GetValue().strip()
        if not ciphertext:
            wx.MessageBox("请输入要解密的文本", "警告", wx.OK | wx.ICON_WARNING)
            return

        try:
            # 解码Base64数据
            encrypted_data = base64.b64decode(ciphertext)
            iv = encrypted_data[:16]
            ciphertext_bytes = encrypted_data[16:]

            cipher = AES.new(base64.b64decode(key_str), AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(ciphertext_bytes), AES.block_size)

            result = decrypted_data.decode('utf-8')
            self.output_text.SetValue(result)
        except Exception as e:
            wx.MessageBox(f"解密失败: {str(e)}\n请检查密钥和输入数据是否正确", "错误", wx.OK | wx.ICON_ERROR)

    def on_clear(self, event):
        """清除输入输出"""
        self.input_text.SetValue("")
        self.output_text.SetValue("")
