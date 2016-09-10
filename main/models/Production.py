import numpy as np

from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from sympy.abc import x,y
from random import choice

class Production:
	plus = lambda f1,f2: f1 + f2
	minus = lambda f1, f2: f2 - f1
	times = lambda f1, f2: f1 * f2
	divide = lambda f1, f2: f1 / f2
	compose = lambda f1, f2: f1.subs({'x' : f2})

	complexityMap = { plus: 1, minus: 1, times: 2, divide: 3, compose: 4 }
	nameMap = { plus: "plus", minus: "minus", times: "times", divide: "divide", compose: "compose", '': "no func"}
	functionArray = [ plus, minus, times, divide, compose ]

	def getRandomProductionRule( self ):
		return choice( self.functionArray )


