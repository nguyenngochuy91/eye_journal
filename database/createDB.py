#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Create a database for user, journal, and subsription
    Start   : 03/08/2018
    End     : 08/08/2018
'''
import sqlite3 as lite
import argparse
from db import Journal
import zipfile
from openpyxl import load_workbook
# get the argument
def get_arguments():
    parser = argparse.ArgumentParser(description='The purpose of this program is  \
                                     to create a database mysql')
    parser.add_argument("-db_name", "--DB_NAME", default = "pb",
                help="Name of the database")
    parser.add_argument("-db_user", "--DB_USER", default = "pb",
                help="Name of the databse user") 
    parser.add_argument("-db_password", "--DB_PASSWORD",
                help="password for the db") 
    parser.add_argument("-db_host", "--DB_HOST", default = "127.0.0.1",
                help="Host for the db server")       
    parser.add_argument("-s", "--scopus", default = "scopus_2017.xlsx",
                help="Scopus that store all the name of peerer review journals (https://www.scopus.com/sources.uri?DGCID=Scopus_blog_post_check2015) ")                                  
    return parser.parse_args()

# program that parse all article name into a dictionary
def read_xlsx(infile):
    load         = load_workbook(infile)
    worksheet    = load.active
    interest_col = worksheet['B']        
    return [item.value.encode('utf-8').replace("'"," ") for item in interest_col]
    
if __name__ == '__main__':
    separation   = "*"*100
    args         = get_arguments()
    DB_NAME      = args.DB_NAME
    DB_USER      = args.DB_USER
    DB_PASSWORD  = args.DB_PASSWORD
    DB_HOST      = args.DB_HOST
    scopus       = args.scopus
    # store all of scopus of journal into a dic:
    journal_name = read_xlsx(scopus)[1:]
    # open database connection
    db = lite.connect(DB_NAME,detect_types=lite.PARSE_DECLTYPES)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Drop table if it already exist using execute() method.
    cursor.execute("DROP TABLE IF EXISTS USER")
    cursor.execute("DROP TABLE IF EXISTS JOURNAL")
    cursor.execute("DROP TABLE IF EXISTS SUBSCRIPTION")
    
    # generate sql table for user,journal,subscription
    user = """CREATE TABLE USER (
    ID  INT NOT NULL,
    EMAIL  CHAR(30) NOT NULL,
    UPDATE_PERIOD INT,  
    [CREATE_DATE] TIMESTAMP ,
    [LAST_UPDATED] TIMESTAMP ,
    PRIMARY KEY (ID))"""
    
    journal = """CREATE TABLE JOURNAL (
    ID  INT NOT NULL,
    NAME  CHAR(255) NOT NULL,
    PRIMARY KEY (ID))"""
    
    subscription = """CREATE TABLE SUBSCRIPTION (
    ID  INT NOT NULL,
    USER_ID  INT NOT NULL,
    JOURNAL_ID  INT, 
    [CREATE_DATE] TIMESTAMP ,
    PRIMARY KEY (ID),
    FOREIGN KEY (USER_ID) REFERENCES USER(ID),
    FOREIGN KEY (JOURNAL_ID) REFERENCES JOURNAL(ID))"""
    
    cursor.execute(user) # add user table
    cursor.execute(journal) # add journal table
    cursor.execute(subscription)
    
    # insert our journal_name into the journals database
    for i in range(len(journal_name)):
        j = Journal((i+1,journal_name[i]))
        command = j.to_sql_command()
        cursor.execute(command)
    # disconnect from server
    db.commit()
    cursor.close()
    