from MythTV.services_api import send as api
import smythbot_outputs
class smythbot_command(object):
    def __init__(self, raw_command, formatting = True, mythtv_backend = "not set", mythtv_port = 6544):
        self.raw_command = raw_command
        self.formatting = formatting
        self.mythtv_backend = mythtv_backend
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
            elif piece.startswith("view mythbackend address"):
                self.command_results.append(await self.view_mythbackend_address())
            elif piece.startswith("view mythbackend port"):
                self.command_results.append(await self.view_mythbackend_port())
            elif piece.startswith("display upcoming recordings"):
                self.command_results.append(await self.display_upcoming_recordings())
            elif piece.startswith("display recorded programs"):
                self.command_results.append(await self.display_recorded_programs(piece))
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
            <p>Version: 0.0.1</p>
            <p>WARNING: I am still in early alpha, use at your own risk. I take NO RESPONSIBILITY for any data loss</p>
            <p> I currently support the following commands:</p>
            <br><br>
            <strong>!smythbot help:</strong> Display this message <br>
            <strong>!smythbot set mythbackend address:</strong> Sets the mthtv backend address to use for this room.  <br>
            <strong>!smythbot set mythbacked port:</strong> Sets the mthtv backend port to use for this room. <br>
            <strong>!smythbot display upcoming recordings:</strong> Displays the upcoming recordings on your Myth Tv Backend.  <br>
            <strong>!smythbot display recorded programs:</strong> Displays the recordings from the default recording group that are stored on your Myth Tv Backend.  <br>
            """
            #<strong></strong>  <br>
        else:
            pass
        command_shard = {"command name":"help", "command output": help_string}
        return command_shard

    async def set_mythbackend_address(self, raw_command_input):
        split_command_string = raw_command_input.split()
        if len(split_command_string) < 4:
            return await self.malformed_command("set mythbackend address", "No Myth Tv Backend address was specified")
        if split_command_string[3].startswith("http:") or split_command_string[3].startswith("https:"):
            return await self.malformed_command("set mythbackend address", "the Myth Tv Backend URL cannot start with \"http://\" or \"https://\"")
        return await self.set_client_property("MythTv Backend Address", split_command_string[3])
    
    async def set_mythbackend_port(self, raw_command_input):
        split_command_string = raw_command_input.split()
        if len(split_command_string) < 4:
            return await self.malformed_command("set mythbackend port", "No Myth Tv Backend port was specified")
        
        if not split_command_string[3].isdecimal():
            return await self.malformed_command("set mythbackend port", "Port value may only be a positive whole number")

        return await self.set_client_property("MythTv Backend Port", split_command_string[3])

    async def view_mythbackend_address(self):
        return await self.view_client_property("MythTv Backend Address", self.mythtv_backend)

    async def view_mythbackend_port(self):
        return await self.view_client_property("MythTv Backend Port", self.mythtv_port)
    
    async def display_upcoming_recordings(self):
        if self.mythtv_backend == "not set":
            return await self.malformed_command("display upcoming recordings", "The Myth Tv Backend URL for this room has not been set yet.<br>Please set it before using this command")
        try:
            upcoming_queue = await self._processed_mythtv_data("Dvr/GetUpcomingList")
        except RuntimeError:
            return await self.connection_error()
        if upcoming_queue.isEmpty():
            return {"command output": "<h1>No sceduled recordings are coming up soon</h1>"}
        schedule_output = "<h1>Upcoming Shows</h1>" + await upcoming_queue.output_as_html()
        return{"command output": schedule_output}

    async def display_recorded_programs(self, raw_command):
        if self.mythtv_backend == "not set":
            return await self.malformed_command("display recorded programs", "The Myth Tv Backend Address for this room has not been set yet.<br>Please set it before using this command")

        rest_options = "Descending=True&StorageGroup=Default&RecGroup=Default"
        try:
            RecordedShowsList = await self._processed_mythtv_data("Dvr/GetRecordedList", rest_commands=rest_options)
        except RuntimeError:
            return await self.connection_error()
        if RecordedShowsList.isEmpty():
            return {"command output": "<h1>No recordings are available at ths time</h1>"}        

        schedule_output = "<h1>Recorded Programs</h1>"
        schedule_output = schedule_output + await RecordedShowsList.output_as_html()
        return{"command output": schedule_output}



    # Internal stuff
    async def return_error(self, bad_string):
        command_shard = {}
        command_shard["command name"] = "command not found"
        command_shard["command output"] = "<h1> The Command: " + bad_string + " was not recognized.</h1><p>Type: <strong>!smythbot help</strong> for more information about currently supported commands.</p>"
        return command_shard
    
    async def connection_error(self):
        error_output = {"command output":"""<h1>There was a problem</h1>
        <p>There was a connection problem when querying your Myth Tv.
        <br>This could mean a few things:
        <ul>
        <li>Your backend URL or port is set incorrectly</li>
        <li>Your Myth Tv backend is down</li>
        <li>Your connection to the Myth Tv is faulty.</li></ul></p>"""}
        return error_output
        
    async def malformed_command(self, command_name, error_reason):
        command_shard = {}
        command_shard["command name"] = "\"" + command_name + "\" was malformed"
        command_shard["command output"] = "<h1>Malformed Command</h1> The command " + command_shard["command name"] +"<p>The reason: " + error_reason + "</p>"
        return command_shard

    async def set_client_property(self, property_name, property_value):
        command_shard = {}
        command_shard["command name"] = "set the " + property_name + " for this room"
        command_shard["room settings data"] = {"property name":property_name, "property value":property_value}
        command_shard["command output"] = "<h1>You " + command_shard["command name"] + " to " + property_value + " </h1>"
        return command_shard

    async def view_client_property(self, property_name, property_value):
        command_shard = {}
        command_shard["command name"] = "The " + property_name + " for this room"
        command_shard["command output"] = "<h1>" + command_shard["command name"] + " is " + property_value + " </h1>"
        return command_shard
    
    async def _interrogate_mythbackend(self, endpoint_string, command_rest_parameters = ""):
        mythtv_backend_server = api.Send(host=self.mythtv_backend, port=self.mythtv_port)
        try:
            mythtv_response = mythtv_backend_server.send(endpoint=endpoint_string, rest=command_rest_parameters)
        except RuntimeError as e:
            print(e)
            raise  
        return mythtv_response

    async def _processed_mythtv_data(self, endpoint_string, rest_commands = "", table_header = ["Series", "Episode", "Start Time", "End Time"], body_attributes = ["Title", "SubTitle", "StartTime", "EndTime"]): 
        try:
            raw_mythbackend_info = await self._interrogate_mythbackend(endpoint_string, command_rest_parameters = rest_commands)
        except RuntimeError:
            raise 
        formatted_table = smythbot_outputs.Table(table_header)
        progs = raw_mythbackend_info['ProgramList']['Programs']
        for program in progs:
            for attribute in body_attributes:
                await formatted_table.add_cell_item(program[attribute])
        return formatted_table
