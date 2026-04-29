from Jack_Tokenizer import JackTokenizer
from Symbol_Table import SymbolTable

class CompilationEngine:

    def __init__(self, input_file_path, output_file_path):
        self.input_file = open(input_file_path, 'r')
        self.output_file = open(output_file_path, 'w')
        self.tokenizer = JackTokenizer(input_file_path)
        self.class_symbol_table = SymbolTable()
        self.iden_type = self.iden_kind = self.class_name = None
        # wherever there is a '*' sign it means one or more. wherever there is a '?' sign it means zero or one.

    def compile_class(self):
        #CLASS STRUCTURE: 'class' className '{' classVarDec(*zero or more) subroutineDec(*zero or more) '}'
        self.output_file.write('<class>' + '\n')
        self.output_file.write('\n')
        self.tokenizer.advance() # 'class'
        self.tokenizer.advance()
        self.class_name = self.tokenizer.current_token # I need this because every method's symbol table starts with "this, class_name, arg, 0"
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            if self.tokenizer.current_token in {'field', 'static'}:
                self.compile_class_var_dec()
            elif self.tokenizer.current_token in {'constructor','function', 'method'}:
                self.compile_subroutine()
        for key in self.class_symbol_table.fields:
            self.output_file.write(key)
            self.output_file.write(', ')
            self.output_file.write(self.class_symbol_table.kind_of(key))
            self.output_file.write(', ')
            self.output_file.write(self.class_symbol_table.type_of(key))
            self.output_file.write(', ')
            self.output_file.write(str(self.class_symbol_table.index_of(key)))
            self.output_file.write('\n')
        self.output_file.write('\n')
        self.output_file.write('</class>' + '\n')

    def compile_class_var_dec(self):
        #CLASS VAR DEC SYNTAX: ('static' | 'field') type varName (',' varName)*zero or more ';'
        self.iden_kind = self.tokenizer.current_token
        self.tokenizer.advance()
        self.iden_type = self.tokenizer.current_token
        self.tokenizer.advance()
        self.class_symbol_table.define(self.tokenizer.current_token, self.iden_type, self.iden_kind)
        self.tokenizer.advance()
        if self.tokenizer.current_token == ',':  # optional second variable separated by a comma ','.
            while self.tokenizer.current_token != ';':
                self.tokenizer.advance()
                self.class_symbol_table.define(self.tokenizer.current_token, self.iden_type, self.iden_kind)
                self.tokenizer.advance()

    def compile_subroutine(self):
        # SUBROUTINE DEC STRUCTURE: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        # subroutine dec
        self.output_file.write('<subroutine>' + '\n')
        if self.tokenizer.current_token == 'method':
            self.class_symbol_table.define('this', self.class_name, 'arg')
        self.tokenizer.advance() # void, type
        self.tokenizer.advance() # subroutineName
        self.tokenizer.advance() # opening parenthesis '('
        self.compile_parameter_list()  # parameterList #I don't advance here so I can look ahead in compile_parameter()

        # SUBROUTINE BODY STRUCTURE: '{' varDec (*zero or more) statements '}'
        # subroutine body
        self.tokenizer.advance() # opening curley bracket '{'
        self.tokenizer.advance()
        while self.tokenizer.current_token != 'return':
            if self.tokenizer.current_token == 'var':  # zero or more var decs.
                self.compile_var_dec()
                self.tokenizer.advance()
            self.tokenizer.advance()
        for key in self.class_symbol_table.args:
            self.output_file.write(key)
            self.output_file.write(', ')
            self.output_file.write(self.class_symbol_table.kind_of(key))
            self.output_file.write(', ')
            self.output_file.write(self.class_symbol_table.type_of(key))
            self.output_file.write(', ')
            self.output_file.write(str(self.class_symbol_table.index_of(key)))
            self.output_file.write('\n')
        for key in self.class_symbol_table.vars:
            self.output_file.write(key)
            self.output_file.write(', ')
            self.output_file.write(self.class_symbol_table.kind_of(key))
            self.output_file.write(', ')
            self.output_file.write(self.class_symbol_table.type_of(key))
            self.output_file.write(', ')
            self.output_file.write(str(self.class_symbol_table.index_of(key)))
            self.output_file.write('\n')
        self.class_symbol_table.start_subroutine()
        self.output_file.write('</subroutine>' + '\n')
        self.output_file.write('\n')

    def compile_parameter_list(self):
        #PARAMETER LIST SYNTAX: type varName (',' type varName)*zero or more
        self.tokenizer.advance()
        if self.tokenizer.current_token != ')':
            # (food for thought: it's possible for a type to be user-defined, in which case it would be an identifier)
            self.iden_type = self.tokenizer.current_token # Type.
            self.tokenizer.advance() # var name.
            self.class_symbol_table.define(self.tokenizer.current_token, self.iden_type, 'arg')
            self.tokenizer.advance()
            while self.tokenizer.current_token != ')':
                self.tokenizer.advance()
                self.iden_type = self.tokenizer.current_token  # Type.
                self.tokenizer.advance()  # var name.
                self.class_symbol_table.define(self.tokenizer.current_token, self.iden_type, 'arg')
                self.tokenizer.advance()

    def compile_var_dec(self):
        #VAR DEC SYNTAX: 'var' type varName (',' varName)*zero or more. ';'
        self.iden_kind = self.tokenizer.current_token # 'var'
        self.tokenizer.advance()
        self.iden_type = self.tokenizer.current_token # type.
        self.tokenizer.advance() #var name.
        self.class_symbol_table.define(self.tokenizer.current_token, self.iden_type, self.iden_kind)
        self.tokenizer.advance() # if there's only one var, this is ';'. otherwise it's a comma ','.
        if self.tokenizer.current_token == ',':  # optional additional variables separated by a comma ','
            while self.tokenizer.current_token != ';':
                self.tokenizer.advance()  # var name.
                self.class_symbol_table.define(self.tokenizer.current_token, self.iden_type, self.iden_kind)
                self.tokenizer.advance()

    def close(self):
        self.tokenizer.close()
        self.input_file.close()
        self.output_file.close()

if __name__ == "__main__":
    parser = CompilationEngine('Pong/Ball.jack', 'Pong/Ball.txt')#change input and output files
    import time
    start_time = time.time()
    parser.compile_class()
    end_time = time.time()
    parser.close()
    print("Runtime: ", round(end_time - start_time, 4), " seconds")