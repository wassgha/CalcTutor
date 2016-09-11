import numpy as np

from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from sympy.abc import x,y
from random import choice, randint
from Function import *

class Production:
	# plus = lambda f1,f2: f1 + f2
	# minus = lambda f1, f2: f2 - f1
	# times = lambda f1, f2: f1 * f2
	# divide = lambda f1, f2: f1 / f2
	# compose = lambda f1, f2: f1.subs({'x' : f2})

	# complexityMap = { plus: 1, minus: 1, times: 2, divide: 3, compose: 4 }
	# nameMap = { plus: "plus", minus: "minus", times: "times", divide: "divide", compose: "compose", '': "no func"}
	# functionArray = [ plus, minus, times, divide, compose ]

	def getRandomProductionRule( self ):
		return choice( self.productions )


	def simplify( func ):
		return simplify( func.toString() )


	def plus( func1, func2 ):
		str1 = func1.getStringFunc()
		str2 = func2.getStringFunc()
		if func1.constant() and func2.constant():
			# output function is also a constant
			return Function( str( int(str1) + int(str2) ), True )
		else:
			if func1.isNotElementary():
				str1 = "(" + str1 + ")"
			if func2.isNotElementary():
				str2 = "(" + str2 + ")"
			return Function( str1 + " + " + str2, False, False )


	def minus( func1, func2 ):
		str1 = func1.getStringFunc()
		str2 = func2.getStringFunc()
		if func1.constant() and func2.constant():
			# output function is also a constant
			return Function( str( int(str1) - int(str2) ), True )
		else:
			if func1.isNotElementary():
				str1 = "(" + str1 + ")"
			if func2.isNotElementary():
				str2 = "(" + str2 + ")"
			return Function( str1 + " - " + str2, False, False )


	def times( func1, func2 ):
		str1 = func1.getStringFunc()
		str2 = func2.getStringFunc()
		if func1.constant():
			# output function is also a constant
			if func2.constant():
				return Function( str( int(str1) * int(str2) ), True )
			# if func1 = 1, output is just func2
			elif int( func1.getStringFunc() ) == 1:
				return func2
		# if func2 is a constant, swap the 2 functions
		elif func2.constant():
			return times( func2, func1 )
		# if no function is constant, append the two
		if func1.isNotElementary():
			str1 = "(" + str1 + ")"
		if func2.isNotElementary():
			str2 = "(" + str2 + ")"
		return Function( str1 + " * " + str2, False, False )


	def divide( func1, func2 ):
		str1 = func1.getStringFunc()
		str2 = func2.getStringFunc()
		if func2.constant():
			# output function is also a constant
			if func1.constant():
				return Function( str( int(str1) / int(str2) ), True )
			elif int( func2.getStringFunc() ) == 1:
				return func1
		if func1.isNotElementary():
			str1 = "(" + str1 + ")"
		if func2.isNotElementary():
			str2 = "(" + str2 + ")"
		return Function( str1 + " / " + str2, False, False )


	def power( func1, const ):
		return Function(func1.getStringFunc() + " **const ")


	def compose( func1, func2 ):
		return Function( func1.getStringFunc().replace("x&", func2.getStringFunc()))


	def const():
		return Function( str(randint(1, 10)), True )


	def linear():
		randomConstant = str(randint(1, 10))
		if randomConstant == 1:
			return Function( "&x" )
		else:
			return Function( randomConstant + "*x&" )


	def sin():
		return Function( "sin(x&)" )

	def cos():
		return Function( "cos(x&)" )


	def tan():
		return Function( "tan(x&)" )


	def sec():
		return Function( "sec(x&)" )


	def csc():
		return Function( "csc(x&)" )


	def cot():
		return Function( "cot(x&)" )


	def exp():
		return Function( "exp(x&)" )


	def ln():
		return Function( "ln(x&)" )

	productions = [ plus, minus, times, divide, compose ]
	elemFunctions = [ const, linear, sin, cos, tan, exp ]
	complexityMap = {
		plus : 1,
		minus : 1,
		times: 2,
		divide: 3,
		compose: 4
	}

	# printing name for debugging only
	nameMap = { 
		plus: "plus", 
		minus: "minus", 
		times: "times", 
		divide: "divide", 
		compose: "compose", 
		const: "const",
		linear: "linear",
		sin: "sin",
		cos: "cos",
		tan: "tan",
		exp: "exp"
	}

