import imaplib
import email
import getpass
import re
import base64
import smtplib
from email.mime.text import MIMEText


mail = imaplib.IMAP4_SSL('imap.gmail.com')
email_address = raw_input("Enter your gmail address: ")
password = getpass.getpass("Enter your password: ")



#https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/

# LOG IN VIA GMAIL

def log_in():
	mail.login(email_address, password)
	mail.select("INBOX")
	result, data = mail.search(None, '(UNSEEN)')
	#print "Hello, " + email_address
	print 
	print "You have " + str(len(data[0].split())) + " unread messages"
	

# GET LAST N MESSAGES

def get_last_n_messages():
    n = int(input("How many emails do you want to fetch? "))
    result, data = mail.uid('search', 'CHARSET', 'UTF-8', "ALL")
    ids_list = data[0].split()
    last_email = len(ids_list) - 1
    for i in range(n):
        current_email_uid = ids_list[last_email - i]
        result, message = mail.uid('fetch', current_email_uid, '(RFC822)')
        raw_email = message[0][1]
        email_message = email.message_from_string(raw_email)
        print "Email #", i+1
        print "Date: ",  email_message['Date']
        print "Subject: ", email_message['Subject']
        print "Sender: ", email.utils.parseaddr(email_message['From'])
        print

       
# SEND A MESSAGE

def send_message():
    message = MIMEText(raw_input("Enter the text of your e-mail: "))

    message['Subject'] = raw_input("Enter the subject of your e-mail: ")
    recipient = raw_input("Enter recipient e-mail:  ")
    message['To'] = recipient
    while check_valid_email(recipient)==False:
        recipient = raw_input("Please enter a valid e-mail:  ")
    message['CC'] = raw_input("Enter Carbon Copy e-mail (CC) (not manadatory): ")
    message['From'] = email_address
    email_text = message.as_string()
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email_address, password)
    server.sendmail(email_address, recipient, email_text)
    server.quit()

# CHECK IF EMAIL IS VALID

def check_valid_email(email_address):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email_address)
    if match == None:
        return False
    else:
        return True


log_in()
get_last_n_messages()
send_message()