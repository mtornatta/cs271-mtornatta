// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(Loop)
//Set up screen
  @SCREEN //Base address of screen
  D=A
  @R0
  M=D	//Stores screen base address in R0

//Check for Keyboard input
(Input)
  @KBD
  D=M
  @White
  D;JEQ	//If no key is pressed the screen will jump to chose white as the fill option
  @Black
  D;JGT	//If a key is pressed it will jump to chose black as the fill option

  @Input
  0;JMP

(White)
  @R1
  M=0 //0 will whiten pixels
  @Fill //Jumps to fill screen with set value
  0;JMP

(Black)
  @R1
  M=-1 //-1 will blacken pixels
  @Fill //Jumps to fill screen with set value
  0;JMP

(Fill)
  @R1
  D=M //Get black/white value
  @R0
  A=M //Stores screen value
  M=D	//Fills screen address with either black or white depending on R1
  @R0
  D=M+1 //Peek at next screen pixel
  @KBD
  D=A-D //Used to check if whole screen is filled
  @R0
  M=M+1	//Increment register to next screen pixel

  @Fill
  D;JGT	//Exits fill loop only if whole screen is filled

  @Loop
  0;JMP
