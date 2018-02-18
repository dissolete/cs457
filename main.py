import sys
from parser import Parser

def main():
    if(len(sys.argv) > 1):
        p = Parser(True, sys.argv[1])
    else:
        p = Parser(False)

    if p.usingFile:
        p.read()
        p.print()
    else:
        userInput = ""

        while userInput.lower() != ".exit":
            userInput = input("> ")

            p.read(userInput)
            p.print()


if __name__ == "__main__":
    # execute main function :) just some fancy python stuff here no worries
    main()
