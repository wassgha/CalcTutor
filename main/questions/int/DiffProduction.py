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
	else:
		str1 = "(" + str1 + ")"
		str2 = "(" + str2 + ")"
		function = Function( str1 + " + " + str2, False, False )

	return function


def minus( func1, func2 ):
	str1 = func1.getStringFunc()
	str2 = func2.getStringFunc()

	if func1.constant() and func2.constant():
		# output function is also a constant
		function = Function( str( float(str1) - float(str2) ), True )
	else:
		str1 = "(" + str1 + ")"
		str2 = "(" + str2 + ")"
		function = Function( str1 + " - " + str2, False, False )

	return function


def times( func1, func2 ):
	str1 = func1.getStringFunc()
	str2 = func2.getStringFunc()

	if func1.constant():
		# output function is also a constant
		if func2.constant():
			function = Function( str( float(str1) * float(str2) ), True )
			return function
		# if func1 = 1, output is just func2
		elif float( func1.getStringFunc() ) == 1:
			return func2

	# if func2 is a constant, swap the 2 functions
	elif func2.constant():
		return times( func2, func1 )

	# if no function is constant, append the two
	str1 = "(" + str1 + ")"
	str2 = "(" + str2 + ")"

	function = Function( str1 + " * " + str2, False, False )
	return function


def divide( func1, func2 ):
	str1 = func1.getStringFunc()
	str2 = func2.getStringFunc()

	if func2.constant():
		# output function is also a constant
		if func1.constant():
			function = Function( str( float(str1) / float(str2) ), True )
			return function
		elif float( func2.getStringFunc() ) == 1:
			return func1

	str1 = "(" + str1 + ")"
	str2 = "(" + str2 + ")"
	function = Function( str1 + " / " + str2, False, False )
	return function


def powerConst( func1, func2 ):
	assert func2.constant()
	str1 = "(" + func1.getStringFunc() + ")"
	str2 = func2.getStringFunc()
	function = Function( str1 + "**" + str2 , False, False )
	return function


def power( func1, func2 ):
	str1 = "(" + func1.getStringFunc() + ")"
	str2 = "(" + func2.getStringFunc() + ")"
	function = Function( str1 + "**" + str2 , False, False )
	return function


def compose( func1, func2 ):
	if func1.constant():
		return func1
	function = Function( func1.getStringFunc().replace("x&", "(" + func2.getStringFunc() + ")"), False, False)
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
	content, dContent,
	dIsConstant = False, dIsElementary = False,
	isConstant = False, isElementary = True,):
	func = Function( content, isConstant, isElementary )
	derivative = Function( dContent, dIsConstant, dIsElementary )
	func.setDerivative( derivative )
	return func


def const( number = None ):
	if number is None:
		number = randint(1, 5)
	return buildFunction( str(number), "0", True, True, True, True )


def linear():
	randomConstant = str(randint(1, 10))

	if randomConstant == "1":
		return buildFunction( "x&", randomConstant, True, True )
	else:
		return buildFunction( "(" + randomConstant + "*x&)", randomConstant, True, True )


def sin():
	return buildFunction( "sin(x&)", "cos(x&)", False, True )


def cos():
	return buildFunction( "cos(x&)", "-sin(x&)" )


def tan():
	return buildFunction( "tan(x&)", "sec(x&)**2" )


def sec():
	return buildFunction( "sec(x&)", "sec(x&) * tan(x&)" )


def csc():
	return buildFunction( "csc(x&)", "-(csc(x&) * cot(x&))" )


def cot():
	return buildFunction( "cot(x&)", "-( csc(x&) )**2" )


def exp():
	return buildFunction( "exp(x&)", "exp(x&)", False, True )


def ln():
	return buildFunction( "ln(x&)", "1 / x&" )


def sqrt():
	return buildFunction( "sqrt(x&)", "1/(2 * sqrt(x&))" )


def arcsin():
	return buildFunction( "asin(x&)", "1/sqrt(1 - (x&)**2)" )


def arccos():
	return buildFunction("acos(x&)", "-1/sqrt(1-(x&)**2)" )


def arctan():
	return buildFunction(
		"atan(x&)", "1/((x&)**2+1)" )


def arccot():
	return buildFunction("acot(x&)", "-1/((x&)**2+1)" )


def arcsec():
	return buildFunction( "asec(x&)", "1/((x&)**2 * sqrt(1 - 1/((x&)**2)))" )


def arccsc():
	return buildFunction( "arccsc(x&)", "-1/((x&)**2 * sqrt(1 - 1/((x&)**2)))" )


def sinh():
	return buildFunction( "sinh(x&)", "cosh(x&)", False, True )


def cosh():
	return buildFunction( "cosh(x&)", "sinh(x&)", False, True )


def tanh():
	return buildFunction( "tanh(x&)", "(sech(x&))**2" )


def coth():
	return buildFunction( "coth(x&)", "-csch(x&)**2" )


def sech():
	return buildFunction( "sech(x&)", "-tanh(x&) * sech(x&)" )


def csch():
	return Function( "csch(x&)","-coth(x&) * csch(x&)" )


class DiffProduction:
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
			if upto + w >= r:
				return choice
			upto += w
		assert False, "shouldn't get here"


	@classmethod
	def getDerivative(self, productionRuleString, func1, func2 ):
		# todo. use pointer instead of string?
		func1D = func1.getDerivative()
		func2D = func2.getDerivative()
		assert func1D is not None and func2D is not None
		
		if productionRuleString == "plus":
			return plus( func1D, func2D )
		if productionRuleString == "minus":
			return minus( func1D, func2D )
		if productionRuleString == "times":
			return plus( times(func1D, func2), times(func1, func2D) )
		if productionRuleString == "divide":
			return divide(
				minus( times(func1D, func2), times(func1, func2D) ),
				times( func2, func2 )
			)
		if productionRuleString == "compose":
			return times( compose(func1D, func2), func2D )
		if productionRuleString == "power":
			return times(
				power( func1, func2 ),
				plus(
					times( func2, divide( func1D, func1 ) ),
					times( compose( ln(), func1 ), func2D )
				)
			)
		if productionRuleString == "powerConst":
			assert func2.constant()
			return times(
				func2,
				times(
					powerConst( func1, const(int(func2.toString()) - 1) ),
					func1D
				)
			)
		assert False, "Unrecognized production rule"


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

	# printing name for debugging
	nameMap = {
		plus: "plus",
		minus: "minus",
		times: "times",
		divide: "divide",
		compose: "compose",
		power: "power",
		powerConst: "powerConst",
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


