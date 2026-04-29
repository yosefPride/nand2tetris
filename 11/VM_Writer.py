class VMWriter:

    def __init__(self, output):
        self.output_file = open(output, 'w')
        self.arithmetic_commands = {'+': 'add', '-': 'sub', '=': 'eq', '|': 'or', '>': 'gt', '<': 'lt', '&': 'and', 'neg':'neg', '~': 'not'}

    def write_push(self, segment, index):
        self.output_file.write('push ' + segment + ' ' + str(index) + '\n')

    def write_pop(self, segment, index):
        self.output_file.write('pop ' + segment + ' ' + str(index) + '\n')

    def write_arithmetic(self, command):
        self.output_file.write(self.arithmetic_commands.get(command) + '\n')

    def write_label(self, label):
        self.output_file.write('label ' + label + '\n')

    def write_goto(self, label):
        self.output_file.write('goto' + ' ' + label +  '\n')

    def write_if(self, label):
        self.output_file.write('if-goto' + ' ' + label + '\n')

    def write_call(self, name, n_args):
        self.output_file.write('call ' + name + ' ' + str(n_args) + '\n')

    def write_function(self, name, n_locals):
        self.output_file.write('function ' + name + ' ' + str(n_locals) + '\n')

    def write_return(self):
        self.output_file.write('return' + '\n')

    def close(self):
        self.output_file.close()

# if __name__ == '__main__':
#     vm_writer = VMWriter('test_file.txt')
#     vm_writer.write_push('local', 1)
#     vm_writer.write_pop('this', 2)
#     vm_writer.write_label('NEGATIVE')
#     vm_writer.write_if('NEGATIVE')
#     vm_writer.write_call('math.mult', 2)
#     vm_writer.write_function('func', 2)
#     vm_writer.write_arithmetic('+')
#     vm_writer.write_goto('NEGATIVE')
#     vm_writer.write_return()
#     vm_writer.close()