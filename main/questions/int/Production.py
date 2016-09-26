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
	content, iContent,
	isConstant = False, isElementary = True,):
	func = Function( content, isConstant, isElementary )
	func.setlatex( latex )
	integral = Function( dContent, dIsConstant, dIsElementary )
	func.setDerivative( derivative )
	return func


def const( number = None):
	if number is None:
		number = randint(1, 10)
	return buildFunction( str(number), str(number) + "*x&" )





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
	def getIntegral(
		self, productionRule, 
		func1, func2, func1I, func2I, 
		func1D = None, func2D = None ):
		if productionRule == "plus":
			return plus( func1I, func2I )
		if productionRule == "minus":
			return minus( func1I, func2I )
		if productionRule == "timesConst":
			assert func2.constant()
			return times( func2, func1I )
		if productionRule == "timesCompose":
			return compose( func1I, func2 )
		if productionRule == "times":
			assert func1D is not None
			return minus( times(func1, func2) - times(g, func1D) )

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


