from Jack_Tokenizer import JackTokenizer

class CompilationEngine:

    def __init__(self, input_file_path, xml_file_path):
        self.input_file = open(input_file_path, 'r')
        self.xml_file = open(xml_file_path, 'w')
        self.tokenizer = JackTokenizer(input_file_path)
        # wherever there is a '*' sign it means one or more. wherever there is a '?' sign it means zero or one.

    def compile_class(self):
        #CLASS STRUCTURE: 'class' className '{' classVarDec(*zero or more) subroutineDec(*zero or more) '}'
        self.xml_file.write('<class>' + '\n')
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.keyword()) # 'class'
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.identifier()) # class name
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) # left curley bracket '{'
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            if self.tokenizer.current_token in {'field', 'static'}:
                self.compile_class_var_dec()
            elif self.tokenizer.current_token in {'constructor','function', 'method'}:
                self.compile_subroutine()
        self.xml_file.write(self.tokenizer.symbol()) # right curley bracket '}'
        self.xml_file.write('</class>' + '\n')

    def compile_class_var_dec(self):
        #CLASS VAR DEC SYNTAX: ('static' | 'field') type varName (',' varName)*zero or more ';'
        self.xml_file.write('<classVarDec>' + '\n')
        # if self.tokenizer.token_type() == 'keyword':
        self.xml_file.write(self.tokenizer.keyword())
        # else: self.xml_file.write(self.tokenizer.identifier())
        self.tokenizer.advance()
        if self.tokenizer.token_type() == 'keyword':
            self.xml_file.write(self.tokenizer.keyword())  # type
        else:
            self.xml_file.write(self.tokenizer.identifier())  # type, could be a user defined type, isn't necessarily a built-in type.
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.identifier()) # varName
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol())  # in the case where there is only one varName, this would be ';'. otherwise it's a comma ','.
        if self.tokenizer.current_token == ',':  # optional second variable separated by a comma ','.
            while self.tokenizer.current_token != ';':
                self.tokenizer.advance()
                self.xml_file.write(self.tokenizer.identifier())  # varName
                self.tokenizer.advance()
                self.xml_file.write(self.tokenizer.symbol())  # ';'
        self.xml_file.write('</classVarDec>' + '\n')


    def compile_subroutine(self):
        # SUBROUTINE DEC STRUCTURE: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        # subroutine dec
        self.xml_file.write('<subroutineDec>' + '\n')
        self.xml_file.write(self.tokenizer.keyword()) # 'constructor' | 'function' | 'method'
        self.tokenizer.advance()
