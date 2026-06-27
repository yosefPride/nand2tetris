class SymbolTable:

#FUN FACT: in more advanced languages (e.g. java) you can have nested scoping of variables (indentations, or curly brackets '{').
#the way to deal with it is to make a linked list of symbol tables, and look up the variable in the first scope,
#if I can't find the variable, I go to the next, and so on... until I get to class level scope.
#if I can't find it there either, I can safely conclude that the variable is undefined, and throw an error message.

    def __init__(self):
        self.fields = {}
        self.statics = {}
        self.args = {}
        self.vars = {}
        # self.class_scope = {}
        # self.subroutine_scope = {}

    def start_subroutine(self) -> None: # resets the symbol table.
        self.vars.clear()
        self.args.clear()
        # self.subroutine_scope.clear()

    def define(self, identifier_name: str, identifier_type: str, identifier_kind: str) -> None:
        if identifier_kind == 'field':
            self.fields[identifier_name] = (identifier_type, 'this')
            # self.class_scope[identifier_name] = (identifier_type, 'this')
        elif identifier_kind == 'static':
            self.statics[identifier_name] = (identifier_type, 'static')
            # self.class_scope[identifier_name] = (identifier_type, 'static')
        elif identifier_kind == 'var':
            self.vars[identifier_name] = (identifier_type, 'local')
            # self.subroutine_scope[identifier_name] = (identifier_type, 'local')
        elif identifier_kind == 'arg':
            self.args[identifier_name] = (identifier_type, 'argument')
            # self.subroutine_scope[identifier_name] = (identifier_type, 'argument')

    def var_count(self, identifier_kind: str) -> int:
        if identifier_kind == 'var':
            return len(self.vars)
        elif identifier_kind == 'arg':
            return len(self.args)
        elif identifier_kind == 'field':  # they might have to be in all caps. 'FIELD'.
            return len(self.fields)
        elif identifier_kind == 'static':
            return len(self.statics)
        raise ValueError('must be an identifier kind.')

    def kind_of(self, identifier_name: str):
        if identifier_name in self.vars:
            return self.vars[identifier_name][1]
        elif identifier_name in self.args:
            return self.args[identifier_name][1]
        elif identifier_name in self.fields:
            return self.fields[identifier_name][1]
        elif identifier_name in self.statics:
            return self.statics[identifier_name][1]
        return None

    def type_of(self, identifier_name: str) -> str:
        if identifier_name in self.vars:
            return self.vars[identifier_name][0]
        elif identifier_name in self.args:
            return self.args[identifier_name][0]
        elif identifier_name in self.fields:
            return self.fields[identifier_name][0]
        elif identifier_name in self.statics:
            return self.statics[identifier_name][0]
        raise ValueError('must be an identifier type.')

    def index_of(self, identifier_name: str) -> int:
        if identifier_name in self.vars:
            key_list = list(self.vars.keys())  # gets all the keys in the dict.
            return key_list.index(identifier_name) # gets the index of the given key from the list of keys.
        elif identifier_name in self.args:
            key_list = list(self.args.keys())
            return key_list.index(identifier_name)
        elif identifier_name in self.fields:
            key_list = list(self.fields.keys())
            return key_list.index(identifier_name)
        elif identifier_name in self.statics:
            key_list = list(self.statics.keys())
            return key_list.index(identifier_name)
        raise ValueError('must be an identifier name.')

    # def usage(self):
    #     print("implement")