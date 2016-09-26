import numpy as np

from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from sympy.abc import x,y
from mpmath import *
from random import choice, randint, uniform
from Function import *

########## PRODUCTION RULES ######################
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

########## ELEMENTARY FUNCTIONS ######################

# Build a function with the given string and latex representations and derivative
#	content: string representation of the function
#	latex: latex representation of the function
#	isConstant: indicate whether this function is a constant function
#	isElementary: indicate whether this function is an elementary function
#	dContent: string representation of the derivative
#	dLatex: latex representation of the derivative
def buildFunction( 
	content, latex, dContent, dLatex,  
	dIsConstant = False, dIsElementary = False,
	isConstant = False, isElementary = True,):
	func = Function( content, isConstant, isElementary )
	func.setlatex( latex )
	derivative = Function( dContent, dIsConstant, dIsElementary )
	derivative.setlatex( dLatex )
	func.setDerivative( derivative )
	return func


def const( number = None ):
	if number is None:
		number = randint(1, 5)
	return buildFunction( str(number), str(number), "0", "0", True, True, True, True )


def linear():
	randomConstant = str(randint(1, 10))

	if randomConstant == "1":
		return buildFunction( "x&", "x&", randomConstant, randomConstant, True, True )
	else:
		return buildFunction( 
			"(" + randomConstant + "*x&)", randomConstant + "x&", 
			randomConstant, randomConstant, True, True )


def sin():
	return buildFunction( "sin(x&)", "\\sin x&", "cos(x&)", "\\cos x&", False, True )


def cos():
	return buildFunction( "cos(x&)", "\\cos x&", "-sin(x&)", "-\\sin x&" )


def tan():
	return buildFunction( "tan(x&)", "\\tan x&", "sec(x&)**2", "(\\sec x&)^2" )


def sec():
	return buildFunction( "sec(x&)", "\\sec x&", "sec(x&) * tan(x&)", "\\sec x& \cdot \\tan x&" )


def csc():
	return buildFunction( "csc(x&)", "\\csc x&", "-(csc(x&) * cot(x&))", "-\csc x& \\cdot \\cot x&" )


def cot():
	return buildFunction( "cot(x&)", "\\cot x&", "-( csc(x&) )**2", "-(\csc x&)^2" )


def exp():
	return buildFunction( "exp(x&)", "e^{x&}", "exp(x&)", "e^{x&}", False, True )


def ln():
	return buildFunction( "ln(x&)", "\\ln x&", "1 / x&", "\\dfrac{ 1 }{x&}" )


def sqrt():
	return buildFunction( 
		"sqrt(x&)", "\\sqrt{x&}", "1/(2 * sqrt(x&))", "\\dfrac{1}{2\\sqrt{x&}}" )


def arcsin():
	return buildFunction( 
		"asin(x&)", "\\arcsin(x&)", "1/sqrt(1 - (x&)**2)", "\\dfrac{1}{\\sqrt{1-(x&)^2}" )


def arccos():
	return buildFunction(
		"acos(x&)", "\\arccos(x&)", "-1/sqrt(1-(x&)**2)", "\\dfrac{-1}{\\sqrt{1-(x&)^2}" )


def arctan():
	return buildFunction(
		"atan(x&)", "\\arctan(x&)", "1/((x&)**2+1)", "\\dfrac{1}{(x&)^2 + 1}" )


def arccot():
	return buildFunction("acot(x&)", "\\arccot(x&)", "-1/((x&)**2+1)", "\\dfrac{1}{(x&)^2+1}" )


def arcsec():
	return buildFunction( 
		"asec(x&)", "\\text{arcsec}(x&)", 
		"1/((x&)**2 * sqrt(1 - 1/((x&)**2)))",
		"\\dfrac{1}{(x&)^2 \\sqrt{1 - \\frac{1}{(x&)^2}}}" )


def arccsc():
	return buildFunction(
		"arccsc(x&)", "\\text{arccsc}(x&)",
		"-1/((x&)**2 * sqrt(1 - 1/((x&)**2)))",
		"\\dfrac{1}{(x&)^2 \\sqrt{1 - \\frac{1}{(x&)^2}}}" )


def sinh():
	return buildFunction( "sinh(x&)", "\\sinh(x&)", "cosh(x&)", "\\cosh(x&)", False, True )


def cosh():
	return buildFunction( "cosh(x&)", "\\cosh(x&)", "sinh(x&)", "\\sinh(x&)", False, True )


def tanh():
	return buildFunction( "tanh(x&)", "\\tanh(x&)", "(sech(x&))**2", "\\text{sech}(x&)^2" )


def coth():
	return buildFunction( "coth(x&)", "\\coth(x&)", "-csch(x&)**2", "-\\text{csch}((x&)^2" )


def sech():
	return buildFunction( 
		"sech(x&)", "\\text{sech}(x&)", 
		"-tanh(x&) * sech(x&)", "-\\tanh(x&) \cdot \\text{sech}(x&)" )


def csch():
	return Function( 
		"csch(x&)", "\\text{csch}(x&)", 
		"-coth(x&) * csch(x&)", "-\\coth(x&) \cdot \\text{csch}(x&)" )


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
		divide : 4,
		compose : 4,
		power : 8
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


