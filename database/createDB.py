#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Create a database for user, journal, and subsription
    Start   : 03/08/2018
    End     : 08/08/2018
'''
import sqlite3 as lite
import argparse
from db import Journal

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
    return parser.parse_args()


if __name__ == '__main__':
    separation      = "*"*100
    args            = get_arguments()
    DB_NAME         = args.DB_NAME
    DB_USER         = args.DB_USER
    DB_PASSWORD     = args.DB_PASSWORD
    DB_HOST         = args.DB_HOST
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
    # disconnect from server
    db.commit()
    cursor.close()
    