from Jack_Tokenizer import JackTokenizer
from Symbol_Table import SymbolTable
from VM_Writer import VMWriter

class CompilationEngine:

    def __init__(self, input_file_path, output_file):
        self.input_file = open(input_file_path, 'r')
        self.tokenizer = JackTokenizer(input_file_path)
        self.vm_writer = VMWriter(output_file)
        self.iden_type = self.iden_kind = self.op = self.class_name = None
        self.symbol_table = SymbolTable()
        self.label_counter = 0
        self.num_locals = self.num_args = 0
        self.special_ops = {'*':'Math.multiply', '/':'Math.divide'}
        self.objects = {}
        self.pop_value = ''

    def get_unique_label(self, base_name):
        label = f"{base_name}_{self.label_counter}"
        self.label_counter += 1
        return label

    def compile_class(self):
        # CLASS STRUCTURE: 'class' className '{' classVarDec(*zero or more) subroutineDec(*zero or more) '}'
        self.tokenizer.advance()  # 'class'
        self.tokenizer.advance()  # class name
        self.class_name = self.tokenizer.current_token  # if it causes problems move this under the next advance.
        self.tokenizer.advance()
        while self.tokenizer.has_more_tokens() and self.tokenizer.current_token != '}':
            if self.tokenizer.current_token in {'field', 'static'}:
                self.compile_class_var_dec()
            elif self.tokenizer.current_token in {'constructor', 'function', 'method'}:
                self.compile_subroutine()
            self.tokenizer.advance()

    def compile_class_var_dec(self):
        # CLASS VAR DEC SYNTAX: ('static' | 'field') type varName (',' varName)*zero or more ';'
        self.iden_kind = self.tokenizer.current_token
        self.tokenizer.advance()
        self.iden_type = self.tokenizer.current_token
        self.tokenizer.advance()
        self.symbol_table.define(self.tokenizer.current_token, self.iden_type, self.iden_kind)
        self.tokenizer.advance()
        if self.tokenizer.current_token == ',':  # optional second variable separated by a comma ','.
            while self.tokenizer.current_token != ';':
                self.tokenizer.advance()
                self.symbol_table.define(self.tokenizer.current_token, self.iden_type, self.iden_kind)
                self.tokenizer.advance()

    def compile_subroutine(self):
        self.symbol_table.start_subroutine() # creates new subroutine symbol table.
        if self.tokenizer.current_token == 'function':
            self.tokenizer.advance() # type
            self.tokenizer.advance() # name
            name = self.tokenizer.identifier() # name
            self.tokenizer.advance()  # opening parenthesis
            self.compile_parameter_list()
            self.tokenizer.advance()  # closing parenthesis

            #SUBROUTINE BODY
            self.tokenizer.advance() # opening curly bracket
            while self.tokenizer.current_token == 'var':
                self.compile_var_dec()
                self.tokenizer.advance()
            self.vm_writer.write_function(self.class_name + '.' + name, self.num_locals)
            self.num_locals = 0
            while self.tokenizer.current_token in {'if', 'while', 'let', 'do', 'return'}:
                self.compile_statements()

        elif self.tokenizer.current_token == 'constructor':
            # "constructor" type constructorName '(' parameterList ')' constructor body
            self.tokenizer.advance() #type
            self.tokenizer.advance() #name
            name = self.tokenizer.identifier() # name
            self.tokenizer.advance() # opening parenthesis
            self.compile_parameter_list()
            self.tokenizer.advance() # closing parenthesis

            # SUBROUTINE BODY
            self.tokenizer.advance()  # opening curley bracket
            while self.tokenizer.current_token == 'var':
                self.compile_var_dec()
                self.tokenizer.advance()
            self.vm_writer.write_function(self.class_name + '.' + name, self.num_locals)
            self.num_locals = 0
            self.vm_writer.write_push('constant', self.symbol_table.var_count('field')) # setting the amount of space to allocate according to how many field variables there are.
            self.vm_writer.write_call('Memory.alloc', 1) # calls memory.alloc on the number pushed above.
            self.vm_writer.write_pop('pointer', 0) # anchors 'this' at the base address. so that when the constructor gets called, the caller can then use the base address of the object
            while self.tokenizer.current_token in {'if', 'while', 'let', 'do', 'return'}:
                self.compile_statements()

        elif self.tokenizer.current_token == 'method':
            self.tokenizer.advance()  # type
            self.tokenizer.advance()  # name
            name = self.tokenizer.identifier() # name
            self.tokenizer.advance()  # opening parenthesis
            self.symbol_table.define('this', self.class_name, 'arg')
            self.compile_parameter_list()
            self.tokenizer.advance()  # closing parenthesis

            # SUBROUTINE BODY
            self.tokenizer.advance()  # opening curly bracket
            while self.tokenizer.current_token == 'var':
                self.compile_var_dec()
                self.tokenizer.advance()
            self.vm_writer.write_function(self.class_name + '.' + name, self.num_locals)
            self.num_locals = 0
            self.vm_writer.write_push('argument', 0)
            self.vm_writer.write_pop('pointer', 0)
            while self.tokenizer.current_token in {'if', 'while', 'let', 'do', 'return'}:
                self.compile_statements()

    def compile_parameter_list(self): # adds all arguments to the arg symbol table.
        # PARAMETER LIST SYNTAX: type varName (',' type varName)*zero or more
        while self.tokenizer.current_token != ')':
            self.tokenizer.advance()
            if self.tokenizer.current_token != ')': #this is where I added a line.
                self.iden_type = self.tokenizer.current_token  # type. and I should think about the possibility of it being AN 'identifier'
                self.tokenizer.advance()
                self.symbol_table.define(self.tokenizer.identifier(), self.iden_type, 'arg')  # varName
                self.tokenizer.advance()

    def compile_var_dec(self):
        # VAR DEC SYNTAX: 'var' type varName (',' varName)*zero or more. ';'
        self.tokenizer.advance() #type
        self.iden_type = self.tokenizer.current_token
        while self.tokenizer.current_token != ';':
            self.tokenizer.advance()
            self.symbol_table.define(self.tokenizer.current_token, self.iden_type, 'var')
            self.tokenizer.advance()
            self.num_locals += 1

    def compile_statements(self):
        if self.tokenizer.current_token == 'if':
            self.compile_if()
        elif self.tokenizer.current_token == 'while':
            self.compile_while()
        elif self.tokenizer.current_token == 'let':
            self.compile_let()
        elif self.tokenizer.current_token == 'do':
            self.compile_do()
        elif self.tokenizer.current_token == 'return':
            self.compile_return()

    def compile_if(self):
        # IF SYNTAX: 'if' '(' expression ')' '{' statements '}'
        # VM syntax for 'if': compile expression, 'not', if-goto label, label, statements
        self.tokenizer.advance()
        # opening parenthesis
        self.tokenizer.advance()
        self.compile_expression()
        self.vm_writer.write_arithmetic('~') # not
        label1 = self.get_unique_label('L')
        self.vm_writer.write_if(label1)
        # closing parenthesis
        self.tokenizer.advance()
        # left curly bracket '{'
        while self.tokenizer.token_type() == 'symbol':
            self.tokenizer.advance()

        label2 = self.get_unique_label('L')
        while self.tokenizer.current_token != '}':
            self.compile_statements()

        # For the if statement '}'
        self.tokenizer.advance()  # since there isn't always an 'else' statement, I'll need to advance after every statement.
        if self.tokenizer.current_token == 'else':
            self.vm_writer.write_goto(label2)
        self.vm_writer.write_label(label1)

        # ELSE SYNTAX: ('else' '{' statements '}')? zero or one.
        if self.tokenizer.current_token == 'else':
            # 'else'
            self.tokenizer.advance()
            # left curly bracket '{'
            self.tokenizer.advance()
            while self.tokenizer.current_token != '}':
                self.compile_statements()
            self.vm_writer.write_label(label2)
            # right curly bracket '}'
            self.tokenizer.advance()  # I'm advancing here (and in all the other statements) so that I can peacefully advance to check for 'else' statements.

    def compile_while(self):
        # WHILE SYNTAX: 'while' '(' expression ')' '{' statements '}'
        self.tokenizer.advance()
        self.tokenizer.advance() # Opening parenthesis
        expression_false = self.get_unique_label('L')
        self.vm_writer.write_label(expression_false)
        self.compile_expression()
        self.vm_writer.write_arithmetic('~')
        expression_true = self.get_unique_label('L')
        self.vm_writer.write_if(expression_true)
        self.tokenizer.advance() #')'
        self.tokenizer.advance() #'{'
        while self.tokenizer.current_token != '}':
            self.compile_statements()
        self.vm_writer.write_goto(expression_false)
        self.vm_writer.write_label(expression_true)
        self.tokenizer.advance()

    def compile_let(self):
        # LET SYNTAX: 'let' varname ('[' expression ']')? '=' expression ';' # '?' meaning zero or one.
        # when I encounter a variable, I look it up in the subroutine level symbol table, if it isn't there, I look it up in the class level symbol table,
        # and if I can't find it there either, then I know that it's undefined.
        # EXAMPLE FOR LET STATEMENT: let y = y + dy; VM CODE: push this 1, push local 1, add, pop this 1.
        self.tokenizer.advance()
        self.pop_value = self.tokenizer.identifier()  # variable to which I will pop
        self.tokenizer.advance()  # if it's assigning a value to an index in an array then this is a '[', otherwise it's a '='.
        self.tokenizer.advance()
        self.compile_expression()  # expression
        # if it's assigning a value to an index in an array then this is a ']', otherwise it's a ';'.
        self.tokenizer.advance() #even if there isn't a continuation here I need to advance, because I need to advance in compile_if().
        if self.tokenizer.current_token == '=': # I only get here when it's assigning a value to an array index. so this is a '=' sign.
            self.tokenizer.advance()
            self.compile_expression()  # expression
            self.tokenizer.advance() # I advance here and in all other statements, because I need to advance in compile_if().
        self.vm_writer.write_pop(self.symbol_table.kind_of(self.pop_value), self.symbol_table.index_of(self.pop_value)) # popping the final result into the let statement's variable.

    def compile_do(self):
        # DO SYNTAX: 'do' subroutineCall ';'.
        # subroutine syntax = subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
        self.tokenizer.advance()
        self.compile_expression()
        self.tokenizer.advance() #';'
        self.vm_writer.write_pop('temp', 0) # gets rid of the return value.

    def compile_return(self):
        # RETURN SYNTAX: 'return' expression? zero or one times. ';'
        self.tokenizer.advance()
        if self.tokenizer.current_token == ';':
            self.vm_writer.write_push('constant', 0)
        else: self.compile_expression()
        self.vm_writer.write_return()
        self.tokenizer.advance()  # I'm advancing here (and in all the other statements) so that I can peacefully advance to check for 'else' statements.

    def compile_expression(self):
        # EXPRESSION SYNTAX: term (operator, term)* ("*" means zero or more)
        self.compile_term()
        if self.tokenizer.current_token in {'+', '-', '=', '|', '>', '<', '&'}:
            op = self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compile_term()
            self.vm_writer.write_arithmetic(op)
        elif self.tokenizer.current_token in {'*', '/'}:
            op = self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compile_term()
            self.vm_writer.write_call(self.special_ops.get(op), 2)

    def compile_expression_list(self):
        # EXPRESSION LIST SYNTAX: (expression (',' expression)*)? there can be an empty expression list, or a list with one or more expressions.
        self.tokenizer.advance()
        self.num_args = 0
        while self.tokenizer.current_token != ')':
            self.compile_expression()
            if self.tokenizer.current_token != ')':
                self.tokenizer.advance() #this is to advance past the commas ','. check that this is right.
            self.num_args += 1

    def compile_term(self):
        # TERM SYNTAX: intConst | strConst | keywordConst | (varname | varname '[' expression ']') | subroutineCall | '(' expression ')') | unaryOp term.
        if self.tokenizer.token_type() == 'int_const':
            self.vm_writer.write_push('constant', self.tokenizer.int_val()) # 'push' 'constant' val
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'string_const':
            self.vm_writer.write_call('String.new', 1)
            string = self.tokenizer.current_token.list()
            for letter in string:
                self.vm_writer.write_push('constant', ord(letter))
                self.vm_writer.write_call('String.appendChar', 2) #two, because I need to keep arg 0/this 0 in mind.
                self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'keyword': #true, false, null, and this.
            if self.tokenizer.current_token in ('false', 'null'):
                self.vm_writer.write_push('constant', 0)
            elif self.tokenizer.current_token == 'true':
                self.vm_writer.write_push('constant', 1)
                self.vm_writer.write_arithmetic('neg')
            else: self.vm_writer.write_push('pointer', 0)
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'identifier':
            iden_name = self.tokenizer.identifier()
            self.tokenizer.advance()
            if self.tokenizer.current_token == '.':  # subroutine call
                self.tokenizer.advance() # subroutine name
                subroutine_name = self.tokenizer.identifier()
                self.tokenizer.advance() # opening parenthesis
                self.compile_expression_list()
                if iden_name in self.objects:
                    if iden_name == self.class_name:
                        self.vm_writer.write_push(self.symbol_table.kind_of(iden_name), self.symbol_table.index_of(iden_name))
                    else:
                        self.vm_writer.write_push(self.symbol_table.kind_of(iden_name),
                                                  self.symbol_table.index_of(iden_name))
                    self.vm_writer.write_call(self.objects[iden_name] + '.' + subroutine_name, 1)
                else:
                    if subroutine_name == 'new':
                        self.objects[str(self.pop_value)] = str(iden_name)
                    self.vm_writer.write_call(iden_name + '.' + subroutine_name, self.num_args)

                self.tokenizer.advance()
            elif self.tokenizer.current_token == '[': #push arr, push index, add, pop pointer 1 (that 0)
                self.vm_writer.write_push(self.symbol_table.kind_of(iden_name), self.symbol_table.index_of(iden_name))
                self.tokenizer.advance()
                self.compile_expression()
                self.tokenizer.advance() # ']'
                self.vm_writer.write_arithmetic('+') #add the index to the base address of the array.
                self.vm_writer.write_pop('pointer', 1) # I pop the index into "that 0".
            elif self.tokenizer.current_token == '(':
                self.vm_writer.write_push('pointer', 0)
                self.compile_expression_list()
                self.vm_writer.write_call(self.class_name + '.' +  iden_name, self.num_args + 1) # + 1 because of "this"
                self.tokenizer.advance()
            else:
                self.vm_writer.write_push(self.symbol_table.kind_of(iden_name), self.symbol_table.index_of(iden_name))
        elif self.tokenizer.token_type() == 'symbol':  # and not self.tokenizer.current_token in {'-', '~'}:
            if self.tokenizer.current_token == '(':
                self.tokenizer.advance()
                self.compile_expression()
                self.tokenizer.advance()
            elif self.tokenizer.current_token in {'-', '~'}:
                if self.tokenizer.current_token == '-': #I can't have '-' as two different operators in the commands dictionary. (sub & neg)
                    self.op = 'neg'
                else: self.op = self.tokenizer.current_token
                self.tokenizer.advance()
                self.compile_expression()
                self.vm_writer.write_arithmetic(self.op)

    def close(self):
        self.tokenizer.close()
        self.input_file.close()
        self.vm_writer.close()


if __name__ == "__main__":
    code_generator = CompilationEngine("Square/Main.jack", "Square/Main.vm") # enter file/directory path.
    code_generator.compile_class()
    code_generator.close()
