class Parser:

    def __init__(self, filename):
        self.instructions = []
        self.instructionSet = filename

    # Reads file and parses instructions
    def read(self):
        f = open(self.instructionSet, 'r')

        #Read line by line
        for line in f:
            # Skip line if its a comment or blank
            if line.startswith("--") or line.isspace():
                continue
            else:
                print(line, end="")

