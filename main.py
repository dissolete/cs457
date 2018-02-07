import sys
from parser import Parser

def main():
    p = Parser(sys.argv[1])

    p.read()

if __name__ == "__main__":
    # execute main function :) just some fancy python stuff here no worries
    main()
