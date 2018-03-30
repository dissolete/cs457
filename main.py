# main.py -- The main function call. Program starts here.
#Primary Author: Jake Shepherd
#Secondary Author: Gage Thomas
#Class: CS 457
#Date: 3/29/2018
#Version 3: No changes, but Parser and db_manager now support joins

#Version 2: Program start - reads user input and interprets instructions
#           Can handle multi-line commands now
#           No longer supports reading in a file of commands, redirect input instead
import sys
from parser import Parser
from db_manager import executeCommand

def main():
    leParser = Parser()
    userInput = ""

    # Loop, fetching user input, until user executes 
    while userInput.lower() != ".exit":

        userInput = input().strip()
        if userInput.startswith("--") or userInput.isspace() or not userInput:
            continue
        # instruction ends when there's a semicolon
        while userInput.lower() != ".exit" and not userInput.endswith(";"):
            temp = input().strip()
            userInput = userInput + " " + temp                

        print(userInput)
        leParser.parse(userInput)
        # Uncomment this line to see how the instructions are created
        #leParser.print()
        executeCommand(leParser.singleInstruction)

if __name__ == "__main__":
    # execute main function :) just some fancy python stuff here no worries
    main()


