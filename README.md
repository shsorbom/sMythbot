# sMythbot
Mythbot is a python script for use with the Mythtv project that allows for out-of-home control of a Mythtv DVR via various messaging back ends. I plan to support the IMAP/SMTP and Matrix protocols. Ideally, the bot will be modular enough to add more protocols in the future.

## Installation Prerequisites
This prerequisite guide assumes a modern version of Ubuntu (>= 18.04).
If you are running 18.04, you will need to install version 3.8 or newer of python. 
I may add backwards compatability later, but for now, I reccomend installing [Pyenv](https://realpython.com/intro-to-pyenv/).   
Once you have Python set up, run the following commands in a BASH terminal:   
`sudo apt install libmariadbclient-dev`  
`pip3 install future`  
`pip3 install mysqlclient`  
`pip3 install matrix-nio`  

Now we need to get the Mythtv source code:  
`git clone https://github.com/MythTV/mythtv`  
...Go to the directory where the API's we need are located:  
`cd ./mythtv/bindings/python/`  
...And install the python API  
`python3 setup.py install`  
