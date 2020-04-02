# Distributed-NoobCash

*Created by*: [Nikiforos Katakis](https://github.com/katakisnik) *&* [Dimitris Katsiros](https://www.github.com/DimitrisKatsiros) .

### Dependencies

&ndash; `sudo apt-get install python3 python3-pip python3-requests python3-virtualenv`

&ndash; `virtualenv venv`

&ndash; `pip3 install -r requirements.txt`


### Usage

&ndash; Open a terminal and connect to the VirtualMachine.

&ndash; Activate the virtual environment

​	 `source venv/bin/activate`

&ndash; Start server at [HOST]:[PORT]

​	 `python manage.py runserver [HOST]:[PORT]` 

&ndash; Open a new terminal to use client.

​	 `python client.py [PORT] [NUMBER]`

​	`[NUMBER]` : *number of participants* if you are setting up the coordinator, otherwise *0*



### Client

##### You can use client in order to control the transactions. Client provides the following:

&ndash; `source [number]` 			Read source file.

&ndash; `view`									Print current blockchain

&ndash;`balance`							   Print current balance

&ndash;`exit` 									Exit client. Server continues running.



### Settings 

##### You can always change the settings in `src/trydjango/nbcsettings.py `

`BLOCK_CAPACITY` : Set max transactions contained in a block in blockchain

`DIFFICULTY` : Set difficulty in computing nonce. 

`COORDINATOR_PORT` : Set the coordinator port 

`CORDINATOR` : Set the coordinator's `[HOST]` 

`SOURCE_INPUTS_PATH` : Path which contains the source files for client



### Scripts

##### Some scripts are provided in order to automate some things

&ndash; `plot_diagram.py` : Create diagrams using the statistics saved in `blocktimes.txt`

&ndash; `runserver.sh` : Activates the virtual environment. Then runs 2 servers using `[HOST]` depending on the 								machine's hostname, in the background. Ports used: *8000* and *8001*. 

​								If `-k` is given as an argument, kills all servers running in the background.

&ndash; `client.sh` : If `1` is given as an argument, starts a client on port *8000*. Otherwise on port *8001*.

&ndash; `force_close_ports.sh` : Closes possible open tcp ports on *8000* and *8001*.

&ndash; `ssh_now.sh` : Given an argument `[n]` attempts an ssh connection to the n'th virtual machine.

​							It is useful to provide an RSA key in virtual machines `.ssh/known_hosts`.

&ndash; `update_machine.sh` : Updates all files of each VM in the local network. In order to speed things up

​											the script uses `rsync` , updating only difs since the last version.