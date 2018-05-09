PA4 Design Document

Organizing Multiple Databases:
This program organizes multiple databases by storing each database as a directory inside the directory running the program. The name of the database is the name of the directory. Each database directory has a metadata file that stores the names of each table, one table name per line.


Organizing Multiple Tables:
Within the database directories, each table is stored as a single .txt file. The first row of these files lists every attribute and their respective datatype in this format: the first attribute name, a space, the datatype of that attribute, another space, and then repeat until all attributes for that table are described. After that, each row of the file is a tuple in the table. Note: the Null value is "NULL"


Tuple Storage:
Each table file stores the tuples as a single row with each attribute separated by a space. As noted before, the first line of each table file lists the attribute names and types separated by spaces.


Tuple Insertion Implementation:
Tuple insertion is done by appending a new row for the tuple (as described in Tuple Storage) to the bottom of the table file.


Tuple Query Implementation:
The select function in Table returns a 2D list storing the actual selected data. First, the attribute used in the where clause is identified. The tuples specified from the where clause are then filtered out and appended to the "results" 2D list. Finally, if specific attributes (not *) are selected, the non-specified attributes are removed and the filtered results are returned.


Tuple Deletion and Modification:
Both of these functions use a similar strategy to the Query implementation. For deletion, the correct attribute column that is being tested in the where statement is identified, the tuples are searched and marked in a list for deletion, and then those tuples are removed from the data before the data is rewritten to the file. Update, meanwhile, goes through the same search process but instead of marking tuples for deletion, the data in the object is rewritten in accordance with the query before the data is rewritten to the file.


High-level Implementation Details:
There are four files that make the program work: main.py, parser.py, db.py, and db_manager.py. main.py reads user input and stores a parser object and a calls the executeCommand function from db_manager.py. 

main.py thus reads input, has the parser parse the commands, and then passes that instruction on to the function to handle it. 

Parser.py contains two objects: Instruction and Parser. The parser accepts input and then transforms it into the machine-readable Instruction object, which stores lists and variables for the used database, the table used, which attributes are selected, etc.

db_manager.py has one function that is called by the main file (executeCommand), which calls the appropriate function for the different table operations. It stores 3 global variables: the name of the database currently being used, the path to the current working directory, and a DB object which it uses to execute the instructions. db_manager.py thus selects the appropriate functions, passes the appropriate parameters to the DB object, and does all the error handling.

db.py contains two objects: Table and DB. DB stores a list of table objects, and it handles creating tables, droping tables, writing the metadata file for the database, getting appropriate tables, and reading in data when a pre-existing database is being used. Table, meanwhile, stores the attribute names, types, and the actual data within the tables. All SQL functionality not handled by DB is handled by Table.

In summary, main.py accepts all input and passes it to the parser. The parser interprets the input and puts it into an Instruction object. main.py then calls the db_manager.py function (executeCommand) which then handles any errors and passes it to the Table and DB objects if there are no errors which then handle the actual execution.


Join Implementation:
The way this program works, all data is read from the file into the table objects when "use" is called and every time tables are altered, the data is written back into the file (thought the data is still kept in memory, so both are in step). We use a nested loop join algorithm where first the columns in both tables where they are being joined on are identified. Then, the headers for both tables are printed. Finally, each tuple in the left table is iterated through. There is a boolean set to determine if that tuple was matched with anything. At the end of that iteration, if that tuple was not joined with anything and it was a left outer join, that tuple is printed. In any case, each tuple from the left table is then compared with each tuple from the right table (both tables are completely in memory). If their identified attributes match, both tuples are printed on the same line.

Transaction Implementation:
When a transaction begins, a flag is stored by the DB object. Any time an update command is executed, a lock is put on the table the update is being performed on. This lock is persistent until the transaction is commited. A lock is determined by a {tableName}_lock.txt file. If the file exists in the database, then the table is locked, otherwise the table is unlocked and is free to be updated. This lockfile is checked when updating a table. Due to the nature of this project, since processes are now split, a change to the select implementation has been made. Now, every time a new select is issued, the table is reloaded in case any transactions on other processes modified the table. When a transaction is commited, the locks on any tables the transaction was updating are released. This all ensures that multiple processes can start transactions without any conflict between them -- only one transaction can have the table at a time. If a process wishes to alter a table that is locked during a transaction, a flag is set indicating that an error occurred. If this flag is set, a commit statement is interpreted as an abort and changes are not written to file.

Running the Program:
The program can be executed by typing the following command in the directory that contains the code files:
python3 main.py

Running this command puts the user into input mode, where each command needs to be typed. If commands need to be piped, this can be done by executing:
python3 main.py < inputFile.sql
