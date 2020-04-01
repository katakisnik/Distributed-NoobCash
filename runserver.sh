#!/usr/bin/env bash

# Check mode
if [[ $1 == '-k' ]]
then
	pkill -f python
	echo 'Killed all django subprocess'
	return 1
fi

# Check virual environment
echo "Checking virtual environment.."
if [[ "$VIRTUAL_ENV" == "" ]]
then
  source './venv/bin/activate'
	echo 'virtual environment activated'
else
  echo 'Already in virtual environment'
fi

# Access Folder
cd src/

# Starting servers
if [[ $HOSTNAME == "PC1" ]]
then
	echo 'Starting Server 1'
	python manage.py runserver 192.168.1.5:8000 2>/dev/null &
	echo 'Starting Server 2'
	python manage.py runserver 192.168.1.5:8001 2>/dev/null &
elif [[ $HOSTNAME == "PC2" ]]
then
	echo 'Starting Server 1'
	python manage.py runserver 192.168.1.1:8000 2>/dev/null &
	echo 'Starting Server 2'
	python manage.py runserver 192.168.1.1:8001 2>/dev/null &
elif [[ $HOSTNAME == "PC3" ]]
then
	echo 'Starting Server 1'
	python manage.py runserver 192.168.1.4:8000 2>/dev/null &
	echo 'Starting Server 2'
	python manage.py runserver 192.168.1.4:8001 2>/dev/null &
elif [[ $HOSTNAME == "PC4" ]]
then
	echo 'Starting Server 1'
	python manage.py runserver 192.168.1.2:8000 2>/dev/null &
	echo 'Starting Server 2'
	python manage.py runserver 192.168.1.2:8001 2>/dev/null &
elif [[ $HOSTNAME == "PC5" ]]
then
	echo 'Starting Server 1'
	python manage.py runserver 192.168.1.3:8000 2>/dev/null &
	echo 'Starting Server 2'
	python manage.py runserver 192.168.1.3:8001 2>/dev/null &

else
	echo 'Not in VM'
	echo 'exiting script..'
fi

# Return to previous folder
cd ..
