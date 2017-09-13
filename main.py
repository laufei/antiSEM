# coding: utf-8
__author__ = 'liufei'

import wx
from antiSEM.wxAntiSEM import wxAntiSEM

if __name__ == "__main__":
    app = wx.App()
    wxAntiSEM()
    app.MainLoop()
