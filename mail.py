import imaplib
import email
from email.header import decode_header
import time
import converters
import dictionaries
import re

import os
from imbox import Imbox
import traceback

import pathlib
directory = pathlib.Path(__file__).parent.absolute()

from os import listdir
from os.path import isfile, join

import pygame
import shutil


# account credentials
host = "imap.gmail.com"
username = "YOUR USERNAME"
password = "YOUR PASSWORD"
download_folder = str(directory) + r"\Mail_audio"

if not os.path.isdir(download_folder):
    os.makedirs(download_folder, exist_ok=True)


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

# The get_mail function is a connection of many stackoverflow answers and it probably could have been made more clear
# Essentially, it checks your email and outputs a list with last 2 mails - [subject1, body1, subject2, body2]
# It's more of a setup function, because the next one, find_new_mail() also uses this one and then compares the outputs
# to notice if there was any new mail
def get_email():
    global list_get_mail
    list_get_mail = []
    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)

    status, messages = imap.select("INBOX")
    # number of top emails to fetch
    N = 2
    # total number of emails
    messages = int(messages[0])

    for i in range(messages, messages-N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                # print("Subject:", subject)
                # print("From:", From)

                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        # if content_type == "text/plain":
                            # print(body)

                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    # if content_type == "text/plain":
                        # print only text email parts
                        # print(body)
                list_get_mail.append(subject)
                list_get_mail.append(converters.html_mail_clear(body))
    # close the connection and logout
    imap.close()
    imap.logout()
    return list_get_mail

# As I said earlier, this function uses get_mail() to check if there is any new mail. The tricky part is that it returns
# different lists according to whether there is new mail or not
# - no new mail - returns an empty list
# - 1 new mail - returns a two-item list [new_subject, new_body)
# - 2 or more new mail - returns a four-item list [new_sub1, new_body1, new_sub2, new_body2]
def find_new_mail():
    global list_get_mail
    global last_subject
    global last_body
    get_mail = get_email()
    get_mail[1] = converters.html_mail_clear(get_mail[1])
    get_mail[3] = converters.html_mail_clear(get_mail[3])
    try:
        last_subject
    except NameError:
        last_subject = get_mail[0]
        last_body = get_mail[1]
    if last_subject == get_mail[0] and last_body == get_mail[1]:
        print("No mail recorded! Skipping...")
        return []
    elif last_subject == get_mail[2] and last_body == get_mail[3]:
        print("One new mail found!")
        last_subject = get_mail[0]
        last_body = get_mail[1]
        list_get_mail = get_mail
        return [last_subject, last_body]
    else:
        print("At least 2 new mail found!")
        last_subject = get_mail[0]
        last_body = get_mail[1]
        list_get_mail = get_mail
        return list_get_mail

# This function simply deletes all the mails with a given subject. It also deletes the download folder for
# attachments from mail. It's used to download all attachments, play them and then delete everything to not loop again
def deleteemail(subject):
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)

    imap.select()

    typ, data = imap.search(None, 'Subject "{}"'.format(subject))
    for num in data[0].split():
        imap.store(num, '+FLAGS', r'(\Deleted)')
    imap.expunge()

    imap.close()
    imap.logout()

    shutil.rmtree(download_folder)


# This function is used to download all attachments that are on your mail. They are deleted later with the function
# above
def download_attach():
    if not os.path.isdir(download_folder):
        os.makedirs(download_folder, exist_ok=True)
    mail = Imbox(host, username=username, password=password, ssl=True, ssl_context=None, starttls=False)
    messages = mail.messages()  # defaults to inbox

    for (uid, message) in messages:
        mail.mark_seen(uid)  # optional, mark message as read

        for idx, attachment in enumerate(message.attachments):
            try:
                att_fn = attachment.get('filename')
                download_path = f"{download_folder}/{att_fn}"
                print(download_path)
                with open(download_path, "wb") as fp:
                    fp.write(attachment.get('content').read())
            except:
                print(traceback.print_exc())

    mail.logout()

# This is a weird function, because it's only useful for our case, which is Jarvis. This function uses all of the
# previously mentioned, to check for new mail, download any new attachments, play them, delete them and also check
# for mail with 'Human Input' subject, so that Jarvis can generate (or say) the body of this mail
def jarvis_mail():
    get_email()
    dict_output = dictionaries.mail_dict(find_new_mail())
    # print(dict_output)
    human_input = []
    if "ATTACHMENT" in dict_output:
        download_attach()
        onlyfiles = [f for f in listdir(download_folder) if isfile(join(download_folder, f))]
        deleteemail("Received audio")

        for item in onlyfiles:
            pygame.mixer.init()
            my_sound = pygame.mixer.Sound(str(directory) + r"\Mail_audio\\" + str(item))
            my_sound.play()
            pygame.time.wait(int(my_sound.get_length() * 1000))



    for item in dict_output:
        i = dict_output.index(item)
        if "Human Input" in dict_output[i]:
            dict_output[i] = dict_output[i].replace("Human Input: ", "")
            human_input.append(dict_output[i])
    return human_input


