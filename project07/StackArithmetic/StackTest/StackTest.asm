
            @17 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @17 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            
@SP    // Accesss the stack pointer.
                    AM=M-1   // Decrement the stack pointer to point to the first oparand (top value).
                    D=M      // D now holds the first oparand
                    @SP      // Access SP again
                    AM=M-1   // Decremnet SP to point to the second oparand
                    D=D-M    // First oparand - second oparand
                    @TRUE_4 // Define label
                    D;JEQ    // If D = 0 goto true

                    //false case
                    @SP      // Access SP to store the result.
                    A=M      // A points to the next empty slot.
                    M=0      // Store the result (0) on the stack.
                    @END_5 // Define label.
                    0;JMP    // Goto end.

                    (TRUE_4)
                    @SP      // Access SP to store the result.
                    A=M      // A points to the next empty slot.
                    M=-1     // store the result (-1) on the stack.

                    (END_5)
                    @SP      // Access SP.
                    M=M+1    // Increment SP back to the next empty slot
                    

            @17 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @16 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            
@SP    // Accesss the stack pointer.
                    AM=M-1   // Decrement the stack pointer to point to the first oparand (top value).
                    D=M      // D now holds the first oparand
                    @SP      // Access SP again
                    AM=M-1   // Decremnet SP to point to the second oparand
                    D=D-M    // First oparand - second oparand
                    @TRUE_10 // Define label
                    D;JEQ    // If D = 0 goto true

                    //false case
                    @SP      // Access SP to store the result.
                    A=M      // A points to the next empty slot.
                    M=0      // Store the result (0) on the stack.
                    @END_11 // Define label.
                    0;JMP    // Goto end.

                    (TRUE_10)
                    @SP      // Access SP to store the result.
                    A=M      // A points to the next empty slot.
                    M=-1     // store the result (-1) on the stack.

                    (END_11)
                    @SP      // Access SP.
                    M=M+1    // Increment SP back to the next empty slot
                    

            @16 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @17 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            
@SP    // Accesss the stack pointer.
                    AM=M-1   // Decrement the stack pointer to point to the first oparand (top value).
                    D=M      // D now holds the first oparand
                    @SP      // Access SP again
                    AM=M-1   // Decremnet SP to point to the second oparand
                    D=D-M    // First oparand - second oparand
                    @TRUE_16 // Define label
                    D;JEQ    // If D = 0 goto true

                    //false case
                    @SP      // Access SP to store the result.
                    A=M      // A points to the next empty slot.
                    M=0      // Store the result (0) on the stack.
                    @END_17 // Define label.
                    0;JMP    // Goto end.

                    (TRUE_16)
                    @SP      // Access SP to store the result.
                    A=M      // A points to the next empty slot.
                    M=-1     // store the result (-1) on the stack.

                    (END_17)
                    @SP      // Access SP.
                    M=M+1    // Increment SP back to the next empty slot
                    

            @892 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @891 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            
@SP      //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value)
                    D=M-D     //first operand - second oparand
                    @TRUE_22//define label
                    D;JLT     //if second operand < first operand goto LT_TRUE

                    //false case
                    @SP       //access SP to store the result
                    A=M
                    M=0       //Store the result (0) on the stack
                    @END_23//goto end
                    0;JMP
                    
                (TRUE_22)
                    @SP       //access SP to store result (-1)
                    A=M
                    M=-1       // Store the result (-1) on the stack
                    @END_23      //goto end
                    0;JMP

                (END_23)
                    @SP       //Access SP and increment it back to the next empty slot. 
                    M=M+1

            @891 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @892 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            
@SP      //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value)
                    D=M-D     //first operand - second oparand
                    @TRUE_28//define label
                    D;JLT     //if second operand < first operand goto LT_TRUE

                    //false case
                    @SP       //access SP to store the result
                    A=M
                    M=0       //Store the result (0) on the stack
                    @END_29//goto end
                    0;JMP
                    
                (TRUE_28)
                    @SP       //access SP to store result (-1)
                    A=M
                    M=-1       // Store the result (-1) on the stack
                    @END_29      //goto end
                    0;JMP

                (END_29)
                    @SP       //Access SP and increment it back to the next empty slot. 
                    M=M+1

            @891 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @891 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            
