# Mythbot
Mythbot is a python script for use with the Mythtv project that allows for out-of-home control of a Mythtv DVR via various messaging back ends. I plan to support the IMAP/SMTP and Matrix protocols. Ideally, the bot will be modular enough to add more protocols in the future.

## Installation Prerequisites
This prerequisite guide assumes a modern version of ubuntu.
Run the following commands in a BASH terminal 
`sudo apt install libmariadbclient-dev`
`pip3 install future`
`pip3 install mysqlclient`
Now we need to get the Mythtv source code:
`git clone https://github.com/MythTV/mythtv`
...Go to the directory where the API's we need are located:
`cd ./mythtv/bindings/python/`
...And install the python API
`sudo python3 setup.py install`
