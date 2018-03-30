#Primary Author: Gage Thomas
#Secondary Author: Jake Shepherd
#Class: CS 457
#Date: 3/29/2018
#Version 3: Updated for join support. Select instructions can now be differentiated
#into standard selects and selects that join two tables.

#Version 2: Updated to handle PA2 commands. This file does the error handling,
#           db.py does the bulk of the implementation, with a few exceptions
#           such as drop database.

import os
import sys
from parser import Instruction

from db import DB

currDb = "" #Used to store the current database
currDir = os.getcwd()

database = None;

def executeCommand(instr):

    if instr.primaryInstruction == "use" : 
        cmmdUse(instr)
    elif instr.primaryInstruction == "create database" :
        cmmdCreateDB(instr)
    elif instr.primaryInstruction == "drop database" :
        cmmdDropDB(instr)
    elif instr.primaryInstruction == "create table" :
        cmmdCreateTable(instr)
    elif instr.primaryInstruction == "drop table" :
        cmmdDropTable(instr)
    elif instr.primaryInstruction == "select" :
        if instr.joinType == "":
            cmmdSelect(instr)
        else:
            cmmdJoin(instr)
    elif instr.primaryInstruction == "alter table" :
        cmmdAlterTable(instr)
    elif instr.primaryInstruction == "insert":
        cmdInsert(instr)
    elif instr.primaryInstruction == "update":
        cmdUpdateTable(instr)
    elif instr.primaryInstruction == "delete":
        cmdDelete(instr)
    elif instr.primaryInstruction == "exit" :
        cmmdExit(instr)

#Updated to use db object, most likely functioning
def cmmdUse(instr) :
    #Check to see if the database exists by checking if its directory exists
    dbPath = currDir + "/" + instr.database

    #If it is 
    if os.path.isdir(dbPath):
        print("Using database %s." % instr.database)
        global currDb
        currDb = instr.database
        global database
        database = DB(currDb, True)
    else :
        print("!Failed to use database %s because it does not exist." % instr.database)

#Updated to use db object, functioning
def cmmdCreateDB(instr) :
    #Check to see if the database exists by checking if its directory exists
    dbPath = currDir + "/" + instr.database

    #If it doesn't already exist
    if not os.path.isdir(dbPath) :
        print("Database %s created." % instr.database)
        os.system("mkdir " + instr.database)
        newDB = DB(instr.database, False)#Not storing this, but just creating the file and directory
    else :
        print("!Failed to create database %s because it already exists." % instr.database)

#Updated to use db object, functioning
def cmmdDropDB(instr) :
    #Check to see if the database exists by checking if its directory exists
    dbPath = currDir + "/" + instr.database
    global currDb

    #If it doesn't already exist
    if not os.path.isdir(dbPath) :
        print("!Failed to delete %s because it does not exist." % instr.database)
    else :
        print("Database %s deleted." % instr.database)
        os.system("rm -rf " + instr.database)
        #if you deleted the database you are currently using, remove that from global
        if currDb == instr.database :
            currDb = ""
            global database
            database = None

#Updated to use db object, functioning
def cmmdCreateTable(instr) :
    #If you aren't currently using a database, throw an error
    if currDb == "" :
        print("!Failed to create a table because no database is being used.")
    # Else, if the table already exists...
    elif os.path.isfile(currDb + "/" + instr.tableUsed + ".txt"):
        print("!Failed to create table %s because it already exists." % instr.tableUsed)

    else :
        database.createTable(instr.tableUsed, instr.attrPairs)
        print("Table %s created." % instr.tableUsed)

#Updated to use db object, functioning
def cmmdDropTable(instr) :
    #If you aren't currently using a database, throw an error
    if currDb == "" :
        print("!Failed to delete a table because no database is being used.")
    #else if the file does not exist
    elif not os.path.isfile(currDb + "/" + instr.tableUsed + ".txt") :
        print("!Failed to delete %s because it does not exist." % instr.tableUsed)
    else :
        global database
        database.dropTable(instr.tableUsed)
        print("Table %s deleted." % instr.tableUsed)

def cmmdSelect(instr) :
    # interesting for now since this project doenst require us to add anything to the tables, so they will always return nothing for this project
    if currDb == "":
        print("!Failed to select from table since no database is being used.")
    elif not os.path.isfile(currDb + "/" + instr.tableUsed + ".txt"):
        print("Failed to select from table %s because it does not exist." % instr.tableUsed)
    else:
        table = database.getTable(instr.tableUsed)
        if table:
            results = table.select(instr.attributes, instr.whereClause)
            
            # Print the results in a nice way
            for row in results:
                for c in range(0, len(row) - 1):
                    print(row[c] + " | ", end='')
                print(row[len(row) - 1])

def cmdInsert(instr):
    if currDb == "":
        print("!Failed to alter table since no database is being used.")

    elif not os.path.isfile(currDb + "/" + instr.tableUsed + ".txt"):
        print("!Failed to insert into table %s since it does not exist." % instr.tableUsed)
    else:
        global database
        table = database.getTable(instr.tableUsed)
        if table:
            table.insert(instr.insertValues)
            print("1 new record inserted.")
def cmdUpdateTable(instr):

    if currDb == "":
        print("!Failed to update table since no database is being used.")

    elif not os.path.isfile(currDb + "/" + instr.tableUsed + ".txt"):
        print("!Failed to update into table %s since it does not exist." % instr.tableUsed)
    else:
        table = database.getTable(instr.tableUsed)
        if table:
            numRowsUpdated = table.update(instr.updateAttributeName, instr.updateSetToValue, instr.whereClause)
            if numRowsUpdated > 1 or numRowsUpdated == 0:
                print("{} records modified.".format(numRowsUpdated))
            else:
                print("1 record modified.")
def cmdDelete(instr):
    if currDb == "":
        print("!Failed to delete from table since no database is being used.")

    elif not os.path.isfile(currDb + "/" + instr.tableUsed + ".txt"):
        print("!Failed to delete from table %s since it does not exist." % instr.tableUsed)
    else:
        table = database.getTable(instr.tableUsed)
        if table:
            numRowsUpdated = table.delete(instr.whereClause)
            if numRowsUpdated > 1 or numRowsUpdated == 0:
                print("{} records deleted.".format(numRowsUpdated))
            else:
                print("1 record deleted.")

#Assumes for now that it is alter table add
#Updated to use db object, functioning
def cmmdAlterTable(instr) :
    #until we start saving data in memory, we'll have to read every line and rewrite it
    if currDb == "":
        print("!Failed to alter table since no databe is being used.")
    elif not os.path.isfile(currDb + "/" + instr.tableUsed + ".txt"):
        print("!Failed to alter table %s since it does not exist." % instr.tableUsed)
    else:
        global database
        database.getTable(instr.tableUsed).alter(instr.attrPairs[0][0], instr.attrPairs[0][1])

        print("Table {} altered.".format(instr.tableUsed))
def cmmdExit(instr) :
    print("All done.")
    sys.exit()

def cmmdJoin(instr) :
    database.joinTables(instr.tableUsed, instr.joinTable, instr.leftAlias, instr.rightAlias, instr.whereClause, instr.joinType)
    
