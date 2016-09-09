import numpy as np

from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from enum import Enum
from sympy.abc import x,y

class Production:
	plus = lambda f1,f2: f1 + f2
	minus = lambda f1, f2: f1 - f2
	times = lambda f1, f2: f1 * f2
	divide = lambda f1, f2: f1 / f2
	power = lambda f1, c: f1 ** c
	compose = lambda f1, f2: f1.subs({'x' : f2})

	complexityMap = { plus: 1, minus: 1, times: 2, divide: 3, power: 1, compose: 4 }
	functionArray = [ plus, minus, times, divide, power, compose ]
