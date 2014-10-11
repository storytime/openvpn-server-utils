#!/bin/bash

# $1 = action (up down)

if [ "$1" = "up" ]
then
	echo "up"
	/sbin/iptables -A FORWARD -s 10.19.19.0/24 -j ACCEPT
	/sbin/iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
	/sbin/iptables -t nat -A POSTROUTING -s 10.19.19.0/24 -o eth0 -j MASQUERADE
	echo 1 > /proc/sys/net/ipv4/ip_forward
elif [ "$1" = "down" ]
then
	echo "down"
        /sbin/iptables -D FORWARD -s 10.19.19.0/24 -j ACCEPT
        /sbin/iptables -D FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
        /sbin/iptables -t nat -D POSTROUTING -s 10.19.19.0/24 -o eth0 -j MASQUERADE
	echo 0 > /proc/sys/net/ipv4/ip_forward
fi	