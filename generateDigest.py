#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Generate a json file that store digest to be send
    Start   : 03/08/2018
    End     : 08/08/2018
'''

from googleCrawler import Query,Parser
import json
import argparse
# argument parsing
def get_arguments():
    parser = argparse.ArgumentParser(description='The purpose of this program is to generate digest of the most recent articles from subscribed article given user research topic')
    
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
    parser.add_argument("-o", "--output", 
                help="json file output name ")                                  
    return parser.parse_args()

    
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
    outfile         = "request_json/"+args.output+".json"
    print ("Getting all journals for topic {}".format(research_topic))
    journals        = get_journals(research_topic,ylo,yhi,count_journal)
    print ("Done with getting all journals")
    print (separation)
    journal_article = {}
    for journal in journals:
        print ("Getting articles for journal {}".format(journal))
        journal_article[journal] = get_articles(journal,ylo,yhi,count_article)
    print (journal_article)
    # generate a json file
    with open(outfile,"w") as data_file:
        json.dump(journal_article,data_file)
