import numpy as np

from random import randint
from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from FunctionTree import *
from Production import *

# def makeFn():
# 	return parse_expr("x**2")

# square = makeFn() ** makeFn()
# x = symbols("x")
# print square.subs(x,5)

prod = Production()
tree = FunctionTree()
while tree.getComplexity() < 15:
	productionRule = prod.getRandomProductionRule()
	tree.applyProduction( productionRule )
tree.traverse()