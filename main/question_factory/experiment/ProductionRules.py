from random import choice, uniform, randint
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


def timesCompose( func1, func2 ):
	assert func2.getDerivative() is not None
	return times( compose(func1, func2), func2.getDerivative() )


def timesConst( func1, func2 ):
	assert func1.constant()
	str1 = func1.getStringFunc()
	str2 = func2.getStringFunc()
	function = Function( str1 + "*" + str2 , False, False )
	return function


# I (TIMES (f, (D g))) -> (MINUS ((TIMES (f, g)), I (TIMES (g, (D f)))))
def partialInt( func1, func2 ):
	return None

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
	if number == 1:
		return buildFunction( "x&", "(x&)**2/2", numberS, False, True )
	else:
		return buildFunction( numberS + "*x&", numberS + "*(x&)**2/2", numberS, False, True )


def monomial():
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


def sin():
	return buildFunction( "sin(x&)", "-cos(x&)", "cos(x&)", False, True )


def cos():
	return buildFunction( "cos(x&)", "sin(x&)", "-sin(x&)", False, True )


def tan():
	return buildFunction( "tan(x&)", "-ln(cos(x&))", "sec(x&)**2", False, True )


def cot():
	return buildFunction( "cot(x&)", "ln(sin(x&))", "-( csc(x&) )**2", False, True )


def sec():
	return buildFunction( "sec(x&)", "ln(tan(x&)+sec(x&))", "sec(x&) * tan(x&)", False, True )


def csc():
	return buildFunction( "csc(x&)", "-ln(cot(x&)+csc(x&))", "-(csc(x&) * cot(x&))", False, True )


def arcsin():
	return buildFunction( "asin(x&)", None, "1/sqrt(1 - (x&)**2)" )


def arccos():
	return buildFunction("acos(x&)", None, "-1/sqrt(1-(x&)**2)" )


def arctan():
	return buildFunction( "atan(x&)", None, "1/((x&)**2+1)" )


def arccot():
	return buildFunction( "acot(x&)", None, "-1/((x&)**2+1)" )


def arcsec():
	return buildFunction( "asec(x&)", None, "1/((x&)**2 * sqrt(1 - 1/((x&)**2)))" )


def arccsc():
	return buildFunction( "acsc(x&)", None, "-1/((x&)**2 * sqrt(1 - 1/((x&)**2)))" )


def secSquare():
	return buildFunction( "sec(x&)**2", "tan(x&)", "2*tan(x&)*sec(x&)**2" )


def cscSquare():
	return buildFunction( "csc(x&)**2", "-cot(x&)", "-2*cot(x&)*csc(x&)**2" )


def sectan():
	return buildFunction( "sec(x&)*tan(x&)", "sec(x&)", "sec(x&)*(tan(x&)**2 + sec(x&)**2)" )


def csccot():
	return buildFunction( "csc(x&)*cot(x&)", "-csc(x&)", "-csc(x&)*(cot(x&)**2 + csc(x&)**2)" )


def sinh():
	return buildFunction( "sinh(x&)", None, "cosh(x&)", False, True )


def cosh():
	return buildFunction( "cosh(x&)", None, "sinh(x&)", False, True )


def tanh():
	return buildFunction( "tanh(x&)", None, "(sech(x&))**2" )


def coth():
	return buildFunction( "coth(x&)", None, "-csch(x&)**2" )


def sech():
	return buildFunction( "sech(x&)", None, "-tanh(x&) * sech(x&)" )


def csch():
	return Function( "csch(x&)", None, "-coth(x&) * csch(x&)" )


def exp():
	return buildFunction( "e**x&", "e**x&", "e**x&", False, True )


def ln():
	return buildFunction( "ln(x&)", "x&*ln(x&)-x&", "1/x&", False, True )


def sqrt():
	return buildFunction( "sqrt(x&)", None, "1/(2 * sqrt(x&))" )


def oneOverX():
	return buildFunction( "1/x&", "ln(Abs(x&))", "-1/(x&**2)" )


def divideOnePlusSquare():
	return buildFunction( "1/(x&**2+1)", "atan(x&)", "-2*x&/(x&**2+1)**2" )


def divideSqrtOneMinusSquare():
	return buildFunction( "1/sqrt(1-x&**2)", "asin(x&)", "x&/(1-x&**2)**(3/2)" )


	