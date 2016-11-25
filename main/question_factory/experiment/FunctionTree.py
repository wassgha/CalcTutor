import sys

from ProductionRules import *
from DiffProductionRules import *
from IntProductionRules import *


class Node:

	# holder: object of type Function
	def __init__( self, holder = None, complexity = 0 ):
		self.holder = holder
		self.left = None
		self.right = None
		self.parent = None
		self.complexity = complexity


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


	def setComplexity( self, comp ):
		self.complexity = comp


	# Get the complexity of the subtree rooted at this node
	def getComplexityAtSubtree( self ):
		assert self.isLeaf() or self.complexity > 0
		comp = 0
		if not self.isLeaf():
			comp = comp + self.complexity
		if self.left is not None:
			comp = comp + self.left.getComplexityAtSubtree()
		if self.right is not None:
			comp = comp + self.right.getComplexityAtSubtree()
		return comp


	# Display the name of the function / production in this node
	def display( self ):
		if self.isLeaf():
			sys.stdout.write(self.getValue().toString() + " ")
		else:
			sys.stdout.write( self.holder.__name__ + " " )


class FunctionTree:

	# maxComp: upper bound complexity
	def __init__( self, maxComp ):
		# initialize root as a leaf
		self.root = Node()
		self.solutionSteps = list()
		self.maxComp = maxComp
		self.outputFunction = None


	# Get the entire tree's complexity
	def getComplexity( self ):
		return self.root.getComplexityAtSubtree()


	def getRoot( self ):
		return self.root


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


	# Evaluate the entire tree to get the output function
	def getOutputFunction( self ):
		if self.outputFunction is None:
			self.outputFunction = self.getFunctionAtSubtree( self.root )
		return self.outputFunction


	# Replace an old node with a new node and update the pointer of the parent node
	def replaceNode( self, oldNode, newNode, parent ):
		if parent is None:
			self.root = newNode
		elif oldNode == parent.getLeftChild():
			parent.setLeftChild( newNode )
		else:
			parent.setRightChild( newNode )





