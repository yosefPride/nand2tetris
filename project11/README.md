# Important Things To Remember
## Subroutines:
     A subroutine xxx() in a class yyy is compiled into a VM function yyy.xxx().
     A function or a constructor with K arguments is compiled into a VM function with K arguments.
     A subroutine with K arguments is compiled into a VM function with K+1 arguments. the first argument is always 'this' (the current object).

     Before calling a VM function the caller must push the function's arguments to the stack. 
     If it's a method, the first argument (arg 0) must be 'this'.

     When compiling a method the compiler must set its base address.
     Similarly, for a constructor the compiler must allocate memory for the new object (using memory.alloc(size)),
     and then set the base of 'this' to point at its base.

     Since all methods must return a value, void methods return 'constant 0'.
     The caller of a void method/function must pop (and ignore) the returned value (constant 0).

     Static variables are allocated to and accessed via the static segment of the vm file.
     A field variable is accessed by first pointing to the 'this' segment (using pointer 0) and then using individual indexes.
     An array is accessed by first pointing to the 'that ' segment (using pointer 1) and then using 'that 0'.

### Methods:
     If the method call mentions no varName, we push the symbol table mapping of this.Next,
     we call compileExpressionList.This routine calls compileExpression n times, once
     for each expression in the parentheses.Finally, we generate the command call className.methodName
     informing that arguments were pushed onto the stack.

     The special case of calling an argument-less method is translated into call className.methodName 1.
     Note that className is the symbol table type of the varName identifier.