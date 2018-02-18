import sys
from parser import Parser
from db_manager import executeCommand

def main():
    if(len(sys.argv) > 1):
        p = Parser(True, sys.argv[1])
    else:
        p = Parser(False)

    if p.usingFile:
        p.read()
        for instr in p.instructions :
            executeCommand(instr)
        #p.print()
    else:
        userInput = ""

        while userInput.lower() != ".exit":
            userInput = input("> ")

            p.read(userInput)
            executeCommand(p.singleInstruction)
            #p.print()


if __name__ == "__main__":
    # execute main function :) just some fancy python stuff here no worries
    main()
