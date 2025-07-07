from ui.encryAndDecry.hash.HashPanel import HashPanel
import hashlib
import wx
from typing import Dict
import time
import os
import pyperclip


class Hash(HashPanel):
    select_type = 0

    def __init__(self, parent):
        HashPanel.__init__(self, parent)
        self.__init_view()

    def __init_view(self):
        self.edit_file_path.Hide()
        self.choice_file_btn.Hide()

    def on_text_change(self, event):
        if self.select_type == 1:
            return
        text = self.edit_content.GetValue()
        if text == '':
            self.reset_result()
            return
        self.md5_result.SetValue(hashlib.md5(text.encode()).hexdigest())
        self.sha1_result.SetValue(hashlib.sha1(text.encode()).hexdigest())
        self.sha256_result.SetValue(hashlib.sha256(text.encode()).hexdigest())
        self.sha512_result.SetValue(hashlib.sha512(text.encode()).hexdigest())

    def clear_input(self, event):
        self.edit_content.SetValue('')
        self.reset_result()

    def on_choice_type(self, event):
        position = self.input_type_choice.GetSelection()
        if position == 0:
            self.edit_content.Show()
            self.edit_file_path.Hide()
            self.choice_file_btn.Hide()
        elif position == 1:
            self.edit_content.Hide()
            self.edit_file_path.Show()
            self.choice_file_btn.Show()
        if self.select_type != position:
            self.reset_result()
        self.select_type = position

    def show_choice_file_dialog(self, event):
        with wx.FileDialog(self, "选择文件", wildcard="*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            self.edit_file_path.SetValue(pathname)
            result = self.calculate_file_hashes(pathname)
            self.md5_result.SetValue(result['md5'])
            self.sha1_result.SetValue(result['sha1'])
            self.sha256_result.SetValue(result['sha256'])
            self.sha512_result.SetValue(result['sha512'])

    def copy_md5(self, event):
        if self.md5_result.GetValue() == '-':
            return
        pyperclip.copy(self.md5_result.GetValue())
        self.__show_message('MD5值复制成功')

    def copy_sha1(self, event):
        if self.sha1_result.GetValue() == '-':
            return
        pyperclip.copy(self.sha1_result.GetValue())
        self.__show_message('SHA1值复制成功')

    def copy_sha256(self, event):
        if self.sha256_result.GetValue() == '-':
            return
        pyperclip.copy(self.sha256_result.GetValue())
        self.__show_message('SHA256值复制成功')

    def copy_sha512(self, event):
        if self.sha512_result.GetValue() == '-':
            return
        pyperclip.copy(self.sha512_result.GetValue())
        self.__show_message('SHA512值复制成功')

    def calculate_file_hashes(self, file_path: str) -> Dict[str, str]:
        """
        计算文件的多种哈希值

        :param file_path: 文件路径
        :return: 包含各种哈希值的字典 (md5, sha1, sha256, sha512)
        """
        # 初始化哈希对象
        hash_md5 = hashlib.md5()
        hash_sha1 = hashlib.sha1()
        hash_sha256 = hashlib.sha256()
        hash_sha512 = hashlib.sha512()

        # 获取文件大小（用于进度显示）
        file_size = os.path.getsize(file_path)

        try:
            # 以二进制模式打开文件
            with open(file_path, 'rb') as f:
                print(f"计算 {os.path.basename(file_path)} 的哈希值 ({file_size / 1024 / 1024:.2f} MB)...")

                # 设置读取块大小 (1MB)
                chunk_size = 1024 * 1024
                bytes_read = 0
                start_time = time.time()

                # 逐块读取文件并更新哈希值
                while chunk := f.read(chunk_size):
                    # 更新所有哈希算法
                    hash_md5.update(chunk)
                    hash_sha1.update(chunk)
                    hash_sha256.update(chunk)
                    hash_sha512.update(chunk)

                    # 更新进度
                    bytes_read += len(chunk)

                    # 每5%进度显示一次（避免频繁更新）
                    if bytes_read % (file_size // 20) == 0 or bytes_read == file_size:
                        elapsed = time.time() - start_time
                        speed = bytes_read / (1024 * 1024 * elapsed) if elapsed > 0 else 0
                        percent = bytes_read / file_size * 100
                        print(f"\r进度: {percent:.1f}% - {speed:.1f} MB/s", end="")

                print("\n计算完成!")

        except FileNotFoundError:
            raise FileNotFoundError(f"文件未找到: {file_path}")
        except PermissionError:
            raise PermissionError(f"无权限访问文件: {file_path}")
        except Exception as e:
            raise RuntimeError(f"计算哈希值时出错: {str(e)}")

        # 返回计算结果
        return {
            'md5': hash_md5.hexdigest(),
            'sha1': hash_sha1.hexdigest(),
            'sha256': hash_sha256.hexdigest(),
            'sha512': hash_sha512.hexdigest(),
            'file_size': file_size
        }

    def reset_result(self):
        self.md5_result.SetValue('-')
        self.sha1_result.SetValue('-')
        self.sha256_result.SetValue('-')
        self.sha512_result.SetValue('-')
        self.edit_file_path.SetValue('')

    def __show_message(self, message):
        wx.MessageDialog(self, message, '提示', wx.OK).ShowModal()
