class smythbot_command(object):
    def __init__(self, raw_command, formatting = True, mythyv_backend = "not set", mythtv_port = 6544):
        self.raw_command = raw_command
        self.formatting = formatting
        self.mythtv_backend = mythyv_backend
        self.mythtv_port = mythtv_port
        self.command_results = [] # A List of dict entries we will be returning to the client
        self.valid_commands = {} # A list of commands we will recognize

        
    

    
    async def parse_raw_command(self):
        self.raw_command = self.raw_command.lower()
        self.raw_command = await self.strip_trailing_spaces(self.raw_command)
        command_list = self.raw_command.split("!smythbot ")
        command_list.pop(0) # The zeroeth element in a split list is always blank, therefore useless.
        return command_list
   
    async def strip_trailing_spaces(self, input_string):
        split_input_string = input_string.split()
        list_index = len(split_input_string) - 1
        while split_input_string[list_index] == " " or split_input_string[list_index] == "":
            split_input_string.pop(list_index)
            list_index = list_index - 1
        return " ".join(split_input_string)

    async def poulate_command_index(self):
        command_string_list = await self.parse_raw_command()
        #print("Debug: Length of command string: " + str(len(command_string_list)))
        
        for piece in command_string_list:
            piece = await self.strip_trailing_spaces(piece)
            if piece.startswith("help"):
                self.command_results.append(await self.get_help(piece))
            elif piece.startswith("set mythbackend address"):
                self.command_results.append(await self.set_mythbackend_address(piece))
            elif piece.startswith("set mythbackend port"):
                self.command_results.append(await self.set_mythbackend_port(piece))
            
            #..
            else:
                self.command_results.append(await self.return_error(piece))
        return self.command_results

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
            <strong>!smythbot set mythbacked port:</strong> Sets the mthtv backend address to use for this room. <br>
            """
            #<strong></strong>  <br>
        else:
            pass
        command_shard = {"command name":"help", "command output": help_string}
        return command_shard

    async def set_mythbackend_address(self, raw_command_input):
        split_command_string = raw_command_input.split()
        return await self.set_client_property("MythTv Backend Address", split_command_string[3])
    
    async def set_mythbackend_port(self, raw_command_input):
        pass

    async def return_error(self, bad_string):
        command_shard = {}
        command_shard["command name"] = "command not found"
        command_shard["command output"] = "<h1> The Command: " + bad_string + " was not recognized.</h1><p>Type: <strong>!smythbot help</strong> for more information about currently supported commands.</p>"
        return command_shard
    
    async def set_client_property(self, property_name, property_value):
        command_shard = {}
        command_shard["command name"] = "set the " + property_name + " for this room"
        command_shard["room settings data"] = {"property name":property_name, "property value":property_value}
        command_shard["command output"] = "<h1>You " + command_shard["command name"] + " to " + property_value + " </h1>"
        return command_shard
