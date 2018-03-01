# main.py -- The main function call. Program starts here.
#Primary Author: Jake Shepherd
#Secondary Author: Gage Thomas
#Class: CS 457
#Date: 2/20/2017
#Version 1: Executes all instructions either coming from a command line
#           or from an input file given as a command-line argument
import sys
from parser import Parser
from db_manager import executeCommand

def main():

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
        #p.read(userInput)
        #executeCommand(p.singleInstruction)

if __name__ == "__main__":
    # execute main function :) just some fancy python stuff here no worries
    main()


