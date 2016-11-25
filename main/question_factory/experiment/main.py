import numpy as np
import sys

from random import choice, uniform, randint
from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from sympy.abc import x,y
from mpmath import *
from ProductionRules import *
from DiffFunctionTree import *

tree = DiffFunctionTree.buildTreeWithMaxComplexity( 12 )
func =  tree.getOutputFunction()
tree.printTree()
derivative = func.getDerivative()
print("The output function is: ")
print(func.toString())
print("The value of the output function for x = 5 is: ")
print(Function.evaluate( func.toString(), 5))
print("Which is approximately: " )
print(N(Function.evaluate( func.toString(), 5)))
print("The derivative is: ")
print( derivative.toString() )
print("The value of the derivative for x = 5 is: ")
print(Function.evaluate( derivative.toString(), 5))
print("checking")
wolfram = "(diff (" + func.toString() + "))-(" + derivative.toString() + ")"
print( wolfram.replace(' ', '') )
