
            @3030 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @SP      // Access the stack pointer
            AM=M-1   // Decrement SP to point to the (top value)
            D=M      // D now holds the top value of the stack
            @THIS // Access THIS
            M=D      // Store the value from the stack in THIS
            

            @3040 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @SP      // Access the stack pointer
            AM=M-1   // Decrement SP to point to the (top value)
            D=M      // D now holds the top value of the stack
            @THAT // Access THAT
            M=D      // Store the value from the stack in THAT
            

            @32 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @THIS       // Load the segment's base address 
            D=M      // D = base address
            @2 // Load index
            D=D+A    // A = base address + index

            @segment_var_12
            M=D      // segment_var now holds the computed address(where the top value of the stack will be poped to)
            
            @SP      // Access the stack pointer.
            AM=M-1   // Decrement SP to point to the (top value).
            D=M      // D now holds the top value of the stack.

            @segment_var_12
            A=M      // Access the address stored in segment_var
            M=D      // the top value of the stack is now stored at the computed address(base_address + index)
            

            @46 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @THAT       // Load the segment's base address 
            D=M      // D = base address
            @6 // Load index
            D=D+A    // A = base address + index

            @segment_var_17
            M=D      // segment_var now holds the computed address(where the top value of the stack will be poped to)
            
            @SP      // Access the stack pointer.
            AM=M-1   // Decrement SP to point to the (top value).
            D=M      // D now holds the top value of the stack.

            @segment_var_17
            A=M      // Access the address stored in segment_var
            M=D      // the top value of the stack is now stored at the computed address(base_address + index)
            

            @THIS// Access "THIS" or "THAT"
            D=M       // D now holds the value at "THIS" or "THAT" respectively
            @SP       // Access SP to store 
            A=M       // A = SP (top of the stack)
            M=D       // *SP = D (value stored at THIS or THAT respectively)
            @SP       // Access SP to increment it
            M=M+1
            

            @THAT// Access "THIS" or "THAT"
            D=M       // D now holds the value at "THIS" or "THAT" respectively
            @SP       // Access SP to store 
            A=M       // A = SP (top of the stack)
            M=D       // *SP = D (value stored at THIS or THAT respectively)
            @SP       // Access SP to increment it
            M=M+1
            
@SP     //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value).
                    M=D+M     //SP now holds the computed value (the sum of both operands).
                    @SP       //Access SP to increment it back to the next empty slot.
                    M=M+1

            @THIS      // Load the base address of current segment 
            D=M       // D = base address
            @2  // Load index
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
                    AM=M-1    //Decrement SP to point to the second operand (next value)
                    M=M-D     //SP now holds the value after substraction.
                    @SP       //Access SP to increment it back to the next empty slot. 
                    M=M+1

            @THAT      // Load the base address of current segment 
            D=M       // D = base address
            @6  // Load index
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
