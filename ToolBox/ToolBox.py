import wx
from loguru import logger
from Home import Home

if __name__ == '__main__':
    logger.add("./log/log.txt", rotation="00:00")
    app = wx.App(False)
    frame = Home(None)
    frame.Show(True)
    app.MainLoop()
