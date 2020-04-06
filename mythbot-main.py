import os
import configparser
def genCfg(cfgPath):
   os.makedirs(os.path.dirname(cfgPath), exist_ok=True) #TODO: Surround this in try-catch block
   print("config dir made. ")
   mCfg = configparser.ConfigParser()
   mCfg ["MythTvProperties"] = {"Host Name": "mythbox", "IP Address": "127.0.0.1", "Mythbackend Port": "6544", "MythFrontend Port":"6547"}
   mCfg ["IMAP Settings"] = {"Sever IP": "127.0.0.1","Username":"username", "Password": "password", "Security": "ssl"}
   mCfg ["SMTP Settings"] = {"Sever IP": "127.0.0.1","Username":"username", "Password": "password", "Security": "startls", "Email Address": "email@example.com"}
   mCfg ["Matrix Settings"] = {"Sever IP": "127.0.0.1","MXID":"@username:matrix.org", "Password": "password"}
   with open(cfgPath, "w") as configfile:
      mCfg.write(configfile)
def main():
    # Obligatory Setup
    #------------------
    cfgDirPath = os.path.expanduser("~/.mythbot/")
    cfgFilePath = os.path.expanduser("~/.mythbot/config.ini")
    cfgExists = os.path.exists(cfgFilePath)
    print (cfgFilePath)
    # TODO: Add argparser, the above settings are temporary
    if not cfgExists:
        genCfg(cfgFilePath)
        print ("Error: no default configuration found.")
        print ("A defaut configuration file was generated at " + cfgFilePath)
        print ("Set your desired values and run this program again.")
        return
    print ("Config found at: " + cfgFilePath)
    
    
if __name__ == "__main__":
    main()
    
print(__name__)
main()
