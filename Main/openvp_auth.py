#!/usr/bin/python
import sys
import hashlib
import time
import argparse
import os

#USERS_FILE = "/etc/openvpn/data/users.db"
#LOG_FILE = "/va/log/openvpn/auth.log"

#path to log file
LOG_FILE = "/home/pollux/tmp/auth.log"
#path to users db file (format user:password hash)
USERS_FILE = "/home/pollux/tmp/test2"

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--auth", help="openVPN auth")
parser.add_argument("-g", "--generate", help="generate password; usage -g user:password")
parser.add_argument("-v", "--verbose", help="increase output verbosity")

args = parser.parse_args()

# print to log
def log(msg):
    try:
        if args.verbose:
            print time.strftime("%Y-%m-%d %H:%M:%S")+ msg;
        f = open(LOG_FILE, 'a+')
        f.write(time.strftime("%Y-%m-%d %H:%M:%S") + msg + '\n')
        f.close()
    except:
        print "could not open log file!"
    
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
            log ("\tfile "+ USERS_FILE+"\tfile is empty:\tstop")
            sys.exit(1)
    else:
        log ("\tfile "+ USERS_FILE+"\t is not exists:\tstop")
        sys.exit(1)      
    #get info fron the opevpn
    auth_data = [line.strip() for line in open(args.auth)]
    #read form db file
    users = [line.strip() for line in open(USERS_FILE)]
    #check login it db   
    if chklogin(users, auth_data[0]):
        login_db = auth_data[0]
    else:
        log("\tincorrect login:" + auth_data[0]+"\tstop")
        sys.exit(1)
    #check password    
    for i in range(len(users)):  # Second Example
        password_db = users[i].split(":")[1]
        # filePasss = sha512( md5(login) + sha512(md5(login) + sha512(passwd)) )
        hash_pwd = hashlib.sha512(hashlib.md5(login_db).hexdigest() + hashlib.sha512(hashlib.md5(login_db).hexdigest() + hashlib.sha512(auth_data[1]).hexdigest()).hexdigest()).hexdigest() 
        if(hash_pwd == password_db):
            log("\tlogin: "+login_db + "\tauthorization successfully\tOK")
            sys.exit(0)
    log("\tlogin: " + login_db + "\tincorrect password\tstop")
    sys.exit(1)

# add new user:password
if args.generate:
    login = args.generate.split(":")[0];
    pwd = args.generate.split(":")[1];
    #if file  is not exists
    if not os.path.isfile(USERS_FILE):
        open(USERS_FILE, "w").close()
        
    if (chklogin([line.strip() for line in open(USERS_FILE)], login)):
        log ("\tlogin:" + login + " \texists" + "\tstop")
        sys.exit(1)
    else:       
        hash_pwd = hashlib.sha512(hashlib.md5(login).hexdigest() + hashlib.sha512(hashlib.md5(login).hexdigest() + hashlib.sha512(pwd).hexdigest()).hexdigest()).hexdigest() 
        open(USERS_FILE, "a+").write(login + ":" + hash_pwd + "\n")
        log("\tlogin:" + login + " \tis added" + "\tOK")
        sys.exit(0)
    