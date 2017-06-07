# Assembly-Interpreter-AQA
An unofficial interpreter for AQA assembly code


for AQA instruction set:
http://filestore.aqa.org.uk/resources/computing/AQA-75162-75172-ALI.PDF


Notes:
- // can be used for comments.
- HALT isn't necessary at the bottom of the file as it terminates automatically.
- Memory locations may be accessed with #n or Rn
- To change the memory size or number of registers, change the constants at the top of interpreter.py

This is a basic interpreter using the instruction set of the AQA exam.
There is minimal syntax checking, but the debug info gives information that can be used to find issues.
If you do find any issues, you can create an issue on Github, or email me directly.


Jack Parsons
7/6/17