##        if self.tokenizer.token_type() == 'keyword':
##            self.xml_file.write(self.tokenizer.keyword()) # a built-in type
##        elif self.tokenizer.token_type() == 'identifier':
##            self.xml_file.write(self.tokenizer.identifier()) # a non-built-in type
        self.xml_file.write(self.tokenizer.current_token) # type. keyword or identifier.
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.identifier()) # subroutineName
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) # opening parenthesis '('
        self.compile_parameter_list() # parameterList #I don't advance here so I can look ahead in compile_parameter()
        self.xml_file.write(self.tokenizer.symbol()) # closing parenthesis ')'

        # SUBROUTINE BODY STRUCTURE: '{' varDec (*zero or more) statements '}'
        # subroutine body
        self.xml_file.write('<subroutineBody>' + '\n')
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) # opening curley bracket '{'
        self.tokenizer.advance()
        if self.tokenizer.current_token != 'var':
            self.xml_file.write('<statements>' + '\n')
        while self.tokenizer.current_token != 'return':
            if self.tokenizer.current_token == 'var':  # zero or more var decs.
                self.compile_var_dec()
                self.tokenizer.advance()
                if self.tokenizer.current_token != 'var':
                    self.xml_file.write('<statements>' + '\n')
            elif self.tokenizer.current_token in {'if', 'while', 'let', 'do'}:  # zero or more statements
                self.compile_statements()
        self.compile_return()
        self.xml_file.write('</statements>' + '\n')
        self.xml_file.write(self.tokenizer.symbol())  # right curly bracket
        self.xml_file.write('</subroutineBody>' + '\n')
        self.xml_file.write('</subroutineDec>' + '\n')

    def compile_parameter_list(self):
        #PARAMETER LIST SYNTAX: type varName (',' type varName)*zero or more
        self.xml_file.write('<parameterList>' + '\n')
        self.tokenizer.advance()
        if self.tokenizer.current_token != ')':
            # (food for thought: it's possible for a type to be user-defined, in which case it would be an identifier)
            self.xml_file.write(self.tokenizer.keyword()) # Type.
            self.tokenizer.advance()
            self.xml_file.write(self.tokenizer.identifier()) # varName
            self.tokenizer.advance()
            while self.tokenizer.current_token != ')':
                self.xml_file.write(self.tokenizer.symbol()) # comma '
                self.tokenizer.advance()
                self.xml_file.write(self.tokenizer.keyword()) # type. and I should think about the possibility of it being AN 'identifier'
                self.tokenizer.advance()
                self.xml_file.write(self.tokenizer.identifier()) # varName
                self.tokenizer.advance()
        self.xml_file.write('</parameterList>' + '\n')

    def compile_var_dec(self):
        #VAR DEC SYNTAX: 'var' type varName (',' varName)*zero or more. ';'
        self.xml_file.write('<varDec>' + '\n')
        self.xml_file.write(self.tokenizer.keyword()) # 'var'
        self.tokenizer.advance()
        if self.tokenizer.current_token in {'int', 'boolean', 'char', 'string'}:
            self.xml_file.write(self.tokenizer.keyword()) #type.
        else:
            self.xml_file.write(self.tokenizer.identifier()) #user defined type.
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.identifier()) #varName.
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol())  # if there's only one var, this is ';'. otherwise it's a comma ','.
        if self.tokenizer.current_token == ',':  # optional additional variables separated by a comma ','
            while self.tokenizer.current_token != ';':
                self.tokenizer.advance()
                self.xml_file.write(self.tokenizer.identifier())  # varName.
                self.tokenizer.advance()
                self.xml_file.write(
                    self.tokenizer.symbol())  # if there are numerous vars then this is a comma ','. otherwise it's ';'.
        self.xml_file.write('</varDec>' + '\n')

    ### UP UNTIL COMPILE_STATEMENTS() EVERYTHING WORKED FINE.

    def compile_statements(self):
        if self.tokenizer.current_token == 'if':
            self.compile_if()
        elif self.tokenizer.current_token == 'while':
            self.compile_while()
        elif self.tokenizer.current_token == 'let':
            self.compile_let()
        elif self.tokenizer.current_token == 'do':
            self.compile_do()

    def compile_if(self):
        #IF SYNTAX: 'if' '(' expression ')' '{' statements '}'
        self.xml_file.write('<ifStatement>' + '\n')
        self.xml_file.write(self.tokenizer.keyword()) # 'if'
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) # opening parenthesis
        self.tokenizer.advance()
        self.compile_expression()
        self.xml_file.write(self.tokenizer.symbol()) # closing parenthesis
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) # left curley bracket '{'
        self.xml_file.write('<statements>' + '\n')
        self.tokenizer.advance()
        while self.tokenizer.current_token != '}':
            self.compile_statements()
        self.xml_file.write('</statements>' + '\n')
        self.xml_file.write(self.tokenizer.symbol())  # For the if statement '}'
        self.tokenizer.advance() # since there isn't always an 'else' statement, I'll need to advance after every statement.

        # ELSE SYNTAX: ('else' '{' statements '}')? zero or one.
        if self.tokenizer.current_token == 'else':
            self.xml_file.write(self.tokenizer.keyword()) # 'else'
            self.tokenizer.advance()
            self.xml_file.write(self.tokenizer.symbol()) # left curley bracket '{'
            self.tokenizer.advance()
            self.xml_file.write('<statements>' + '\n')
            while self.tokenizer.current_token != '}':
                self.compile_statements()
            self.xml_file.write('</statements>' + '\n')
            self.xml_file.write(self.tokenizer.symbol()) # right curley bracket '}'
            self.tokenizer.advance() #I'm advancing here (and in all the other statements) so that I can peacefully advance to check for 'else' statements.
        self.xml_file.write('</ifStatement>' + '\n')

    def compile_while(self):
        #WHILE SYNTAX: 'while' '(' expression ')' '{' statements '}'
        self.xml_file.write('<whileStatement>' + '\n')
        self.xml_file.write(self.tokenizer.keyword()) # 'while'
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) # opening parenthesis '('
        self.tokenizer.advance()
        self.compile_expression() # expression
        self.xml_file.write(self.tokenizer.symbol()) # closing parenthesis ')'
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) # left curley bracket '{'
        self.tokenizer.advance()
        self.xml_file.write('<statements>' + '\n')
        while self.tokenizer.current_token != '}':
            self.compile_statements()
        self.xml_file.write('</statements>' + '\n')
        self.xml_file.write(self.tokenizer.symbol()) # right curley bracket '}'
        self.tokenizer.advance() #I'm advancing here (and in all the other statements) so that I can peacefully advance to check for 'else' statements.
        self.xml_file.write('</whileStatement>' + '\n')

    def compile_let(self):
        #LET SYNTAX: 'let' varname ('[' expression ']')? '=' expression ';' # '?' meaning zero or one.
        self.xml_file.write('<letStatement>' + '\n')
        self.xml_file.write(self.tokenizer.keyword()) # 'let'
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.identifier()) # varName
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) # if it's assigning a value to an index in an array then this is a '[', otherwise it's a '='.
        self.tokenizer.advance()
        self.compile_expression() # expression
        self.xml_file.write(self.tokenizer.symbol()) # if it's assigning a value to an index in an array then this is a ']', otherwise it's a ';'.
        self.tokenizer.advance()
        if self.tokenizer.current_token == '=':
            self.xml_file.write(self.tokenizer.symbol()) # I only get here when it's assigning a value to an array index. so this is a '=' sign.
            self.tokenizer.advance()
            self.compile_expression() # expression
            self.xml_file.write(self.tokenizer.symbol()) # semi-colon ';'
            self.tokenizer.advance()
        self.xml_file.write('</letStatement>' + '\n')

    def compile_do(self):
        # DO SYNTAX: 'do' subroutineCall ';'.
        # subroutine syntax = subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
        self.xml_file.write('<doStatement>' + '\n')
        self.xml_file.write(self.tokenizer.keyword()) # 'do'
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.identifier()) # subroutineName | (className | varName)
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) # for an expression list this is a '(', for subroutine call this is a '.'
        if self.tokenizer.current_token == '.':
            self.tokenizer.advance()
            self.xml_file.write(self.tokenizer.identifier()) # subroutineName (*method)
            self.tokenizer.advance()
            self.xml_file.write(self.tokenizer.symbol()) # opening parenthesis '('
        # self.tokenizer.advance()
        self.compile_expression_list()
        self.xml_file.write(self.tokenizer.symbol()) # closing parenthesis ')'
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) # semi-colon ';'
        self.tokenizer.advance() #I'm advancing here (and in all the other statements) so that I can peacefully advance to check for 'else' statements.
        self.xml_file.write('</doStatement>' + '\n')

    def compile_return(self):
        # RETURN SYNTAX: 'return' expression? zero or one times. ';'
        self.xml_file.write('<returnStatement>' + '\n')
        self.xml_file.write(self.tokenizer.keyword()) # 'return'
        self.tokenizer.advance()
        if self.tokenizer.current_token != ';':
            self.compile_expression()
        self.xml_file.write(self.tokenizer.symbol()) # semi-colon ';'
        self.tokenizer.advance() #I'm advancing here (and in all the other statements) so that I can peacefully advance to check for 'else' statements.
        self.xml_file.write('</returnStatement>' + '\n')

    def compile_expression(self):
        #EXPRESSION SYNTAX: term (operator, term)* ("*" means zero or more)
        self.xml_file.write('<expression>' + '\n')
        self.compile_term() # term
        if self.tokenizer.current_token in {'+', '-', '*', '=', '|', '>', '<', '/', '&'}:
            self.xml_file.write(self.tokenizer.symbol()) # operator
            self.tokenizer.advance()
            self.compile_term()
        self.xml_file.write('</expression>' + '\n')

    def compile_expression_list(self):
        #EXPRESSION LIST SYNTAX: (expression (',' expression)*)? there can be an empty expression list, or a list with one or more expressions.
        self.xml_file.write('<expressionList>' + '\n')
        self.tokenizer.advance()
        while self.tokenizer.current_token != ')':
            self.compile_expression()
            if self.tokenizer.current_token != ',' and self.tokenizer.current_token != ')':
                self.tokenizer.advance()
            if self.tokenizer.current_token == ',':
                self.xml_file.write(self.tokenizer.symbol())
                self.tokenizer.advance()
        self.xml_file.write('</expressionList>' + '\n')

    def compile_term(self):
        #TERM SYNTAX: intConst | strConst | keywordConst | (varname | varname '[' expression ']' | subroutineCall | '(' expression ')') | unaryOp term.
        self.xml_file.write('<term>' + '\n')
        if self.tokenizer.token_type() == 'int_const':
            self.xml_file.write(self.tokenizer.int_val())
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'string_const':
            self.xml_file.write(self.tokenizer.string_val())
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'keyword':
            self.xml_file.write(self.tokenizer.keyword())
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'identifier':
            self.xml_file.write(self.tokenizer.identifier())
            self.tokenizer.advance()
            if self.tokenizer.current_token == '.': # subroutine call
                self.xml_file.write(self.tokenizer.symbol()) # '.'
                self.tokenizer.advance()
                self.xml_file.write(self.tokenizer.identifier()) # method
                self.tokenizer.advance()
                self.xml_file.write(self.tokenizer.symbol()) # left parenthesis
                self.compile_expression_list()
                self.xml_file.write(self.tokenizer.symbol())  # right parenthesis.
                self.tokenizer.advance()
            elif self.tokenizer.current_token == '[':
                self.xml_file.write(self.tokenizer.symbol())  # '['
                self.tokenizer.advance()
                self.compile_expression()
                self.xml_file.write(self.tokenizer.symbol()) # ']'
                self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'symbol':# and not self.tokenizer.current_token in {'-', '~'}:
            if self.tokenizer.current_token == '(':
                self.xml_file.write(self.tokenizer.symbol()) # '('
                self.tokenizer.advance()
                self.compile_expression()
                self.xml_file.write(self.tokenizer.symbol()) # ')'
                self.tokenizer.advance()
            elif self.tokenizer.current_token in {'-', '~'}:
                self.xml_file.write(self.tokenizer.symbol())  # '-' or '~'
                self.tokenizer.advance()
                self.compile_term()
        self.xml_file.write('</term>' + '\n')

    def close(self):
        self.tokenizer.close()
        self.input_file.close()
        self.xml_file.close()

if __name__ == "__main__":
    parser = CompilationEngine('ExpressionLessSquare/SquareGame.jack', 'MyXmlFiles/SquareGameEx.xml')#change input and output files
    import time
    start_time = time.time()
    parser.compile_class()
    end_time = time.time()
    parser.close()
    print("Runtime: ", round(end_time - start_time, 4), " seconds")
