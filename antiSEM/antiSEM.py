# coding: utf-8
__author__ = 'liufei'
import time, sys
import random
import threading
import wx
from wx.lib.pubsub import pub
from element.page import page
from data.data import data

class antiSEM(page):
    def __init__(self, searcher, driverType, isPhantomjs, proxyType, proxyConfig, keyworks, urlkw, runtime):
        #搜索关键词
        self.data = data()
        self.searcher = searcher
        self.driverType = driverType
        self.isPhantomjs = isPhantomjs
        self.getURL = self.getURL()
        self.proxyType = proxyType
        self.proxyConfig = proxyConfig
        self.SearchKeywords = keyworks
        self.URLKeywords = urlkw
        self.Runtime = runtime

        # 常量设置
        self.PagesCount = 3     # 搜索结果页面中，遍历结果页面数量
        self.radio_sorted = 0.7  # 首页正序随机点击URL比例
        self.output_Result(info=self.print_task_list(self.SearchKeywords, self.URLKeywords, self.Runtime))

    def __del__(self):
        self.end()

    def print_task_list(self, keyworks, urlkw, runtime):
        template = u'''
        ===============
        【运行平台】: %s
        【Driver类型】: %s
        【搜索平台】: %s
        【目标执行次数】: %s
        【搜索关键词】: %s
        【白名单关键字】: %s

        ''' %(
            self.getdriverType(self.isPhantomjs).split("_")[0],
            self.getdriverType(self.isPhantomjs).split("_")[1],
            self.getSearcher(),
            runtime,
            keyworks,
            "".join(urlkw),
            )
        return template

    def getdriverType(self, isPhantomjs):
        if isPhantomjs:
            return "web_phantomjs" if self.driverType == 0 else "h5_phantomjs"
        else:
            return "web_firefox" if self.driverType == 0 else "h5_firefox"

    def getURL(self):
        return (self.data.baidu_url_web if self.driverType == 0 else self.data.baidu_url_h5) if self.searcher == 0 else (self.data.sm_url if self.searcher == 1 else self.data.sogou_url)

    def getSearcher(self):
        return "百度" if self.searcher == 0 else ("神马" if self.searcher == 1 else "搜狗")

    def getMethod(self):
        if [self.searcher, self.driverType] == [0, 0]:
            self.rank_baidu_web()
        if [self.searcher, self.driverType] == [0, 1]:
            self.rank_baidu_m()
        if [self.searcher, self.driverType] == [1, 0]:
            self.rank_sm_m()
        if [self.searcher, self.driverType] == [1, 1]:
            self.rank_sm_web()
        if [self.searcher, self.driverType] == [2, 0]:
            self.rank_sogou_m()
        if [self.searcher, self.driverType] == [2, 1]:
            self.rank_sogou_web()

    def begin(self):
        # 实例化
        isProxy = True
        try:
            self.pageobj = page(self.getdriverType(self.isPhantomjs), self.proxyType, self.proxyConfig, isProxy)
        except Exception, e:
            self.output_Result(info=str(e))
            wx.CallAfter(pub.sendMessage, "reset")
            sys.exit("Failed to run~!")

    def end(self):
        try:
            self.pageobj.quit()
        except:
            pass

    def updateResultInfo(self, threadid, succtime, runtime):
        wx.CallAfter(pub.sendMessage, "succTime", threadID=threadid, value=succtime)
        process = succtime*100/self.Runtime
        wx.CallAfter(pub.sendMessage, "process", value=process)
        try:
            succRatio = round(succtime/float(runtime), 2)
            wx.CallAfter(pub.sendMessage, "succRatio", value=str(succRatio))
        except ZeroDivisionError:
            pass

    def rank_baidu_web(self):
        threadname = threading.currentThread().getName()
        threadID = int(threadname[-1])
        succtime, runtime = 0, 0         # succtime: 记录当前关键字下成功点击次数;     runtime: 记录当前关键字下所有点击次数
        # succTimeAll, succRatio = 0, 0   # succTimeAll: 记录当前任务下总的成功点击次数;     succRatio: 记录当前关键字下所有点击成功率
        self.updateResultInfo(threadID, succtime, runtime)
        self.output_Result(info=u"【%s】：当前关键词 - %s" % (threadname, self.SearchKeywords), mode=1, threadID=threadID)
        while True:
            if int(self.Runtime) == int(succtime):
                break
            runtime += 1
            self.begin()
            driver = self.pageobj.getDriver()
            self.output_Result(info=u"----------------------------------------------", threadID=threadID)
            self.output_Result(info=u"[%s] 当前使用代理: %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), self.pageobj.getProxyAddr()), threadID=threadID)
            # 1. 打开搜索页面并使用关键词搜索
            try:
                self.pageobj.gotoURL(self.getURL)
                window = driver.current_window_handle
                self.pageobj.find_element(*self.baidu_kw).click()
                time.sleep(1)
                self.pageobj.find_element(*self.baidu_kw).send_keys(unicode(self.SearchKeywords))
                time.sleep(2)
                self.pageobj.find_element(*self.baidu_submit).click()
                time.sleep(self.data.toSearchPage_waittime)
            except Exception, e:
                self.updateResultInfo(threadID, succtime, runtime)
                self.output_Result(log=str(e), threadID=threadID)
                self.end()
                continue

            # 2.获取到广告模块数据
            baidu_result_ad_items = self.pageobj.find_elements(*self.baidu_result_ad_items)
            if not len(baidu_result_ad_items):
                self.output_Result(info=u"     [获取失败] - 该结果页并没有获取到广告链接", threadID=threadID)
                self.end()
                self.updateResultInfo(threadID, succtime, runtime)
                continue
            # 按照比例随机点击URL，正序80%，乱序20%
            ra = random.random()
            if ra < self.radio_sorted:
                targets = sorted(random.sample(range(len(baidu_result_ad_items)), random.sample(range(1, len(baidu_result_ad_items)+1), 1)[0]))
            else:
                targets = random.sample(range(len(baidu_result_ad_items)), random.sample(range(1, len(baidu_result_ad_items)+1), 1)[0])
            for index in targets:
                resultURL = baidu_result_ad_items[index].get_attribute("data-landurl")
                if self.URLKeywords in resultURL:
                    self.output_Result(info=u"     [白名单] - 广告链接处于白名单, 跳过~", threadID=threadID)
                    continue
                self.output_Result(info=u"     [尝试点击] - 点击结果页面第[%d]个链接" % (index+1), threadID=threadID)
                try:
                    baidu_result_ad_items[index].click()
                    time.sleep(self.data.toSearchPage_waittime)
                    driver.switch_to.window(window)
                except Exception, e:
                    self.output_Result(info=u"     [点击失败] - Oops，并没有点到您想要的链接.....  T_T, %s" % str(e), threadID=threadID)
                    self.end()
                    continue

            succtime += 1
            self.end()
            self.updateResultInfo(threadID, succtime, runtime)
        self.output_Result(info=u"进程[%s]结束, 当前关键词, 成功点击%d次" % (threadname, succtime))

    def rank_baidu_m(self):
        wx.CallAfter(self.output_Result, log=u"该功能尚未支持!")

    def rank_sm_web(self):
        wx.CallAfter(self.output_Result, log=u"该功能尚未支持!")

    def rank_sm_m(self):
        wx.CallAfter(self.output_Result, log=u"该功能尚未支持!")

    def rank_sogou_web(self):
        wx.CallAfter(self.output_Result, log=u"该功能尚未支持!")

    def rank_sogou_m(self):
        wx.CallAfter(self.output_Result, log=u"该功能尚未支持!")