class Parser:

    def __init__(self, filename):
        self.instructions = []
        self.instructionSet = filename

    # Reads file and parses instructions
    def read(self):
        f = open(self.instructionSet, 'r')

        #Read line by line
        for line in f:
            print(line, end='')

