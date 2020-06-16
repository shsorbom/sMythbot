import asyncio
import os
import configparser
from importlib import util
from nio import (AsyncClient, SyncResponse, RoomMessageText)

class smythClient(object):
    response = None
    def __init__(self, homeserver, username, password):
        self.homeserver = homeserver
        self.username = username
        self.password = password
        self.client = AsyncClient(self.homeserver, self.username, ssl = False)
        

        #Initialize per room configurator
        self.roomConfigsPath = os.path.expanduser("~/.mythbot/rooms.ini")
        self.smythbotRoomConfigs = configparser.ConfigParser()
        self.roomCfgDefaults = self.get_default_room_options_for_smythbot()
        return

    async def init_login(self):
        self.response = await self.client.login(self.password)
        return
    
    async def start_client(self):
        """
        Name: start_client
        Expected input: None
        Expected output: None (may change)
        Description: This function is meant to be called in the main program loop
        It's job is to start all the other functions asscociated with the Matrix client
        end of sMythbot.
        First it calls the init_login function. If that is successful, it will request 
        a list of available rooms that we have joined to check for configuration options
        (which will be checked via other functons). When that is done, it will start the
        synchronization loop in AsyncClient and return
        """
        
        await self.init_login()
        await self.sync_room_configs()
        #await self.client.sync_forever(timeout=30000)
        return

    async def sync_room_configs(self):
        """
        Name: Sync_room_configs
        Expected input: None
        Expected output: None (may change)
        Description: This function reads sMythbot room configurations from the rooms.ini file, or creates them. 
        Each room that sMythbot is part of can be configured with seperate properties.
        These properties will be updated as the bot's settings are changed.
        """
        # Fire an initial sync to get a rooms list:
        first_sync = await self.client.sync(300000)
        # Then we check if roooms.ini exists.  
        if os.path.exists(self.roomConfigsPath):
            self.smythbotRoomConfigs.read(self.roomConfigsPath) #If so, we read the existing values into the configparser

        for room_id in first_sync.rooms.join: # Now we check for individual room configurations via the existence of a room ID in the file
            # First, the easy part. If a room ID DOES NOT exist, we can safely assume there are no config options for it yet:
            newDataWritten = False
            if not self.smythbotRoomConfigs.has_section(room_id):
                newDataWritten = True
                self.smythbotRoomConfigs[room_id] = {}
                self.smythbotRoomConfigs[room_id]["MythTv Backend address"] = "None"
                self.smythbotRoomConfigs[room_id]["MythTv Backend Port"] = "6544"
                self.smythbotRoomConfigs[room_id]["Room Notifications"] = "False"
                print("Added new room Configuration " + room_id)
                
        if newDataWritten:
            print("Writing New data to file: " + self.roomConfigsPath)
            with open(self.roomConfigsPath, "w") as roomsFile:
                self.smythbotRoomConfigs.write(roomsFile) 
        else:
            print ("No new room configurations found") 


    def get_default_room_options_for_smythbot(self):
        """
        NOTE: Not used, I may delete this
        Name: get_default_room_options_for_smythbot
        Expected input: None
        Expected output: dict of all room configuration options and their default values
        Description: used internally for updating out of date room configurations.
        """
        roomOptsDict = {}
        roomOptsDict["Backend URL"] = "None"
        roomOptsDict["Backend Port"] = 6544
        roomOptsDict["Notifications"] = False
        return roomOptsDict
        



           
