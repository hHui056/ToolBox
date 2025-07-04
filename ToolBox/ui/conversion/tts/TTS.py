from ui.conversion.tts.TTSFileDialog import TTSFileDialog
from ui.conversion.tts.TTSPanel import TTSPanel


class TTS(TTSPanel):
    all_voices = [
        "zh-CN-YunjianNeural",
        "zh-CN-YunjianNeura1",
        "zh-CN-XiaoxiaoNeural",
        "zh-CN-XiaoyiNeural",
        "zh-CN-YunjianNeural",
        "zh-CN-YunjianNeura1"]

    def __init__(self, parent):
        TTSPanel.__init__(self, parent)
        self.init_view()

    def init_view(self):
        for voice in self.all_voices:
            self.voice_choices.Append(voice)

    def list_box_click(self, event):
        print(str(self.voice_choices.GetSelection()))

    def show_tts_dialog(self, event):
        print("show_tts_dialog")
        dlg = TTSFileDialog(None)
        dlg.ShowModal()
