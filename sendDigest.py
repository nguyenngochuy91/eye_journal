#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Send digest module
    Start   : 03/08/2018
    End     : 08/08/2018
'''
import smtplib
import argparse
try:
    from email.MIMEText import MIMEText
except: 
    from email.mime.text import MIMEText
import codecs
# argument parsing
def get_arguments():
    parser = argparse.ArgumentParser(description='The purpose of this program is to send digest of the most recent articles from subscribed article given user research topic')
    
    parser.add_argument("-i", "--input", 
                help="json file of the digest") 
    parser.add_argument("-u", "--username", 
                help="username/ email address of the sender") 
    parser.add_argument("-p", "--password", 
                help="password of the user") 
    parser.add_argument("-t", "--toAddr", 
                help="email address of the receiver")                                  
    return parser.parse_args()


'''@function: sending digest
   @input   : a lot
   @output  : none
'''    
def send_digets(json_file, from_addr,username,password,to_addr):
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(username,password)
#    with open(json_file) as data_file:
#        journal_article = json.load(data_file)
#    print (json.dumps(journal_article))
    f = codecs.open(json_file, "r", "utf-8")
    msg = MIMEText(f.read().rstrip("\n"), 'html', 'utf-8')
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "New digest"
    msg.set_charset('utf-8')
    server.sendmail(from_addr, to_addr,msg.as_string())
    server.quit()  
    
'''@function: given the dictionary of articles, we pretify this using json with html thingy
   @input   : articles(dic)
   @output  : articles(dic) 
'''  
def add_html(json_file):
    return json_file

if __name__ == '__main__':
    args      = get_arguments()
    json_file = args.input
    username  = args.username
    password  = args.password
    to_addr   = args.toAddr
    send_digets(json_file, username,username,password,to_addr)