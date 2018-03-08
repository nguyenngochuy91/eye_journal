#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Provide a parser and crawler of google scholar 
    Start   : 03/08/2018
    End     : 05/08/2018
'''

import smtplib
from selenium import webdriver
import time
try:
    from bs4 import BeautifulSoup as bs
except ImportError:
    try:
        from BeautifulSoup import BeautifulSoup as bs
    except ImportError:
        print ("You need beautifulSoup package buddy")
        
class Parser(object):
    def __init__(self,url):
        self.url = url+'&scisbd=1'
        self.driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
        self.driver.set_window_size(1124, 850)
        self.driver.get(self.url)
        self.soup  =  bs(self.driver.page_source)
        self.url = []
        self.articles = [] # list of articles appear on the url, we will retrieve the bibtext file 
    def retrieve_info(self):
        elements = self.driver.find_elements_by_class_name('gs_or_cit')
        size     = len(elements)
        for i in range(size):
            elements = self.driver.find_elements_by_class_name('gs_or_cit')
            element  = elements[i]
            element.click()
            time.sleep(5)
            element = self.driver.find_element_by_class_name('gs_citi')
            element.click()
            time.sleep(5)
            self.articles.append(self.driver.page_source)
            time.sleep(5)
            self.driver.get(self.url)
    def get_articles(self):
        return self.articles
            