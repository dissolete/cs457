PA1 Design Document

Organizing Multiple Databases:
This program organizes multiple databases by storing each database as a directory inside the directory running the program. The name of the database is the name of the directory. Currently there are no metadata files within the directory running the program or within the database directories.

Organizing Multiple Tables:
Within the database directories, each table is stored as a single .txt file. The first row of these files lists every attribute and their respective datatype in this format: the first attribute name, a space, the datatype of that attribute, another space, and then repeat until all attributes for that table are described. After that, each row of the file is a tuple in the table.

High-level Implementation Details:
There are three files that make the program work: main.py, parser.py, and db_manager.py. main.py accepts an input file (if one is passed as a command line argument) or gets user input. Parser.py contains two objects: Instruction and Parser. Main.py contains an instance of the Parser object which it uses to interpret the user input. The parser outputs Instruction objects which contain the parsed commands to db_manager.py which uses these Instruction objects to execute each of the commands. Thus, main.py handles all of the user interaction, parser.py handles all of the parsing, and db_manager.py handles all of the actual execution and database manipulation. Please keep in mind that db_manager.py maintains two global variables: currDir and currDb. CurrDir stores the directory that the program begins execution in. Please note it will not actually store the current working directory if any changeDir commands are made, so databases will always be stored in the directory where execution begins. CurrDb stores the current database being used. An empty string indicates that no database is currently being used, either because USE was never used or because the currently used database was dropped.

Running the Program:
The program can be executed by typing the following command in the directory that contains the code files:
python3 main.py
One can automatically read in the test file provided by typing this command:
python3 main.py PA1_test.sql
