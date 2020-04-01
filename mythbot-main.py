import os
import configparser
def genCfg(cfgPath):
   os.makedirs(os.path.dirname(cfgPath), exist_ok=True) #TODO: Surround this in try-catch block
   print("config dir found. ")
def main():
    # Obligatory Setup
    #------------------
    cfgDirPath = os.path.expanduser("~/.mythbot/")
    cfgFilePath = os.path.expanduser("~/.mythbot/")
    cfgExists = os.path.exists(cfgFilePath)
    print (cfgFilePath)
    # TODO: Add argparser, the above settings are temporary
    if not cfgExists:
        genCfg(cfgFilePath)
        print ("Error: no default configuration found.")
        print ("A defaut configuration file was generated at " + cfgFilePath)
        print ("Set your desired values and run this program again.")
        return
    
    
if __name__ == "__main__":
    main()
    
print(__name__)
main()
