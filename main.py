# coding: utf-8
__author__ = 'liufei'

import wx
from antiSEM.wxAntiSEM import wxAntiSEM
app = wx.App()
wxAntiSEM().Show()
app.MainLoop()
