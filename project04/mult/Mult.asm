// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

    //for_i_in_range_R1 R2+=R0

    @R2
    M=0     //result = 0

    @R1
    D=M
    @i
    M=D     //(num of iterations) i = R1

(LOOP)
    @i
    D=M
    @END
    D;JEQ   //if i (number of iterations) = 0 goto end

    @R0
    D=M
    @R2
    M=M+D   //R2 += R0, R1 times

    @i
    M=M-1   //1 iteration less

    @LOOP
    0;JMP   //goto loop until i = 0

(END)
    @END    //programs end
    0;JMP   //infinite loop
