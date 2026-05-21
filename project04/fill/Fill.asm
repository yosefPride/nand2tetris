// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

    //if kbd == 1+, screen == -1, else == 0

(START)
    @SCREEN
    D=A
    @screen_base
    M=D     //screen's base address

    @KBD
    D=M
    @Clear
    D;JEQ   //if no key is pressed goto Clear
    D=-1    //fill screen

(Clear)
    @screen_color
    M=D     //storeing color

(LOOP)
    @screen_base
    D=M     //storeing the index in D

    @KBD
    D=D-A   //last index of screen
    @START
    D;JGE   //if screen was filled already goto start

    @screen_color
    D=M     //storeing color in D
    @screen_base
    A=M     //puting the index to A
    M=D     //this pixel is done

    D=A+1   //next pixel
    @screen_base
    M=D     //incrementing the index

    @LOOP
    0;JMP   //goto loop