@SP      //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value)
                    D=M-D     //first operand - second oparand
                    @TRUE_34//define label
                    D;JLT     //if second operand < first operand goto LT_TRUE

                    //false case
                    @SP       //access SP to store the result
                    A=M
                    M=0       //Store the result (0) on the stack
                    @END_35//goto end
                    0;JMP
                    
                (TRUE_34)
                    @SP       //access SP to store result (-1)
                    A=M
                    M=-1       // Store the result (-1) on the stack
                    @END_35      //goto end
                    0;JMP

                (END_35)
                    @SP       //Access SP and increment it back to the next empty slot. 
                    M=M+1

            @32767 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @32766 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            
@SP    // Access SP 
                    AM=M-1   // Decrement SP to point to the first oparand
                    D=M      // D now holds the first oparand
                    @SP      // Access SP again
                    AM=M-1   // Decrement Sp to point to the second oparand
                    D=M-D    // First oparand - second oparand 
                    @TRUE_40 // Define label
                    D;JGT    // if D > 0 goto true

                    //false case
                    @SP      // Access SP 
                    A=M      // A points to the next empty slot.
                    M=0      // store the result (0) on the stack
                    @END_41 // Define label
                    0;JMP    // Goto end

                    (TRUE_40)
                    @SP      // Access SP
                    A=M      // A points to the next empty slot.
                    M=-1     // Store the result (-1) on the stack

                    (END_41)
                    @SP      // Access SP 
                    M=M+1    // Increment SP to point to the next empty slot
                    

            @32766 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @32767 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            
@SP    // Access SP 
                    AM=M-1   // Decrement SP to point to the first oparand
                    D=M      // D now holds the first oparand
                    @SP      // Access SP again
                    AM=M-1   // Decrement Sp to point to the second oparand
                    D=M-D    // First oparand - second oparand 
                    @TRUE_46 // Define label
                    D;JGT    // if D > 0 goto true

                    //false case
                    @SP      // Access SP 
                    A=M      // A points to the next empty slot.
                    M=0      // store the result (0) on the stack
                    @END_47 // Define label
                    0;JMP    // Goto end

                    (TRUE_46)
                    @SP      // Access SP
                    A=M      // A points to the next empty slot.
                    M=-1     // Store the result (-1) on the stack

                    (END_47)
                    @SP      // Access SP 
                    M=M+1    // Increment SP to point to the next empty slot
                    

            @32766 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @32766 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            
@SP    // Access SP 
                    AM=M-1   // Decrement SP to point to the first oparand
                    D=M      // D now holds the first oparand
                    @SP      // Access SP again
                    AM=M-1   // Decrement Sp to point to the second oparand
                    D=M-D    // First oparand - second oparand 
                    @TRUE_52 // Define label
                    D;JGT    // if D > 0 goto true

                    //false case
                    @SP      // Access SP 
                    A=M      // A points to the next empty slot.
                    M=0      // store the result (0) on the stack
                    @END_53 // Define label
                    0;JMP    // Goto end

                    (TRUE_52)
                    @SP      // Access SP
                    A=M      // A points to the next empty slot.
                    M=-1     // Store the result (-1) on the stack

                    (END_53)
                    @SP      // Access SP 
                    M=M+1    // Increment SP to point to the next empty slot
                    

            @57 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @31 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            

            @53 //get value.
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

            @112 //get value.
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
@SP      // Access the stack pointer.
                    A=M-1    // Access the topmost value at SP - 1.
                    M=-M     // Negate the value in place.
@SP      //Access the stack pointer.
                    AM=M-1    //Decrement SP to point to the first operand (top value).
                    D=M       //D now holds the first operand.
                    @SP       //Access SP again.
                    AM=M-1    //Decrement SP to point to the second operand (next value).
                    M=D&M     //SP now holds the computed value (a boolean).
                    @SP       //Access SP to increment it back to the next empty slot.
                    M=M+1

            @82 //get value.
            D=A      //D now holds the constant value 
            @SP      //access SP to store the result.
            A=M      //A points to the next empty slot. 
            M=D      //Store the result.
            @SP      //Access SP to increment it back to the next empty slot.
            M=M+1
            
@SP    //Access the stack pointer.
                    AM=M-1   //Decrement SP to point to the first operand (top value).      
                    D=M      //D now holds the first operand.
                    @SP      //Access SP again.
                    AM=M-1   //Decrement SP to point to the second operand (next value).     
                    M=D|M    //SP now holds the computed value (a boolean). 
                    @SP      //Access SP to increment it back to the next empty slot.
                    M=M+1
@SP    // Access the stack pointer. 
                    A=M-1    // Decrement SP to point to the top value of the stack.
                    M=!M     // Apply NOT(!) directly to the top value and store it back. 
                    
