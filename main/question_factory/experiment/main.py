import numpy as np
import sys

from random import choice, uniform, randint
from sympy.parsing.sympy_parser import parse_expr
from DiffFunctionTree import *
from IntFunctionTree import *

from sympy import *
from sympy.integrals.manualintegrate import manualintegrate
from sympy.abc import x

# tree = IntFunctionTree.buildTreeWithMaxComplexity( 12 )
# func =  tree.getOutputFunction()
# tree.printTree()
# integral = func.getIntegral()
# print("The output function is: ")
# print(func.toString())
# print("The value of the output function for x = 5 is: ")
# print(Function.evaluate( func.toString(), 5))
# print("Which is approximately: " )
# print(N(Function.evaluate( func.toString(), 5)))
# print("The integral is: ")
# print( integral.toString() )
# print("The value of the derivative for x = 5 is: ")
# print(Function.evaluate( integral.toString(), 5))
# print("checking")
# wolfram = "(int (" + func.toString() + "))-(" + integral.toString() + ")"
# print( wolfram.replace(' ', '') )

print( srepr(manualintegrate( 1/sin(x), x)) )