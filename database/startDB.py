#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Main function that calls other function in crawler, this file will run 
              on our database pb
    Start   : 03/08/2018
    End     : 03/25/2018
'''
import sys
sys.path.append('../crawler/')
import sqlite3 as lite
import random
import datetime
import db
from sendDigest import send_digest
from generateDigest import get_articles
import argparse
import time
import json
# adding argurment parsing
def get_arguments():
    parser = argparse.ArgumentParser(description='The purpose of this program is  \
                                     to fire off our database and continuosly checking \
                                     if we have to send a new digest to any user')
    parser.add_argument("-u", "--username", 
                help="username/ email address of the sender") 
    parser.add_argument("-p", "--password", 
                help="password of the user")  
    return parser.parse_args()

'''@function: given a user id, return email of the user and the list of journal
              the user subscribes to 
   @input   : database (sqlite), subscriptions (list)
   @output  : journals(dictionary)
'''    
def get_journals_from_user(database,user_id):
    cursor = database.cursor()
    journals = {"email":None,"journal":[]}
    command = """
    SELECT USER.EMAIL,JOURNAL.NAME FROM SUBSCRIPTION 
    INNER JOIN JOURNAL ON JOURNAL.ID= SUBSCRIPTION.JOURNAL_ID 
    INNER JOIN USER ON USER.ID= SUBSCRIPTION.USER_ID 
    WHERE SUBSCRIPTION.USER_ID ={}
    """.format(user_id)
    cursor.execute(command)
    info  = cursor.fetchall()
    if not info:
        return None
    else:
        for item in info:
            journals["journal"].append(item[1])
        journals["email"] = info[0][0]
        return journals

'''@function: given several user ids, return a list of journals dictionary to send off
   @input   : database (sqlite), users (list)
   @output  : journals(dictionary)
'''
def get_journals_for_users(database,users):
    all_journals =[]
    for user in users:
        all_journals.apped(get_journals_from_user(database,user))
    return all_journals
# create some basic fake data for testing purpose
def testing(database,emails,num_user,num_subscription):
    cursor = database.cursor()
    # adding several users
    for i in range(1,num_user+1):
        command = db.User((i,emails[i-1],random.randint(120,150),datetime.datetime.now(),datetime.datetime.now()))
        cursor.execute(command.to_sql_command())
        
    # adding several subscriptions
    c= 1
    for i in range(1,num_user+1):
        for j in range(1,num_subscription+1):
            command = db.Subscription((c,i,random.randint(1,30000),datetime.datetime.now()))
            cursor.execute(command.to_sql_command())
            c+=1
#    # print out table user
#    cursor.execute("""SELECT * FROM USER""")
#    print ("USER TABLE:")
#    print (cursor.fetchall())
#    # print out table subscription
#    cursor.execute("""SELECT * FROM SUBSCRIPTION""")
#    print ("SUBSCRIPTION TABLE:")
#    print (cursor.fetchall())    
#    for i in range(1,num_user+1):
#        print (get_journals_from_user(database,i))
'''@function: provide list of user id that need to have digest
   @input   : database (sqlite), num_user,num_subscription
   @output  : nothing
'''  
def need_update_user(database,current_time):
    cursor = database.cursor()
    command = """
    SELECT * FROM USER
    """
    cursor.execute(command)
    user_ids = [db.User(item,True) for item in cursor.fetchall()]
    user_ids = [item.id for item in user_ids if (current_time-item.last_updated).seconds>=item.update_period]
    return user_ids
    
'''@function: updating user last update column
   @input   : database (sqlite), users(list)
   @output  : nothing
''' 
def update_user(database,users,current_time):
    cursor = database.cursor()
    for user in users:
        command = """
        UPDATE USER SET
        LAST_UPDATED = {}
        """.format("'"+current_time+"'")
        cursor.execute(command)     
if __name__ == '__main__':
    args      = get_arguments()
    username  = args.username
    password  = args.password
    log_dir   = "logs/"
    database  = lite.connect("pb",detect_types=lite.PARSE_DECLTYPES)
    # testing, add some random thingy
    emails = ["huyn@iastate.edu","alex_koshmarkin@mail.ru","amarkin@iastate.edu","kmousavi@iastate.edu"]
    testing(database,4,5)
    c=1
    while True:
        current_time = datetime.datetime.now()
        users = need_update_user(database,current_time)
        print (users)
        # for each of these users
        # update the time in the user table of the last_updated
        update_user(database,users,str(current_time))  
        
        # receive a list of email, and journals to send a digest 
        all_journals = get_journals_for_users(database,users)
        for item in all_journals:
            to_addr          = item["email"]
            json_file        = log_dir+to_addr+"_"+str(c)
            list_of_journals = item["journal"]
            all_articles = {}
            for journal in list_of_journals:
                all_articles[journal]= get_articles(journal,2)
            with open(json_file,"w") as data_file:
                json.dump(all_articles,data_file)
            send_digest(json_file, username,username,password,to_addr)
        time.sleep(60)
        c+=1