import numpy as np

from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from sympy.abc import x,y
from mpmath import *
from random import choice, randint, uniform
from Function import *


def plus( func1, func2 ):
	str1 = func1.getStringFunc()
	str2 = func2.getStringFunc()

	if func1.constant() and func2.constant():
		# output function is also a constant
		function = Function( str( float(str1) + float(str2) ), True )
		function.setlatex( function.getStringFunc() )
	else:
		str1 = "(" + str1 + ")"
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
		function = Function( str( float(str1) - float(str2) ), True )
		function.setlatex( function.getStringFunc() )
	else:
		str1 = "(" + str1 + ")"
		latex1 = "(" + latex1 + ")"
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
			function = Function( str( float(str1) * float(str2) ), True )
			function.setlatex( function.getStringFunc() )
			return function
		# if func1 = 1, output is just func2
		elif float( func1.getStringFunc() ) == 1:
			return func2

	# if func2 is a constant, swap the 2 functions
	elif func2.constant():
		return times( func2, func1 )

	# if no function is constant, append the two
	str1 = "(" + str1 + ")"
	latex1 = "(" + latex1 + ")"
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
			function = Function( str( float(str1) / float(str2) ), True )
			function.setlatex( function.getStringFunc() )
			return function
		elif float( func2.getStringFunc() ) == 1:
			return func1

	str1 = "(" + str1 + ")"
	str2 = "(" + str2 + ")"
	function = Function( str1 + " / " + str2, False, False )
	function.setlatex( "\\dfrac{" + func1.getlatex() + "}{" + func2.getlatex() + "}" )
	return function


def powerConst( func1, func2 ):
	assert func2.constant()
	str1 = "(" + func1.getStringFunc() + ")"
	str2 = func2.getStringFunc()
	latex1 = "(" + func1.getlatex() + ")"
	latex2 = func2.getlatex() # no need for ( ) in power
	function = Function( str1 + "**" + str2 , False, False )
	function.setlatex( latex1 + "^{" + latex2 + "}")
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


def const( number = None ):
	if number is None:
		number = randint(1, 9)
	function = Function( str(number), True )
	function.setlatex( function.getStringFunc() )
	derivative = Function( "0" )
	derivative.setlatex( "0" )
	function.setDerivative( derivative )
	return function


def linear():
	randomConstant = str(choice([1]*10+list(range(2,9))))

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



class Production:
	# get a uniformly random production rule
	@classmethod
	def getRandomProductionRule( self ):
		return choice( list(self.complexityMap.keys()) )


	# get a weighted random elementary function
	@classmethod
	def getRandomElemFunction( self ):
		r = uniform(0, self.totalElemWeight)
		upto = 0.0
		for choice in self.elemFunctions.keys():
			w = self.elemFunctions[choice]
			#prfloat(w)
			if upto + w >= r:
				return choice
			upto += w
		assert False, "shouldn't get here"


	@classmethod
	def getDerivative(self, productionRule, func1, func2, func1D, func2D ):
		if productionRule == "plus":
			return plus( func1D, func2D )
		if productionRule == "minus":
			return minus( func1D, func2D )
		if productionRule == "times":
			return plus( times(func1D, func2), times(func1, func2D) )
		if productionRule == "divide":
			return divide(
				minus( times(func1D, func2), times(func1, func2D) ),
				times( func2, func2 )
			)
		if productionRule == "compose":
			return times( compose(func1D, func2), func2D )
		if productionRule == "power":
			return times(
				power( func1, func2 ),
				plus(
					times( func2, divide( func1D, func1 ) ),
					times( compose( ln(), func1 ), func2D )
				)
			)
		if productionRule == "powerC":
			assert func2.constant()
			return times(
				func2,
				times(
					powerConst( func1, const(int(func2.toString()) - 1) ),
					func1D
				)
			)
		#prfloat("no match")


	@classmethod
	def simplify(self, func ):
		return simplify( func.toString() )


	elemFunctions = {
	    const : 5.0,
	    linear : 15.0,
	    sqrt : 4.0,
	    sin : 4.0,
	    cos : 4.0,
	    tan : 3.0,
	    cot : .50,
	    sec : 1.0,
	    csc : .50,
	    #arcsin : 1.0,
	    #arccos : 0.5,
	    #arctan : 1.0,
	    #arccot : 0.5,
	    #arcsec : 0.25,
	    #arccsc : 0.25,
	    # sinh : 1.0/36,
	    # cosh : 1.0/36,
	    # tanh : 1.0/36,
	    # coth : 1.0/36,
	    # sech : 1.0/36,
	    # csch : 1.0/36
	}
	totalElemWeight = sum(w for c, w in elemFunctions.items())
	complexityMap = {
		plus : 1,
		minus : 1,
		powerConst: 1,
		times : 2,
		divide : 3,
		compose : 3,
		#power : 8
	}

	# printing name for debugging only
	nameMap = {
		plus: "plus",
		minus: "minus",
		times: "times",
		divide: "divide",
		compose: "compose",
		power: "power",
		powerConst: "powerC",
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


