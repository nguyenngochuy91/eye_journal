#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Generate an url, get the journals 
    Start   : 03/08/2018
    End     : 08/08/2018
'''
from googleCrawler import Parser
'''@function: given the url, return the set of journals of interest
   @input   : research_topic(string),ylo(string),yhi(string)
   @output  : journals(set)
'''    
def get_journals_from_url(url,count):
    parser         = Parser(url,count)
    parser.retrieve_journals() # retrieve all the articles
    journals       = parser.get_journals()
    return journals

