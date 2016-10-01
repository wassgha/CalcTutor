import numpy as np

from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from FunctionTree import *
from mpmath import *


tree = FunctionTree.buildTreeWithMaxComplexity( 8 )
func =  tree.getOutputFunction() 
integral = tree.getOutputIntegral()
tree.printTree()
integral = tree.getOutputIntegral()
print("The output function is: ")
print(func.toString())
# print("The integral is: ")
# print(integral.toString())
