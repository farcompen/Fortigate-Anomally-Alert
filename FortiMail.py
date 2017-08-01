#! /usr/bin/ python
# -*- coding:utf-8 -*-


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class mail_gonder():

    def __init__(self,mesaj):
        self.mesaj=mesaj


    def mail(self):

        gonderen = "sender e-mail"
        pswd = "sender e-mail passwd"
        alici = "receiver e mail "
        cc = "if you need add cc e-mail "
        body=self.mesaj
        messg = MIMEMultipart()
        messg['To'] = alici
        messg['Cc'] = cc
        messg['From'] = gonderen
        messg['Subject'] = "ANomaly tespit sistemi"

        text = MIMEText(body, 'plain')
        messg.attach(text)
        print(self.mesaj)
        try:
            server = smtplib.SMTP("smtp.live.com", 587)
            server.starttls()
            server.login(gonderen, pswd)
            server.sendmail(gonderen,[alici,cc,alici],messg.as_string())
            server.close()
            print("mail gönderildi")
        except smtplib.SMTPException as e:
            print(str(e))




