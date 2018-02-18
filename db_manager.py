#Primary Author: Gage Thomas
#Secondary Author: Jake Shepherd
#Class: CS 457

import os
import sys
from parser import Instruction

currDb = "" #Used to store the current database
currDir = os.getcwd()

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
        cmmdSelect(instr)
    elif instr.primaryInstruction == "alter table" :
        cmmdAlterTable(instr)
    elif instr.primaryInstruction == "exit" :
        cmmdExit(instr)

def cmmdUse(instr) :
    #Check to see if the database exists by checking if its directory exists
    dbPath = currDir + "/" + instr.database

    #If it is 
    if os.path.isdir(dbPath):
        print("Using database %s." % instr.database)
        global currDb
        currDb = instr.database
    else :
        print("!Failed to use database %s because it does not exist." % instr.database)


def cmmdCreateDB(instr) :
    #Check to see if the database exists by checking if its directory exists
    dbPath = currDir + "/" + instr.database

    #If it doesn't already exist
    if not os.path.isdir(dbPath) :
        print("Database %s created." % instr.database)
        os.system("mkdir " + instr.database)
    else :
        print("!Failed to create database %s because it already exists." % instr.database)

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

def cmmdCreateTable(instr) :
    #If you aren't currently using a database, throw an error
    if currDb == "" :
        print("!Failed to create a table because no database is being used.")
    # Else, if the table already exists...
    elif os.path.isfile(currDb + "/" + instr.tableUsed + ".txt"):
        print("!Failed to create table %s because it already exists." % instr.tableUsed)

    else :
        #os.system("touch " + currDb + "/" + instr.tableUsed + ".txt")
        fout = open(currDb + "/" + instr.tableUsed + ".txt", "w+")
        #write each of the attributes

        fout.close();
        print("Table %s created." % instr.tableUsed)

def cmmdDropTable(instr) :
    #If you aren't currently using a database, throw an error
    if currDb == "" :
        print("!Failed to delete a table because no database is being used.")
    #else if the file does not exist
    elif not os.path.isfile(currDb + "/" + instr.tableUsed + ".txt") :
        print("!Failed to delete %s because it does not exist." % instr.tableUsed)
    else :
        os.remove(currDb + "/" + instr.tableUsed + ".txt")
        print("Table %s deleted." % instr.tableUsed)

def cmmdSelect(instr) :
    print("Select command")

def cmmdAlterTable(instr) :
    print("Alter table command")

def cmmdExit(instr) :
    sys.exit()