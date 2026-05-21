
            @ARG      // Load the base address of current segment 
            D=M       // D = base address
            @1  // Load index
            D=D+A     // A = base address + index
            A=D       // set A to computed address
            D=M       // D = *(base address + index)
            @SP
            A=M       // A = SP, top of the stack
            M=D       // *SP = value at computed address
            @SP
            M=M+1     // SP++, increment the stack pointer
            

            @SP      // Access the stack pointer
            AM=M-1   // Decrement SP to point to the (top value)
            D=M      // D now holds the top value of the stack
            @THAT // Access THAT
            M=D      // Store the value from the stack in THAT
            

            @0 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @THAT       // Load the segment's base address 
            D=M      // D = base address
            @0 // Load index
            D=D+A    // A = base address + index

            @segment_var_0
            M=D      // segment_var now holds the computed address(where the top value of the stack will be poped to)
            
            @SP      // Access the stack pointer.
            AM=M-1   // Decrement SP to point to the (top value).
            D=M      // D now holds the top value of the stack.

            @segment_var_0
            A=M      // Access the address stored in segment_var
            M=D      // the top value of the stack is now stored at the computed address(base_address + index)
            

            @1 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @THAT       // Load the segment's base address 
            D=M      // D = base address
            @1 // Load index
            D=D+A    // A = base address + index

            @segment_var_1
            M=D      // segment_var now holds the computed address(where the top value of the stack will be poped to)
            
            @SP      // Access the stack pointer.
            AM=M-1   // Decrement SP to point to the (top value).
            D=M      // D now holds the top value of the stack.

            @segment_var_1
            A=M      // Access the address stored in segment_var
            M=D      // the top value of the stack is now stored at the computed address(base_address + index)
            

            @ARG      // Load the base address of current segment 
            D=M       // D = base address
            @0  // Load index
            D=D+A     // A = base address + index
            A=D       // set A to computed address
            D=M       // D = *(base address + index)
            @SP
            A=M       // A = SP, top of the stack
            M=D       // *SP = value at computed address
            @SP
            M=M+1     // SP++, increment the stack pointer
            

            @2 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            
@SP     //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value)
                    M=M-D     //SP now holds the value after substraction.
                    @SP       //Access SP to increment it back to the next empty slot. 
                    M=M+1

            @ARG       // Load the segment's base address 
            D=M      // D = base address
            @0 // Load index
            D=D+A    // A = base address + index

            @segment_var_4
            M=D      // segment_var now holds the computed address(where the top value of the stack will be poped to)
            
            @SP      // Access the stack pointer.
            AM=M-1   // Decrement SP to point to the (top value).
            D=M      // D now holds the top value of the stack.

            @segment_var_4
            A=M      // Access the address stored in segment_var
            M=D      // the top value of the stack is now stored at the computed address(base_address + index)
            
(O)

            @ARG      // Load the base address of current segment 
            D=M       // D = base address
            @0  // Load index
            D=D+A     // A = base address + index
            A=D       // set A to computed address
            D=M       // D = *(base address + index)
            @SP
            A=M       // A = SP, top of the stack
            M=D       // *SP = value at computed address
            @SP
            M=M+1     // SP++, increment the stack pointer
            

        @SP       // Access SP
        AM=M-1    // Decrement SP to point to the top of the stack
        D=M       // D now holds the value at the top of the stack
        @O  
        D;JGT     //if the vaalue at the top of the stack is greater than zero goto label
        
@N   //goto command
0;JMP
(O)

            @THAT      // Load the base address of current segment 
            D=M       // D = base address
            @0  // Load index
            D=D+A     // A = base address + index
            A=D       // set A to computed address
            D=M       // D = *(base address + index)
            @SP
            A=M       // A = SP, top of the stack
            M=D       // *SP = value at computed address
            @SP
            M=M+1     // SP++, increment the stack pointer
            

            @THAT      // Load the base address of current segment 
            D=M       // D = base address
            @1  // Load index
            D=D+A     // A = base address + index
            A=D       // set A to computed address
            D=M       // D = *(base address + index)
            @SP
            A=M       // A = SP, top of the stack
            M=D       // *SP = value at computed address
            @SP
            M=M+1     // SP++, increment the stack pointer
            
@SP     //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value).
                    M=D+M     //SP now holds the computed value (the sum of both operands).
                    @SP       //Access SP to increment it back to the next empty slot.
                    M=M+1

            @THAT       // Load the segment's base address 
            D=M      // D = base address
            @2 // Load index
            D=D+A    // A = base address + index

            @segment_var_7
            M=D      // segment_var now holds the computed address(where the top value of the stack will be poped to)
            
            @SP      // Access the stack pointer.
            AM=M-1   // Decrement SP to point to the (top value).
            D=M      // D now holds the top value of the stack.

            @segment_var_7
            A=M      // Access the address stored in segment_var
            M=D      // the top value of the stack is now stored at the computed address(base_address + index)
            

            @THAT// Access "THIS" or "THAT"
            D=M       // D now holds the value at "THIS" or "THAT" respectively
            @SP       // Access SP to store 
            A=M       // A = SP (top of the stack)
            M=D       // *SP = D (value stored at THIS or THAT respectively)
            @SP       // Access SP to increment it
            M=M+1
            

            @1 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            
@SP     //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value).
                    M=D+M     //SP now holds the computed value (the sum of both operands).
                    @SP       //Access SP to increment it back to the next empty slot.
                    M=M+1

            @SP      // Access the stack pointer
            AM=M-1   // Decrement SP to point to the (top value)
            D=M      // D now holds the top value of the stack
            @THAT // Access THAT
            M=D      // Store the value from the stack in THAT
            

            @ARG      // Load the base address of current segment 
            D=M       // D = base address
            @0  // Load index
            D=D+A     // A = base address + index
            A=D       // set A to computed address
            D=M       // D = *(base address + index)
            @SP
            A=M       // A = SP, top of the stack
            M=D       // *SP = value at computed address
            @SP
            M=M+1     // SP++, increment the stack pointer
            

            @1 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            
@SP     //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value)
                    M=M-D     //SP now holds the value after substraction.
                    @SP       //Access SP to increment it back to the next empty slot. 
                    M=M+1

            @ARG       // Load the segment's base address 
            D=M      // D = base address
            @0 // Load index
            D=D+A    // A = base address + index

            @segment_var_12
            M=D      // segment_var now holds the computed address(where the top value of the stack will be poped to)
            
            @SP      // Access the stack pointer.
            AM=M-1   // Decrement SP to point to the (top value).
            D=M      // D now holds the top value of the stack.

            @segment_var_12
            A=M      // Access the address stored in segment_var
            M=D      // the top value of the stack is now stored at the computed address(base_address + index)
            
@O   //goto command
0;JMP
(N)
