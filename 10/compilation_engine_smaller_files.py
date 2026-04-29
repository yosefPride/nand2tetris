#from xml.etree.ElementTree import indent
from Jack_Tokenizer import JackTokenizer

class CompilationEngine:

    def __init__(self, input_file_path, xml_file_path):
        self.input_file = open(input_file_path, 'r')
        self.xml_file = open(xml_file_path, 'w')
        self.tokenizer = JackTokenizer(input_file_path)
        self.doCase = self.expression = False
        # maybe I should make an indenter() function, that has increase() and decrease() methods.

    def compile_class(self):
        #CLASS STRUCTURE: 'class' className '{' classVarDec(*zero or more) subroutineDec(*zero or more) '}'
        self.xml_file.write('<class>' + '\n')
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.keyword()) #class
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.identifier()) #class name
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) # left curly bracket '{'
        while self.tokenizer.has_more_tokens(): #there can only be a loop here
            self.tokenizer.advance()
            if self.tokenizer.current_token in {'field', 'static'}: #zero or more class variable declarations.
                self.compile_class_var_dec()
            if self.tokenizer.current_token in {'method', 'constructor', 'function'}: #zero or more subroutines.
                self.compile_subroutine()
        self.xml_file.write(self.tokenizer.symbol()) # right curly bracket '}'
        self.xml_file.write('</class>')

    def compile_class_var_dec(self):
        #CLASS VAR DEC SYNTAX: ('static' | 'field') type varName (',' varName)*zero or more ';'
        self.xml_file.write('<classVarDec>' + '\n')
        if self.tokenizer.token_type() == 'keyword':
            self.xml_file.write(self.tokenizer.keyword()) #'static' | 'field'
        else: self.xml_file.write(self.tokenizer.identifier())
        self.tokenizer.advance()
        if self.tokenizer.token_type() == 'keyword':
            self.xml_file.write(self.tokenizer.keyword()) #type
        else: self.xml_file.write(self.tokenizer.identifier()) #type, could be a user defined type, isn't necessarily a built-in type.
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.identifier()) #varName
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) #in the case where there is only one varName, this would be ';'. otherwise it's a comma ','.
        if self.tokenizer.current_token == ',': #optional second variable separated by a comma ','.
            while self.tokenizer.current_token != ';':
                self.tokenizer.advance()
                self.xml_file.write(self.tokenizer.identifier()) #varName
                self.tokenizer.advance()
                self.xml_file.write(self.tokenizer.symbol()) # ';'
        self.xml_file.write('</classVarDec>' + '\n')

    def compile_subroutine(self):
        #SUBROUTINE DEC STRUCTURE: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        #subroutine dec
        self.xml_file.write('<subroutineDec>' + '\n')
        self.xml_file.write(self.tokenizer.keyword()) #'constructor' | 'function' | 'method'
        if self.tokenizer.current_token == 'constructor':
            self.tokenizer.advance()
            self.xml_file.write(self.tokenizer.identifier()) #type
        else:
            self.tokenizer.advance()
            self.xml_file.write(self.tokenizer.keyword()) #'void' | type
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.identifier()) #subroutine name
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) # left parenthesis '('
        self.compile_parameter_list() #parameter list (compile_parameterList() also deals with the closing parenthesis.)

        #SUBROUTINE BODY STRUCTURE: '{' varDec (*zero or more) statements '}'
        #subroutine body
        self.xml_file.write('<subroutineBody>' + '\n')
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) #left curly bracket '{'
        self.tokenizer.advance()
        if self.tokenizer.current_token != 'var':
            self.xml_file.write('<statements>' + '\n')
        while self.tokenizer.current_token != 'return':
            if self.tokenizer.current_token == 'var': #zero or more var decs.
                self.compile_var_dec()
                self.tokenizer.advance()
                if self.tokenizer.current_token != 'var':
                    self.xml_file.write('<statements>' + '\n')
            elif self.tokenizer.current_token in {'if', 'while', 'let', 'do'}: #zero or more statements
                self.compile_statements()
                # self.tokenizer.advance()
        self.compile_return()
        # self.tokenizer.advance()
        self.xml_file.write('</statements>' + '\n')
        self.xml_file.write(self.tokenizer.symbol())  # right curly bracket
        self.xml_file.write('</subroutineBody>' + '\n')
        self.xml_file.write('</subroutineDec>' + '\n')

    def compile_parameter_list(self):
        #PARAMETER LIST SYNTAX: type varName (',' type varName)*zero or more
        self.xml_file.write('<parameterList>' + '\n')
        self.tokenizer.advance()
        if self.tokenizer.current_token != ')': #if it is ")", then the parameter list is empty. and we just print the tags.
            self.xml_file.write(self.tokenizer.keyword()) #type.
            self.tokenizer.advance()
            self.xml_file.write(self.tokenizer.identifier()) #varName.
            self.tokenizer.advance()
            self.xml_file.write(self.tokenizer.symbol()) #if there is only one parameter, symbol here is ';'. otherwise symbol is ','.
            if self.tokenizer.current_token == ',':
                while self.tokenizer.current_token != ')':
                    self.tokenizer.advance()
                    self.xml_file.write(self.tokenizer.keyword()) #type.
                    self.tokenizer.advance()
                    self.xml_file.write(self.tokenizer.identifier()) #varName.
                    self.tokenizer.advance()
                    if self.tokenizer.current_token == ',':
                        self.xml_file.write(self.tokenizer.symbol())
        self.xml_file.write('</parameterList>' + '\n')
        self.xml_file.write(self.tokenizer.symbol())

    def compile_var_dec(self):
        #VAR DEC SYNTAX: 'var' type varName (',' varName)*zero or more. ';'
        self.xml_file.write('<varDec>' + '\n')
        self.xml_file.write(self.tokenizer.keyword()) #'var'.
        self.tokenizer.advance()
        if self.tokenizer.current_token in {'int', 'boolean', 'char', 'string'}:
            self.xml_file.write(self.tokenizer.keyword()) #type.
        else:
            self.xml_file.write(self.tokenizer.identifier()) #user defined type.
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.identifier()) #varName.
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) #if there's only one var, this is ';'. otherwise it's a comma ','.
        if self.tokenizer.current_token == ',': #optional additional variables separated by a comma ','
            while self.tokenizer.current_token  != ';':
                self.tokenizer.advance()
                self.xml_file.write(self.tokenizer.identifier()) #varName.
                self.tokenizer.advance()
                self.xml_file.write(self.tokenizer.symbol()) #if there are numerous vars then this is a comma ','. otherwise it's ';'.
        self.xml_file.write('</varDec>' + '\n')

    def compile_statements(self): #I need to set self.last_time to true for the times when I want the end root element.
        if self.tokenizer.current_token == 'if':
            self.compile_if()
        elif self.tokenizer.current_token == 'while':
            self.compile_while()
        elif self.tokenizer.current_token == 'let':
            self.compile_let()
        elif self.tokenizer.current_token == 'do':
            self.compile_do()
        # elif self.tokenizer.current_token == 'return':
        #     self.compile_return()

    def compile_do(self):
        #DO SYNTAX: 'do' subroutineCall ';'.
        #subroutine syntax = subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
        self.xml_file.write('<doStatement>' + '\n')
        self.xml_file.write(self.tokenizer.keyword()) #do
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.identifier()) #subroutineName | (className | varName)
        self.tokenizer.advance()
        if self.tokenizer.current_token == '.':
            self.xml_file.write(self.tokenizer.symbol()) # '.'
            self.tokenizer.advance()
            self.xml_file.write(self.tokenizer.identifier())  # method
            self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol())  # left parenthesis
        #self.tokenizer.advance()
        self.doCase = True
        self.compile_expression_list() #expression list
        self.doCase = False
        if self.tokenizer.current_token != ')':
            self.tokenizer.advance() #maybe I shouldn't always blindly advance. I need to check if I've advanced one more than I know. (in compile_term)
        self.xml_file.write(self.tokenizer.symbol())  # right parenthesis ')'.
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) # ';'
        self.tokenizer.advance()  # I'm advancing here (and in all the other statements) so that I can peacefully advance to check for 'else' statements.
        self.xml_file.write('</doStatement>' + '\n')

    def compile_let(self):
        #LET SYNTAX: 'let' varname ('[' expression ']')? '=' expression ';'
        self.xml_file.write('<letStatement>' + '\n')
        self.xml_file.write(self.tokenizer.keyword()) #let
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.identifier()) #varName
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) #in case where it's assigning a value to an array index, this would be the right square bracket '['. otherwise it's '='.
        self.tokenizer.advance()
        self.compile_expression() #expression
        if self.tokenizer.current_token != ';' and self.tokenizer.current_token != ']': #because I looked ahead in 'compile_term' to check for array entries or subroutine calls.
            self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) #if it's an array index then symbol is ']' (right square bracket. closing bracket). otherwise it's the colon ';'.
        if self.tokenizer.current_token == ']': #check if we have an array on our hand
            self.tokenizer.advance()
            self.xml_file.write(self.tokenizer.symbol()) # '='
            self.tokenizer.advance()
            self.compile_expression()
            if self.tokenizer.current_token != ';': #because I had to look ahead in 'compile_term' to check for array entries or subroutine calls.
                self.tokenizer.advance()
            self.xml_file.write(self.tokenizer.symbol()) # ';'
        self.tokenizer.advance()  # I'm advancing here (and in all the other statements) so that I can peacefully advance to check for 'else' statements.
        self.xml_file.write('</letStatement>' + '\n')

    def compile_while(self):
        #WHILE SYNTAX: 'while' '(' expression ')' '{' statements '}'
        self.xml_file.write('<whileStatement>' + '\n')
        self.xml_file.write(self.tokenizer.keyword()) #'while'.
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) #left parenthesis '('.
        self.tokenizer.advance()
        self.compile_expression() #expression
        if self.tokenizer.current_token != ')':  #I might've advanced in compile_expression, if there were more than one term.
            self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) #right parenthesis ')'
        self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) #openning curly bracket '{'
        self.tokenizer.advance()
        self.xml_file.write('<statements>' + '\n')
        while self.tokenizer.current_token != '{' and self.tokenizer.current_token != '}': #one or more statements.
            self.compile_statements()
            # self.tokenizer.advance()
        self.xml_file.write('</statements>' + '\n')
        self.xml_file.write(self.tokenizer.symbol()) #closing curly bracket '}'
        self.tokenizer.advance()  # I'm advancing here (and in all the other statements) so that I can peacefully advance to check for 'else' statements.
        self.xml_file.write('</whileStatement>' + '\n')

    def compile_return(self):
        #RETURN SYNTAX: 'return' expression? zero or one times. ';'
        self.xml_file.write('<returnStatement>' + '\n')
        self.xml_file.write(self.tokenizer.keyword()) #return.
        self.tokenizer.advance()
        if self.tokenizer.current_token != ';': #if the current token is not ';', then there must be an expression.
            self.compile_expression()
            #if self.tokenizer.current_token !=:
                #self.tokenizer.advance()
        self.xml_file.write(self.tokenizer.symbol()) # ';'
        self.tokenizer.advance() #I'm advancing here (and in all the other statements) so that I can peacefully advance to check for 'else' statements.
        self.xml_file.write('</returnStatement>' + '\n')

    def compile_if(self):
        #IF SYNTAX: 'if' '(' expression ')' '{' statements '}'
        if self.tokenizer.current_token == 'if':
            self.xml_file.write('<ifStatement>' + '\n')
            self.xml_file.write(self.tokenizer.keyword()) #'if'
            self.tokenizer.advance()
            self.xml_file.write(self.tokenizer.symbol()) #'('
            self.tokenizer.advance()
            self.compile_expression() #expression
            if self.tokenizer.current_token != ')':
                self.tokenizer.advance() # I don't think I should advance here. because I've advanced in compile_term to 'look ahead'
            self.xml_file.write(self.tokenizer.symbol())# right parenthesis ')'
            self.tokenizer.advance()
            self.xml_file.write(self.tokenizer.symbol()) #left curly bracket '{'
            self.xml_file.write('<statements>' + '\n')
            self.tokenizer.advance()
            while self.tokenizer.current_token != '}': #and self.tokenizer.current_token != '{': # one or more statements.
                self.compile_statements()
                # self.tokenizer.advance()
            self.xml_file.write('</statements>' + '\n')
            self.xml_file.write(self.tokenizer.symbol())  # For the if statement '}'

            self.tokenizer.advance() #There isn't always an 'else' statement following the if statement. and therefore advancing here is causing problems.
            #ELSE SYNTAX: ('else' '{' statements '}')? zero or one.
            if self.tokenizer.current_token == 'else':
                self.xml_file.write(self.tokenizer.keyword()) #'else'
                self.tokenizer.advance()
                self.xml_file.write(self.tokenizer.symbol()) #'{'
                self.tokenizer.advance()
                self.xml_file.write('<statements>' + '\n')
                while self.tokenizer.current_token != '}':  #And self.tokenizer.current_token != '{': # one or more statements.
                    self.compile_statements()
                    # self.tokenizer.advance()
                self.xml_file.write('</statements>' + '\n')
                self.xml_file.write(self.tokenizer.symbol()) #'}'
                self.tokenizer.advance() #I'm advancing here (and in all the other statements) so that I can peacefully advance to check for 'else' statements.
            self.xml_file.write("</ifStatement>" + '\n')

    def compile_expression(self):
        #EXPRESSION SYNTAX: term (operator, term)* ("*" means zero or more)
        self.xml_file.write('<expression>' + '\n')
        self.compile_term()  # term
        if self.tokenizer.current_token in {'+', '-', '*', '=', '|', '>', '<', '/', '&'}:
            self.xml_file.write(self.tokenizer.symbol()) #operator
            self.tokenizer.advance()
            if self.tokenizer.current_token == '(':
                self.expression = True
            self.compile_term() #term
        self.xml_file.write('</expression>' + '\n')

    # def compile_identifier_term(self): #I made this a separate method since compile_term() is so long
    #     self.xml_file.write(self.tokenizer.identifier())
    #     self.tokenizer.advance()  # just looking ahead. so if it's just a var name, I can't advance after the term, when calling compile_expression (in other methods).
    #     if self.tokenizer.current_token == '.':  # subroutine call
    #         self.xml_file.write(self.tokenizer.symbol())  # '.'
    #         self.tokenizer.advance()
    #         self.xml_file.write(self.tokenizer.identifier())  # method
    #         self.tokenizer.advance()
    #         self.xml_file.write(self.tokenizer.symbol())  # left parenthesis
    #         self.compile_expression_list()
    #         if not self.doCase:  # in the case of a do statement I don't want to write the symbols inside the parenthesis.
    #             if self.tokenizer.current_token != ')':  # because I advanced in compile_expression_list.
    #                 self.tokenizer.advance()
    #             self.xml_file.write(self.tokenizer.symbol())  # right parenthesis.
    #     elif self.tokenizer.current_token == '[':
    #         self.xml_file.write(self.tokenizer.symbol())  # '['
    #         self.compile_expression()
    #         # self.tokenizer.advance()
    #         self.xml_file.write(self.tokenizer.symbol())  # ']'
    #         self.tokenizer.advance()
    #
    # def compile_symbol_term(self): #I made this a separate method since compile_term() is so long
    #     if self.tokenizer.current_token in {'~', '-'}:  # unary op.
    #         self.xml_file.write(self.tokenizer.symbol())  # '-' or '~'
    #         self.compile_term()
    #     if not self.expression:
    #         self.tokenizer.advance()
    #     if self.tokenizer.current_token == '(':  # '( expression ')'.
    #         self.expression = False
    #         self.xml_file.write(self.tokenizer.symbol())  # '('
    #         self.compile_expression()
    #         if self.tokenizer.current_token == ')':
    #             self.xml_file.write(self.tokenizer.symbol())
    #             # self.tokenizer.advance()
    #     #else:
    #
    #
    # def compile_term(self):
    #     #TERM SYNTAX: intConst | strConst | keywordConst | varname | varname '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term.
    #     self.xml_file.write('<term>' + '\n')
    #     if self.tokenizer.token_type() == 'symbol':
    #         self.compile_symbol_term()
    #     elif self.tokenizer.token_type() == 'int_const': #int const
    #         self.xml_file.write(self.tokenizer.int_val())
    #         self.tokenizer.advance()
    #     elif self.tokenizer.token_type() == 'string_const': #string const
    #         self.xml_file.write(self.tokenizer.string_val())
    #         self.tokenizer.advance()
    #     elif self.tokenizer.token_type() == 'keyword': #keyword const
    #         self.xml_file.write(self.tokenizer.keyword())
    #         self.tokenizer.advance()
    #     elif self.tokenizer.token_type() == 'identifier': #this is where I need to check if the identifier is a var name, a subroutine call or an array index
    #         self.compile_identifier_term()
    #     self.xml_file.write('</term>' + '\n')

    def compile_term(self):
        #TERM SYNTAX: intConst | strConst | keywordConst | varname | varname '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term.
        self.xml_file.write('<term>' + '\n')
        if self.tokenizer.token_type() == 'symbol' and not self.tokenizer.current_token in {'-', '~'}: #because I advanced in expression list, to check if it's an empty expression list.
            if not self.expression:
                self.tokenizer.advance()
            if self.tokenizer.current_token == '(':  # '( expression ')'.
                self.expression = False
                self.xml_file.write(self.tokenizer.symbol())  # '('
                self.compile_expression()
                if self.tokenizer.current_token == ')':
                    self.xml_file.write(self.tokenizer.symbol())
                    self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'int_const': #int const
            self.xml_file.write(self.tokenizer.int_val())
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'string_const': #string const
            self.xml_file.write(self.tokenizer.string_val())
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'keyword': #keyword const
            self.xml_file.write(self.tokenizer.keyword())
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == 'identifier': #this is where I need to check if the identifier is a var name, a subroutine call or an array index
            self.xml_file.write(self.tokenizer.identifier())
            self.tokenizer.advance() #just looking ahead. so if it's just a var name, I can't advance after the term, when calling compile_expression (in other methods).
            if self.tokenizer.current_token == '.': #subroutine call
                self.xml_file.write(self.tokenizer.symbol()) # '.'
                self.tokenizer.advance()
                self.xml_file.write(self.tokenizer.identifier()) # method
                self.tokenizer.advance()
                self.xml_file.write(self.tokenizer.symbol()) # left parenthesis
                self.compile_expression_list()
                if not self.doCase: #in the case of a do statement I don't want to write the symbols inside the parenthesis.
                    if self.tokenizer.current_token != ')': #because I advanced in compile_expression_list.
                        self.tokenizer.advance()
                    self.xml_file.write(self.tokenizer.symbol()) # right parenthesis.
                    self.tokenizer.advance()
            elif self.tokenizer.current_token == '[':
                self.xml_file.write(self.tokenizer.symbol()) # '['
                self.compile_expression()
                # self.tokenizer.advance()
                self.xml_file.write(self.tokenizer.symbol()) # ']'
                self.tokenizer.advance()
        elif self.tokenizer.current_token in {'~', '-'}: #unary op  #CAUSES MAJOR PROBLEM (for '-'), NEED A CLEVER SOLUTION.
            self.xml_file.write(self.tokenizer.symbol()) # '-' or '~'
            self.compile_term()
        self.xml_file.write('</term>' + '\n')

    def compile_expression_list(self):
        self.xml_file.write('<expressionList>' + '\n')
        self.tokenizer.advance()
        if self.tokenizer.current_token == '(':
            self.expression = True   #I must advance here, to learn if the expression list is empty, but if it isn't empty, this will then stop me from advancing in compile_term()
        while self.tokenizer.current_token != ')': #if it's not an empty expression list. I need to find a way to loop over an expression list separated by commas.
            self.compile_expression()
            if self.tokenizer.current_token != ',' and self.tokenizer.current_token != ')':
                self.tokenizer.advance()
            if self.tokenizer.current_token == ',':
                self.xml_file.write(self.tokenizer.symbol())
                self.tokenizer.advance()
        self.xml_file.write('</expressionList>' + '\n')

    def close(self):
        self.tokenizer.close()
        self.input_file.close()
        self.xml_file.close()

