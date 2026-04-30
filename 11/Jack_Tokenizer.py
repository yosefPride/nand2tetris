import re
import token


class JackTokenizer:

    def __init__(self, file_path):
        try:
            self.file = open(file_path, 'r')
        except FileNotFoundError:
            print(f"Error: {file_path} not found.")
            self.file = None
        self.current_token = None
        self.tokens = []
        self.keywords = ['class', 'method', 'function','constructor', 'int', 'boolean', 'char', 'void', 'var', 'static',
                         'field', 'let', 'do', 'if', 'else', 'while', 'return', 'true', 'false', 'null', 'this']
        self.symbols = ['[', ']', '{', '}', '(', ')', '=', '.', ',', '/', '+', '-', '*', '>', '<', ';', '&', '~', '|']

    def has_more_tokens(self):
        pos = self.file.tell()# pos = current line of the file (tell() gets the position)
        line = self.file.readline()# reads the next line of the file and stores it in 'line'
        if line:#check whole line so that it won't stop at an '\n' character
            self.file.seek(pos)  # Resets file pointer to previous position (pos) so that when
            #has_more_tokens() is called the file pointer remains at its original position
            return True # if there's another token return true
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
        elif self.current_token in self.symbols:
            return 'symbol'
        #re.match() detects patterns. the pattern is r'^[A-Za-z_]\w*$'.
        # ^             → Anchors the match to the start of the string
        # [A-Za-z_]     → First character must be a letter (A–Z, a–z) or an underscore (_)
        # \w*           → Followed by zero or more word characters:
        #                 - letters (A–Z, a–z)
        #                 - digits (0–9)
        #                 - underscore (_)
        # $             → Anchors the match to the end of the string
        elif re.match(r'^[A-Za-z_]\w*$', self.current_token) and self.current_token not in self.keywords:
            return 'identifier'
        elif self.current_token.isdigit() :
            return 'int_const'
        elif self.current_token.startswith('"') and self.current_token.endswith('"'):
            return 'string_const'
        return None #explicit return statement required.

    def keyword(self):
        return self.current_token

    def symbol(self):
        # xml_markups = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
        # if  self.current_token in xml_markups:
        #     self.current_token = xml_markups.get(self.current_token)
        return self.current_token

    def identifier(self):
        return self.current_token

    def int_val(self):
        return self.current_token

    def string_val(self):
        token = self.current_token.split('"')[1]
        return token

    def close(self):#closes input file
        self.file.close()

# if __name__ == '__main__':
# # ADD TEST TO SEE IF "Square" TRANSFORMS TO "square".
#     tokenizer = JackTokenizer('Square/Square.jack')
#     while tokenizer.has_more_tokens():
#         tokenizer.advance()
#         print(tokenizer.current_token)