import re

class JackTokenizer:

    def __init__(self, file_path):#, output_file_path):
        try:
            self.file = open(file_path, 'r')
            # print(f"File {file_path} opened successfully.")
##            self.output_file = open(output_file_path, 'w')
        except FileNotFoundError:
            print(f"Error: {file_path} not found.")
            self.file = None
        self.current_token = None
        self.tokens = []
##        self.output_file.write('<tokens>' + '\n')
        self.keywords = ['class', 'method', 'function','constructor', 'int', 'boolean', 'char', 'void', 'var', 'static',
                         'field', 'let', 'do', 'if', 'else', 'while', 'return', 'true', 'false', 'null', 'this']
        self.chars = ['[', ']', '{', '}', '(', ')', '=', '.', ',', '/', '+', '-', '*', '>', '<', ';', '&', '~', '|']

    def has_more_tokens(self):
        pos = self.file.tell()# pos = current line of the file (tell() gets the position)
        line = self.file.readline()# reads the next line of the file and stores it in 'line'
        if line:#check whole line so that it won't stop at an '\n' character
            self.file.seek(pos)  # Resets file pointer to previous position (pos) so that when
            #has_more_tokens() is called the file pointer remains at its original position
            return True # if there's another token return true
##        self.output_file.write('</tokens>' + '\n')
        return False # otherwise return false

    def advance(self):
        if not self.has_more_tokens(): # if there aren't more tokens
            raise ValueError("No more tokens!")
        if not self.tokens:#if self.tokens is an empty list
            line = self.file.readline().split('//')[0].strip()
            line = line.split('/**')[0].strip()#get rid of comments and whitespace
            if line.startswith('*'):
                line = line.split('*')[0].strip()
            regex = r'"[^"]*"|[{}()[\].,;+\-*/&|<>=~]|\w+'#keeps a string in its original form so that I can check
            #for strings in "token_type()". allows the set of characters and alphanumeric values (including '_').
            self.tokens = re.findall(regex, line)#separates the line into individual tokens
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.advance()

    def token_type(self):
        if self.current_token in self.keywords:
            return 'keyword'
        elif self.current_token in self.chars:
            return 'symbol'
        elif self.current_token.isalpha() and self.current_token not in self.keywords:
            return 'identifier'
        elif self.current_token.isdigit() :
            return 'int_const'
        elif self.current_token.startswith('"') and self.current_token.endswith('"'):
            return 'string_const'

    def keyword(self):
        if self.token_type() == 'keyword':
##            self.output_file.write('\t' + '<keyword>' + ' ' +  self.current_token + ' ' + '</keyword>' + '\n')
            return '<keyword>' + ' ' +  self.current_token + ' ' + '</keyword>' + '\n'

    def symbol(self):
        if self.token_type() == 'symbol':
            xml_markups = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
            if  self.current_token in xml_markups:
                self.current_token = xml_markups.get(self.current_token)
##            self.output_file.write('\t' + '<symbol>' + ' ' + self.current_token + ' ' + '</symbol>' + '\n')
            return '<symbol>' + ' ' + self.current_token + ' ' + '</symbol>' + '\n'

    def identifier(self):
        if self.token_type() == 'identifier':
##            self.output_file.write('\t' + '<identifier>' + ' ' + self.current_token + ' ' + '</identifier>' + '\n')
            return '<identifier>' + ' ' + self.current_token + ' ' + '</identifier>' + '\n'

    def int_val(self):
        if self.token_type() == 'int_const':
            return '<integerConstant>' + ' ' + self.current_token + ' ' + '</integerConstant>' + '\n'
##            self.output_file.write('\t' + '<integerConstant>' + ' ' + self.current_token + ' ' + '</integerConstant>' + '\n')

    def string_val(self):
        if self.token_type() == 'string_const':
            token = self.current_token.split('"')[1]
            return '<stringConstant>' + ' ' + token + ' ' + '</stringConstant>' + '\n'
##            self.output_file.write('\t' + '<stringConstant>' + ' ' + token + ' ' + '</stringConstant>' + '\n')

    def close(self):#closes input file
        self.file.close()
##        self.output_file.close()

if __name__ == "__main__":
    tokenizer = JackTokenizer('Square/Square.jack')#Or any other file I want to test
    while tokenizer.has_more_tokens():
        tokenizer.advance()
        tokenizer.keyword()
        tokenizer.symbol()
        tokenizer.identifier()
        tokenizer.int_val()
        tokenizer.string_val()

    tokenizer.close()
