from sympy.parsing.sympy_parser import parse_expr
from sympy import *
from sympy.abc import x,y
from mpmath import *
from random import choice, randint, uniform
import sys
from DiffProd import Function, FunctionTree, Production

class IntNode:

	# holder: object of type Function
	def __init__( self, holder = None):
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
			complexity = complexity + IntProduction.complexityMap[self.holder]
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
			sys.stdout.write( IntProduction.nameMap[self.holder] + " " )



class IntFunctionTree:

	# maxComp: upper bound complexity
	def __init__( self, maxComp ):
		# initialize root as a leaf
		self.root = IntNode()
		self.solutionSteps = list()
		self.maxComp = maxComp
		self.outputFunction = None


	def applyProduction( self, production ):
		leaf = self.getRandomLeaf()

		# if this leaf's value has already been set, do nothing
		if leaf.getValue() is not None:
			return

		parent = leaf.getParent()

		# replace leaf with a combo of Inner Node, Left Child, Right Child
		newNode = IntNode( production )
		# create new leaf
		newLeaf = IntNode()
		newNode.setLeftChild( leaf )
		newNode.setRightChild( newLeaf )
		self.replaceNode( leaf, newNode, parent )


		# if rule "timesConst", its left child must be a const
		if production == timesConst:
			leaf.setValue( const() )

		# if rule "timesCompose" 
		# right child must be an output of diff production rules
		if production == timesCompose:
			diffTree = FunctionTree.buildTreeWithMaxComplexity( self.maxComp / 5 )
			func = diffTree.getOutputFunction()
			newLeaf.setValue( func )

		# if rule "times", both children must be outputs of diff production rules
		if production == timesDerivative:
			diffTree1 = FunctionTree.buildTreeWithMaxComplexity( self.maxComp / 5 )
			diffTree2 = FunctionTree.buildTreeWithMaxComplexity( self.maxComp / 5 )
			func1 = diffTree1.getOutputFunction()
			func2 = diffTree2.getOutputFunction()
			leaf.setValue( func1 )
			newLeaf.setValue( func2 )


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
				func = IntProduction.getRandomElemFunction()
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
			production = node.getValue()
			leftFunction = self.getFunctionAtSubtree( node.getLeftChild() )
			rightFunction = self.getFunctionAtSubtree( node.getRightChild() )
			result = production( leftFunction, rightFunction )

			# get the integral
			integral = IntProduction.getIntegral( IntProduction.nameMap[production], leftFunction, rightFunction )
			result.setIntegral( integral )
			return result


	# Evaluate the entire tree to get the output function
	def getOutputFunction( self ):
		if self.outputFunction is None:
			self.outputFunction = self.getFunctionAtSubtree( self.root )
		return self.outputFunction
		

	def getOutputIntegral( self ):
		return self.getOutputFunction().getIntegral()


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
		iteration = 0
		tree = IntFunctionTree( complexity )
		while tree.getComplexity() < complexity and iteration < 20:
			productionRule = IntProduction.getRandomProductionRule()
			tree.applyProduction( productionRule )
			iteration = iteration + 1

		tree.assignFunctionsToLeaves()
		return tree


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


class IntProduction:
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


