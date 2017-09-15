# coding: utf-8
__author__ = 'liufei'

import os, time, datetime
import platform
import wx, wx.html
from wx.lib.pubsub import pub
from element.page import page
from data.data import data
from antiSEM import antiSEM

class wxAntiSEM(wx.Frame, page):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, title=u'反SEM刷点击小工具 v1.0', size=(935, 700), style=wx.MAXIMIZE_BOX|wx.CLOSE_BOX)
        self.data = data()
        self.task, self.urlkw, self.proxyType, self.proxyConfig, self.antiSEMobj = "", "", "", "", None
        self.proValue, self.spend = 0, 0
        self.note = self.data.note
        self.threadNote = self.data.threadNote
        # self.font = wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False)
        self.update()
        self.Bind(wx.EVT_CLOSE, self.OnClickStop)
        # 添加drivers到环境变量
        if platform.system() == "Darwin":
            self.dir = os.environ["HOME"]+os.sep+"drivers"+os.sep
            self.gdname = "geckodriver-v0.15.0-macos.tar.gz"
        elif platform.system() == "Windows":
            self.dir = os.environ["USERPROFILE"]+os.sep+"drivers"+os.sep
            self.gdname = "geckodriver-v0.15.0-win64.zip"
        os.environ["PATH"] += ':' + self.dir

        self.controllers()
        self.ui_design()

    def controllers(self):
        # 创建定时器
        self.beginTime = 0
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        # 运行log
        self.om = wx.StaticBox(self, -1, u"▼ 运行日志:")
        self.multiText = wx.TextCtrl(self, 0, value=self.note, size=(320, 248), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.multiText.SetInsertionPoint(0)
        self.multiText.SetBackgroundColour('#FFF0AC')
        self.om1 = wx.StaticBox(self, -1, u"▼ Thread - 1:")
        self.multiText1 = wx.TextCtrl(self, -1, value=self.threadNote, size=(320, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.multiText1.SetInsertionPoint(0)
        self.multiText1.SetBackgroundColour('#FFB090')
        self.om2 = wx.StaticBox(self, -1, u"▼ Thread - 2:")
        self.multiText2 = wx.TextCtrl(self, -1, value=self.threadNote, size=(320, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.multiText2.SetInsertionPoint(0)
        self.multiText2.SetBackgroundColour('#FFB090')
        self.om3 = wx.StaticBox(self, -1, u"▼ Thread - 3:")
        self.multiText3 = wx.TextCtrl(self, -1, value=self.threadNote, size=(320, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.multiText3.SetInsertionPoint(0)
        self.multiText3.SetBackgroundColour('#FFB090')
        self.om4 = wx.StaticBox(self, -1, u"▼ Thread - 4:")
        self.multiText4 = wx.TextCtrl(self, -1, value=self.threadNote, size=(320, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.multiText4.SetInsertionPoint(0)
        self.multiText4.SetBackgroundColour('#FFB090')
        self.om5 = wx.StaticBox(self, -1, u"▼ Thread - 5:")
        self.multiText5 = wx.TextCtrl(self, -1, value=self.threadNote, size=(320, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.multiText5.SetInsertionPoint(0)
        self.multiText5.SetBackgroundColour('#FFB090')
        self.om6 = wx.StaticBox(self, -1, u"▼ Thread - 6:")
        self.multiText6 = wx.TextCtrl(self, -1, value=self.threadNote, size=(320, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.multiText6.SetInsertionPoint(0)
        self.multiText6.SetBackgroundColour('#FFB090')

        # 选择搜索引擎: baidu, sm, sogou
        self.sm = wx.StaticBox(self, -1, u"▼ 搜索平台:")
        spfList = ["Baidu", "SM", "Sogou"]
        self.rb_splatform = wx.RadioBox(self, -1, "", wx.DefaultPosition, (140, 100), spfList, 3, wx.SL_VERTICAL)
        # 选择平台：web，h5
        self.dm = wx.StaticBox(self, -1, u"▼ 运行平台:")
        pfList = ["Web", "H5"]
        self.rb_platform = wx.RadioBox(self, -1, "", wx.DefaultPosition, (140, 60), pfList, 2, wx.SL_HORIZONTAL)
        # 是否使用模拟浏览器
        self.cb_isPhantomjs = wx.CheckBox(self, -1, u"模拟浏览器?", wx.DefaultPosition, (120, 30))

        self.fm = wx.StaticBox(self, -1, u"▼ 搜索关键词文件路径:")
        self.kwText = wx.TextCtrl(self, -1, value=u"点击右侧按钮选择文件...", size=(250, 21), style=wx.TE_READONLY)
        # self.kwText.SetFont(self.font)
        self.kwBtn = wx.Button(self, label='...', size=(30, 21))
        self.Bind(wx.EVT_BUTTON, self.OnOpenKWFile, self.kwBtn)
        self.tmpBtn = wx.Button(self, label='+', size=(30, 21))
        self.Bind(wx.EVT_BUTTON, self.OnCreateTmpFile, self.tmpBtn)
        # 关键词运行次数
        self.rm = wx.StaticBox(self, -1, u"▼ 运行次数:")
        self.runTime = wx.CheckBox(self, -1, u"是否统一配置?  输入运行次数:")
        self.runText = wx.TextCtrl(self, -1, size=(105, 21))
        self.runText.SetEditable(False)
        self.runText.SetValue("100")
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox_RT, self.runTime)
        # 选择代理方式：Local, api，txt
        self.pm = wx.StaticBox(self, -1, u"▼ 代理方式:")
        sampleList = ["API", "Local", "TXT"]
        self.rb_proxy = wx.RadioBox(self, -1, "", wx.DefaultPosition, (200, 45), sampleList, 3)
        self.proxyType = self.rb_proxy.GetItemLabel(self.rb_proxy.GetSelection())
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox_Proxy, self.rb_proxy)
        self.proxyTextBtn = wx.Button(self, label='...', size=(30, 21))
        self.proxyTextBtn.Hide()
        self.Bind(wx.EVT_BUTTON, self.OnOpenProxyFile, self.proxyTextBtn)
        # 代理DNS，API, TXT配置输入框
        self.proxyText = wx.TextCtrl(self, -1, value=self.data.proxy_api, size=(200, 21))
        # self.proxyText.SetFont(self.font)
        # 代理数量显示
        self.apiCount, self.dnsCount = 0, 0
        try:
            self.apiCount = self.getProxyCount("API", self.data.proxy_api)
        except:
            self.errInfo(u'API代理方式下: 并没有获取到代理数量. ', True)
        try:
            self.dnsCount = self.getProxyCount("Local", self.data.proxy_dns)
        except:
            self.errInfo(u'Local代理方式下: 并没有获取到代理数量. ', True)

        self.proxyCount = wx.StaticText(self, -1, label=" |%d" % self.apiCount, size=(100, 21))
        # 版权模块
        self.copyRight = wx.StaticText(self, -1, u"© LiuFei      mail: goodlf@qq.com", style=1)
        self.spendTime = wx.StaticText(self, -1, u"▶ 耗时: 00:00:00  ")
        self.curThread = wx.StaticText(self, -1, u"▶ 当前进程ID: None  ")
        self.succTime = wx.StaticText(self, -1, u"▶ 成功次数: 0  ")
        self.succRatio = wx.StaticText(self, -1, u"▶ 成功率: 0.0  ")
        self.proText = wx.StaticText(self, -1, u"▶ 进度:")
        self.process = wx.Gauge(self, -1, size=(150, 20), style=wx.GA_HORIZONTAL)
        self.Bind(wx.EVT_IDLE, self.Onprocess)
        # 运行按钮
        self.buttonRun = wx.Button(self, label=u"运行")
        self.Bind(wx.EVT_BUTTON, self.OnClickRun, self.buttonRun)
        # 终止按钮
        self.buttonStop = wx.Button(self, label=u"关闭")
        self.Bind(wx.EVT_BUTTON, self.OnClickStop, self.buttonStop)

    def ui_design(self):
        mbox = wx.BoxSizer(wx.VERTICAL)
        vbox = wx.BoxSizer(wx.HORIZONTAL)

        # 左侧布局
        leftbox = wx.BoxSizer(wx.VERTICAL)
        sbmbox = wx.BoxSizer(wx.HORIZONTAL)
        searchbox = wx.StaticBoxSizer(self.sm, wx.HORIZONTAL)
        searchbox.Add(self.rb_splatform, 0, wx.ALL, 5)

        driverbox = wx.StaticBoxSizer(self.dm, wx.VERTICAL)
        driverbox.Add(self.rb_platform, 0, wx.ALL, 5)
        driverbox.Add(self.cb_isPhantomjs, 0, wx.ALL, 5)

        filebox = wx.StaticBoxSizer(self.fm, wx.HORIZONTAL)
        filebox.Add(self.kwText, 0, wx.ALIGN_LEFT, 5)
        filebox.Add(self.kwBtn, 0, wx.ALIGN_RIGHT, 5)
        filebox.Add(self.tmpBtn, 0, wx.ALIGN_RIGHT, 5)

        runBox = wx.StaticBoxSizer(self.rm, wx.HORIZONTAL)
        runBox.Add(self.runTime, 0, wx.ALL, 5)
        runBox.Add(self.runText, 0, wx.ALL, 5)

        sbmbox.Add(searchbox, 0, wx.ALIGN_LEFT, 5)
        sbmbox.Add(driverbox, 0, wx.ALIGN_RIGHT, 5)

        proxyBox = wx.StaticBoxSizer(self.pm, wx.VERTICAL)
        proxymodBox = wx.BoxSizer(wx.HORIZONTAL)
        proxymodBox.Add(self.rb_proxy, 0, wx.ALL, 5)
        proxymodBox.Add(self.proxyTextBtn, 0, wx.CENTER, 5)
        proxyConfBox = wx.BoxSizer(wx.HORIZONTAL)
        proxyConfBox.Add(self.proxyText, 0, wx.ALIGN_LEFT, 5)
        proxyConfBox.Add(self.proxyCount, 0, wx.ALIGN_RIGHT, 5)
        proxyBox.Add(proxymodBox, 0, wx.ALL, 5)
        proxyBox.Add(proxyConfBox,  0, wx.ALL, 5)

        runInfoBox = wx.BoxSizer(wx.VERTICAL)
        processBox1 = wx.BoxSizer(wx.HORIZONTAL)
        processBox2 = wx.BoxSizer(wx.HORIZONTAL)
        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        crInfoBox = wx.BoxSizer(wx.HORIZONTAL)
        processBox1.Add(self.spendTime, 0, wx.ALL, 5)
        processBox1.Add(self.proText, 0, wx.ALL, 5)
        processBox1.Add(self.process, 0, wx.ALL, 5)
        processBox2.Add(self.curThread, 0, wx.ALL, 5)
        processBox2.Add(self.succTime, 0, wx.ALL, 5)
        processBox2.Add(self.succRatio, 0, wx.ALL, 5)
        runInfoBox.Add(processBox1, 0, wx.ALL, 5)
        runInfoBox.Add(processBox2, 0, wx.ALL, 5)
        btnBox.Add(self.buttonRun, 0, wx.ALL, 5)
        btnBox.Add(self.buttonStop, 0, wx.ALL, 5)
        crInfoBox.Add(self.copyRight, 0, wx.ALL, 5)

        leftbox.Add(sbmbox, 0, wx.ALL, 5)
        leftbox.Add(filebox, 0, wx.ALL, 5)
        leftbox.Add(runBox, 0, wx.ALL, 5)
        leftbox.Add(proxyBox, 0, wx.ALL, 5)
        leftbox.Add(runInfoBox, 0, wx.ALL, 5)
        leftbox.Add(btnBox, 0, wx.ALIGN_CENTER, 5)
        leftbox.Add(crInfoBox, 0, wx.ALL, 5)

        #中间布局
        middleBox = wx.BoxSizer(wx.VERTICAL)
        logBox = wx.StaticBoxSizer(self.om, wx.HORIZONTAL)
        logBox.Add(self.multiText, 1, wx.ALL, 5)
        logBox1 = wx.StaticBoxSizer(self.om1, wx.HORIZONTAL)
        logBox1.Add(self.multiText1, 0, wx.ALL, 5)
        logBox2 = wx.StaticBoxSizer(self.om2, wx.HORIZONTAL)
        logBox2.Add(self.multiText2, 0, wx.ALL, 5)
        middleBox.Add(logBox, 0, wx.ALL, 5)
        middleBox.Add(logBox1, 0, wx.ALL, 5)
        middleBox.Add(logBox2, 0, wx.ALL, 5)

        # 右侧布局
        rightBox = wx.BoxSizer(wx.VERTICAL)
        logBox3 = wx.StaticBoxSizer(self.om3, wx.HORIZONTAL)
        logBox3.Add(self.multiText3, 0, wx.ALL, 5)
        logBox4 = wx.StaticBoxSizer(self.om4, wx.HORIZONTAL)
        logBox4.Add(self.multiText4, 0, wx.ALL, 5)
        logBox5 = wx.StaticBoxSizer(self.om5, wx.HORIZONTAL)
        logBox5.Add(self.multiText5, 0, wx.ALL, 5)
        logBox6 = wx.StaticBoxSizer(self.om6, wx.HORIZONTAL)
        logBox6.Add(self.multiText6, 0, wx.ALL, 5)
        rightBox.Add(logBox3, 0, wx.ALL, 5)
        rightBox.Add(logBox4, 0, wx.ALL, 5)
        rightBox.Add(logBox5, 0, wx.ALL, 5)
        rightBox.Add(logBox6, 0, wx.ALL, 5)


        # 整体布局
        vbox.Add(leftbox, 0, wx.ALL, 5)
        vbox.Add(middleBox, 0, wx.ALL, 5)
        vbox.Add(rightBox, 0, wx.ALL, 5)
        mbox.Add(vbox, 0, wx.ALL, 5)

        self.SetSizer(mbox)
        mbox.Fit(self)
        self.Show()

    def OnStart(self):
        self.timer.Start(1000)

    def OnStop(self):
        self.timer.Stop()

    def OnTimer(self, evt):
        now = int(time.mktime(datetime.datetime.now().timetuple()))
        self.spend = now - self.beginTime
        hour = str(self.spend/3600)
        min = str((self.spend % 3600)/60)
        sec = str(self.spend % 3600 % 60)
        self.spendTime.SetLabel(u"▶ 耗时: %s:%s:%s" % (
            "".join(["0", hour]) if int(hour) < 10 else hour,
            min if int(min) >= 10 else "".join(["0", min]),
            sec if int(sec) >= 10 else "".join(["0", sec])
        ))

    def EvtRadioBox_PF(self, evt):
        return self.rb_platform.GetSelection()

    def EvtRadioBox_SPF(self, evt):
        return self.rb_splatform.GetSelection()

    def getIsPhantomjs(self, evt):
        return self.cb_isPhantomjs.GetValue()

    def EvtCheckBox_RT(self, evt):
        if self.runTime.GetValue():
            self.runText.SetEditable(True)
        else:
            self.runText.SetEditable(False)

    def EvtRadioBox_Proxy(self, evt):
        self.proxyType = self.rb_proxy.GetItemLabel(self.rb_proxy.GetSelection())
        if self.proxyType == "API": self.OnClickAPI(evt)
        if self.proxyType == "Local": self.OnClickDNS(evt)
        if self.proxyType == "TXT": self.OnClickTXT(evt)

    def getProcess(self, value):
        self.proValue = value

    def setSuccTime(self, threadID, value):
        self.curThread.SetLabel(u"▶ 当前进程ID: %s  " % threadID)
        self.succTime.SetLabel(u"▶ 成功次数: %d  " % value)

    def setSuccRatio(self, value):
        self.succRatio.SetLabel(u"▶ 成功率: %s  " % value)

    def Onprocess(self, evt):
        self.process.SetValue(self.proValue)

    def DisableOnRun(self):
        self.buttonRun.Disable()
        self.rb_splatform.Disable()
        self.rb_platform.Disable()
        self.cb_isPhantomjs.Disable()
        self.kwBtn.Disable()
        self.tmpBtn.Disable()
        self.runTime.Disable()
        self.runText.Disable()
        self.rb_proxy.Disable()
        self.proxyTextBtn.Disable()
        self.proxyText.Disable()

    def EnableOnStop(self):
        self.buttonRun.Enable()
        self.cb_isPhantomjs.Enable()
        self.tmpBtn.Enable()
        self.rb_proxy.Enable()
        self.proxyTextBtn.Enable()
        self.proxyText.Enable()

    def getProxyCount(self, type, conf):
        return len(page.getProxy(type, conf, False))

    def OnClickAPI(self, evt):
        self.proxyText.Enable()
        self.proxyText.SetValue(self.data.proxy_api)
        self.proxyText.SetEditable(True)
        self.proxyTextBtn.Hide()
        self.proxyCount.SetLabel(" |%d" % self.apiCount)

    def OnClickDNS(self, evt):
        self.proxyText.Enable()
        self.proxyText.SetValue(self.data.proxy_dns)
        self.proxyText.SetEditable(True)
        self.proxyTextBtn.Hide()
        self.proxyCount.SetLabel(" |%d" % self.dnsCount)

    def OnClickTXT(self, evt):
        self.proxyText.Disable()
        self.proxyText.SetValue(u"点击右侧按钮选择文件...")
        self.proxyCount.SetLabel(" |0")
        self.proxyTextBtn.Show()
        self.Layout()

    def OnClickRun(self, evt):
        self.beginTime = int(time.mktime(datetime.datetime.now().timetuple()))
        runtime, allRuntime = 0, 0

        # 未选择keyworks文件, 提示错误
        if not self.task:
            self.errInfo(u"请选择关键词配置文件!")
            return
        self.proxyConfig = self.proxyText.GetValue().strip()
        # 如果选择了固定运行次数, 但是赋值为空, 提示错误
        if self.runTime.GetValue():
            allRuntime = self.runText.GetValue().strip()
            if (not allRuntime) or (not allRuntime.isdigit()) or (not int(allRuntime)):
                self.errInfo(u"运行次数配置有误!")
                return

        # 如果代理配置为空, 提示错误
        if self.proxyConfig == "" or self.proxyConfig == u"点击右侧按钮选择文件...":
            self.errInfo(u"代理设置不能为空!")
            return
        self.multiText.SetValue("")
        self.buttonRun.SetLabel(u"运行中")
        self.buttonStop.SetLabel(u"停止")
        self.DisableOnRun()
        self.OnStart()
        isPhantomjs = self.getIsPhantomjs(evt)
        searcher = self.EvtRadioBox_SPF(evt)
        driverType = self.EvtRadioBox_PF(evt)
        for k in self.task.keys():
            value = self.task[k]
            keyword = value["keyword"]
            targetkw = value['targeturl_keyword']
            runtime = allRuntime if allRuntime else value['runtime']
            antiSEM(searcher, driverType, isPhantomjs, self.proxyType, self.proxyConfig, keyword, targetkw, int(runtime))


    def OnClickStop(self, evt):
        ret = wx.MessageBox(u"确定要关闭吗?", "", wx.YES_NO)
        if ret == wx.YES:
            self.Destroy()
            wx.GetApp().ExitMainLoop()

    def OnOpenKWFile(self, evt):
        file_wildcard = "All files(*.*)|*.*"
        dlg = wx.FileDialog(self, u"请选择关键词文件", os.getcwd(), style=wx.FC_OPEN, wildcard=file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            kwfilename = dlg.GetPath()
            self.kwText.SetLabel(kwfilename)
            self.multiText.SetValue(self.note)
            self.task = self.kyFileHeadle(kwfilename)
            if len(self.task.keys()) > 6:
                self.errInfo(u"配置文件中最多设置6个关键词！")
                self.kwText.SetLabel(u"关键词文件种最多设置6个关键词！")
        dlg.Destroy()

    def OnOpenProxyFile(self, evt):
        file_wildcard = "All files(*.*)|*.*"
        dlg = wx.FileDialog(self, u"请选择代理文件", os.getcwd(), style=wx.FC_OPEN, wildcard=file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            kwfilename = dlg.GetPath()
            self.proxyText.SetValue(kwfilename)
            self.proxyConfig = kwfilename
            self.multiText.SetValue(self.note)
            self.proxyCount.SetLabel(" |%d" % self.getProxyCount("TXT", kwfilename))
        dlg.Destroy()

    def kyFileHeadle(self, filename):
        name = os.path.basename(filename)
        if name != "kw.data":
            self.errInfo(u"关键词文件名必须为: 'kw.data'")
            return False
        try:
            with open(filename, "r") as ff:
                kw = ff.read().decode("utf-8")
                return eval(kw)
        except Exception, e:
            self.errInfo(u"获取关键词文件失败:%s" % str(e))
            return False

    def cpDriver(self, evt):
        os.system("mkdir %s" % self.dir)
        import pkgutil, tarfile, zipfile
        gd = pkgutil.get_data('antiSEM', "drivers"+os.sep+self.gdname)
        gdpath = self.dir + self.gdname

        ''' # for chrome driver, no used in code now
        cdname = "chromedriver_mac64.tar.gz"
        cd = pkgutil.get_data('antiSEM', cdname)
        cdpath = self.dir + cdname
        try:
            if self.EvtRadioBox_PF(evt) == "H5-C":
                with open(cdpath, 'wb') as ff:
                    ff.write(cd)
                zfile = tarfile.open(cdpath)
                zfile.extractall(path=self.dir)
                self.errInfo(u"成功解压%s到目录: %s\n\n" % (cdname, self.dir))
            else:
                with open(gdpath, 'wb') as ff:
                    ff.write(gd)
                tfile = tarfile.open(gdpath)
                tfile.extractall(path=self.dir)
                self.errInfo(u"成功解压%s到目录: %s\n\n" % (gdname, self.dir))
        except Exception, e:
            self.errInfo(u"解压web driver文件失败: %s" % str(e))
        '''
        try:
            with open(gdpath, 'wb') as ff:
                ff.write(gd)
            if platform.system() == "Darwin":
                tfile = tarfile.open(gdpath)
                tfile.extractall(path=self.dir)
            if platform.system() == "Windows":
                zfile = zipfile.ZipFile(gdpath,'r')
                zfile.extractall(path=self.dir)
            self.errInfo(u"成功解压%s到目录: %s\n\n" % (self.gdname, self.dir))
        except Exception, e:
            self.errInfo(u"解压web driver文件失败: %s" % str(e))

    def OnCreateTmpFile(self, evt):
        ret = wx.MessageBox(u"点击确定会覆盖当前已存在的配置文件, 确定要创建模板文件吗?", "", wx.YES_NO)
        if ret == wx.YES:
            kwconf = u'''{
                        'T1': {
                                        'keyword': '域名注册',
                                        'targeturl_keyword': 'xinnet.com',
                                        'runtime': 3,
                        },
                        'T2': {
                                        'keyword': '虚拟主机',
                                        'targeturl_keyword': 'xinnet.com',
                                        'runtime': 6,
                        },
                        'T3': {
                                        'keyword': '虚拟空间',
                                        'targeturl_keyword': 'xinnet.com',
                                        'runtime': 3,
                        },
                        'T4': {
                                        'keyword': '企业邮箱',
                                        'targeturl_keyword': 'xinnet.com',
                                        'runtime': 6,
                        },
                        'T5': {
                                        'keyword': '云主机',
                                        'targeturl_keyword': 'xinnet.com',
                                        'runtime': 3,
                        },
                        'T6': {
                                        'keyword': '云服务器',
                                        'targeturl_keyword': 'xinnet.com',
                                        'runtime': 6,
                        },
            }'''
            try:
                with open("kw.data", "w") as ff:
                    ff.write(kwconf)
                self.errInfo(u"已在当前目录下创建关键词模板文件: kw.data")
            except:
                self.errInfo(u"创建关键词模板文件失败!")

    def getThreadTextObj(self, id):
            ThreadTextObj = [self.multiText, self.multiText1, self.multiText2, self.multiText3, self.multiText4, self.multiText5, self.multiText6]
            return ThreadTextObj[id]


    def errInfo(self, log, mode=0, threadID=0):
            self.getThreadTextObj(threadID).SetDefaultStyle(wx.TextAttr("RED"))
            if not mode:
                self.getThreadTextObj(threadID).SetValue("\n\n" + log)
            else:
                self.getThreadTextObj(threadID).AppendText(log)
            self.getThreadTextObj(threadID).SetDefaultStyle(wx.TextAttr("BLACK"))

    def printLog(self, info, mode=0, threadID=0):
        if not mode:
            try:
                self.getThreadTextObj(threadID).AppendText(info)
            except Exception, e:
                self.getThreadTextObj(threadID).AppendText(str(e))
        else:
            try:
                self.getThreadTextObj(threadID).SetValue(info)
            except Exception, e:
                self.getThreadTextObj(threadID).SetValue(str(e))

    def reset(self):
        self.EnableOnStop()
        self.buttonRun.Enable(True)
        self.buttonRun.SetLabel(u"运行")
        self.buttonStop.SetLabel(u"关闭")
        self.OnStop()

    def closeApp(self):
        wx.GetApp().ExitMainLoop()

    def update(self):
        pub.subscribe(self.errInfo, "log")
        pub.subscribe(self.printLog, "info")
        pub.subscribe(self.reset, "reset")
        pub.subscribe(self.getProcess, "process")
        pub.subscribe(self.setSuccTime, "succTime")
        pub.subscribe(self.setSuccRatio, "succRatio")
        pub.subscribe(self.closeApp, "close")

if __name__ == "__main__":
    wr = wxAntiSEM()
    wr.get_data_from_db()