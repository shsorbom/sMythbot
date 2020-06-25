class smythbot_command(object):
    def __init__(self, raw_command, formatting = True, mythyv_backend = "not set", mythtv_port = 6544):
        self.raw_command = raw_command
        self.formatting = formatting
        self.mythtv_backend = mythyv_backend
        self.mythtv_port = mythtv_port
        self.command_results = [] # A List of dict entries we will be returning to the client
        self.valid_commands = {} # A list of commands we will recognize

        # Valid commands:
        
    
    async def setValidCommands(self):
        self.valid_commands["help"] = await self.get_help()
    
    async def parse_raw_command(self):
        self.raw_command = self.raw_command.lower()
        command_list = self.raw_command.split("!smythbot")
        return command_list

    async def poulate_command_index(self):
        command_string_list = await self.parse_raw_command()
        #print("Debug: Length of command string: " + str(len(command_string_list)))
        
        for piece in command_string_list:
            if piece.startswith("help"):
                self.command_results.append(self.get_help(piece))
            elif piece.startswith("set mythbackend address"):
                pass
            elif piece.startswith("set mythbackend port"):
                pass
            
            #..
            else:
                self.command_results.append(self.return_error)


    async def compiled_command_index(self):
        pass
    
    # Actual bot commands go here: 
    async def get_help(self, help = "help"):
        if help.lower() == "help":
            help_string = """<h1> Hi, I am sMythbot</h1>
            <p>I exist to manage the MythTv DVR via Matrix chat.</p>
            <p> I currently support the following commands:</p>
            <br><br>
            <strong>!smythbot help:</strong> Display this message <br>
            <strong>!smythbot set mythbackend address:</strong> Sets the mthtv backend address to use for this room.  <br>
            <strong>!smythbot set mythbacked port</strong> Sets the mthtv backend address to use for this room. <br>
            """
            #<strong></strong>  <br>
        else:
            pass
        command_shard = {"command name":"help", "command output": help_string}
        return command_shard

    async def return_error(bad_string):
        command_shard = {}
        command_shard["command name"] = "command not found"
        command_shard["command output"] = "<h1> The Command: " + bad_string + " was not recognized.<\h1><p>Type: <strong>!smythbot help</strong> for more information about currently supported commands.</p>"
        return command_shard