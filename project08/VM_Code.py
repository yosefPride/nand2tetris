class Code:

    def __init__(self, asm_file_path):#opens output file and gets ready to write into it
        self.asm_file = open(asm_file_path, 'w')
        self.label_counter = 0
        
    def set_file_name(self, file_name):#keeps track of current vm file being translated  
        self.current_file_name = file_name.split('.vm')[0]

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
            // Pop pointer
            @SP      // Access the stack pointer
            AM=M-1   // Decrement SP to point to the (top value)
            D=M      // D now holds the top value of the stack
            @{base_address} // Access {"THIS" if index == "0" else "THAT"}
            M=D      // Store the value from the stack in {"THIS" if index == "0" else "THAT"}
            '''
        elif command == 'pop' and segment == 'static':
            code = f'''
            //Pop static
            @SP
            AM=M-1   // A = SP, top of the stack
            D=M
            @{self.current_file_name}.{index} // Load the static variable using the file name and the index
            M=D      //
            '''
        self.asm_file.write(code + '\n')

    def write_init(self):#writes assembly bootstrap code
        code = f'''
        // Sys.init, bootstrap code
        @256     //address for the top of the stack
        D=A      //D == 256
        @SP      //access SP 
        M=D      //SP = 256
        
        //@Sys.init// Jump to Sys.init program
        //0;JMP
        '''
        self.asm_file.write(code)
        self.write_call('Sys.init', 0)

    def write_label(self, label):#writes assembly translation for the VM command "label"
        if label[0].isdigit():
            label = label[1:]
        code = label.strip()
        self.asm_file.write(f'({code})' + '\n')#returns the given label in parenthesis

    def write_goto(self, label):#writes assembly translation for Goto commands
        if label[0].isdigit():
            label = label[1:]
        label = label.strip()
        self.asm_file.write(f'//goto command\n@{label}\n0;JMP\n')

    def write_if(self, label):#writes assembly translation for if-goto commands
        if label[0].isdigit():
            label = label[1:]
        label = label.strip()
        code = f'''
        // If-goto command
        @SP       // Access SP
        AM=M-1    // Decrement SP to point to the top of the stack
        D=M       // D now holds the value at the top of the stack
        @{label}  
        D;JNE     // If the value at the top of the stack is not equal to zero goto label
        '''
        self.asm_file.write(code + '\n')

    def write_call(self, function_name, num_args):#writes assembly translation for call command
        return_address = self.get_unique_label('return_address')
        code = f'''
        // Call command
        // Push the return address 
        @{return_address}//
        D=A      // D now holds the return address
        @SP      // Access SP to store the return address.
        A=M      // A points to the next empty slot. 
        M=D      // Store the return address.
        @SP      // Access SP to increment it back to the next empty slot.
        M=M+1

        // Save LCL
        @LCL     // Access LCL
        D=M      // D now holds the value at LCL
        @SP      // Access SP
        A=M      // A points to the next empty slot
        M=D      // Store the value in D on the stack
        @SP      // Access Sp
        M=M+1    // Increment it back to the next empty slot

        // Save ARG
        @ARG     // Access ARG
        D=M      // D now holds the value at ARG
        @SP      // Access SP
        A=M      // A points to the next empty slot
        M=D      // Store the value in D on the stack
        @SP      // Access Sp
        M=M+1    // Increment it back to the next empty slot

        // Save THIS
        @THIS    // Access THIS
        D=M      // D now holds the value at THIS
        @SP      // Access SP
        A=M      // A points to the next empty slot
        M=D      // Store the value in D on the stack
        @SP      // Access Sp
        M=M+1    // Increment it back to the next empty slot

        // Save THAT
        @THAT    //Access THAT
        D=M      // D now holds the value at THAT
        @SP      // Access SP
        A=M      // A points to the next empty slot
        M=D      // Store the value in D on the stack
        @SP      // Access Sp
        M=M+1    // Increment it back to the next empty slot

        // Reposition ARG ((ARG=SP-n-5),n = number of args)
        @SP      // Access SP
        D=M      // D = SP
        @5       // Load 5
        D=D-A    // D - 5
        @{num_args}// Access num_args (n)
        D=D-A    // SP - 5 - n
        @ARG     // Access ARG
        //A=M
        M=D      // ARG = SP - 5 - n

        // Reposition LCL (LCL = SP)
        @SP      // Access SP
        D=M      // D = SP 
        @LCL     // Access LCL
        //A=M
        M=D      // Set LCL to SP

        // Transfer control to the called function (goto f)
        @{function_name}
        0;JMP
        
        ({return_address})
        '''
        self.asm_file.write(code + '\n')
        
    def write_return(self):#writes assembly translation for return command
        code = f'''
        // Return command ****THERE IS AN ERROR IN THE CODE CHECK IT OUT**** 
        // Save the current LCL frame
        @LCL     // Access LCL
        D=M      
        @R13     // Access temporary register
        M=D      // store LCL in R13

        //Put the return address (LCL frame - 5) in a temporary variable
        @R13     // Access R13
        D=M      // D now holds the address at R13
        @5
        A=D-A    // R13 - 5
        D=M
        @R14     // Access R14
        M=D      // Store the address in R14

        //reposition the  return value for the caller
        @SP      // Access SP
        AM=M-1   // Decrement SP to point to the top value(the return value of the function)
        D=M      // D now holds the return value 
        @ARG     // Access ARG
        A=M      // Goto ARG segment
        M=D      // Store the return value in ARG

        //restore SP of the caller
        @ARG     // Access ARG
        D=M+1    // Set D to arg +1
        @SP      // Access SP
        M=D      // Set SP to ARG+1 
        
        //restore the "THAT" segment
        @R13     // Access R13
        AM=M-1   // Decrement R13 to point to R13-1
        D=M      // D now holds the value at R13-1
        @THAT    // Access the "THAT" segment
        M=D      // Set "THAT" to R13-1
        
        //restore the "THIS" segment
        @R13     // Access R13
        AM=M-1   // Decrement R13 to point to R13-2
        D=M      // D now holds the value at R13-2
        @THIS    // Access the "THIS" segment
        M=D      // Set "THIS" to R13-2

        //restore the "ARG" segment
        @R13     // Access R13
        AM=M-1   // Decrement R13 to point to R13-3
        D=M      // D now holds the value at R13-3
        @ARG    // Access the "ARG" segment
        M=D      // Set "ARG" to R13-3

        //restore the "LCL" segment
        @R13     // Access R13
        AM=M-1   // Decrement R13 to point to R13-4
        D=M      // D now holds the value at R13-4
        @LCL     // Access the "LCL" segment
        M=D      // Set "LCL" to R13-4

        //jump to the return address
        @R14
        A=M
        0;JMP
        '''
        self.asm_file.write(code + '\n')

    def write_function(self, function_name, num_locals):#writes assembly translation for function command
        func_loop = self.get_unique_label('func_loop')
        end = self.get_unique_label('end')
        code = f'''
        ({function_name})

        @{num_locals}
        D=A
        @{end}
        D;JLE    // If num_locals == 0 goto end

        ({func_loop})
        @SP      // Access SP to store the result.
        A=M      // A points to the next empty slot. 
        M=0      // Store the result.
        @SP      // Access SP.
        M=M+1    // Increment SP back to the next empty slot
        D=D-1    // Decrement num_locals
        @{func_loop}
        D;JGT    // if D(num_locals) > 0 goto loop

        ({end})
        '''
        self.asm_file.write(code + '\n')
        
    def close(self):#closes output file
        self.asm_file.close()
