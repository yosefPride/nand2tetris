
            @111 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @333 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @888 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            
 
            @SP
            AM=M-1   // A = SP, top of the stack
            D=M
            @StaticTest.8 // Load the static variable using the file name and the index
            M=D      //
            
 
            @SP
            AM=M-1   // A = SP, top of the stack
            D=M
            @StaticTest.3 // Load the static variable using the file name and the index
            M=D      //
            
 
            @SP
            AM=M-1   // A = SP, top of the stack
            D=M
            @StaticTest.1 // Load the static variable using the file name and the index
            M=D      //
            

            @StaticTest.3 // Load the static variable using the file name and the index
            D=M      // D = the value at that address
            @SP
            A=M      // A = SP, top of the stack
            M=D      // *SP = value at computed address
            @SP
            M=M+1    // SP++, increment the stack pointer
            

            @StaticTest.1 // Load the static variable using the file name and the index
            D=M      // D = the value at that address
            @SP
            A=M      // A = SP, top of the stack
            M=D      // *SP = value at computed address
            @SP
            M=M+1    // SP++, increment the stack pointer
            
@SP     //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value)
                    M=M-D     //SP now holds the value after substraction.
                    @SP       //Access SP to increment it back to the next empty slot. 
                    M=M+1

            @StaticTest.8 // Load the static variable using the file name and the index
            D=M      // D = the value at that address
            @SP
            A=M      // A = SP, top of the stack
            M=D      // *SP = value at computed address
            @SP
            M=M+1    // SP++, increment the stack pointer
            
@SP     //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value).
                    M=D+M     //SP now holds the computed value (the sum of both operands).
                    @SP       //Access SP to increment it back to the next empty slot.
                    M=M+1
