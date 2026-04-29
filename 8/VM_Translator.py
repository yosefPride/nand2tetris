#! python3
import sys

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} [path to file]')
    sys.exit()

import os
from VM_Parser import Parser
from VM_Code import Code

def VmTranslator(file_path):
    #Check if the file exists before proceeding
    if os.path.isfile(file_path):# Check if the file_path is a file
        parser = Parser(file_path)# construct the parser
        output_file = file_path.replace('.vm', '.asm')
        code = Code(output_file)# construct the codewriter with the out-put file name
        file_name = file_path.split('/')[2]
        code.set_file_name(file_name)
        code.write_init()
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
            elif parser.command_type() == 'c_label':# if it's a label command
                label = parser.arg1()# get label
                code.write_label(label)# generate assembly translation
            elif parser.command_type() == 'c_goto':# if it's a goto command
                label = parser.arg1()# get label
                code.write_goto(label)# generate assembly translation
            elif parser.command_type() == 'c_if':# if it's an if-goto command
                label = parser.arg1()# get label
                code.write_if(label)# generate assembly translation
            elif parser.command_type() == 'c_call':
                function_name = parser.arg1()
                num_args = parser.arg2()
                code.write_call(function_name, num_args)
            elif parser.command_type() == 'c_function':
                function_name = parser.arg1()
                num_locals = parser.arg2()
                code.write_function(function_name, num_locals)
            elif parser.command_type() == 'c_return':
                code.write_return()
        parser.close()
        code.close()

    elif os.path.isdir(file_path):# Check if the file_path is a directory
        code = Code(os.path.join(file_path, os.path.basename(file_path) + '.asm'))# Initialize codewriter with the output file name
        code.write_init()# Write bootstrap code
        for file in os.listdir(file_path):# Iterate through the files in the directory
            if file.endswith('.vm'):  # Process only .vm files
                print(f"Checking directory: {file}")  # Debug line to see the files being checked
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
                    elif parser.command_type() == 'c_label':# if it's a label command
                        label = parser.arg1()# get label
                        code.write_label(label)# generate assembly translation
                    elif parser.command_type() == 'c_goto':# if it's a goto command
                        label = parser.arg1()# get label
                        code.write_goto(label)# generate assembly translation
                    elif parser.command_type() == 'c_if':# if it's an if-goto command
                        label = parser.arg1()# get label
                        code.write_if(label)# generate assembly translation
                    elif parser.command_type() == 'c_call':
                        function_name = parser.arg1()
                        num_args = parser.arg2()
                        code.write_call(function_name, num_args)
                    elif parser.command_type() == 'c_function':
                        function_name = parser.arg1()
                        num_locals = parser.arg2()
                        code.write_function(function_name, num_locals)
                    elif parser.command_type() == 'c_return':
                        code.write_return()
                parser.close()
        code.close()

VmTranslator(sys.argv[1])
