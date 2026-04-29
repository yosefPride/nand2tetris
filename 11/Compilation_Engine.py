from Jack_Tokenizer import JackTokenizer
from Symbol_Table import SymbolTable
from VM_Writer import VMWriter

class CompilationEngine:

    def __init__(self, input_file_path, output_file):
        self.input_file = open(input_file_path, 'r')
        self.tokenizer = JackTokenizer(input_file_path)
        self.vm_writer = VMWriter(output_file)
        self.iden_type = self.iden_kind = None
        self.symbol_table = SymbolTable()
        self.label_counter = 0
        self.num_locals = 0 #this is supposed to help keep track of how many local variables a given subroutine has.
        self.special_ops = {'*':'Math.multiply', '/':'Math.divide'}
        self.op = None
        self.class_name = None
        # string constants are created using String.new(length). string assignments are handled by a series of calls to String.appendChar(nextChar).
        # when I compute a value (an expression) I need to put the given value at the top of the vm stack.
        # I need to be working with a stack. so what is the last (and therefor first to access) node of the stack at any given moment?

    def get_unique_label(self, base_name):
        label = f"{base_name}_{self.label_counter}"  # Create a label by appending current counter value to base name
        self.label_counter += 1  # Increment the counter to ensure the next label is unique
        return label  # Return the generated unique label in the format 'base_name_counter'

    def compile_class(self):
        # CLASS STRUCTURE: 'class' className '{' classVarDec(*zero or more) subroutineDec(*zero or more) '}'
        self.tokenizer.advance()  # 'class'
        self.tokenizer.advance()  # class name
        self.class_name = self.tokenizer.current_token  # I need this because every method's symbol table starts with "this, class_name, arg, 0"
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
        # a subroutine xxx() in a class yyy is compiled into a VM function yyy.xxx().
        # a function or a constructor with K arguments is compiled into a VM function with K arguments
        # a subroutine with K arguments is compiled into a VM function with K+1 arguments. the first argument is always 'this' (the current object)
        # when calling a subroutine you must specify how many arguments there'll be.
        # before calling a VM function the caller must push the function's arguments to the stack. if it's a method, the first argument (arg 0) must be 'this'.
        # when compiling a method the compiler must set its base address.
        # similarly for a constructor the compiler must allocate memory for the new object (using memory.alloc(size)). and then set the base of 'this' to point at its base.
        # since all methods must return a value, void methods return 'constant 0'
        # the caller of a void method/function must pop (and ignore) the returned value (constant 0).

        # static variables are allocated to and accessed via the static segment of the vm file
        # a field variable is accessed by first pointing to the 'this' segment (using pointer 0) and then using individual indexes.
        # an array is accessed by first pointing to the 'that ' segment (using pointer 1) and then using 'that 0'.

        self.symbol_table.start_subroutine() # creates new subroutine symbol table.
        if self.tokenizer.current_token == 'function':
            self.tokenizer.advance() # type
            self.tokenizer.advance() # name
            name = self.tokenizer.identifier() # name
            self.tokenizer.advance()  # opening parenthesis
            self.compile_parameter_list()
            self.tokenizer.advance()  # closing parenthesis

            #SUBROUTINE BODY
            self.tokenizer.advance() # opening curley bracket
            while self.tokenizer.current_token == 'var':
                self.compile_var_dec()
                self.tokenizer.advance()
            self.vm_writer.write_function(self.class_name + '.' + name, self.num_locals)
            self.num_locals = 0
            while self.tokenizer.current_token in {'if', 'while', 'let', 'do', 'return'}:
                self.compile_statements()

        elif self.tokenizer.current_token == 'constructor':


            #here I need to save the name of the class being constructed to use whenever one fo its methods is being called.


            # "constructor" type constructorName '(' parameterList ')' constructor body
            # self.vm_writer.output_file.write('\n' + 'starting constructor ' + '\n') #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
            # self.vm_writer.output_file.write('\n' + 'finishing constructor ' + '\n') #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        elif self.tokenizer.current_token == 'method':
            self.tokenizer.advance()  # type
            self.tokenizer.advance()  # name
            name = self.tokenizer.identifier() # name
            # self.vm_writer.output_file.write('\n' + 'starting method ' + subroutineName + '\n') #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.tokenizer.advance()  # opening parenthesis
            self.symbol_table.define('this', self.class_name, 'arg') #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!POSSIBLY WRONG!!!!!!!!
            self.compile_parameter_list()
            self.tokenizer.advance()  # closing parenthesis

            # SUBROUTINE BODY
            self.tokenizer.advance()  # opening curley bracket
            while self.tokenizer.current_token == 'var':
                self.compile_var_dec()
                self.tokenizer.advance()
            self.vm_writer.write_function(self.class_name + '.' + name, self.num_locals)
            self.num_locals = 0
            self.vm_writer.write_push('argument', 0)
            self.vm_writer.write_pop('pointer', 0)
            while self.tokenizer.current_token in {'if', 'while', 'let', 'do', 'return'}:
                self.compile_statements()
            # self.vm_writer.output_file.write('finished method ' + subroutineName + '\n') #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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
    #
    def compile_if(self):
        # IF SYNTAX: 'if' '(' expression ')' '{' statements '}'
        # VM syntax for 'if': compile expression, 'not', if-goto label, label, statements
        # 'if'
        # self.vm_writer.output_file.write('\n' + 'starting compile_if()' + '\n')#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.tokenizer.advance()
        # opening parenthesis
        self.tokenizer.advance()
        self.compile_expression()
        self.vm_writer.write_arithmetic('~') # not
        label1 = self.get_unique_label('L') # I may need to use this label in other places, so I should consider making it a class scope variable.
        self.vm_writer.write_if(label1) #I need to create a unique label to jump to, right here...
        # and since I negated "if's" condition, right after the if goto statement I must write code that just continues down the stream, right?
        # self.vm_writer.output_file.write(self.tokenizer.current_token + ' 1' +'\n') #TEST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

        # closing parenthesis
        self.tokenizer.advance()
        # self.vm_writer.output_file.write(self.tokenizer.current_token + '\n') #TEST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        # self.compile_term()
        # left curley bracket '{'
        while self.tokenizer.token_type() == 'symbol':
            self.tokenizer.advance()
            # self.vm_writer.output_file.write(self.tokenizer.current_token + '\n')  # TEST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

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
            # left curley bracket '{'
            self.tokenizer.advance()
            while self.tokenizer.current_token != '}':
                self.compile_statements()
            self.vm_writer.write_label(label2)
            # right curley bracket '}'
            self.tokenizer.advance()  # I'm advancing here (and in all the other statements) so that I can peacefully advance to check for 'else' statements.
        # self.vm_writer.output_file.write('finished compile_if()' + '\n')#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def compile_while(self):
        # WHILE SYNTAX: 'while' '(' expression ')' '{' statements '}'
        # self.vm_writer.output_file.write('\n' + 'starting compile_while()' + '\n')#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
        # while self.tokenizer.token_type() != 'keyword':
        self.tokenizer.advance()
        # self.vm_writer.output_file.write('finished compile_while()' + '\n')#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def compile_let(self):
        # LET SYNTAX: 'let' varname ('[' expression ']')? '=' expression ';' # '?' meaning zero or one.
        # 'let'
        # when I encounter a variable, I look it up in the subroutine level symbol table, if it isn't there, I look it up in the class level symbol table,
        # and if I can't find it there either, then I know that it's undefined.
        # EXAMPLE FOR LET STATEMENT: let y = y + dy; VM CODE: push this 1, push local 1, add, pop this 1.
        # self.vm_writer.output_file.write('\n' + 'starting compile_let()' + '\n')#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.tokenizer.advance()
        pop_value = self.tokenizer.identifier()  # variable to which I will pop
        self.tokenizer.advance()  # if it's assigning a value to an index in an array then this is a '[', otherwise it's a '='.
        self.tokenizer.advance()
        self.compile_expression()  # expression
        # if it's assigning a value to an index in an array then this is a ']', otherwise it's a ';'.
        self.tokenizer.advance() #even if there isn't a continuation here I need to advance, because I need to advance in compile_if().
        if self.tokenizer.current_token == '=': # I only get here when it's assigning a value to an array index. so this is a '=' sign.
            self.tokenizer.advance()
            self.compile_expression()  # expression
            self.tokenizer.advance() # I advance here and in all other statements, because I need to advance in compile_if().
        self.vm_writer.write_pop(self.symbol_table.kind_of(pop_value), self.symbol_table.index_of(pop_value)) # popping the final result into the let statement's variable.
        # self.vm_writer.output_file.write('finished compile_let()' + '\n')#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def compile_do(self):
        # DO SYNTAX: 'do' subroutineCall ';'.
        # subroutine syntax = subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
        # self.vm_writer.output_file.write('\n' + 'starting compile_do()' + '\n')#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.tokenizer.advance()
        self.compile_expression()
        self.tokenizer.advance() #';'
        self.vm_writer.write_pop('temp', 0) # gets rid of the return value.
        # self.vm_writer.output_file.write('finished compile_do()' + '\n')#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def compile_return(self):
        # RETURN SYNTAX: 'return' expression? zero or one times. ';'
        # self.vm_writer.output_file.write('\n' + 'starting compile_return()' + '\n')#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.tokenizer.advance()
        if self.tokenizer.current_token == ';':
            self.vm_writer.write_push('constant', 0)
        else: self.compile_expression()
        self.vm_writer.write_return()
        self.tokenizer.advance()  # I'm advancing here (and in all the other statements) so that I can peacefully advance to check for 'else' statements.
        # self.vm_writer.output_file.write('finished compile_return()' + '\n')#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def compile_expression(self):
        # EXPRESSION SYNTAX: term (operator, term)* ("*" means zero or more)
        self.compile_term()
        if self.tokenizer.current_token in {'+', '-', '=', '|', '>', '<', '&'}: # I'm not so sure about '=' being 'eq' over here. I think it just means assignment.
            op = self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compile_term()
            self.vm_writer.write_arithmetic(op) #does this ensure that the operation happens in the right place?
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
                self.tokenizer.advance() #this should be to advance past the commas ','. check that this is right.
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
                self.vm_writer.write_push('constant', ord(letter)) #ord() takes a char and returns its ASCII code. chr() does the opposite.
                self.vm_writer.write_call('String.appendChar', 2) #two, because I need to keep arg 0/this 0 in mind.!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'keyword': #true, false, null, and this.
            if self.tokenizer.current_token in ('false', 'null'):
                self.vm_writer.write_push('constant', 0)
            elif self.tokenizer.current_token == 'true':
                self.vm_writer.write_push('constant', 1)
                self.vm_writer.write_arithmetic('neg')
            else: self.vm_writer.write_push('this', 0)
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'identifier':
            iden_name = self.tokenizer.identifier()
            self.tokenizer.advance()
            if self.tokenizer.current_token == '.':  # subroutine call
                self.tokenizer.advance() # subroutine name
                subroutine_name = self.tokenizer.identifier()
                self.tokenizer.advance() # opening parenthesis
                self.compile_expression_list()
                self.vm_writer.write_call(iden_name + '.' + subroutine_name, self.num_args) #HOW DO I GET N_ARGS FROM COMPILE_EXPRESSION_LIST?
                self.tokenizer.advance()
            elif self.tokenizer.current_token == '[': #push arr, push index, add, pop pointer 1 (that 0)
                self.vm_writer.write_push(self.symbol_table.kind_of(iden_name), self.symbol_table.index_of(iden_name))
                self.tokenizer.advance()
                self.compile_expression()
                self.tokenizer.advance() # ']'
                self.vm_writer.write_arithmetic('+') #add the index to the base address of the array.
                self.vm_writer.write_pop('pointer', 1) # I pop the index into "that 0".
            elif self.tokenizer.current_token == '(':
                self.compile_expression_list()
                self.vm_writer.write_call(iden_name, self.num_args)
                self.tokenizer.advance()
            else: self.vm_writer.write_push(self.symbol_table.kind_of(iden_name), self.symbol_table.index_of(iden_name))
        elif self.tokenizer.token_type() == 'symbol':  # and not self.tokenizer.current_token in {'-', '~'}:
            if self.tokenizer.current_token == '(':
                self.tokenizer.advance()
                self.compile_expression()
                self.tokenizer.advance()
            elif self.tokenizer.current_token in {'-', '~'}:
                if self.tokenizer.current_token == '-': #I can't have '-' as two different operators in the commands dictionary. (sub & neg)
                    self.op = 'neg' #maybe define this in the constructor.
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