if __name__ == "__main__":
    parser = CompilationEngine('Square/Square.jack', 'MyXmlFiles/SquareS.xml')#change input and output files
    #works for the following files:     ExpressionLessSquare/Main.jack,     Square/Main.jack,   ArrayTest/Main.jack,
    #Square/SquareGame.jack,   ExpressionLessSquare/SquareGame.jack,    ExpressionLessSquare/Square.jack

    #if I don't advance in compile if() at the end (before 'else' case), and I don't advance in compile_return() after compile_expression(), then this one works for:
    #Square/SquareGame.jack,   ExpressionLessSquare/SquareGame.jack,    ExpressionLessSquare/Square.jack

    #if I don't have an elif statement for '~' and '-' in compile_term(), and i don't advance in compile_if() at the end (before 'else' case),
    #then this one works for:   Square/Square.jack

    #the issue with advancing in compile_return() stems from the fact that there could be a keyword in a return statement (e.g. 'this'). and in compile_term() for keywords
    #I don't advance after  writing to the xml file.

    #THE SOLUTION: advance for keywords as well.

    #the issue with advancing in compile_if() stems from the fact that an 'if' statement isn't always followed by an 'else' statement.

    #THE SOLUTION: advance at the end of every statement (if, let, do, etc.), and don't advance in the compile_statements() loop

    #the issue with an 'elif' statement for '~' and '-' in compile_term() stems from the fact that I'm not differentiating between a negative number and an arithmatic
    #expression (e.g. '-1' vs 'x - 1').

    import time
    start_time = time.time()
    parser.compile_class()
    end_time = time.time()
    parser.close()
    print("Runtime: ", round(end_time - start_time, 4), " seconds")