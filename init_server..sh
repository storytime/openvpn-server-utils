#!/bin/bash

cp -rp openvpn /etc/openvpn

cd /tmp
wget  https://github.com/OpenVPN/easy-rsa/archive/master.zip 
unzip master.zip
cd easy-rsa-master

./build/build-dist.sh
tar zxvf EasyRSA-git-development.tgz
mv EasyRSA-git-development/ /etc/openvpn/
rm -rf /tmp/easy-rsa-master/

cd /etc/openvpn/EasyRSA-git-development
./easyrsa init-pki
./easyrsa build-ca
./easyrsa build-server-full server
./easyrsa gen-dh

openvpn --genkey --secret keys/ta.key