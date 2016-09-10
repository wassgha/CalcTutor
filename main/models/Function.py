from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from random import randint

class Function:
	def __init__( self, input ):
		self.func = input


	def getStringFunc( self ):
		return self.func

	def toString( self ):
		return self.func.replace("x&", "x")


	def plus( func1, func2 ):
		return Function(func1.getStringFunc() + " + " + func2.getStringFunc())


	def minus( func1, func2 ):
		return Function(func1.getStringFunc() + " - " + func2.getStringFunc())


	def times( func1, func2 ):
		return Function(func1.getStringFunc() + " * " + func2.getStringFunc())

	def divide( func1, func2 ):
		return Function(func1.getStringFunc() + " / " + func2.getStringFunc())


	def power( func1, const ):
		return Function(func1.getStringFunc() + " **const ")


	def compose( func1, func2 ):
		return Function( func1.getStringFunc().replace("x&", func2.getStringFunc()))


	def const:
		return Function( str(randint(1, 10)) )


	def linear:
		return Function( str(randint(1, 10)) + "*x&" )


	def sin:
		return Function( "sin(x&)" )

	def cos:
		return Function( "cos(x&)" )


	def tan:
		return Function( "tan(x&)" )


	def sec:
		return Function( "sec(x&)" )


	def csc:
		return Function( "csc(x&)" )


	def cot:
		return Function( "cot(x&)" )


	def exp:
		return Function( "exp(x&)" )


	def ln:
		return Function( "ln(x&)" )


f1 = Function("exp(x&)")
f2 = Function("sin(x&)")
f3 = Function.compose(f1, f2)
print(f3.toString())
realF = parse_expr(f3.toString())
print( N(realF.subs({"x": 5})) )
