import asyncio
import smythbotCommandRunner

async def debug_runner(test_command_string):
    commander = smythbotCommandRunner.smythbot_command(test_command_string)
    print ("executing command: " + test_command_string)
    await commander.poulate_command_index()
async def main():
    test1 = "!smythbot help !smythbot help"
    await debug_runner(test1)

asyncio.run(main())
