import imaplib
import smtplib
import email
import getpass
import re
from email.mime.text import MIMEText
import time


mail = imaplib.IMAP4_SSL('imap.gmail.com')

# LOG IN VIA GMAIL

def log_in():
    mail.login(email_address, password)
    mail.select("INBOX")
    status, response = mail.search(None, '(UNSEEN)')
    unread_msg_num = response[0].split()
    return len(unread_msg_num)

# GET LAST N MESSAGES

def get_last_n_messages(n, ids_list):
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
    print "Sending message..."

    server.sendmail(email_address, recipient, email_text)
    server.quit()
    print "Email successfully sent to %s" %(message['To']) 

# CHECK IF EMAIL IS VALID

def check_valid_email(email_address):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email_address)
    if match == None:
        return False
    else:
        return True

# DISPLAY NUMBER OF ATTACHMENTS

def number_of_attachments(n, ids_list):
    last_email = len(ids_list) - 1
    attachment_count = 0
    for i in range(n):
        current_email_uid = ids_list[last_email - i]
        result, message_fetch = mail.uid('fetch', current_email_uid, '(RFC822)')
        raw_email = message_fetch[0][1]
        email_message = email.message_from_string(raw_email)
        for part in email_message.walk():
            if part.get('Content-Disposition'):
                attachment_count += 1
        if attachment_count == 0:
            print "No attachments found"
        else:
            print "%d attachments found" %(attachment_count) 
        attachment_count = 0

# DISPLAY PREVIEW OF MESSAGE

def display_preview(n, ids_list):
    last_email = len(ids_list) - 1
    for i in range(n):
        current_email_uid = ids_list[last_email - i]
        result, message_fetch = mail.uid('fetch', current_email_uid, '(RFC822)')
        raw_email = message_fetch[0][1]
        raw_email_string = raw_email.decode('utf-8')
        #continue inside the same for loop as above
        # converts byte literal to string removing b''
        email_message = email.message_from_string(raw_email_string)
        # this will loop through all the available multiparts in mail
        for part in email_message.walk():
            if part.get_content_type() == "text/plain": # ignore attachments/html
                email_body_text = part.get_payload(decode=True)
                print "PREVIEW OF EMAIL #", i+1, email_body_text.strip().split('\n')[0]

def read_email(ids_list):
    last_email = len(ids_list) - 1
    mail_number = int(input("Enter the number of mail you want to open ")) - 1
    current_email_uid = ids_list[last_email - mail_number]
    result, message_fetch = mail.uid('fetch', current_email_uid, '(RFC822)')
    raw_email = message_fetch[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    for part in email_message.walk():
        if part.get_content_type() == "text/plain": # ignore attachments/html
            email_body_text = part.get_payload(decode=True)
            print "CONTENT OF EMAIL IS: ", email_body_text

print
print
print "IMPLEMENTED TASKS: \n\n"
print "Log in \n"
print "Get number of unread messages\n"
print "Get last N received messages (display subject, date, sender)\n"
print "Send a message\n "
print "Display number of attachments \n"
print "Display preview of messages \n"
print "Display content of an email \n\n"


print "\t\tLOG IN\n"
email_address = raw_input("Enter your gmail address: ")
password = getpass.getpass("Enter your password: ")
print "Logging you in..."
unread_messages = log_in()
print "Hello, %s, you were successfully logged in!" %(email_address)

result, data = mail.uid('search', 'CHARSET', 'UTF-8', "ALL")
ids_list = data[0].split()
print "\t\tGET NUMBER OF UNREAD MESSAGES"
time.sleep(1.0)
print "You have %s unread messages" % (unread_messages)


print"\t\tGET LAST N RECEIVED MESSAGES"
n = input("How many emails do you want to fetch? ")
print "Fetching emails..."
get_last_n_messages(n, ids_list)

print "\t\tGET NUMBER OF ATTACHMENTS FROM EACH EMAIL"
time.sleep(0.5)
number_of_attachments(n, ids_list)
print

print "\t\tPREVIEW EACH MESSAGE"
print "Displaying preview..."
time.sleep(0.5)
display_preview(n, ids_list)
print

print"\t\tSEND A MESSAGE\n"
send_message()

print"\t\tDISPLAY CONTENT OF AN EMAIL\n"
read_email(ids_list)



