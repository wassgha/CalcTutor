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

	@classmethod
	def getRandomProductionRule(self):
		return choice( list(Production.production.values()) )


	def getDerivative(self, productionRule, func1, func2, func1D, func2D ):
		if productionRule == self.plus:
			return self.plus( func1D, func2D )
		if productionRule == self.minus:
			return self.minus( func1D, func2D )
		if productionRule == self.times:
			return self.plus( self.times(func1D, func2), self.times(func1, func2D) )
		if productionRule == self.divide:
			return self.divide( 
				self.minus( self.times(func1D, func2), self.times(func1, func2D) ), 
				self.power(func2, 2)
			)
		if productionRule == self.compose:
			return self.times( self.compose(func1D, func2), func2D )
		print("no match")


	@classmethod
	def simplify(self, func ):
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


	def times(func1, func2 ):
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
			elif float( func1.getStringFunc() ) == 1:
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

		# TODO. f(x) ^ g(x) ?
	def power( func1, const ):
		function = Function( func1.getStringFunc() + " **" + str(const) )
		function.setlatex( func1.getlatex() + "^{" + str(const) + "}")
		return function


	def compose( func1, func2 ):
		function = Function( func1.getStringFunc().replace("x&", "(" + func2.getStringFunc() + ")"))
		function.setlatex( func1.getlatex().replace("x&", "(" + func2.getlatex() + ")") )
		return function


	def const():
		function = Function( str(randint(1, 10)), True )
		function.setlatex( function.getStringFunc() )
		derivative = Function( "0" )
		derivative.setlatex( "0" )
		function.setDerivative( derivative )
		return function


	def linear():
		randomConstant = "1"

		if randomConstant == "1":
			function =  Function( "x&" )
			function.setlatex( "x&")
		else:
			function = Function( "(" + randomConstant + "*x&)" )
			function.setlatex( randomConstant + "x&" )

		derivative = Function( randomConstant )
		derivative.setlatex( randomConstant )
		function.setDerivative( derivative )
		return function


	def sin():
		function = Function( "sin(x&)" )
		function.setlatex( "\\sin x&" )
		derivative = Function( "cos(x&)")
		derivative.setlatex( "\cos x&" )
		function.setDerivative( derivative )
		return function


	def cos():
		function = Function( "cos(x&)" )
		function.setlatex( "\\cos x&" )
		derivative = Function( "-sin(x&)")
		derivative.setlatex( "-\\sin x&" )
		function.setDerivative( derivative )
		return function


	def tan():
		function = Function( "tan(x&)" )
		function.setlatex( "\\tan x&" )
		derivative = Function( "sec(x&)**2")
		derivative.setlatex( "(\\sec x&)^2" )
		function.setDerivative( derivative )
		return function


	def sec():
		function = Function( "sec(x&)" )
		function.setlatex( "\\sec x&" )
		derivative = Function( "sec(x&) * tan(x&)")
		derivative.setlatex( "\\sec x& \cdot \\tan x&" )
		function.setDerivative( derivative )
		return function


	def csc():
		function = Function( "csc(x&)" )
		function.setlatex( "\\csc x&" )
		derivative = Function( "-(csc(x&) * cot(x&))")
		derivative.setlatex( "-\csc x& \\cdot \\cot x&" )
		function.setDerivative( derivative )
		return function


	def cot():
		function = Function( "cot(x&)" )
		function.setlatex( "\\cot x&" )
		derivative = Function( "-( csc(x&) )**2" )
		derivative.setlatex( "-(\csc x&)^2" )
		function.setDerivative( derivative )
		return function


	def exp():
		function = Function( "exp(x&)" )
		function.setlatex( "e^{x&}" )
		derivative = Function( "exp(x&)")
		derivative.setlatex( "e^{x&}" )
		function.setDerivative( derivative )
		return function


	def ln():
		function = Function( "ln(x&)" )
		function.setlatex( "\\ln x&" )
		derivative = Function( "1 / x&")
		derivative.setlatex( "\\dfrac{ 1 }{x&}" )
		function.setDerivative( derivative )
		return function

	# productions = [ plus, minus, times, divide, compose ]

	# list of python functions, not Functions
	elemFunctions = [ const, linear, sin, cos, tan, exp ]
	complexityMap = {
		plus : 1,
		minus : 1,
		times: 2,
		divide: 3,
		compose: 4
	}
	production = {
		"plus" : plus,
		"minus" : minus,
		"times" : times,
		"divide" : divide,
		"compose" : compose,
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

