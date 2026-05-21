#! python3
import sys

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} [path to file]')
    sys.exit()

import os
from Compilation_Engine import CompilationEngine
from pathlib import Path # pathlib is an object-oriented replacement for os.path, used for filesystem paths.

def jack_analyzer(file_path):
    if os.path.isfile(file_path):# Check if the file_path is a file
        output_file = file_path.replace('.jack', '.xml')
        compilation_engine = CompilationEngine(file_path, output_file)
        #construct the compilation engine with the out-put file name
        compilation_engine.compile_class()
        compilation_engine.close()
        print('finished compiling')


    elif os.path.isdir(file_path):# Check if the file_path is a directory
        directory = Path(file_path) # The truth is that I don't need to use both pathlib's Path and os.path, I should use only one of them.
        for file in directory.glob("*.jack"): # Returns all files or directories matching a specified pattern
            output_file = file.with_suffix('.xml') # replaces all specified suffixes above (.jack) with (.xml)
            compilation_engine = CompilationEngine(str(file), str(output_file))  # CompilationEngine takes two strings as inputs
            print(f"Checking file: {file}")  # Debug line to see the files currently being checked
            compilation_engine.compile_class()
            compilation_engine.close()
        print('finished compiling')

jack_analyzer(sys.argv[1])
