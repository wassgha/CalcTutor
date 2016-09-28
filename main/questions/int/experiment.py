import numpy as np

from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from FunctionTree import *
from Production import *
from mpmath import *



tree = FunctionTree.buildTreeWithMaxComplexity( 8 )
func =  tree.getOutputFunction() 
tree.printTree()
derivative = tree.getOutputDerivative()
print("The output function is: ")
print(func.toString())