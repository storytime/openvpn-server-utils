#!/usr/bin/python
import sys
import hashlib
import time
import argparse
import os
import logging                                                                                                                                                                               

#path to users data file
USERS_FILE = "/tmp/users.db"
LOG_FILE = "/var/log/openvputils.log"

#init logger
try:
  logger = logging.getLogger('openvpn')                                                                                                                                                  
  hdlr = logging.FileHandler(LOG_FILE)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s ',datefmt='%Y-%h-%d %H:%M:%S')
  hdlr.setFormatter(formatter)
  logger.addHandler(hdlr) 
  logger.setLevel(logging.DEBUG)
except:
  print "logger failed"

#init parser
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--auth", help="recived from OpenVPN deamon path to file with user and passwd")
parser.add_argument("-g", "--generate", help="generate password; usage -g user:password")
parser.add_argument("-v", "--verbose", help="increase output verbosity")
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
            logger.critical("db is empty")
            sys.exit(1)
    else:
        logger.critical("cannt find db")
        sys.exit(1)      
    #get info fron the opevpn deamon
    auth_data = [line.strip() for line in open(args.auth)]
    #read form db file
    users = [line.strip() for line in open(USERS_FILE)]
    #check login it db   
    if chklogin(users, auth_data[0]):
        login_db = auth_data[0]
    else:
        logger.critical("incorrect user")
        sys.exit(1)
    #check password    
    for i in range(len(users)):  # Second Example
        password_db = users[i].split(":")[1]
        # filePasss = sha512( md5(login) + sha512(md5(login) + sha512(passwd)) )
        hash_pwd = hashlib.sha512(hashlib.md5(login_db).hexdigest() + hashlib.sha512(hashlib.md5(login_db).hexdigest() + hashlib.sha512(auth_data[1]).hexdigest()).hexdigest()).hexdigest() 
        if(hash_pwd == password_db):
            logger.info("authorization successfully")
            sys.exit(0)
    logger.critical("incorrect password")
    sys.exit(1)

# add new user:password
if args.generate:
    login = args.generate.split(":")[0];
    pwd = args.generate.split(":")[1];
    #if file is not exists
    if not os.path.isfile(USERS_FILE):
        open(USERS_FILE, "w").close()
  
    if (chklogin([line.strip() for line in open(USERS_FILE)], login)):
        logger.error("login exists in db")
        sys.exit(1)
    else:       
        hash_pwd = hashlib.sha512(hashlib.md5(login).hexdigest() + hashlib.sha512(hashlib.md5(login).hexdigest() + hashlib.sha512(pwd).hexdigest()).hexdigest()).hexdigest() 
        open(USERS_FILE, "a+").write(login + ":" + hash_pwd + "\n")
        logger.info("user successfully added")
        sys.exit(0)