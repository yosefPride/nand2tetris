
        // Sys.init, bootstrap code
        @256     //address for the top of the stack
        D=A      //D == 256
        @SP      //access SP 
        M=D      //SP = 256
        
        //@Sys.init// Jump to Sys.init program
        //0;JMP
        
        // Call command
        // Push the return address 
        @return_address_0//
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
        @0// Access num_args (n)
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
        @Sys.init
        0;JMP
        
        (return_address_0)
        

        (Sys.init)

        @0
        D=A
        @end_2
        D;JLE    // If num_locals == 0 goto end

        (func_loop_1)
        @SP      // Access SP to store the result.
        A=M      // A points to the next empty slot. 
        M=0      // Store the result.
        @SP      // Access SP.
        M=M+1    // Increment SP back to the next empty slot
        D=D-1    // Decrement num_locals
        @func_loop_1
        D;JGT    // if D(num_locals) > 0 goto loop

        (end_2)
        

            @4000 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            // Pop pointer
            @SP      // Access the stack pointer
            AM=M-1   // Decrement SP to point to the (top value)
            D=M      // D now holds the top value of the stack
            @THIS // Access THIS
            M=D      // Store the value from the stack in THIS
            

            @5000 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            // Pop pointer
            @SP      // Access the stack pointer
            AM=M-1   // Decrement SP to point to the (top value)
            D=M      // D now holds the top value of the stack
            @THAT // Access THAT
            M=D      // Store the value from the stack in THAT
            

        // Call command
        // Push the return address 
        @return_address_3//
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
        @0// Access num_args (n)
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
        @Sys.main
        0;JMP
        
        (return_address_3)
        

            @5       // Load the base address of temp
            D=A      // D = 5
            @1 // Load index
            D=D+A    // A = base address + index

            @temp_var_4
            M=D      // temp_var now holds the computed address(where the top value of the stack will be poped to)
            
            @SP      // Access the stack pointer.
            AM=M-1   // Decrement SP to point to the (top value).
            D=M      // D now holds the top value of the stack.

            @temp_var_4
            A=M      // Access the address stored in temp_var
            M=D      // the top value of the stack is now stored at the computed address(base_address + index)
            
(LOOP)
//goto command
@LOOP
0;JMP

        (Sys.main)

        @5
        D=A
        @end_6
        D;JLE    // If num_locals == 0 goto end

        (func_loop_5)
        @SP      // Access SP to store the result.
        A=M      // A points to the next empty slot. 
        M=0      // Store the result.
        @SP      // Access SP.
        M=M+1    // Increment SP back to the next empty slot
        D=D-1    // Decrement num_locals
        @func_loop_5
        D;JGT    // if D(num_locals) > 0 goto loop

        (end_6)
        

            @4001 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            // Pop pointer
            @SP      // Access the stack pointer
            AM=M-1   // Decrement SP to point to the (top value)
            D=M      // D now holds the top value of the stack
            @THIS // Access THIS
            M=D      // Store the value from the stack in THIS
            

            @5001 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            // Pop pointer
            @SP      // Access the stack pointer
            AM=M-1   // Decrement SP to point to the (top value)
            D=M      // D now holds the top value of the stack
            @THAT // Access THAT
            M=D      // Store the value from the stack in THAT
            

            @200 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @LCL       // Load the segment's base address 
            D=M      // D = base address
            @1 // Load index
            D=D+A    // A = base address + index

            @segment_var_7
            M=D      // segment_var now holds the computed address(where the top value of the stack will be poped to)
            
            @SP      // Access the stack pointer.
            AM=M-1   // Decrement SP to point to the (top value).
            D=M      // D now holds the top value of the stack.

            @segment_var_7
            A=M      // Access the address stored in segment_var
            M=D      // the top value of the stack is now stored at the computed address(base_address + index)
            

            @40 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @LCL       // Load the segment's base address 
            D=M      // D = base address
            @2 // Load index
            D=D+A    // A = base address + index

            @segment_var_8
            M=D      // segment_var now holds the computed address(where the top value of the stack will be poped to)
            
            @SP      // Access the stack pointer.
            AM=M-1   // Decrement SP to point to the (top value).
            D=M      // D now holds the top value of the stack.

            @segment_var_8
            A=M      // Access the address stored in segment_var
            M=D      // the top value of the stack is now stored at the computed address(base_address + index)
            

            @6 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @LCL       // Load the segment's base address 
            D=M      // D = base address
            @3 // Load index
            D=D+A    // A = base address + index

            @segment_var_9
            M=D      // segment_var now holds the computed address(where the top value of the stack will be poped to)
            
            @SP      // Access the stack pointer.
            AM=M-1   // Decrement SP to point to the (top value).
            D=M      // D now holds the top value of the stack.

            @segment_var_9
            A=M      // Access the address stored in segment_var
            M=D      // the top value of the stack is now stored at the computed address(base_address + index)
            

            @123 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

        // Call command
        // Push the return address 
        @return_address_10//
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
        @1// Access num_args (n)
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
        @Sys.add12
        0;JMP
        
        (return_address_10)
        

            @5       // Load the base address of temp
            D=A      // D = 5
            @0 // Load index
            D=D+A    // A = base address + index

            @temp_var_11
            M=D      // temp_var now holds the computed address(where the top value of the stack will be poped to)
            
            @SP      // Access the stack pointer.
            AM=M-1   // Decrement SP to point to the (top value).
            D=M      // D now holds the top value of the stack.

            @temp_var_11
            A=M      // Access the address stored in temp_var
            M=D      // the top value of the stack is now stored at the computed address(base_address + index)
            

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
            

            @LCL      // Load the base address of current segment 
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
            

            @LCL      // Load the base address of current segment 
            D=M       // D = base address
            @3  // Load index
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
            @4  // Load index
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
@SP     //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value).
                    M=D+M     //SP now holds the computed value (the sum of both operands).
                    @SP       //Access SP to increment it back to the next empty slot.
                    M=M+1
@SP     //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value).
                    M=D+M     //SP now holds the computed value (the sum of both operands).
                    @SP       //Access SP to increment it back to the next empty slot.
                    M=M+1
@SP     //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value).
                    M=D+M     //SP now holds the computed value (the sum of both operands).
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
        

        (Sys.add12)

        @0
        D=A
        @end_21
        D;JLE    // If num_locals == 0 goto end

        (func_loop_20)
        @SP      // Access SP to store the result.
        A=M      // A points to the next empty slot. 
        M=0      // Store the result.
        @SP      // Access SP.
        M=M+1    // Increment SP back to the next empty slot
        D=D-1    // Decrement num_locals
        @func_loop_20
        D;JGT    // if D(num_locals) > 0 goto loop

        (end_21)
        

            @4002 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            // Pop pointer
            @SP      // Access the stack pointer
            AM=M-1   // Decrement SP to point to the (top value)
            D=M      // D now holds the top value of the stack
            @THIS // Access THIS
            M=D      // Store the value from the stack in THIS
            

            @5002 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            // Pop pointer
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
            

            @12 //get value.
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
        
