// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

//Loading some values into R0 and R1 to test out multiplication (Answer stored in R2 should be 40)
  @10
  D=A //Get integer value 10
  @R0
  M=D //Set R0 to 10

  @4
  D=A //Get integer value 4
  @R1
  M=D //Set R1 to 4

//Setting R3 as a counter with value of R1
  D=M //Get value of R1 which is 4
  @R3
  M=D //Set R3 to the value of R1 which in this example is 4

//Multiply by looping addition using value of R3 as a counter
(Mult)
  @R0 //Loop begins here
  D=M //Get value of R0 which is 10
  @R2
  M=D+M //Add 10 to whatever is in R2 and store it in R2

  @R3
  M=M-1 //Decrement counter
  D=M

  @Mult
  D;JGT //If the counter hasn't run out, loop

//Infinite Loop
(End)
  @End
  0;JMP
