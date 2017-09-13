# coding: utf-8
__author__ = 'liufei'

import sys

reload(sys)
sys.setdefaultencoding('utf8')

class data:

    def __init__(self):
        self.openURL_waittime = 3
        self.toSearchPage_waittime = 3
        self.baidu_url_web = "https://www.baidu.com"
        self.baidu_url_h5 = "https://m.baidu.com"
        self.baidu_url_request_web = "https://www.baidu.com/s?wd=%s&pn=%d&rsv_spt=1&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg\
                                                            &rsv_enter=0&rsv_sug3=16&rsv_sug1=18&rsv_sug7=101&inputT=6882&rsv_sug4=8327&rsv_sug=1"
        self.baidu_url_request_m = "https://m.baidu.com/s?word=%s&pn=%d&ref=www_colorful&st=111041&from=1014994a"
        self.sm_url = "http://m.sm.cn"
        self.sogou_url = "https://www.sogou.com"
        self.proxy_dns = "http://127.0.0.1:8083/proxies.txt"
        self.proxy_api = "http://127.0.0.1:8000/?types=0&count=300"
        self.proxy_txt = "proxy.txt"

        self.threadNote = u"当前进程状态 -【空闲】"
        self.note = u'''【使用说明】:
 1. 搜索平台&运行平台: 可以选择各个搜索平台对应的H5或者Web平台进行操作.
 2. 关键词文件路径: 文件名须为"kw.data"; 点击生成模板按钮"+", 查看具体文件格式.
 3. 运行次数: 勾选了该复选框, 每个关键词运行次数被统一配置.
 4. 代理方式: 对于每个代理方式需配置对应请求地址或文件路径; 如选择TXT方式, 需要点击按钮"..."来选择代理文件.
 5. 运行日志: 程序执行过程中会输入log信息, 包括各种报错及提示信息; 程序会在该app所在路径下生成日志文件: Result.txt.
'''