"""
Handles the work of validating and processing command input.
"""
# Importing the required python modules
import datetime
import time
import subprocess
from multiprocessing import Queue

# Importing local modules
from db import session
from base import Base, Command

# Module to get 'commands.txt' 
def get_valid_commands(queue, filename):
    # TODO: efficiently evaluate commands from filename passed

    #Initialise lists
    # This list will hold all the lines from commands.txt
    content = []
    # This list will hold the VALID_COMMANDS section of commands.txt
    valid_commands_list = []
    # This list will hold the COMMAND_LIST section of commands.txt
    total_commands_list = []
    # Reading all lines of commands.txt
    for line in open(filename, 'r'):
        content.append(line)
    # removing whitespace characters like '\n' at the end of each line
    content = [x.strip() for x in content]
    # Separating the total commands and valid commands
    start_idx = content.index('[COMMAND_LIST]')
    stop_idx = content.index('[VALID_COMMANDS]')
    valid_commands_list = content[start_idx+1:stop_idx-2]
    total_commands_list = content[stop_idx+1:len(content)]

    # Extracting only the valid commands from the commands to be executed
    to_be_executed = list(set(total_commands_list).intersection(valid_commands_list))
    
    # Putting those commands in queue to be executed
    for x in range(len(to_be_executed)):
        queue.put(to_be_executed[x])

    # command = queue.get()    

def process_command_output(queue):
    # TODO: execute the command and put its data in the db

    q = queue

    # Initialise list that will hold the database entry objects
    put_results_database = []
    while not q.empty():
        work = q.get(True)
        try:
            # execute is the command string to be executed
            execute = work
            # Timing the process of executing each command
            tic = time.clock()
            process = subprocess.run(execute,shell=True, timeout=60, stdout=subprocess.PIPE)
            toc = time.clock()
            # Storing the meta-data in each column of the defind database
            output = process.stdout
            duration = toc-tic
            length = len(execute)
            command_string = execute
        # Specifying the exception condition when the commands takes greater than 1 minute to process
        except subprocess.TimeoutExpired as e:
            print('long running or not finished scenario')
            duration = 0
            output = e.stdout

        # Appending the meta-data object in list
        result_entry = Command(command_string, length, duration, output)
        put_results_database.append(result_entry)

    # Putting results in database
    session.add_all(put_results_database)
    session.commit()



    # command = queue.get()
