#!/bin/bash

OVPN_ROOT='/etc/openvpn'
ERSA=$OVPN_ROOT/easy-rsa-release-2.x/easy-rsa/2.0
ERSA_KEYS=$ERSA/keys
SERVER_NAME="server"

cd
git clone https://github.com/storytime/openvpn-server-utils.git
cd openvpn-server-utils

rm -rf $OVPN_ROOT
mkdir -p $OVPN_ROOT
cp -rp openvpn/* $OVPN_ROOT

cd $OVPN_ROOT
wget https://github.com/OpenVPN//easy-rsa/archive/release/2.x.zip
unzip 2.x.zip  > /dev/null
rm 2.x.zip
cd $ERSA

source ./vars
./clean-all
./build-dh
./pkitool --initca
./pkitool --server $SERVER_NAME
openvpn --genkey --secret keys/ta.key

mkdir -p $OVPN_ROOT/keys
ln -s $ERSA_KEYS/ca.crt  $OVPN_ROOT/keys/ca.crt
ln -s $ERSA_KEYS/ta.key  $OVPN_ROOT/keys/ta.key
ln -s $ERSA_KEYS/dh2048.pem $OVPN_ROOT/keys/dh2048.pem
ln -s $ERSA_KEYS/$SERVER_NAME.key $OVPN_ROOT/keys/$SERVER_NAME.key
ln -s $ERSA_KEYS/$SERVER_NAME.crt $OVPN_ROOT/keys/$SERVER_NAME.crt

systemctl start openvpn@server

cd
rm openvpn-server-utils