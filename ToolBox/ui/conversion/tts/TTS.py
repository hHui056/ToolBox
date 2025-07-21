import os.path
import time
import wx

from ui.conversion.tts.TTSFileDialog import TTSFileDialog
from ui.conversion.tts.TTSPanel import TTSPanel
import asyncio
import edge_tts


class TTS(TTSPanel):
    all_voices = []
    selected_voice = ''

    def __init__(self, parent):
        TTSPanel.__init__(self, parent)
        self.init_view()

    def init_view(self):
        asyncio.run(self.get_voice())

    def list_box_click(self, event):
        self.selected_voice = self.all_voices[self.voice_choices.GetSelection()]
        print(self.selected_voice)

    def show_tts_dialog(self, event):
        print(f'{self.selected_voice}')

    # dlg = TTSFileDialog(None)
    # dlg.ShowModal()

    async def get_voice(self):
        try:
            voices = await edge_tts.list_voices()
            self.all_voices = [voice for voice in voices if voice['ShortName'].startswith('zh-CN')]
            # self.all_voices = [voice['ShortName'].replace('zh-CN-', '', 1).replace('Neural', '', 1) for voice in
            #                    enabled_voices]
            for voice in self.all_voices:
                self.voice_choices.Append(
                    f'{voice["ShortName"].replace("zh-CN-", "", 1).replace("Neural", "", 1)} - {'男' if voice['Gender'] == 'Male' else '女'}')
        except Exception as e:
            print(e)

    def __show_message(self, message):
        wx.MessageDialog(self, message, '提示', wx.OK).ShowModal()

    def start_tts(self, event):
        asyncio.run(self.make_voice())

    async def make_voice(self):
        content = self.tts_content.GetValue().strip()
        if content == "":
            self.__show_message('请输入要转换的文本')
            return
        if self.selected_voice == '':
            self.__show_message('请选择音色')
            return
        dlg = wx.DirDialog(None, "选择保存目录", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            download_path = dlg.GetPath()
            dlg.Destroy()
            communicate = edge_tts.Communicate(content, self.selected_voice['ShortName'])
            file_path = f'{download_path}\\{int(time.time())}.mp3'
            progress_dialog = wx.ProgressDialog(
                "语音合成中",
                "正在处理，请稍候...",
                parent=None,
                style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_SMOOTH
            )
            await communicate.save(file_path)
            self.__show_message(f'文件保存成功，路径为：{file_path}')
        else:
            dlg.Destroy()
            self.__show_message('请选择保存目录')
            return
