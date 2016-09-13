import numpy as np

from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from FunctionTree import *
from Production import *

# def makeFn():
# 	return parse_expr("x**2 + 2*x + 1 - (x+1)*(x+1)")

# square = simplify(makeFn())
# print (square == 0)


tree = FunctionTree.buildTreeWithMaxComplexity( 10 )
tree.printTree()
func =  tree.getOutputFunction() 
derivative = tree.getOutputDerivative()
print("The output function is: ")
print(func.toString())
print("The value of the output function for x = 5 is: ")
print(func.evaluate(5))
print("Which is approximately: " )
print(N(func.evaluate(5)))
print("The latex representation is: ")
print( func.getDisplayLatex() )
print("The derivative is: ")
print( derivative.toString() )
print("The value of the derivative for x = 5 is: ")
print( derivative.evaluate(5) )
print("The latex representation is: ")
print( derivative.getDisplayLatex() )