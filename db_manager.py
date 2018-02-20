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
        fout = open(currDb + "/" + instr.tableUsed + ".txt", "w")
        #write each of the attributes
        for attr in instr.attrPairs:
            fout.write("{} {} ".format(attr[0], attr[1]))

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
    # interesting for now since this project doenst require us to add anything to the tables, so they will always return nothing for this project
    if currDb == "":
        print("!Failed to select from table since no database is being used.")
    elif not os.path.isfile(currDb + "/" + instr.tableUsed + ".txt"):
        print("Failed to select from table %s because it does not exist." % instr.tableUsed)
    else:
        f = open(currDb + "/" + instr.tableUsed + ".txt", "r")

        # get attr pairs for the table
        # maybe make this a function? i dunno
        attrLine = f.readline().split()
        attrPairs = []
        for i in range(0, len(attrLine), 2):
            attrPairs.append([attrLine[i], attrLine[i + 1]])

        # this should be a function later? for like formatting
        for i in range(0, len(attrPairs)):
            print("{} {}".format(attrPairs[i][0], attrPairs[i][1]), end="")
            if i < len(attrPairs) - 1:
                print(" | ", end="")
        print(" ")

        f.close()

def cmmdAlterTable(instr) :
    #until we start saving data in memory, we'll have to read every line and rewrite it
    if currDb == "":
        print("!Failed to alter table since no databe is being used.")
    elif not os.path.isfile(currDb + "/" + instr.tableUsed + ".txt"):
        print("!Failed to alter table %s since it does not exist." % instr.tableUsed)
    else:
        f = open(currDb + "/" + instr.tableUsed + ".txt", "r+")
        attrs = f.readline().split()

        # Remove file
        f.close()
        os.remove(currDb + "/" + instr.tableUsed + ".txt")
        # add new attr
        attrs.append(instr.attrPairs[0][0])
        attrs.append(instr.attrPairs[0][1])
        #rewrite
        f = open(currDb + "/" + instr.tableUsed + ".txt", "w+")
        for attr in attrs:
           f.write("{} ".format(attr))
        f.close()

        print("Table {} altered.".format(instr.tableUsed))
def cmmdExit(instr) :
    sys.exit()
