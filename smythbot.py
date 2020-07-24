#!/usr/bin/env python3
import os
import configparser
import asyncio
from sMythClient import smythClient

smythbot_version = "0.0.1"

async def genCfg(cfgPath):
    os.makedirs(os.path.dirname(cfgPath), exist_ok=True) #TODO: Surround this in try-catch block
    print("config dir made. ")
    mCfg = configparser.ConfigParser()
    mCfg["MythTvProperties"] = {"Host Name": "mythbox", "IP Address": "127.0.0.1", "Mythbackend Port": "6544", "MythFrontend Port":"6547"}
    mCfg["Matrix Settings"] = {"Server Name": "127.0.0.1","User Name":"username", "Password": "password", "SSL Check": True} 
    with open(cfgPath, "w") as configfile:
        mCfg.write(configfile)


async def main():
    # Obligatory Setup
    #------------------
    print("Welcome to sMythbot, Version 0.0.1")
    print("Checking for sMythbot configuration settings...")
    cfgFilePath = os.path.expanduser("~/.smythbot/config.ini") # TODO: Rewrite this statement for non POSIX systems
    cfgExists = os.path.exists(cfgFilePath)
    print (cfgFilePath)
    # TODO: Add argparser, the above settings are temporary
    if not cfgExists:
        await(genCfg(cfgFilePath))
        print("Error: no default configuration found.")
        print("A defaut configuration file was generated at " + cfgFilePath)
        print("Set your desired values and run this program again.")
        return
    print("Config found at: " + cfgFilePath)
    botCfg = configparser.ConfigParser()
    botCfg.read(cfgFilePath)
    print('Loading configuration.')
    matrix_bot = smythClient(botCfg["Matrix Settings"]["Server Name"], botCfg["Matrix Settings"]["User Name"], botCfg["Matrix Settings"]["Password"], use_ssl = botCfg.getboolean("Matrix Settings", "SSL Check"))
    await matrix_bot.start_client()
    await matrix_bot.client.close()
    #print(matrix_bot.response)
    
    
    
    
    
asyncio.get_event_loop().run_until_complete(main())
