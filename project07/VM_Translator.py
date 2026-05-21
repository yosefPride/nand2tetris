#! python3
import sys

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} [path to file]')
    sys.exit()

import os
from VM_Parser import Parser
from VM_code import Code

def VmTranslator(file_path):
    #Check if the file exists before proceeding
    if not os.path.isfile(file_path):
        print(f"Error: The file {file_path} does not exist.")
        sys.exit(1)  # Exit if the file doesn't exist
    if os.path.isfile(file_path):# Check if the file_path is a file
        parser = Parser(file_path)# construct the parser
        output_file = file_path.replace('.vm', '.asm')
        code = Code(output_file)# construct the codewriter with the out-put file name
        file_name = file_path.split('/')[2]
        print(f'the file name is: {file_name}')
        code.set_file_name(file_name)
        while parser.has_more_commands():# as long as there are more commands in the file
            parser.advance()# advance to the next command
            if parser.command_type() == 'c_arithmetic':# if it's an arithmetic command
                command = parser.arg1()# get command
                if command: # if command is not an empty string
                    code.write_arithmetic(command)# genarate assembly translation
                else:
                    print("Error: Received invalid command")
            elif parser.command_type() == 'c_push' or parser.command_type() == 'c_pop':# if it's a push or pop command
                command = parser.command_type().lower().split('c_')[1]# get command (e.g. push or pop)
                segment = parser.arg1()# get memory segment
                index = parser.arg2()# get index or value
                code.write_push_pop(command, segment, index)# genarate assembly translation
        parser.close()
        code.close()

    elif os.path.isdir(file_path):# Check if the file_path is a directory
        code = Code(os.path.join(file_path, os.path.basename(file_path) + '.asm'))# Initialize codewriter with the output file name
        for file in os.listdir(file_path):# Iterate through the files in the directory
            print(f"Checking file: {file}")  # Debug line to see the files being checked
            if file.endswith('.vm'):  # Process only .vm files
                code.set_file_name(file)  # Set the current file name
                full_file_path = os.path.join(file_path, file)# Get full path by joining directory path and file name
                parser = Parser(full_file_path)# construct the parser with the current file to process
                while parser.has_more_commands():# as long as there are more commands in the file
                    parser.advance()# advance to the next command
                    if parser.command_type() == 'c_arithmetic':# if it's an arithmetic command
                        command = parser.arg1()# get command
                        code.write_arithmetic(command)# genarate assembly translation
                    elif parser.command_type() == 'c_push' or parser.command_type() == 'c_pop':# if it's a push or pop command
                        command = parser.command_type().lower().split('c_')[1]# get command (e.g. push or pop)
                        segment = parser.arg1()# get memory segment
                        index = parser.arg2()# get index or value
                        code.write_push_pop(command, segment, index)# genarate assembly translation
                parser.close()
        code.close()

VmTranslator(sys.argv[1])

    #The main program should construct a Parser, to parse the VM
    #input file, and a CodeWriter, to generate code into the corresponding output file.
    #It should then march through the VM commands in the input file, and generate
    #assembly code for each one of them.
    #If the program’s argument is a directory name rather than a file name, the
    #main program should process all the .vm files in this directory. In doing so, it
    #should use a separate Parser for handling each input file and a single CodeWriter
    #for handling the output.

    #1. Check the Input Argument:
    #Determine if the argument is a file or a directory.
    #Use os or pathlib for this.
            
    #2. For a Single File:
    #If the input is a file:
    #Verify it ends with .vm.
    #Initialize a Parser for the file.
    #Initialize a CodeWriter with an output file name based on the input file name (e.g., replace .vm with .asm).
    #Process each command using the Parser and generate assembly code using the CodeWriter.
            
    #3. For a Directory:
    #If the input is a directory:
    #Find all .vm files in the directory.
    #Initialize a single CodeWriter with an output file named after the directory (e.g., directory_name.asm).
    #For each .vm file in the directory:
    #Create a Parser for that file.
    #Process each command in the file using the Parser and generate assembly code using the same CodeWriter.
