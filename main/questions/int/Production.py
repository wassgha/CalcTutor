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
		function = Function( str1 + "+" + str2, False, False )

	return function


def minus( func1, func2 ):
	str1 = func1.getStringFunc()
	str2 = func2.getStringFunc()

	if func1.constant() and func2.constant():
		# output function is also a constant
		function = Function( str( float(str1) - float(str2) ), True )
	else:
		function = Function( str1 + "-" + str2, False, False )

	return function


def timesDerivative( func1, func2 ):
	func2D = func2.getDerivative()
	assert func2D is not None
	return times( func1, func2D )


def timesCompose( func1, func2 ):
	assert func2.getDerivative() is not None
	return times( compose(func1, func2), func2.getDerivative() )


def timesConst( func1, func2 ):
	assert func1.constant()
	str1 = func1.getStringFunc()
	str2 = func2.getStringFunc()
	function = Function( str1 + "*" + str2 , False, False )
	return function


########## HELPER FUNCTIONS THAT ARE NOT PRODUCTION RULES ###########

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

	function = Function( str1 + "*" + str2, False, False )
	return function


def compose( func1, func2 ):
	if func1.constant():
		return func1
	function = Function( func1.getStringFunc().replace("x&", "(" + func2.getStringFunc() + ")"), False, False)
	return function


########## ELEMENTARY FUNCTIONS ######################

# Build a function with the given string and latex representations and derivative
#	content: string representation of the function
#	dContent: string representation of the derivative
#	iContent: string representation of the integral
#	isConstant: indicate whether this function is a constant function
#	isElementary: indicate whether this function is an elementary function
def buildFunction( content, iContent, dContent, isConstant = False, isElementary = False ):
	func = Function( content, isConstant, isElementary )
	integral = Function( iContent )
	derivative = Function( dContent )
	func.setDerivative( derivative )
	func.setIntegral( integral )
	return func


def const( number = None ):
	if number is None:
		number = randint(1, 10)
	numberS = str(number)
	return buildFunction( numberS, numberS + "*x&", "0", True, True )


def linear():
	number = randint(1, 10)
	numberS = str(number)
	return buildFunction( numberS + "*x&", numberS + "*(x&)**2/2", numberS )


def powerConst():
	number = randint(-10, 10)
	while number == -1:
		number = randint(-10, 10)
	numberS = str(number)
	plusOne = str(number + 1)
	minusOne = str(number - 1)
	return buildFunction( 
		"x&**" + numberS, 
		"x&**" + plusOne + "/" + plusOne,
		numberS + "*x&**" + minusOne
	)


def constPower():
	number = randint(2, 10)
	numberS = str(number)
	return buildFunction( 
		numberS + "**x&", 
		numberS + "**x&/ln(" + numberS + ")",
		numberS + "**x&*ln(" + numberS + ")",
	)
	

def ln():
	return buildFunction( "ln(x&)", "x&*ln(x&)-x&", "1/x&", False, True )


def sin():
	return buildFunction( "sin(x&)", "-cos(x&)", "cos(x&)", False, True )


def cos():
	return buildFunction( "cos(x&)", "sin(x&)", "-sin(x&)", False, True )


def secSquare():
	return buildFunction( "sec(x&)**2", "tan(x&)", "2*tan(x&)*sec(x&)**2" )


def cscSquare():
	return buildFunction( "csc(x&)**2", "-cot(x&)", "-2*cot(x&)*csc(x&)**2" )


def sectan():
	return buildFunction( "sec(x&)*tan(x&)", "sec(x&)", "sec(x&)*(tan(x&)**2 + sec(x&)**2)" )


def csccot():
	return buildFunction( "csc(x&)*cot(x&)", "-csc(x&)", "-csc(x&)*(cot(x&)**2 + csc(x&)**2)" )


def exp():
	return buildFunction( "e**x&", "e**x&", "e**x&" )


def oneOverX():
	return buildFunction( "1/x&", "ln(Abs(x&))", "-1/(x&**2)" )


def divideOnePlusSquare():
	return buildFunction( "1/(x&**2+1)", "atan(x&)", "-2*x&/(x&**2+1)**2" )


def divideSqrtOneMinusSquare():
	return buildFunction( "1/sqrt(1-x&**2)", "asin(x&)", "x&/(1-x&**2)**(3/2)" )


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
	def getIntegral( self, productionRuleString, func1, func2 ):
		if productionRuleString == "plus":
			return plus( func1.getIntegral(), func2.getIntegral() )

		if productionRuleString == "minus":
			return minus( func1.getIntegral(), func2.getIntegral() )

		if productionRuleString == "timesConst":
			assert func1.constant()
			return times( func1, func2.getIntegral() )

		if productionRuleString == "timesCompose":
			return compose( func1.getIntegral(), func2 )


		if productionRuleString == "timesDerivative":
			func1D = func1.getDerivative()
			assert func1D is not None
			return minus( times(func1,func2), times(func2, func1D) )
		assert False, "unrecognized production rule: " + productionRuleString
		

	@classmethod
	def simplify(self, func ):
		return simplify( func.toString() )


	elemFunctions = {
	    const : 5.0,
	    linear : 15.0,
	    powerConst: 15.0,
	    constPower: 15.0,
	    ln: 4.0,
	    sin : 4.0,
	    cos : 4.0,
	    secSquare: 3.0,
	    cscSquare: 3.0,
	    sectan: 5.0,
	    csccot: 5.0,
	    exp: 15.0,
	    oneOverX: 3.0,
	    divideOnePlusSquare: 2.0,
	    divideSqrtOneMinusSquare: 1.0
	}

	totalElemWeight = sum(w for c, w in elemFunctions.items())
	complexityMap = {
		plus : 1,
		minus : 1,
		timesConst: 1,
		timesCompose: 5,
		timesDerivative: 3
	}

	# printing name for debugging only
	nameMap = {
		plus: "plus",
		minus: "minus",
		timesDerivative: "timesDerivative",
		timesConst: "timesConst",
		timesCompose: "timesCompose",
		const : "const",
	    linear : "linear",
	    ln: "ln",
	    sin : "sin",
	    cos : "cos",
	    secSquare: "secSquare",
	    cscSquare: "cscSquare",
	    sectan: "sectan",
	    csccot: "csccot",
	    exp: "e^x",
	    oneOverX: "1/x",
	    divideOnePlusSquare: "1/(x^2+1)",
	    divideSqrtOneMinusSquare: "1/sqrt(1-x^2)"
	}


