#!/bin/bash

if [ "$(id -u)" != "0" ]; then
	echo "Sorry, you are not root."
	exit 1
fi

OVPN_ROOT='/etc/openvpn'
ERSA='/etc/openvpn/EasyRSA-git-development'
ERSA_NAME="EasyRSA-git-development"
ERSA_K='/etc/openvpn/EasyRSA-git-development/pki'
ERSA_HOME='/etc/openvpn/EasyRSA-git-development/easyrsa'

rm -rf $OVPN_ROOT/
mkdir -p $OVPN_ROOT/

cp -rp openvpn/* $OVPN_ROOT/
cd /tmp
wget  https://github.com/OpenVPN/easy-rsa/archive/master.zip 
unzip master.zip  > /dev/null
cd easy-rsa-master

./build/build-dist.sh
tar zxvf $ERSA_NAME.tgz > /dev/null
rm -rf $ERSA >> /dev/null
mv $ERSA_NAME/ $OVPN_ROOT/

rm -rf /tmp/easy-rsa-master/
rm /tmp/master.zip

cd $ERSA
$ERSA_HOME init-pki
$ERSA_HOME build-ca
$ERSA_HOME build-server-full server nopass
$ERSA_HOME gen-dh

cd $OVPN_ROOT
mkdir -p $OVPN_ROOT/keys
openvpn --genkey --secret keys/ta.key

ln -s $ERSA_K/ca.crt  $OVPN_ROOT/keys/ca.crt
ln -s $ERSA_K/dh.pem $OVPN_ROOT/keys/dh2048.pem
ln -s $ERSA_K/private/server.key $OVPN_ROOT/keys/server.key
ln -s $ERSA_K/issued/server.crt $OVPN_ROOT/keys/server.crt

/etc/init.d/openvpn restart