#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : This defines 3 classes of user, journals, and subscription
              Each class initiate with a tuple according to the schema in db,
              has a function to string that return a string to insert to the 
              corresponding db
    Start   : 03/08/2018
    End     : 03/08/2018
'''

class User(object):
    def __init__(self,myTuple,fromDB= False):
        if fromDB:
            self.id            = myTuple[0]
            self.email         = myTuple[1]
            self.update_period = myTuple[2]
            self.create_day    = myTuple[3]
            self.last_updated  = myTuple[4]
        else:           
            self.id            = myTuple[0]
            self.email         = "'"+myTuple[1]+"'"
            self.update_period = myTuple[2]
            self.create_day    = "'"+str(myTuple[3])+"'"
            self.last_updated  = "'"+str(myTuple[4])+"'"
    def to_sql_command(self):
        return """INSERT INTO USER VALUES ({},{},{},{},{})""".format(self.id,self.email,
                                         self.update_period,self.create_day,self.last_updated)     
                            
class Journal(object):
    def __init__(self,myTuple,fromDB= False):
        if fromDB:
            self.id   = myTuple[0]
            self.name = myTuple[1] 
        else:
            self.id   = myTuple[0]
            self.name = "'"+myTuple[1]+"'"
    def to_sql_command(self):
        return """INSERT INTO JOURNAL VALUES ({},{})""".format(self.id,self.name)
        
class Subscription(object):
    def __init__(self,myTuple,fromDB= False):
        if fromDB:
            self.id            = myTuple[0]
            self.user_id       = myTuple[1]
            self.journal_id    = myTuple[2]
            self.create_day    = myTuple[3]
        else:
            self.id            = myTuple[0]
            self.user_id       = myTuple[1]
            self.journal_id    = myTuple[2]
            self.create_day    = "'"+str(myTuple[3])+"'"
    def to_sql_command(self):
        return """INSERT INTO SUBSCRIPTION VALUES ({},{},{},{})""".format(self.id,self.user_id,
                                         self.journal_id,self.create_day)
