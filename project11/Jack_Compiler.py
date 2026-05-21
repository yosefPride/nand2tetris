#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} [path to file/directory]')
    sys.exit()

import os
from Compilation_Engine import CompilationEngine
from pathlib import Path # pathlib is an object-oriented replacement for os.path, used for filesystem paths.

def jack_compiler(file_path):
    if os.path.isfile(file_path):# Check if the file_path is a file
        output_file = file_path.replace('.jack', '.vm')
        compilation_engine = CompilationEngine(file_path, output_file)
        #construct the compilation engine with the out-put file name
        compilation_engine.compile_class()
        compilation_engine.close()
        print('finished compiling')

# WHENEVER A WE WANT TO RUN A PROGRAM ON THE VM EMULATOR, WE MUST LOAD THE JACK OS AS WELL AS THE .VM FILES

    elif os.path.isdir(file_path):# Check if the file_path is a directory
        directory = Path(file_path) # The truth is that I don't need to use both pathlib's Path and os.path, I should use only one of them.
        for file in directory.glob("*.jack"): # Returns all files or directories matching a specified pattern
            output_file = file.with_suffix('.vm') # replaces all specified suffixes above (.jack) with (.vm)
            compilation_engine = CompilationEngine(str(file), str(output_file))  # CompilationEngine takes two strings as inputs
            print(f"Checking file: {file}")  # Debug line to see the files currently being checked
            compilation_engine.compile_class()
            # print('got here' + '\n')
            compilation_engine.close()
        print('finished compiling')

jack_compiler(sys.argv[1])

# RECOMMENDED TESTING METHOD:
# 1) copy all supplied OS files from tools/OS into the program directory, together with the supplied jack file/s
# 2) compile the program directory
# 3) if there are any errors, fix compiler and return to step 2
# 4) at this point the program directory should contain a single .vm file for each .jack file, as well as the supplied OS files. if it doesn't go back to step 3
# 5) execute the vm files in the VM emulator, loading the entire directory and using 'no animation' mode.
# 6) if the program behaves unexpectedly or some error message is displayed, go back to step 3