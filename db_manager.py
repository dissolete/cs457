import os
from parser import Instruction

currDb = "" #Used to store the current database
currDir = os.getcwd();

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
    print("Use command")

def cmmdCreateDB(instr) :
    print("Create DB command")

def cmmdDropDB(instr) :
    print("Drop DB command")

def cmmdCreateTable(instr) :
    print("Create Table command")

def cmmdDropTable(instr) :
    print("Drop Table command")

def cmmdSelect(instr) :
    print("Select command")

def cmmdAlterTable(instr) :
    print("Alter table command")

def cmmdExit(instr) :
    print("Exit command")