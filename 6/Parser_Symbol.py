class Parser:
    
    def __init__(self, file_path):
        self.file = open(file_path, 'r')
        self.current_command = None
        self.line = None
        self.value = None
                
    def has_more_commands(self):
        pos = self.file.tell()
        line = self.file.readline()
        if line:
            self.file.seek(pos)  # Reset file pointer to previous position
            return True
        return False

    def advance(self): 
        if self.has_more_commands():
            line = self.file.readline().strip()
            line = line.split('//')[0].strip()
            if line:  # Skip empty lines
                self.current_command = line
            else:
                self.advance()  # Skip to the next valid command
        
    def command_type(self):
        if self.current_command.startswith('@'):
            return 'A_COMMAND'
        elif self.current_command.startswith('('):
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'

    def symbol(self):
        if self.command_type() == 'A_COMMAND':
            return self.current_command[1:]  # Return the part after '@', could be a number or a symbol
        elif self.command_type() == 'L_COMMAND':
            return self.current_command[1:-1] #return label without perantheses
        
    def comp(self):
        if self.command_type() == 'C_COMMAND':
            if '=' in self.current_command:
                comp = self.current_command.split('=')[1]
            elif ';' in self.current_command:
                comp = self.current_command.split(';')[0]
            return comp
        return None

    def dest(self):
        if self.command_type() == 'C_COMMAND':
            if '=' in self.current_command:
                return self.current_command.split('=')[0]
        return ''

    def jump(self):
        if self.command_type() == 'C_COMMAND':
            if ';' in self.current_command:
                return self.current_command.split(';')[1]
        return ''

    def close(self):
        self.file.close()
