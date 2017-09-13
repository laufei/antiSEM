﻿# coding: utf-8
__author__ = 'liufei'

import sys
from selenium.webdriver.common.by import By
from lib.base import base
reload(sys)
sys.setdefaultencoding('utf8')

class page(base):
    baidu_kw = (By.ID, 'kw')                # WEB百度首页输入框
    baidu_kw_m = (By.ID, 'index-kw')        # H5百度首页输入框
    baidu_se_kw_m = (By.ID, 'kw')      # H5百度搜索结果页输入框
    baidu_submit = (By.ID, 'su')                # WEB百度首页搜索button
    baidu_submit_m = (By.ID, 'index-bn')                # H5百度首页搜索button
    baidu_result_pages = (By.CSS_SELECTOR, 'span.pc')       # WEB百度搜索结果页面中翻页控件
    baidu_result_pages_m = (By.CSS_SELECTOR, 'a[class^=new-nextpage]')       # H5百度搜索结果页面中翻页控件
    baidu_result_items = (By.CSS_SELECTOR, 'h3.t a')    # WEB百度搜索结果页面中搜索结果模块
    baidu_result_items_m = (By.CSS_SELECTOR, 'div[class=c-container] > a:first-child')      # H5百度搜索结果页面中搜索结果模块
    baidu_result_item = '(By.ID, "{id}")'    # WEB百度搜索结果页面中搜索结果模块
    baidu_result_url = (By.CSS_SELECTOR, 'h3.t a')      # WEB百度搜索结果页面中搜索结果模块URL

    baidu_result_ad_items = (By.CSS_SELECTOR, 'a[data-is-main=true], a[data-landurl]')  # WEB百度搜索结果页面中的广告URL
