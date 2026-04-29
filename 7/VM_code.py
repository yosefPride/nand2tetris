class Code:

    def __init__(self, asm_file_path):#opens output file and gets ready to write into it
        self.asm_file = open(asm_file_path, 'w')
        self.label_counter = 0
        
    def set_file_name(self, file_name):#keeps track of current vm file being translated  
        self.current_file_name = file_name.split('.vm')[0]
        print(f'setting file name {self.current_file_name}')

    def get_unique_label(self, base_name):
        label = f"{base_name}_{self.label_counter}"  # Create a label by appending current counter value to base name
        self.label_counter += 1 # Increment the counter to ensure the next label is unique
        return label # Return the generated unique label in the format 'base_name_counter'

    def write_arithmetic(self, command):#writs assembly translation for arithmetic commands
        command = command.lower()
        true_label = self.get_unique_label("TRUE")
        end_label = self.get_unique_label("END")
        arithmetic_code = {
            'add': '''@SP     //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value).
                    M=D+M     //SP now holds the computed value (the sum of both operands).
                    @SP       //Access SP to increment it back to the next empty slot.
                    M=M+1''',  
            
            'sub': '''@SP     //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value)
                    M=M-D     //SP now holds the value after substraction.
                    @SP       //Access SP to increment it back to the next empty slot. 
                    M=M+1''',
            
            'neg': '''@SP      // Access the stack pointer.
                    A=M-1    // Access the topmost value at SP - 1.
                    M=-M     // Negate the value in place.''',

            'and':'''@SP      //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value).
                    M=D&M     //SP now holds the computed value (a boolean).
                    @SP       //Access SP to increment it back to the next empty slot.
                    M=M+1''',
            
            'or' : '''@SP    //Access the stack pointer.
                    AM=M-1   //Decrement SP to point to the first operand (top value).      
                    D=M      //D now holds the first operand.
                    @SP      //Access SP again.
                    AM=M-1   //Decrement SP to point to the second operand (next value).     
                    M=D|M    //SP now holds the computed value (a boolean). 
                    @SP      //Access SP to increment it back to the next empty slot.
                    M=M+1''',
            
            'not': '''@SP    // Access the stack pointer. 
                    A=M-1    // Decrement SP to point to the top value of the stack.
                    M=!M     // Apply NOT(!) directly to the top value and store it back. 
                    ''',

            'eq': f'''@SP    // Accesss the stack pointer.
                    AM=M-1   // Decrement the stack pointer to point to the first oparand (top value).
                    D=M      // D now holds the first oparand
                    @SP      // Access SP again
                    AM=M-1   // Decremnet SP to point to the second oparand
                    D=D-M    // First oparand - second oparand
                    @{true_label} // Define label
                    D;JEQ    // If D = 0 goto true

                    //false case
                    @SP      // Access SP to store the result.
                    A=M      // A points to the next empty slot.
                    M=0      // Store the result (0) on the stack.
                    @{end_label} // Define label.
                    0;JMP    // Goto end.

                    ({true_label})
                    @SP      // Access SP to store the result.
                    A=M      // A points to the next empty slot.
                    M=-1     // store the result (-1) on the stack.

                    ({end_label})
                    @SP      // Access SP.
                    M=M+1    // Increment SP back to the next empty slot
                    ''',

            'gt': f'''@SP    // Access SP 
                    AM=M-1   // Decrement SP to point to the first oparand
                    D=M      // D now holds the first oparand
                    @SP      // Access SP again
                    AM=M-1   // Decrement Sp to point to the second oparand
                    D=M-D    // First oparand - second oparand 
                    @{true_label} // Define label
                    D;JGT    // if D > 0 goto true

                    //false case
                    @SP      // Access SP 
                    A=M      // A points to the next empty slot.
                    M=0      // store the result (0) on the stack
                    @{end_label} // Define label
                    0;JMP    // Goto end

                    ({true_label})
                    @SP      // Access SP
                    A=M      // A points to the next empty slot.
                    M=-1     // Store the result (-1) on the stack

                    ({end_label})
                    @SP      // Access SP 
                    M=M+1    // Increment SP to point to the next empty slot
                    ''',

            'lt': f'''@SP      //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value)
                    D=M-D     //first operand - second oparand
                    @{true_label}//define label
                    D;JLT     //if second operand < first operand goto LT_TRUE

                    //false case
                    @SP       //access SP to store the result
                    A=M
                    M=0       //Store the result (0) on the stack
                    @{end_label}//goto end
                    0;JMP
                    
                ({true_label})
                    @SP       //access SP to store result (-1)
                    A=M
                    M=-1       // Store the result (-1) on the stack
                    @{end_label}      //goto end
                    0;JMP

                ({end_label})
                    @SP       //Access SP and increment it back to the next empty slot. 
                    M=M+1''',
            }
        if command in arithmetic_code:  # Write the corresponding assembly code directly to the file
            self.asm_file.write(arithmetic_code[command] + '\n')

    def write_push_pop(self, command, segment, index): #writes assembly tanslation for push and pop commands
        segment_map = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT'  
            }

        this_label = self.get_unique_label("this_label")
        end_label = self.get_unique_label("end_label")
            
        if command == 'push' and segment == 'constant':
            code = f'''
            @{index} //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            '''
        elif command == 'push' and segment in segment_map:
            base_address = segment_map[segment]
            code = f'''
            @{base_address}      // Load the base address of current segment 
            D=M       // D = base address
            @{index}  // Load index
            D=D+A     // A = base address + index
            A=D       // set A to computed address
            D=M       // D = *(base address + index)
            @SP
            A=M       // A = SP, top of the stack
            M=D       // *SP = value at computed address
            @SP
            M=M+1     // SP++, increment the stack pointer
            '''
        elif command == 'push' and segment == 'temp': 
            code = f'''
            @5       // Load the base address of temp
            D=A      // D = 5
            @{index} // Load index
            D=D+A    // A = base address + index
            A=D      // set A to computed address
            D=M      // D = *(base address + index)
            @SP
            A=M      // A = SP, top of the stack
            M=D      // *SP = value at computed address
            @SP
            M=M+1    // SP++, increment the stack pointer
            '''
        elif command == 'push' and segment == 'pointer':
            base_address = "THIS" if index == "0" else "THAT"
            code = f'''
            @{base_address}// Access "THIS" or "THAT"
            D=M       // D now holds the value at "THIS" or "THAT" respectively
            @SP       // Access SP to store 
            A=M       // A = SP (top of the stack)
            M=D       // *SP = D (value stored at THIS or THAT respectively)
            @SP       // Access SP to increment it
            M=M+1
            '''
        elif command == 'push' and segment == 'static':
            code = f'''
            @{self.current_file_name}.{index} // Load the static variable using the file name and the index
            D=M      // D = the value at that address
            @SP
            A=M      // A = SP, top of the stack
            M=D      // *SP = value at computed address
            @SP
            M=M+1    // SP++, increment the stack pointer
            '''
        elif command == 'pop' and segment in segment_map:
            base_address_pop = segment_map[segment]
            segment_var = self.get_unique_label('segment_var')
            code = f'''
            @{base_address_pop}       // Load the segment's base address 
            D=M      // D = base address
            @{index} // Load index
            D=D+A    // A = base address + index

            @{segment_var}
            M=D      // segment_var now holds the computed address(where the top value of the stack will be poped to)
            
            @SP      // Access the stack pointer.
            AM=M-1   // Decrement SP to point to the (top value).
            D=M      // D now holds the top value of the stack.

            @{segment_var}
            A=M      // Access the address stored in segment_var
            M=D      // the top value of the stack is now stored at the computed address(base_address + index)
            '''
        elif command == 'pop' and segment == 'temp':
            temp_var = self.get_unique_label("temp_var")
            code = f'''
            @5       // Load the base address of temp
            D=A      // D = 5
            @{index} // Load index
            D=D+A    // A = base address + index

            @{temp_var}
            M=D      // temp_var now holds the computed address(where the top value of the stack will be poped to)
            
            @SP      // Access the stack pointer.
            AM=M-1   // Decrement SP to point to the (top value).
            D=M      // D now holds the top value of the stack.

            @{temp_var}
            A=M      // Access the address stored in temp_var
            M=D      // the top value of the stack is now stored at the computed address(base_address + index)
            '''
        elif command == 'pop' and segment == 'pointer':
            base_address = "THIS" if index == "0" else "THAT"
            code = f'''
            @SP      // Access the stack pointer
            AM=M-1   // Decrement SP to point to the (top value)
            D=M      // D now holds the top value of the stack
            @{base_address} // Access {"THIS" if index == "0" else "THAT"}
            M=D      // Store the value from the stack in {"THIS" if index == "0" else "THAT"}
            '''
            
        elif command == 'pop' and segment == 'static':
            code = f''' 
            @SP
            AM=M-1   // A = SP, top of the stack
            D=M
            @{self.current_file_name}.{index} // Load the static variable using the file name and the index
            M=D      //
            '''
        self.asm_file.write(code + '\n')

    def close(self):#closes output file
        self.asm_file.close()
