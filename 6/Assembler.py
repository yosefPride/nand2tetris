#! python3
import sys

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} [path to file]')
    sys.exit()

from class_parser import Parser
from Code import Code

def Assembler(file_path):
    parser = Parser(file_path)
    binary_code = []
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == 'A_COMMAND':
            value = int(parser.current_command.split('@')[1])
            binary_code.append('0' + format(value, '015b'))
        else:
            comp = Code.get_comp(parser.comp())
            dest = Code.get_dest(parser.dest())
            jump = Code.get_jump(parser.jump())
            binary_code.append('111' + comp + dest + jump)

    hack_file_path = file_path.replace('.asm', '.hack')

    hack_file = open(hack_file_path, 'w')
    
    for item in binary_code:
        hack_file.write(item + "\n")
    hack_file.close()
    
    parser.close()

Assembler(sys.argv[1])
    
