import numpy as np
import sys

from random import choice, uniform, randint
from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from sympy.abc import x,y
from mpmath import *

class Function:
	# input: string representation of the function. Variables are marked as "x&" instead of "x"
	# because later "x&" will be replaced with an actual number.
	# isConstant: boolean to indicate if this function is a constant
	# elementary: boolean to indicate if this function is an elementary function.
	def __init__( self, input, isConstant = False, elementary = False ):
		self.func = input
		self.isConstant = isConstant
		self.elementary = elementary
		self.derivative = None
		self.integral = None


	# Return the string currently held
	def getStringFunc( self ):
		if self.elementary or self.isConstant:
			return self.func
		return "(" + self.func + ")"


	# Return the proper representation of this function
	def toString( self ):
		return self.func.replace("x&", "x")


	def constant( self ):
		return self.isConstant


	def isNotElementary( self ):
		return not self.elementary


	def getlatex( self ):
		return latex(parse_expr(self.toString()), inv_trig_style="full")


	def setDerivative( self, derivative ):
		self.derivative = derivative


	def getDerivative( self ):
		return self.derivative


	def getIntegral( self ):
		return self.integral


	def setIntegral( self, integral ):
		self.integral = integral

		
	# Evalute this function given an x-value using SymPy
	@classmethod
	def evaluate(self, funcString, number):
		return N(parse_expr(funcString).subs(symbols("x"),  number))



class Node:

	# holder: object of type Function
	# diff: is this a node in a differential tree or integral tree?
	def __init__( self, holder = None ):
		self.holder = holder
		self.left = None
		self.right = None
		self.parent = None


	def setValue( self, holder ):
		self.holder = holder


	def getValue( self ):
		return self.holder


	def setLeftChild( self, left ):
		self.left = left
		left.setParent( self )


	def setRightChild( self, right ):
		self.right = right
		right.setParent( self )


	def getLeftChild( self ):
		return self.left


	def getRightChild( self ):
		return self.right


	def setParent( self, parent ):
		self.parent = parent


	def getParent( self ):
		return self.parent


	def isLeaf( self ):
		return self.left is None and self.right is None


	# Get the complexity of the subtree rooted at this node
	def getComplexity( self ):
		complexity = 0
		if not self.isLeaf():
			complexity = complexity + Production.complexityMap[self.holder]
		if self.left is not None:
			complexity = complexity + self.left.getComplexity()
		if self.right is not None:
			complexity = complexity + self.right.getComplexity()
		return complexity


	# Display the name of the function / production in this node
	def display( self ):
		if self.isLeaf():
			sys.stdout.write(self.getValue().toString() + " ")
		else:
			sys.stdout.write( Production.nameMap[self.holder] + " " )


class FunctionTree:

	def __init__( self ):
		# initialize root as a leaf
		self.root = Node()
		self.solutionSteps = list()
		self.outputFunction = None


	def applyProduction( self, production ):
		leaf = self.getRandomLeaf()

		# if this leaf's value has already been set to a constant, do nothing
		if leaf.getValue() is not None:
			return

		parent = leaf.getParent()

		# avoid (f*g)^k to prevent large coefficients
		if parent is not None:
			if parent.getValue() == powerConst and production == times:
				return
		# else, replace it with a combo of Inner Node - Left Child, Right Child

		# create new inner node holding a production rule
		newNode = Node( production )
		# create new leaf
		newLeaf = Node()
		newNode.setLeftChild( leaf )
		newNode.setRightChild( newLeaf )
		self.replaceNode( leaf, newNode, parent )
		# if an inner node has rule "powerConst", its right child must be a const
		if production == powerConst:
			newLeaf.setValue( const() )

	# Move left / right randomly until arriving at a leaf
	def getRandomLeaf( self ):
		currentNode = self.root
		while not currentNode.isLeaf():
			goLeft = choice([0, 1])
			if goLeft == 1:
				currentNode = currentNode.getLeftChild()
			else:
				currentNode = currentNode.getRightChild()
		return currentNode


	# Get the entire tree's complexity
	def getComplexity( self ):
		return self.root.getComplexity()


	def getRoot( self ):
		return self.root


	# Get all the leaves in the subtree rooted at the input node
	def getAllLeaves( self, node ):
		leaves = []
		if node is not None:
			if node.isLeaf():
				leaves.append( node )
			else:
				leaves = leaves + self.getAllLeaves( node.getLeftChild() )
				leaves = leaves + self.getAllLeaves( node.getRightChild() )
		return leaves


	# Assign an elementary function to each leaf whose value has not been set
	def assignFunctionsToLeaves( self ):
		leaves = self.getAllLeaves( self.root )
		for leaf in leaves:
			if leaf.getValue() is None:
				func = Production.getRandomElemFunction()
				# Move coefficient if (a*x)^b
				if func == linear and leaf.getParent() is not None and leaf.getParent().getValue() == powerConst:
				    leaf.setValue( buildFunction( "x&", "1", True, True ) )
				    parent = leaf.getParent()
				    grandparent = parent.getParent()
				    # create new inner node for coefficient multiplication
				    newNode = Node( times )
				    # create new leaf
				    newLeaf = Node( const() )
				    newNode.setLeftChild( newLeaf )
				    newNode.setRightChild( parent )
				    self.replaceNode( parent, newNode, grandparent )
				else:
				    leaf.setValue( func() )


	# Print the tree level by level
	def printTree( self ):
		print("*****************")
		thisLevel = [ self.root ]
		while len(thisLevel) > 0:
			nextLevel = list()
			for node in thisLevel:
				node.display()
				if node.getLeftChild() is not None:
					nextLevel.append( node.getLeftChild() )
				if node.getRightChild() is not None:
					nextLevel.append( node.getRightChild() )
			print()
			thisLevel = nextLevel
		print("*****************")


	# Evaluate the subtree rooted at node to get the output function
	def getFunctionAtSubtree( self, node ):
		if node.isLeaf():
			return node.getValue()
		else:
			# get the function
			production = node.getValue()
			leftFunction = self.getFunctionAtSubtree( node.getLeftChild() )
			rightFunction = self.getFunctionAtSubtree( node.getRightChild() )
			result = production( leftFunction, rightFunction )

			# get the derivative
			derivative = Production.getDerivative( Production.nameMap[production], leftFunction, rightFunction )
			result.setDerivative( derivative )
			return result


	# Evaluate the entire tree to get the output function
	def getOutputFunction( self ):
		if self.outputFunction == None:
			self.outputFunction = self.getFunctionAtSubtree( self.root )
		return self.outputFunction


	# Get the derivative of the function of this entire tree
	def getOutputDerivative( self ):
		return self.getOutputFunction().getDerivative()


	# Replace an old node with a new node and update the pointer of the parent node
	def replaceNode( self, oldNode, newNode, parent ):
		if parent is None:
			self.root = newNode
		elif oldNode == parent.getLeftChild():
			parent.setLeftChild( newNode )
		else:
			parent.setRightChild( newNode )


	# Build a function tree with the input complexity bound
	@classmethod
	def buildTreeWithMaxComplexity(self, complexity ):
		tree = FunctionTree()
		while tree.getComplexity() < complexity:
			productionRule = Production.getRandomProductionRule()
			tree.applyProduction( productionRule )
		tree.assignFunctionsToLeaves()
		return tree


"""
	
	Production

"""


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
			if upto + w >= r:
				return choice
			upto += w
		assert False, "shouldn't get here"


	@classmethod
	def getDerivative(self, productionRule, func1, func2 ):
		func1D = func1.getDerivative()
		func2D = func2.getDerivative()
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
