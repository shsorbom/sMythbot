class smythbot_command(object):
    def __init__(self, raw_command, formatting = True, mythyv_backend = "not set", mythtv_port = 6544):
        self.raw_command = raw_command
        self.formatting = formatting
        self.mythtv_backend = mythyv_backend
        self.mythtv_port = mythtv_port
        self.command_index = [] # A List of dict pairs we will be returning to the 
    
    async def parse_raw_command(self):
        if self.raw_command.find("!smythbot help"):
            self.command_index.append(self.get_help())

    async def compiled_command_index(self):
        pass
    
    # Actual bot commands go here: 
    def get_help(self, help = "help"):
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

