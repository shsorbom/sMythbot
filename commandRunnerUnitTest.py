import asyncio
import smythbotCommandRunner
import smythbot_outputs


async def debug_runner(test_command_string):
    commander = smythbotCommandRunner.smythbot_command(test_command_string)
    print ("executing command: " + test_command_string)
    return await commander.poulate_command_index()
async def main():
    #print("Hi")
    testTable = smythbot_outputs.Table(["Name", "Animal Type", "Age"])
    await testTable.add_cell_item("Darla")
    await testTable.add_cell_item("Eagle")
    await testTable.add_cell_item("5")

    await testTable.add_cell_item("Alfalfa")
    await testTable.add_cell_item("Eagle")
    await testTable.add_cell_item("6")

    await testTable.add_cell_item("Skippy")
    await testTable.add_cell_item("Eagle")
    await testTable.add_cell_item("7")
    output = await testTable.output_as_html()
    print(output)
    return

asyncio.run(main())
