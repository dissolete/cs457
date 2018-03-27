PA2 Design Document

Organizing Multiple Databases:
This program organizes multiple databases by storing each database as a directory inside the directory running the program. The name of the database is the name of the directory. Each database directory has a metadata file that stores the names of each table, one table name per line.


Organizing Multiple Tables:
Within the database directories, each table is stored as a single .txt file. The first row of these files lists every attribute and their respective datatype in this format: the first attribute name, a space, the datatype of that attribute, another space, and then repeat until all attributes for that table are described. After that, each row of the file is a tuple in the table. Note: the Null value is "NULL"


High-level Implementation Details:
There are four files that make the program work: main.py, parser.py, db.py, and db_manager.py. main.py reads user input and stores a parser object and a calls the executeCommand function from db_manager.py. 

main.py thus reads input, has the parser parse the commands, and then passes that instruction on to the function to handle it. 

Parser.py contains two objects: Instruction and Parser. The parser accepts input and then transforms it into the machine-readable Instruction object, which stores lists and variables for the used database, the table used, which attributes are selected, etc.

db_manager.py has one function that is called by the main file (executeCommand), which calls the appropriate function for the different table operations. It stores 3 global variables: the name of the database currently being used, the path to the current working directory, and a DB object which it uses to execute the instructions. db_manager.py thus selects the appropriate functions, passes the appropriate parameters to the DB object, and does all the error handling.

db.py contains two objects: Table and DB. DB stores a list of table objects, and it handles creating tables, droping tables, writing the metadata file for the database, getting appropriate tables, and reading in data when a pre-existing database is being used. Table, meanwhile, stores the attribute names, types, and the actual data within the tables. All SQL functionality not handled by DB is handled by Table.

In summary, main.py accepts all input and passes it to the parser. The parser interprets the input and puts it into an Instruction object. main.py then calls the db_manager.py function (executeCommand) which then handles any errors and passes it to the Table and DB objects if there are no errors which then handle the actual execution.


Running the Program:
The program can be executed by typing the following command in the directory that contains the code files:
python3 main.py < PA2_test.sql
