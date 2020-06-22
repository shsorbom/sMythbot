import asyncio
import os
import configparser
from importlib import util
from nio import (AsyncClient, SyncResponse, RoomMessageText)
import smythbotCommandRunner

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

        # Declare the nessescary variables:
        self.isSynced = False
        self.smythbot_handler = "!smythbot"

        #Add callbacks
        self.client.add_event_callback(self.onNewMatrixEventReccieved, RoomMessageText)
        sync_event = asyncio.create_task(self.watch_for_sync(self.client.synced))

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
        await self.client.sync_forever(timeout=30000, full_state=True)
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
                await self.populateRoomConfigs(room_id, False)
        if newDataWritten:
            await self.writeChangesToDisk()
        else:
            print ("No new room configurations found") 


    async def populateRoomConfigs(self, room_id, writeToDisk):
        self.smythbotRoomConfigs[room_id] = {}
        self.smythbotRoomConfigs[room_id]["MythTv Backend address"] = "None"
        self.smythbotRoomConfigs[room_id]["MythTv Backend Port"] = "6544"
        self.smythbotRoomConfigs[room_id]["Room Notifications"] = "False"
        print("Added new room Configuration " + room_id)
        if writeToDisk:
           await self.writeChangesToDisk()
        return
        
    async def writeChangesToDisk(self):
        print("Writing New data to file: " + self.roomConfigsPath)
        with open(self.roomConfigsPath, "w") as roomsFile:
            self.smythbotRoomConfigs.write(roomsFile)

    async def watch_for_sync(self, sync_event):
        """
        Input: AsyncClient Sync Event
        Output: None
        Description: When AsyncClient fires a synced event (which only happens during a "sync_forever" loop), this function is called.
        """
        while True:
            await sync_event.wait()
            
            await self.onIsSyncedCalled()
            
            
    
    async def onIsSyncedCalled(self):
        """
        Called from the "watch_for_sync" event. This funtion sets the client state as being up to speed with 
        the current messages.
        """
        print ("We are synced!")
        self.isSynced = True
        return

    async def onNewMatrixEventReccieved(self, room, event):
        print("New Event")
        if self.isSynced and event.body.startswith(self.smythbot_handler):
            await self.client.room_send(room.machine_name, "m.room.message", await self.reply("<h1>Command reccieved</h1>")) #debug
            print("DEBUG: New command: " + event.body)
            #Debugging:
            command_list = []
            command_list.append("<h1>Test Reply 1</h1>")
            command_list.append("<h1>Test Reply 2</h1>")
            command_list.append("<h1>Test Reply 3</h1>")
            for item in command_list:
                await self.client.room_send(room.machine_name, "m.room.message", await self.reply(item))
        else:
            return

    async def reply(self, reply_body):
        reply_content = {}
        reply_content["msgtype"] = "m.notice"
        reply_content["body"] =""
        reply_content["format"] = "org.matrix.custom.html"
        reply_content["formatted_body"] = reply_body
        return reply_content

