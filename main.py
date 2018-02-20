# main.py -- The main function call. Program starts here.
# Author -- Jake Shepherd

import sys
from parser import Parser
from db_manager import executeCommand

def main():
    # Check argument count, if one was supplied then we assume this
    # is the file to read the SQL commands from.
    # If no argument is supplied, then we jump into manual entry
    if(len(sys.argv) > 1):
        # p is our parser object
        p = Parser(True, sys.argv[1]) 
    else:
        p = Parser(False)

    if p.usingFile:
        # Read and parse commands from SQL file
        p.read()
        # Process commands
        for instr in p.instructions :
            executeCommand(instr)
    else:
        userInput = ""

        # Loop, fetching user input, until user executes 
        while userInput.lower() != ".exit":
            userInput = input("> ")

            p.read(userInput)
            executeCommand(p.singleInstruction)

if __name__ == "__main__":
    # execute main function :) just some fancy python stuff here no worries
    main()


