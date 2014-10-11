#!/usr/bin/python

import sys
import hashlib
import time
import argparse
import os
import logging                                                                                                                                                                               
from datetime import datetime, timedelta

#path to users data file
USERS_FILE = "/etc/openvpn/users.db"
LOG_FILE = "/var/log/openvpn/auth.log"
STAT_FILE="/etc/openvpn/statistics.log"

#init loggerAuth
try:
  loggerAuth = logging.getLogger('openvpn')    
  hdlr = logging.FileHandler(LOG_FILE)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s ',datefmt='%Y-%h-%d %H:%M:%S')
  hdlr.setFormatter(formatter)
  loggerAuth.addHandler(hdlr) 
  loggerAuth.setLevel(logging.DEBUG)
  
  loggerStat = logging.getLogger('statistics')
  hdlr = logging.FileHandler(STAT_FILE)
  formatter = logging.Formatter('%(asctime)s %(message)s',datefmt='%h-%d %H:%M:%S')
  hdlr.setFormatter(formatter)
  loggerStat.addHandler(hdlr) 
  loggerStat.setLevel(logging.DEBUG)
except:
  print "loggers failed"
  
#bytes convertor
def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size

#init parser
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--auth", help="recived from OpenVPN deamon path to file with user and passwd")
parser.add_argument("-g", "--generate", help="generate password; usage -g user:password")
parser.add_argument("-d", "--disconnect", help="client disconnect",action='store_true')
args = parser.parse_args()
    
# check uniq login in db
def chklogin(users, login):
    for i in range(len(users)):
        if (users[i].split(":")[0] == login):
            return 1
    return 0

#auth user
if args.auth:
    #check db file
    if os.path.isfile(USERS_FILE):
        if (os.path.getsize(USERS_FILE) == 0):
            loggerAuth.critical("db is empty")
            sys.exit(1)
    else:
        loggerAuth.critical("cannt find db")
        sys.exit(1)      
    #get info fron the opevpn deamon
    auth_data = [line.strip() for line in open(args.auth)]
    #read form db file
    users = [line.strip() for line in open(USERS_FILE)]
    #check login it db   
    if chklogin(users, auth_data[0]):
        login_db = auth_data[0]
    else:
        loggerAuth.critical("incorrect user")
        sys.exit(1)
    #check password    
    for i in range(len(users)):  # Second Example
        password_db = users[i].split(":")[1]
        # filePasss = sha512( md5(login) + sha512(md5(login) + sha512(passwd)) )
        hash_pwd = hashlib.sha512(hashlib.md5(login_db).hexdigest() + hashlib.sha512(hashlib.md5(login_db).hexdigest() + hashlib.sha512(auth_data[1]).hexdigest()).hexdigest()).hexdigest() 
        if(hash_pwd == password_db):
            loggerAuth.info("authorization successfully")
            sys.exit(0)
    loggerAuth.critical("incorrect password")
    sys.exit(1)

# add new user:password
if args.generate:
    login = args.generate.split(":")[0];
    pwd = args.generate.split(":")[1];
    #if file is not exists
    if not os.path.isfile(USERS_FILE):
        open(USERS_FILE, "w").close()
  
    if (chklogin([line.strip() for line in open(USERS_FILE)], login)):
        loggerAuth.error("login exists in db")
        sys.exit(1)
    else:       
        hash_pwd = hashlib.sha512(hashlib.md5(login).hexdigest() + hashlib.sha512(hashlib.md5(login).hexdigest() + hashlib.sha512(pwd).hexdigest()).hexdigest()).hexdigest() 
        open(USERS_FILE, "a+").write(login + ":" + hash_pwd + "\n")
        loggerAuth.info("user successfully added")
        sys.exit(0)
 
if args.disconnect:
  try:
    #https://community.openvpn.net/openvpn/wiki/Openvpn23ManPage
    res="------------------------------------------------------"
    res+="\n\tCommon name: "+os.environ['common_name']
    
    #IPs
    res+="\n\tVPN address: "+os.environ['ifconfig_pool_remote_ip']+" / "+os.environ['ifconfig_pool_local_ip']
    res+="\n\tClient address and port: "+os.environ['trusted_ip']+":"+os.environ['trusted_port']
   
    #traffic
    res+="\n\tTraffic usage: "+convert_bytes(os.environ['bytes_received'])+" reviced / "+convert_bytes(os.environ['bytes_sent'])+" sent"
  
    #Client  connection timestamp
    res+="\n\tClient connection timestamp: "+os.environ['time_ascii']
  
    #session time in seconds
    d = datetime(1,1,1) + timedelta(seconds=int(os.environ['time_duration']))
    res+= "\n\tClient session time:"+str(d.day-1)+"day " +str(d.hour)+"h "+str(d.minute)+"min "+str(d.second)+"sec"
    loggerStat.info(res)
    try:
  except:
    loggerStat.critical("cannt get info from environment variables")
    