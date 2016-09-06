
import numpy as np

from random import randint
from sympy.parsing.sympy_parser import parse_expr
from sympy import *

def const():
	constant = randint(1, 10)
	print constant
	return constant
	
def rand_fn():
	x = "x"
	elementfn = [
				lambda x,y: "(" + str(x) + "*" + str(y) + ")",
				lambda x,y: "(" + str(x) + "/" + str(y) + ")",
				lambda x,y: "(" + str(x) + "**" + str(y) + ")",
				lambda x,y: "exp(" + str(x) + ")",
				lambda x,y: "ln(" + str(x) + ")",
				lambda x,y: "cos(" + str(x) + ")",
				lambda x,y: "sin(" + str(x) + ")",
				lambda x,y: "tan(" + str(x) + ")",
				lambda x,y: "sec(" + str(x) + ")",
				lambda x,y: "csc(" + str(x) + ")",
				lambda x,y: "cot(" + str(x) + ")"]
	chaining = [	
				lambda x: "+" + str(x),
				lambda x: "-" + str(x)]
	fn_parts = []
	for i in range(randint(1,3)):
		fn = x
		for i in range(randint(1,2)):
			fn = elementfn[randint(0, len(elementfn)-1)](fn, const())
		fn_parts.append(fn)
	print fn_parts
	fn = fn_parts[0]
	for fn_part in fn_parts[1:]:
		fn += chaining[randint(0, len(chaining)-1)](fn_part)
	return parse_expr(fn)