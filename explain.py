#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This software must not be used by military or secret service organisations.
import os, sys, argparse
from subprocess import call, check_output

version = "0.0.1#alpha"
parser = argparse.ArgumentParser(description="explain " + version + "\nhttps://github.com/honze-net/explain", epilog="This software must not be used by military or secret service organisations.", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("command", help="Command to explain in double quotes, e.g. \"ls -lisah\"")
if len(sys.argv) == 1: # If no arguments are specified, print help and exit.
    parser.print_help()
    sys.exit(1)    
args = parser.parse_args()
command = args.command

current_tool = ""

def next_token(command, delimiter=" "):
    if delimiter not in command:
        return (command, "")
    return command.split(" ",1)


print("Explaining: " + command)

while len(command) > 0:
    if command[0] == " ":
        command = command[1:]
        continue
    if command[0].isalpha():
        (tool, command) = next_token(command)
        if call(["man", "-f", tool]) == 0:
            current_tool = tool
        continue
    if command[0] == '-':
        (option, command) = next_token(command)
        output = check_output(["./manopt.sh", current_tool, option])
        if len(output) > 0:
            print(output)
        else:
            for char in option:
                if char.isalpha():
                    call(["./manopt.sh", tool, "-"+char])
        continue
    if command[:2] == "||":
        print("\n||\n")
        command = command[2:]
        continue
    if command[:2] == "&&":
        print("\n&&\n")
        command = command[2:]
        continue
    if command[0] == "|":
        print("\n|\n")
        command = command[1:]
        continue
    (skip, command) = next_token(command)
    print(skip)
