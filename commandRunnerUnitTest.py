import asyncio
import smythbotCommandRunner

async def debug_runner(test_command_string):
    commander = smythbotCommandRunner.smythbot_command(test_command_string)
    print ("executing command: " + test_command_string)
    return await commander.poulate_command_index()
async def main():
    
    main_runner = smythbotCommandRunner.smythbot_command(" ")
    test1 = "!smythbot help !smythbot help  "
    command_output = await debug_runner(test1)
    for command in command_output:
        print(command["command name"])
        print("Checking command " + test1 + " for trailing spaces.")
        await main_runner.strip_trailing_spaces(test1)

asyncio.run(main())
