#!/usr/bin/python

import sys
import subprocess
import os

CLIENT_CN = sys.argv[1]
SEP = '==========> '
OVPN_ROOT='/etc/openvpn/'
ERSA=OVPN_ROOT+'EasyRSA-git-development/pki/'

TA_PLACEHOLDER = 'placeholder_ta'
CA_PLACEHOLDER = 'placeholder_ca'
CL_KEY_PLACEHOLDER = 'placeholder_ck'
CL_CR_PLACEHOLDER = 'placeholder_crt'
CONFIG_TEMPLATE = OVPN_ROOT+'client/template.ovpn'
TA_FILE = OVPN_ROOT+'keys/ta.key'
CA = OVPN_ROOT+'keys/ca.crt'
RES_FILE = OVPN_ROOT+'client/'+CLIENT_CN+".ovpn"

CLIENT_KEY_FILE = ERSA+'private/'+CLIENT_CN+".key"
CLIENT_CER_FILE = ERSA+'issued/'+CLIENT_CN+".crt"

if not os.geteuid() == 0:
    sys.exit('Script must be run as root')

cmd = 'cd EasyRSA-git-development/; ./easyrsa build-client-full ' + CLIENT_CN + ' nopass'
print SEP+cmd

if subprocess.call(cmd, shell=True):
    print SEP+"CN in use"
    sys.exit()

print SEP+"Data has been generated: "+CLIENT_CN

#contents = open(CONFIG_TEMPLATE, "r+").read()
conf = open(RES_FILE, 'w+')

# tls key
taKey = open(TA_FILE, 'r').read()[:-1]
# CA isnt encrypted
serverCa = open(CA, 'r').read()[:-1]
# client key
clientKey = open(CLIENT_KEY_FILE, 'r').read()[:-1]
# client cert
clientCert = open(CLIENT_CER_FILE, 'r').read()[:-1]

resultConfig = open(CONFIG_TEMPLATE, "r+").read().replace(TA_PLACEHOLDER, taKey)
resultConfig = resultConfig.replace(CA_PLACEHOLDER, serverCa)
resultConfig = resultConfig.replace(CL_KEY_PLACEHOLDER, clientKey)
resultConfig = resultConfig.replace(CL_CR_PLACEHOLDER, clientCert)

conf.write(resultConfig)
conf.close()
open(OVPN_ROOT+'ccd/'+CLIENT_CN, 'w').close()
 
print SEP+"Client: "+RES_FILE