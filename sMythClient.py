import asyncio
from importlib import util
from nio import (AsyncClient, SyncResponse, RoomMessageText)

class smythClient(object):
    response = None
    def __init__(self, homeserver, username, password):
        self.homeserver = homeserver
        self.username = username
        self.password = password
        self.client = AsyncClient(self.homeserver, self.username, ssl = False)
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
        #await self.sync_room_configs()
        #await self.client.sync_forever(timeout=30000)
        return

    async def sync_room_configs():
        """
        Name: Sync_room_configs
        Expected input: None
        Expected output: None (may change)
        Description: This function reads sMythbot room configurations from the rooms.ini file, or creates them. 
        Each room that sMythbot is part of can be configured with seperate properties.
        These properties will be updated as the bot's settings are changed.
        """
        pass
    
        
