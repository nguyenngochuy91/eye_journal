#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Send digest module
    Start   : 03/08/2018
    End     : 08/08/2018
'''
import smtplib
try:
    from email.MIMEText import MIMEText
except: 
    from email.mime.text import MIMEText
import codecs


'''@function: sending digest
   @input   : diction
   @output  : none
'''    
def send_digest(json_file, from_addr,username,password,to_addr):
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
