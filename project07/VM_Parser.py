class Parser:

    #def __init__(self, file_path):
       # self.file = open(file_path, 'r')
       # self.current_command = None
    def __init__(self, file_path):
        try:
            self.file = open(file_path, 'r')
            print(f"File {file_path} opened successfully.")
        except FileNotFoundError:
            print(f"Error: {file_path} not found.")
            self.file = None
        self.current_command = None

    def has_more_commands(self):
        pos = self.file.tell()# pos = current line of the file (tell() gets the position)
        line = self.file.readline()# reads the next line of the file and stores it in "line"
        if line:# checks if "line" is an empty string
            self.file.seek(pos)  # Resets file pointer to previous position (pos) so that when
            #has_more_commands() is called the file pointer remains at it's original position
            return True # if there is another command return true
        return False # otherwise return false

    def advance(self):
        if self.has_more_commands(): # if there are more commands
            line = self.file.readline().strip() # Reads next line of the file and removes leading&trailing whitespace
            line = line.split('//')[0].strip() # removes comments
            if line:  # Checks if the line still has content after removing comments and extra whitespace
                self.current_command = line # if it does stores it in self.current_command
                print(f"Processing command: {self.current_command}")
            else: 
                self.advance()  # Skips to next valid command

    def command_type(self):
        command = self.current_command.split()[0].lower()  # convert everything to lower case
        if command in {'add', 'sub', 'neg', 'and', 'or', 'not','eq', 'gt', 'lt'}:
            return 'c_arithmetic'
        elif command == 'push':
            return 'c_push'
        elif command == 'pop':
            return 'c_pop'
        elif command == 'label':
            return 'c_label'
        elif command == 'goto':
            return 'c_goto'
        elif command == 'if-goto':
            return 'c_if'
        elif command == 'function':
            return 'c_function'
        elif command == 'return':
            return 'c_return'
        else:
            return 'c_call'
        
    def arg1(self):
        if self.command_type() == 'c_arithmetic':
            return self.current_command.split()[0]# if it's an arithmetic command return the command itself 
        elif not self.command_type() in {'c_return', 'c_arithmetic'}: 
            return self.current_command.split()[1] # return segment (second index)    
                                            
    def arg2(self):
        if self.command_type() in {'c_push', 'c_pop', 'c_function', 'c_call'}: 
            return self.current_command.split()[2] # return index (third index)

    def close(self):
        self.file.close()
