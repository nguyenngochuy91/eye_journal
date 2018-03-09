#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Provide a parser and crawler of google scholar, and a query 
    Start   : 03/08/2018
    End     : 08/08/2018
'''
from selenium import webdriver
import time
try:
    from bs4 import BeautifulSoup as bs
except ImportError:
    try:
        from BeautifulSoup import BeautifulSoup as bs
    except ImportError:
        print ("You need beautifulSoup package buddy")
class Query(object):
    google_query = 'https://scholar.google.com/scholar?scisbd=1&hl=en&as_sdt=0,16'\
        + '&q=%(query)s' \
        + '&as_ylo=%(ylo)s' \
        + '&as_yhi=%(yhi)s' \
        + '&btnG=&hl=en' \
        + 'as_sdt=0,16' \
        + '&scisbd=1'
    
    def __init__(self,research_topic= "",journals= "",ylo = "",yhi= ""):
        self.research_topic = research_topic
        self.journals       = journals
        self.ylo            = ylo
        self.yhi            = yhi
        self.query          = ""
    def generate_query(self):
        if self.research_topic:
            self.query+=self.research_topic.replace(" ","+")
        elif self.journals:
            self.query+=self.journals.replace(" ","+")
        args = {'query': self.query,
               'ylo': self.ylo,
               'yhi': self.yhi}
        return self.google_query % args
class Article(object):
    def __init__(self,html):
        self.html = bs(html,"lxml").text
        self.info = {"title":None,
                     "author":None,
                     "booktitle":None,
                     "volume":None,
                     "year":None,
                     "journal":None,
                     "pages":None,
                     "organization":None}
    def parse(self):
        items = self.html.split("\n")
        for item in items:
            try:
                item = item.split("=")
                tag  = item[0].replace(" ","")
                info = item[1].split("{")[1].split("}")[0]
                try:
                    self.info[tag]= info
                except:
                    print ("tag {} was not found!!!".format(tag))
            except:
                continue
            
                
class Parser(object):
    def __init__(self,url,size):
        self.size     = min(size,10)
        self.url      = url
        self.driver   = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
        self.driver.set_window_size(1124, 850)
        self.driver.get(self.url)
        self.soup     =  bs(self.driver.page_source,"lxml") # this is the parrent page to query the date and urls
        self.urls     = []
        self.articles = [] # list of articles appear on the url, we will retrieve the bibtext file 
        self.times    = []   
        self.journals = set()
    def retrieve_articles(self):
        # using selenium to crawl to bibtex info
        for i in range(self.size):
            elements = self.driver.find_elements_by_class_name('gs_or_cit')
            element  = elements[i]
            element.click()
            time.sleep(2)
            element = self.driver.find_element_by_class_name('gs_citi')
            element.click()
            time.sleep(2)
            html = self.driver.page_source
            art  = Article(html)
            art.parse()
            self.articles.append(art.info)
            print ("Done with article {}".format(art.info["title"]))
            self.driver.get(self.url)
    def retrieve_journals(self):
        # using selenium to crawl to bibtex info
        for i in range(10):
            elements = self.driver.find_elements_by_class_name('gs_or_cit')
            element  = elements[i]
            element.click()
            time.sleep(2)
            element = self.driver.find_element_by_class_name('gs_citi')
            element.click()
            time.sleep(2)
            html = self.driver.page_source
            art  = Article(html)
            art.parse()
            self.journals.add(art.info["journal"])
            print ("Done with article {}".format(art.info["title"]))
            self.driver.get(self.url)
            if len(self.journals)== self.size:
                break
    def retrieve_urls(self):
        tags = self.soup.find_all("h3")
        for t in tags:
            href = t.find("a",href= True)
            self.urls.append(href.attrs['href'])
    def retrieve_times(self):
        myspans = self.soup.find_all("span",{"class":"gs_age"})
        for span in myspans:
            self.times.append(span.contents[0].split("-")[0])
    def get_articles(self):
        return self.articles
    def get_urls(self):
        return self.urls
    def get_times(self):
        return self.times
    def get_journals(self):
        return self.journals
    def generate_articles(self):
        self.retrieve_articles()
        self.retrieve_times()
        self.retrieve_urls()
        for i in range(self.size):
            url  = self.urls[i]
            time = self.times[i]
            self.articles[i]["url"]  = url
            self.articles[i]["time"] = time
            