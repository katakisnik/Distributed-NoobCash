#!/usr/bin/env bash

MESSAGE='Connecting to machine number'

if [[ $1 == "1" ]]
then
	echo $MESSAGE 1
	ssh user@2001:648:2ffe:501:cc00:13ff:fecf:930
	exit 0
elif [[ $1 == "2" ]]
then
	echo $MESSAGE 2
	ssh user@2001:648:2ffe:501:cc00:13ff:fe06:3460
	exit 0
elif [[ $1 == "3" ]]
then
	echo $MESSAGE 3
	ssh user@2001:648:2ffe:501:cc00:13ff:fec0:1ee9
	exit 0
elif [[ $1 == "4" ]]
then
	echo $MESSAGE 4
	ssh user@2001:648:2ffe:501:cc00:13ff:fe39:6080
	exit 0 
else
	echo $MESSAGE 0
	ssh user@83.212.75.5 
	exit 0
fi
