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

class Article(object):
    def __init__self(html):
        self.html = soup(html).text
        self.title = None
        self.author = None
        self.booktitle = None
        self.volume = None
        self.year = None
        self.title = None
        self.is_journal = False
        self.journal = None
        self.pages   = None
        
class Parser(object):
    def __init__(self,url):
        self.url      = url+'&scisbd=1'
        self.driver   = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
        self.driver.set_window_size(1124, 850)
        self.driver.get(self.url)
        self.soup     =  bs(self.driver.page_source)
        self.urls     = []
        self.articles = [] # list of articles appear on the url, we will retrieve the bibtext file 
        self.ages     = []        
    def retrieve_articles(self):
        elements = self.driver.find_elements_by_class_name('gs_or_cit')
        size     = len(elements)
        for i in range(size):
            elements = self.driver.find_elements_by_class_name('gs_or_cit')
            element  = elements[i]
            element.click()
            time.sleep(1)
            element = self.driver.find_element_by_class_name('gs_citi')
            element.click()
            time.sleep(2)
            self.articles.append(self.driver.page_source)
            self.driver.get(self.url)
    def retrieve_urls(self):
        tags = self.soup.find_all("h3")
        for t in tags:
            href = t.find("a",href= True)
            self.urls.append(href.attrs['href'])
    def get_articles(self):
        return self.articles
    def get_urls(self):
        return self.urls
            