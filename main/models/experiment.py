import numpy as np

from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from FunctionTree import *
from Production import *

# def makeFn():
# 	return parse_expr("cos(x) * sin(x - 3)")

# square = makeFn()
# x = symbols("x")
# print (square.subs({x: 5}))

prod = Production()
tree = FunctionTree()
while tree.getComplexity() < 10:
	productionRule = prod.getRandomProductionRule()
	tree.applyProduction( productionRule )
tree.assignFunctionsToLeaves()
tree.printTree()
func =  tree.getOutputFunction() 
print("The output function is: ")
print(func)
print("The value of the output function for x = 5 is: ")
print(func.subs({'x':5}))
print("Which is approximately: " )
print(N(func.subs({'x':5})))