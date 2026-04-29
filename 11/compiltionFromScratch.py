from Jack_Tokenizer import JackTokenizer
from Symbol_Table import SymbolTable
from VM_Writer import VMWriter

class CompilationEngine:

    def __init__(self, input_file_path, output_file):
        self.input_file = open(input_file_path, 'r')
        self.tokenizer = JackTokenizer(input_file_path)
        self.vm_writer = VMWriter(output_file)
        self.label_counter = 0
        self.iden_type = self.iden_kind = None
        self.symbol_table = SymbolTable()
        self.class_name = None
        self.num_locals = 0  # this is supposed to help keep track of how many local variables a given subroutine has. (haven't quite gotten it to work)*
        self.special_ops = {'*': 'Math.multiply', '/': 'Math.divide'}

    def get_unique_label(self, base_name):
        label = f"{base_name}_{self.label_counter}"  # Create a label by appending current counter value to base name
        self.label_counter += 1  # Increment the counter to ensure the next label is unique
        return label  # Return the generated unique label in the format 'base_name_counter'

    def compile_class(self):
        # CLASS STRUCTURE: 'class' className '{' classVarDec(*zero or more) subroutineDec(*zero or more) '}'
        self.tokenizer.advance()  # 'class'
        self.tokenizer.advance()
        self.class_name = self.tokenizer.current_token  # I need this because every method's symbol table starts with "this, class_name, arg, 0"
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            if self.tokenizer.current_token in {'field', 'static'}:
                self.compile_class_var_dec()
            elif self.tokenizer.current_token in {'constructor', 'function', 'method'}:
                self.compile_subroutine()

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


    def compile_parameter_list(self):


    def compile_var_dec(self):
        # VAR DEC SYNTAX: 'var' type varName (',' varName)*zero or more. ';'
        self.tokenizer.advance()  # var
        self.iden_type = self.tokenizer.current_token
        while self.tokenizer.current_token != ';':
            self.tokenizer.advance()
            self.symbol_table.define(self.tokenizer.current_token, self.iden_type, 'var')
            self.tokenizer.advance()

    def compile_statements(self):


    def compile_if(self):


    def compile_let(self):


    def compile_do(self):


    def compile_while(self):


    def compile_return(self):


    def compile_expression(self):
        # EXPRESSION SYNTAX: term (operator, term)* ("*" means zero or more)
        self.compile_term()
        if self.tokenizer.current_token in {'+', '-', '=', '|', '>', '<', '&'}:  # I'm not so sure about '=' being 'eq' over here. I think it just means assignment.
            op = self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compile_term()
            self.vm_writer.write_arithmetic(op)  # does this ensure that the operation happens in the right place?
        elif self.tokenizer.current_token in {'*', '/'}:
            op = self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compile_term()
            self.vm_writer.write_call(self.special_ops.get(op), 2)

    def compile_expression_list(self):


    def compile_term(self):
        # TERM SYNTAX: intConst | strConst | keywordConst | (varname | varname '[' expression ']') | subroutineCall | '(' expression ')') | unaryOp term.
        if self.tokenizer.token_type() == 'int_const':
            self.vm_writer.write_push('constant', self.tokenizer.int_val())  # 'push' 'constant' val
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'string_const':
            self.vm_writer.write_call('String.new', 1)
            string = self.tokenizer.current_token.list()
            for letter in string:
                self.vm_writer.write_push('constant',
                                          ord(letter))  # ord() takes a char and returns its ASCII code. chr() does the opposite.
                self.vm_writer.write_call('String.appendChar', 2)  # two, because I need to keep arg 0/this 0 in mind.
                self.tokenizer.advance()
        #     elif self.tokenizer.token_type() == 'keyword': #true, false, null, and this.

        elif self.tokenizer.token_type() == 'identifier':
            iden_name = self.tokenizer.identifier()
            self.vm_writer.output_file.write(self.tokenizer.current_token + '\n')
            self.tokenizer.advance()
            if self.tokenizer.current_token == '.':  # subroutine call
                self.tokenizer.advance()  # subroutine name
                subroutine_name = self.tokenizer.identifier()
                self.vm_writer.output_file.write(self.tokenizer.current_token + '\n')
                self.tokenizer.advance()  # opening parenthesis
                self.compile_expression_list()
                if self.tokenizer.current_token != ')':  # VERY INTRESTING! WHY WOULD I HAVE TO ADVANCE IF THIS WASN'T ')'?
                    self.tokenizer.advance()  # closing parenthesis
                self.vm_writer.output_file.write('got here!' + '\n')
                self.vm_writer.write_call(iden_name + '.' + subroutine_name,
                                          self.num_args)  # HOW DO I GET N_ARGS FROM COMPILE_EXPRESSION_LIST?
            elif self.tokenizer.current_token == '[':  # push arr, push index, add, pop pointer 1 (that 0)
                self.vm_writer.write_push(self.symbol_table.kind_of(iden_name), self.symbol_table.index_of(iden_name))
                self.tokenizer.advance()
                self.compile_expression()
                self.tokenizer.advance()  # ']'
                self.vm_writer.write_arithmetic('+')  # add the index to the base address of the array.
                self.vm_writer.write_pop('pointer', 1)  # I pop the index into "that 0".
            else:
                self.vm_writer.write_push(self.symbol_table.kind_of(iden_name), self.symbol_table.index_of(iden_name))
        elif self.tokenizer.token_type() == 'symbol':  # and not self.tokenizer.current_token in {'-', '~'}:
            if self.tokenizer.current_token == '(':
                # '('
                self.tokenizer.advance()
                self.compile_expression()
                # ')'
                self.tokenizer.advance()
            elif self.tokenizer.current_token in {'-', '~'}:
                # I must first write the value and then write the command.
                if self.tokenizer.current_token == '-':  # I can't have '-' as two different operators in the commands dictionary. (sub & neg)
                    self.op = 'neg'  # maybe define this in the constructor.
                else:
                    self.op = self.tokenizer.current_token
                self.tokenizer.advance()
                integer = self.tokenizer.current_token
                self.vm_writer.write_push('constant', integer)
                # I should note that at some point this will have to work for '~' as well. and then this could be a boolean as well as an integer

                self.vm_writer.write_arithmetic(
                    self.op)  # there may be a problem here. cause where I assign 'op' isn't in the same scope.
                # self.tokenizer.advance() #maybe if I don't have to advance for identifiers then I won't advance here either.
                # currently I'm not advancing here because for subroutine calls I need to stay within my limits of handling identifiers in compile_term().

    def close(self):
        self.tokenizer.close()
        # self.input_file.close()
        self.vm_writer.close()

    if __name__ == "__main__":
        code_generator = CompilationEngine("ConvertToBin/Main.jack", "ConvertToBin/Main.vm")  # enter file/directory path.
        code_generator.compile_class()
        code_generator.close()