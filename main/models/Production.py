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
			function = Function( str( int(str1) + int(str2) ), True )
			function.setlatex( function.getStringFunc() )
		else:
			if func1.isNotElementary():
				str1 = "(" + str1 + ")"
			if func2.isNotElementary():
				str2 = "(" + str2 + ")"
			function = Function( str1 + " + " + str2, False, False )
			function.setlatex( func1.getlatex() + " + " + func2.getlatex() )

		return function


	def minus( func1, func2 ):
		str1 = func1.getStringFunc()
		str2 = func2.getStringFunc()
		latex1 = func1.getlatex()
		latex2 = func2.getlatex()

		if func1.constant() and func2.constant():
			# output function is also a constant
			function = Function( str( int(str1) - int(str2) ), True )
			function.setlatex( function.getStringFunc() )
		else:
			if func1.isNotElementary():
				str1 = "(" + str1 + ")"
				latex1 = "(" + latex1 + ")"
			if func2.isNotElementary():
				str2 = "(" + str2 + ")"
				latex2 = "(" + latex2 + ")"
			function = Function( str1 + " - " + str2, False, False )
			function.setlatex( latex1 + " - " + latex2 )

		return function


	def times( func1, func2 ):
		str1 = func1.getStringFunc()
		str2 = func2.getStringFunc()
		latex1 = func1.getlatex()
		latex2 = func2.getlatex()

		if func1.constant():
			# output function is also a constant
			if func2.constant():
				function = Function( str( int(str1) * int(str2) ), True )
				function.setlatex( function.getStringFunc() )
				return function
			# if func1 = 1, output is just func2
			elif int( func1.getStringFunc() ) == 1:
				return func2

		# if func2 is a constant, swap the 2 functions
		elif func2.constant():
			return times( func2, func1 )

		# if no function is constant, append the two
		if func1.isNotElementary():
			str1 = "(" + str1 + ")"
			latex1 = "(" + latex1 + ")"
		if func2.isNotElementary():
			str2 = "(" + str2 + ")"
			latex2 = "(" + latex2 + ")"

		function = Function( str1 + " * " + str2, False, False )
		function.setlatex( latex1 + " \cdot " + latex2 )
		return function


	def divide( func1, func2 ):
		str1 = func1.getStringFunc()
		str2 = func2.getStringFunc()

		if func2.constant():
			# output function is also a constant
			if func1.constant():
				function = Function( str( int(str1) / int(str2) ), True )
				function.setlatex( function.getStringFunc() )
				return function
			elif int( func2.getStringFunc() ) == 1:
				return func1

		if func1.isNotElementary():
			str1 = "(" + str1 + ")"
		if func2.isNotElementary():
			str2 = "(" + str2 + ")"
		function = Function( str1 + " / " + str2, False, False )
		function.setlatex( "\\dfrac{" + func1.getlatex() + "}{" + func2.getlatex() + "}" )

		return function


	def power( func1, const ):
		function = Function( func1.getStringFunc() + " **const " )
		function.setlatex( func1.getlatex() + "^{" + str(const) + "}")


	def compose( func1, func2 ):
		function = Function( func1.getStringFunc().replace("x&", "(" + func2.getStringFunc() + ")"))
		function.setlatex( func1.getlatex().replace("x&", "(" + func2.getlatex() + ")") )
		return function


	def const():
		function = Function( str(randint(1, 10)), True )
		function.setlatex( function.getStringFunc() )
		return function


	def linear():
		randomConstant = str(randint(1, 10))
		if randomConstant == "1":
			function =  Function( "x&" )
			function.setlatex( "x&")
		else:
			function = Function( "(" + randomConstant + "*x&)" )
			function.setlatex( randomConstant + "x&" )
		return function

	def sin():
		function = Function( "sin(x&)" )
		function.setlatex( "\\sin x&" )
		return function


	def cos():
		function = Function( "cos(x&)" )
		function.setlatex( "\\cos x&" )
		return function


	def tan():
		function = Function( "tan(x&)" )
		function.setlatex( "\\tan x&" )
		return function


	def sec():
		function = Function( "sec(x&)" )
		function.setlatex( "\\sec x&" )
		return function


	def csc():
		function = Function( "csc(x&)" )
		function.setlatex( "\\csc x&" )
		return function


	def cot():
		function = Function( "cot(x&)" )
		function.setlatex( "\\cot x&" )
		return function


	def exp():
		function = Function( "exp(x&)" )
		function.setlatex( "e^{x&}" )
		return function


	def ln():
		function = Function( "ln(x&)" )
		function.setlatex( "\\ln x&" )
		return function

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

