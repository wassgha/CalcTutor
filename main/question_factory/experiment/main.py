import numpy as np
import sys

from random import choice, uniform, randint
from sympy.parsing.sympy_parser import parse_expr
from DiffFunctionTree import *
from IntFunctionTree import *

from sympy.integrals.manualintegrate import manualintegrate
from sympy.abc import x

# for i in range(1):
#     tree = IntFunctionTree.buildTreeWithMaxComplexity( 12 )
#     tree.printTree()
#     func =  tree.getOutputFunction()
#     integral = func.getIntegral()
#     print("The output function is: ")
#     print(func.toString())
#     print("The value of the output function for x = 5 is: ")
#     print(Function.evaluate( func.toString(), 5))
#     print("Which is approximately: " )
#     print(N(Function.evaluate( func.toString(), 5)))
#     print("The integral is: ")
#     print( integral.toString() )
#     print("The value of the derivative for x = 5 is: ")
#     print(Function.evaluate( integral.toString(), 5))
#     print("checking")
#     wolfram = "(int (" + func.toString() + "))-(" + integral.toString() + ")"
#     print( wolfram.replace(' ', '') )

IntFunctionTree.constructFunctionsForPartialInt( None, None, None )
# u = parse_expr("(((10*x) + ((x**-5)))) / (((6) - ((x**-6))))")
# u = manualintegrate( u, x )
# for args in preorder_traversal(u):
#     print(args)
#     if isinstance( args, Integral ):
#         print("yo")
print("done")

# u = parse_expr( "1/(x**2-1)" )
# u = manualintegrate( u, x )
# print( u )