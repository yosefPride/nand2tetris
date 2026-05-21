#! python3
import sys

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} [path to file]')
    sys.exit()

from Parser_Symbol import Parser
from Code import Code
from Symbol_Table import SymbolTable

def Assembler_Symbol(file_path):
    #first pass
    symbol_table = SymbolTable()#constructer for the symbol table
    parser = Parser(file_path)#constructer for the parser
    rom_address = 0
    
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == 'L_COMMAND':
            symbol = parser.symbol()
            symbol_table.add_entry(symbol, rom_address)#if there are any lables add them to the symbol table
        else:
            rom_address += 1
                                             
    #second pass
    parser = Parser(file_path)
    binary_code = []
    next_avilable_address = 16 #address for variables
    
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == 'A_COMMAND':
            symbol = parser.symbol()
            if symbol.isdigit():#check if it's an intager
                value = int(symbol)#if is digit return value
            else:
                if not symbol_table.contains(symbol):#if is not digit check if in symbol table if not 
                    symbol_table.add_entry(symbol, next_avilable_address)#add to symbol table
                    next_avilable_address += 1 #address is taken so moving to the next one
                value = symbol_table.get_address(symbol)#get value from the symbol table 
            binary_code.append('0' + format(value, '015b'))
        elif parser.command_type() == 'C_COMMAND':
            comp = Code.get_comp(parser.comp())
            dest = Code.get_dest(parser.dest())
            jump = Code.get_jump(parser.jump())
            binary_code.append('111' + comp + dest + jump)

    hack_file_path = file_path.replace('.asm', '.hack')

    hack_file = open(hack_file_path, 'w')
    
    for item in binary_code:
        hack_file.write(item + "\n")
    hack_file.close()
    
    parser.close() #method in parser class to close the input file

Assembler_Symbol(sys.argv[1])
    
