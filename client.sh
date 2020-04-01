#!/usr/bin/env bash

# Access Folder
cd src/

if [[ $1 == '1' ]]
then
	# Starting servers
	if [[ $HOSTNAME == "PC1" ]]
	then
		python cli.py 192.168.1.5 8000 10

	elif [[ $HOSTNAME == "PC2" ]]
	then
		python cli.py 192.168.1.1 8000 0

	elif [[ $HOSTNAME == "PC3" ]]
	then
		python cli.py 192.168.1.4 8000 0

	elif [[ $HOSTNAME == "PC4" ]]
	then
		python cli.py 192.168.1.2 8000 0

	elif [[ $HOSTNAME == "PC5" ]]
	then
		python cli.py 192.168.1.3 8000 0


	else
		echo 'Not in VM'
		echo 'exiting script..'
	fi

else

	# Starting servers
	if [[ $HOSTNAME == "PC1" ]]
	then
		python cli.py 192.168.1.5 8001 0
	elif [[ $HOSTNAME == "PC2" ]]
	then
		python cli.py 192.168.1.1 8001 0
	elif [[ $HOSTNAME == "PC3" ]]
	then
		python cli.py 192.168.1.4 8001 0
	elif [[ $HOSTNAME == "PC4" ]]
	then
		python cli.py 192.168.1.2 8001 0
	elif [[ $HOSTNAME == "PC5" ]]
	then
		python cli.py 192.168.1.3 8001 0

	else
		echo 'Not in VM'
		echo 'exiting script..'
	fi

fi

# Return to previous folder
cd ..
