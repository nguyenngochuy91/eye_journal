#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Generate a json (digest) file given journals name from database
    Start   : 03/08/2018
    End     : 08/08/2018
'''
from googleCrawler import Query,Parser

'''@function: given the url, return the set of journals of interest (call by front end)
   @input   : research_topic(string),ylo(string),yhi(string)
   @output  : journals(set)
'''    
def get_journals_from_url(url,count):
    parser         = Parser(url,count)
    parser.retrieve_journals() # retrieve all the articles
    journals       = parser.get_journals()
    return journals    


'''@function: given the journal name, return a dictionary that store information of all recent articles
              of a given journal
   @input   : research_topic(string),ylo(string),yhi(string),count(int)
   @output  : articles(dic) 
'''  
def get_articles(journal,count):
    journal_query  = Query(research_topic= journal)
    url            = journal_query.generate_query()
    parser         = Parser(url,count)
    parser.generate_articles() # retrieve all the articles
    articles       = parser.get_articles()
    return articles




        

