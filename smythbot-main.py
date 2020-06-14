import os
import configparser
import asyncio
from sMythClient import smythClient


async def genCfg(cfgPath):
    os.makedirs(os.path.dirname(cfgPath), exist_ok=True) #TODO: Surround this in try-catch block
    print("config dir made. ")
    mCfg = configparser.ConfigParser()
    mCfg["MythTvProperties"] = {"Host Name": "mythbox", "IP Address": "127.0.0.1", "Mythbackend Port": "6544", "MythFrontend Port":"6547"}
    mCfg["IMAP Settings"] = {"Sever IP": "127.0.0.1","Username":"username", "Password": "password", "Security": "ssl"}
    mCfg["SMTP Settings"] = {"Sever IP": "127.0.0.1","Username":"username", "Password": "password", "Security": "startls", "Email Address": "email@example.com"}
    mCfg["Matrix Settings"] = {"Server Name": "127.0.0.1","User Name":"username", "Password": "password"}
    with open(cfgPath, "w") as configfile:
        mCfg.write(configfile)


async def main():
    # Obligatory Setup
    #------------------

    cfgFilePath = os.path.expanduser("~/.mythbot/config.ini")
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
    matrix_bot = smythClient(botCfg["Matrix Settings"]["Server Name"], botCfg["Matrix Settings"]["User Name"], botCfg["Matrix Settings"]["Password"])
    await matrix_bot.init_login()
    await matrix_bot.client.close()
    print(matrix_bot.response)
    
    
    
    
    
asyncio.get_event_loop().run_until_complete(main())
