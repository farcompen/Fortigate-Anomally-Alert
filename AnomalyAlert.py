#! /usr/bin python
# -*- coding:utf-8 -*-

import getpass
from pexpect import pxssh
import time
from datetime import datetime
from FortiMail import mail_gonder


giris="""

       -----------------------------------------------------
       ----------------------------------------------------
        *
        *     Anomaly Alert System    
        *
        *       Faruk GÜNGÖR - 2017 
        
        ---------------------------------------------------
        --------------------------------------------------
"""

def login(ip,username,passwd):
    try:
        session=pxssh.pxssh()
        session.force_password=True
        session.login(ip,username,passwd,auto_prompt_reset=False)
        print("Bağlantı Kuruldu. Lütfen bekleyiniz ..")
        dosya=open("anomaly_log.txt",'w')
        session.sendline("execute log filter category 7") #fortigate firewall  uses category 1 as default. we set it category 7 (anomaly)
        session.prompt()
        dosya.write(session.before)
        session.sendline("execute log filter device 2") #fortigate firewall users log device disk as default. we set 2 for fortianalyzer. Fortianalyzer için device 2 olacak
        session.prompt()
        dosya.write(session.before)
        session.sendline("execute log display") #collecting logs . logları getiriyoruz
        session.prompt()
        dosya.write(session.before)
        dosya.flush()
        dosya.close()

    except pxssh.ExceptionPexpect as e :
        print(str(e))



def log_oku():
    dosya=open("anomaly_log.txt",'r')
    a=0
    while(a==0):
        veri=dosya.readline().strip()
        if veri.startswith("1:"):
            global  ilk_veri
            if ilk_veri!=veri:
                ilk_veri=veri
                indeks=ilk_veri.find("srcip")
                ml=mail_gonder(ilk_veri[indeks:indeks+54])
                ml.mail()
                a=1
            else :
                print("yeni anomaly logu yok")
                a=1
        elif veri.startswith("0 logs found"):
            print(veri)
            a=1


print(giris)
ilk_veri="ilk veri"

firewall_ip=raw_input("Firewall Ip:\t")
user=raw_input("Username:\t")
parola=getpass.getpass("Password:\t")

while True:
    login(firewall_ip,user,parola)
    log_oku()
    zaman=datetime.now()
    print(zaman)
    print("*" * 50)
    time.sleep(120)


