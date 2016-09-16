import numpy as np

from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from sympy.abc import x,y
from mpmath import *
from random import choice, randint
from Function import *

class Production:
	@classmethod
	def getRandomProductionRule(self):
		return choice( list(Production.production ) )


	@classmethod
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
				self.powerConst(func2, 2)
			)
		if productionRule == self.compose:
			return self.times( self.compose(func1D, func2), func2D )
		if productionRule == self.power:
			return self.times(
				self.power( func1, func2 ),
				self.plus(
					self.times( func2, self.divide( func1D, func1 ) ),
					self.times( self.compose( self.ln(), func1 ), func2D )
				)
			)
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
			elif float( func1.getStringFunc() ) == 1:
				return func2

		# if func2 is a constant, swap the 2 functions
		elif func2.constant():
			return Production.times( func2, func1 )

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
			elif float( func2.getStringFunc() ) == 1:
				return func1

		if func1.isNotElementary():
			str1 = "(" + str1 + ")"
		if func2.isNotElementary():
			str2 = "(" + str2 + ")"
		function = Function( str1 + " / " + str2, False, False )
		function.setlatex( "\\dfrac{" + func1.getlatex() + "}{" + func2.getlatex() + "}" )

		return function


	def powerConst( func1, const ):
		str1 = "(" + func1.getStringFunc() + ")"
		latex1 = "(" + func1.getlatex() + ")"
		function = Function( str1 + "**" + str(const), False, False )
		function.setlatex( latex1 + "^{" + str(const) + "}")
		return function


	def power( func1, func2 ):
		str1 = "(" + func1.getStringFunc() + ")"
		str2 = "(" + func2.getStringFunc() + ")"
		latex1 = "(" + func1.getlatex() + ")"
		latex2 = func2.getlatex() # no need for ( ) in power
		function = Function( str1 + "**" + str2 , False, False )
		function.setlatex( latex1 + "^{" + latex2 + "}")
		return function


	def compose( func1, func2 ):
		if func1.constant():
			return func1
		function = Function( func1.getStringFunc().replace("x&", "(" + func2.getStringFunc() + ")"), False, False)
		function.setlatex( func1.getlatex().replace("x&", "(" + func2.getlatex() + ")") )
		return function


	def const( number = randint(1, 10) ):
		function = Function( str(number), True )
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
		function.setlatex( "\\sin(x&)" )
		derivative = Function( "cos(x&)")
		derivative.setlatex( "\\cos(x&)" )
		function.setDerivative( derivative )
		return function


	def cos():
		function = Function( "cos(x&)" )
		function.setlatex( "\\cos(x&)" )
		derivative = Function( "-sin(x&)", False, False)
		derivative.setlatex( "-\\sin(x&)" )
		function.setDerivative( derivative )
		return function


	def tan():
		function = Function( "tan(x&)" )
		function.setlatex( "\\tan(x&)" )
		derivative = Function( "sec(x&)**2", False, False)
		derivative.setlatex( "\\sec^2(x&)" )
		function.setDerivative( derivative )
		return function


	def sec():
		function = Function( "sec(x&)" )
		function.setlatex( "\\sec x&" )
		derivative = Function( "sec(x&) * tan(x&)", False, False)
		derivative.setlatex( "\\sec (x&) \cdot \\tan (x&)" )
		function.setDerivative( derivative )
		return function


	def csc():
		function = Function( "csc(x&)" )
		function.setlatex( "\\csc x&" )
		derivative = Function( "-(csc(x&) * cot(x&))", False, False)
		derivative.setlatex( "-\csc x& \\cdot \\cot x&" )
		function.setDerivative( derivative )
		return function


	def cot():
		function = Function( "cot(x&)" )
		function.setlatex( "\\cot x&" )
		derivative = Function( "-(csc(x&))**2", False, False)
		derivative.setlatex( "-\\csc^2(x&)" )
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
		derivative = Function( "1 / x&", False, False)
		derivative.setlatex( "\\dfrac{1}{x&}")
		function.setDerivative( derivative )
		return function

	def sqrt():
		function = Function( "sqrt(x&)" )
		function.setlatex( "\\sqrt{x&}" )
		derivative = Function( "1/(2 * sqrt(x&))", False, False)
		derivative.setlatex( "\\dfrac{1}{2\\sqrt{x&}}")
		function.setDerivative( derivative )
		return function

	def arcsin():
		function = Function( "asin(x&)" )
		function.setlatex( "\\arcsin(x&)")
		derivative = Function("1/sqrt(1 - (x&)**2)", False, False)
		derivative.setlatex("\\dfrac{1}{\\sqrt{1-(x&)^2}")
		function.setDerivative( derivative )
		return function


	def arccos():
		function = Function( "acos(x&)" )
		function.setlatex( "\\arccos(x&)" )
		derivative = Function( "-1/sqrt(1-(x&)**2)", False, False)
		derivative.setlatex("\\dfrac{-1}{\\sqrt{1-(x&)^2}")
		function.setDerivative( derivative )
		return function


	def arctan():
		function = Function( "atan(x&)" )
		function.setlatex( "\\arctan(x&)" )
		derivative = Function( "1/((x&)**2+1)", False, False )
		derivative.setlatex( "\\dfrac{1}{(x&)^2 + 1}")
		function.setDerivative( derivative )
		return function


	def arccot():
		function = Function( "acot(x&)" )
		function.setlatex( "\\arccot(x&)" )
		derivative = Function( "-1/((x&)**2+1)", False, False )
		derivative.setlatex( "\\dfrac{1}{(x&)^2+1}")
		function.setDerivative( derivative )
		return function


	def arcsec():
		function = Function( "asec(x&)" )
		function.setlatex( "\\text{arcsec}(x&)" )
		derivative = Function( "1/((x&)**2 * sqrt(1 - 1/((x&)**2)))", False, False)
		derivative.setlatex( "\\dfrac{1}{(x&)^2 \\sqrt{1 - \\frac{1}{(x&)^2}}}")
		function.setDerivative( derivative )
		return function


	def arccsc():
		function = Function( "arccsc(x&)" )
		function.setlatex( "\\text{arccsc}(x&)" )
		derivative = Function( "-1/((x&)**2 * sqrt(1 - 1/((x&)**2)))", False, False)
		derivative.setlatex( "\\dfrac{1}{(x&)^2 \\sqrt{1 - \\frac{1}{(x&)^2}}}")
		function.setDerivative( derivative )
		return function


	def sinh():
		function = Function( "sinh(x&)" )
		function.setlatex( "\\sinh(x&)" )
		derivative = Function( "cosh(x&)" )
		derivative.setlatex ( "\\cosh(x&)" )
		function.setDerivative( derivative )
		return function


	def cosh():
		function = Function( "cosh(x&)" )
		function.setlatex( "\\cosh(x&)" )
		derivative = Function( "sinh(x&)", False, False )
		derivative.setlatex( "\\sinh(x&)" )
		function.setDerivative( derivative )
		return function


	def tanh():
		function = Function( "tanh(x&)" )
		function.setlatex( "\\tanh(x&)" )
		derivative = Function( "(sech(x&))**2", False, False )
		derivative.setlatex( "\\text{sech}(x&)^2")
		function.setDerivative( derivative )
		return function

	def coth():
		function = Function( "coth(x&)" )
		function.setlatex( "\\coth(x&)" )
		derivative = Function( "-csch(x&)**2", False, False )
		derivative.setlatex( "-\\text{csch}((x&)^2" )
		function.setDerivative( derivative )
		return function


	def sech():
		function = Function( "sech(x&)" )
		function.setlatex( "\\text{sech}(x&)" )
		derivative = Function( "-tanh(x&) * sech(x&)", False, False )
		derivative.setlatex( "-\\tanh(x&) \cdot \\text{sech}(x&)" )
		function.setDerivative( derivative )
		return function


	def csch():
		function = Function( "csch(x&)" )
		function.setlatex( "\\text{csch}(x&)" )
		derivative = Function( "-coth(x&) * csch(x&)", False, False )
		derivative.setlatex( "-\\coth(x&) \cdot \\text{csch}(x&)")
		function.setDerivative( derivative )
		return function

	# productions = [ plus, minus, times, divide, compose ]

	# list of python functions, not Functions
	# elemFunctions = [ const, linear, sin, cos, tan, exp ]
	elemFunctions = [ 
		const, linear, sin, cos, tan, exp,
		arcsin, arccos, arctan, arccot, arcsec, arccsc, 
		sinh, cosh, tanh, coth, sech, csch 
	]
	complexityMap = {
		plus : 1,
		minus : 1,
		times: 2,
		divide: 3,
		compose: 4,
		power: 8
	}

	# printing name for debugging only
	nameMap = { 
		plus: "plus", 
		minus: "minus", 
		times: "times", 
		divide: "divide", 
		compose: "compose", 
		power: "power",
		const: "const",
		linear: "linear",
		sin: "sin",
		cos: "cos",
		tan: "tan",
		exp: "exp",
		arcsin: "arcsin",
		arccos: "arccos",
		arctan: "arctan",
		arccot: "arccot",
		arcsec: "arcsec",
		arccsc: "arccsc",
		sinh: "sinh",
		cosh: "cosh",
		tanh: "tanh",
		coth: "coth",
		sech: "sech",
		csch: "csch"
	}

	# list of all functions
	production = [ plus, minus, times, divide, compose, power ]

