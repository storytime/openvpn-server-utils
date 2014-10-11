import sys
import subprocess

CLIENT_CN = sys.argv[1]
SEP = '==========> '
cmd = 'cd EasyRSA-git-development/; ./easyrsa build-client-full ' + CLIENT_CN + ' nopass'
print SEP+cmd

if subprocess.call(cmd, shell=True):
    print SEP+"CN in use"
    sys.exit()

print SEP+"Data has been generated: "+CLIENT_CN

TA_PLACEHOLDER = 'placeholder_ta'
CA_PLACEHOLDER = 'placeholder_ca'
CL_KEY_PLACEHOLDER = 'placeholder_ck'
CL_CR_PLACEHOLDER = 'placeholder_crt'
BS = '-----BEGIN CERTIFICATE-----'
CONFIG_TEMPLATE = 'client.ovpn'
TA_FILE = 'ta.key'
CA = 'ca.key'
RES_FILE = CLIENT_CN+".ovpn"

CLIENT_KEY_FILE = 'EasyRSA-git-development/pki/private/'+CLIENT_CN+".key"
CLIENT_CER_FILE = 'EasyRSA-git-development/pki/issued/'+CLIENT_CN+".crt"

contents = open(CONFIG_TEMPLATE, "r+").read()
infile = open(RES_FILE, 'w+')

# tls key
taKey = open(TA_FILE, 'r').read()[:-1]
#taKey = taKey.split(TA_HEAD)[-1].split(TA_TAIL)[0]  #format string

# CA isnt encrypted
serverCa = open(CA, 'r').read()[:-1]

# client key
clientKey = open(CLIENT_KEY_FILE, 'r').read()[:-1]

# client cert
clientCert = BS+open(CLIENT_CER_FILE, 'r').read()[:-1].split(BS)[-1][:-1]

resultConfig = contents.replace(TA_PLACEHOLDER, taKey)
resultConfig = resultConfig.replace(CA_PLACEHOLDER, serverCa)
resultConfig = resultConfig.replace(CL_KEY_PLACEHOLDER, clientKey)
resultConfig = resultConfig.replace(CL_CR_PLACEHOLDER, clientCert)

infile.write(resultConfig)
infile.close()
print SEP+"Client: "+RES_FILE