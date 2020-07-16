# sMythbot
sMythbot is a python script for use with the Mythtv project that allows for out-of-home control of a Mythtv DVR via the [Matrix Protocol](https://matrix.org/). Please see the project [wiki](https://github.com/shsorbom/sMythbot/wiki) for setup information. 

## Installation Prerequisites
This prerequisite guide assumes a modern version of Ubuntu (>= 18.04). You also neet to be running  version 0.28 or higher of Myth Tv.
If you are running 18.04, you will need to install version 3.8 or newer of python. 
I may add backwards compatability later, but for now, I reccomend installing [Pyenv](https://realpython.com/intro-to-pyenv/).   
Once you have Python set up, run the following commands in a BASH terminal:   
`sudo apt install libmariadbclient-dev`  
`pip3 install future`  
`pip3 install mysqlclient`  
`pip3 install matrix-nio`  
`pip3 install lxml`  
`pip3 install requests`  

Now we need to get the Mythtv source code:  
`git clone https://github.com/MythTV/mythtv`  
...Go to the directory where the API's we need are located:  
`cd ./mythtv/bindings/python/`  
...And install the python API  
`python3 setup.py install`  

## Known Bugs
* Currently sMythbot hangs if you are using a self-signed SSL Certificate. I recommend using LetsEncrypt, or disabling SSL checking in the `~/.smythbot/config.ini` file.

## Miscellaneous Warts
* E2E Encryption is not implemented yet
* sMythbot currently has the potential to output a lot of data to a room and not many ways to limit it. Please be courteous and keep this in mind when using sMythbot on a public homeserver. 
* All recording times are currently displayed in UTC. This will be fixed soon.
* Matrix room permissions are not implemented yet. Only allow room access to people you trust not to damage your DVR.

## Support
If you need any further assistance, you can find me in the [sMythbot Matrix Help Room](https://matrix.to/#/!PTdRVAqaNwJYXRkcYt:matrix.org?via=matrix.org)
