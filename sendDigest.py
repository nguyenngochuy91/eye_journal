#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Send digest module
    Start   : 03/08/2018
    End     : 08/08/2018
'''
import smtplib
import argparse
from googleCrawler import Query,Article,Parser

# argument parsing
def get_arguments():
    parser = argparse.ArgumentParser(description='The purpose of this program is to send digest of the most recent articles from subscribed article given user research topic')
    
    parser.add_argument("-r", "--research_topic", 
                help="Research topic user want to find, have to be in quotation ('Dynamic Programming')") 
    parser.add_argument("-ylo", "--year_low", 
                help="Lowest bound of the year that the articles were published")   
    parser.add_argument("-yhi", "--year_high", 
                help="Highest bound of the year that the articles were published") 
    parser.add_argument("-cJ", "--count_journal", 
                help="How many journal you want to subscribe? (max 4)")  
    parser.add_argument("-cA", "--count_article", 
                help="How many articles for each journal to be in the digest? (max 3)")                                    
    return parser.parse_args()


'''@function: sending digest
   @input   : a lot
   @output  : none
'''    
def generate_digets(journal_article, fromaddr,username,password,toAddr):
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    header = 'To:' + toAddr + '\n' + 'From: ' + fromaddr + '\n' + 'Subject:New digest \n'
    string   = "\n {}".format(journal)
    for art in articles:
        string+= "\n"+ art.as_txt()+"\n"
    server.sendmail(fromaddr, toAddr,header.encode()+ string.encode())
    server.quit()  
    
'''@function: given the research topic, return the set of journals of interest
   @input   : research_topic(string),ylo(string),yhi(string)
   @output  : journals(set)
'''    
def get_journals(research_topic,ylo,yhi,count):
    research_query = Query(research_topic=research_topic,ylo=ylo,yhi=yhi)
    url            = research_query.generate_query()
    parser         = Parser(url,count)
    parser.retrieve_journals() # retrieve all the articles
    journals       = parser.get_journals()
    return journals

'''@function: given the journal name, return a dictionary that store information of all recent articles
              of a given journal
   @input   : research_topic(string),ylo(string),yhi(string),count(int)
   @output  : articles(dic) 
'''  
def get_articles(journal,ylo,yhi,count):
    journal_query  = Query(research_topic= journal,ylo=ylo,yhi=yhi)
    url            = journal_query.generate_query()
    parser         = Parser(url,count)
    parser.generate_articles() # retrieve all the articles
    articles       = parser.get_articles()
    return articles

if __name__ == '__main__':
    separation      = "*"*100
    args            = get_arguments()
    research_topic  = args.research_topic
    ylo             = args.year_low
    yhi             = args.year_high
    count_journal   = int(args.count_journal)
    count_article   = int(args.count_article)
    
    print ("Getting all journals for topic {}".format(research_topic))
    journals        = get_journals(research_topic,ylo,yhi,count_journal)
    print ("Done with getting all journals")
    print (separation)
    journal_article = {}
    for journal in journals:
        print ("Getting articles for journal {}".format(journal))
        journal_article[journal] = get_articles(journal,ylo,yhi,count_article)
    print (journal_article)