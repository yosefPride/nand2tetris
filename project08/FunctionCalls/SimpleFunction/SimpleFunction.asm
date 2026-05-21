
        // Sys.init, bootstrap code
        @256     //address for the top of the stack
        D=A      //D == 256
        @SP      //access SP 
        M=D      //SP = 256
        
        (SimpleFunction.test)

        @2
        D=A
        @end_1
        D;JLE    // If num_locals == 0 goto end

        (func_loop_0)
        @SP      // Access SP to store the result.
        A=M      // A points to the next empty slot. 
        M=0      // Store the result.
        @SP      // Access SP.
        M=M+1    // Increment SP back to the next empty slot
        D=D-1    // Decrement num_locals
        @func_loop_0
        D;JGT    // if D(num_locals) > 0 goto loop

        (end_1)
        

            @LCL      // Load the base address of current segment 
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
            

            @LCL      // Load the base address of current segment 
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
@SP    // Access the stack pointer. 
                    A=M-1    // Decrement SP to point to the top value of the stack.
                    M=!M     // Apply NOT(!) directly to the top value and store it back. 
                    

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
            
@SP     //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value).
                    M=D+M     //SP now holds the computed value (the sum of both operands).
                    @SP       //Access SP to increment it back to the next empty slot.
                    M=M+1

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
            
@SP     //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value)
                    M=M-D     //SP now holds the value after substraction.
                    @SP       //Access SP to increment it back to the next empty slot. 
                    M=M+1

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
        A=M
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
        
