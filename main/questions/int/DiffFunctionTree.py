import numpy as np

from random import choice

from DiffProduction import *
from Function import *
import sys


class Node:

	# holder: object of type Function
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
			complexity = complexity + DiffProduction.complexityMap[self.holder]
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
			sys.stdout.write( DiffProduction.nameMap[self.holder] + " " )


class DiffFunctionTree:

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
				func = DiffProduction.getRandomElemFunction()
				# Move coefficient if (a*x)^b
				if leaf.getParent() is None :
					leaf.setValue( func() )
				elif func == linear and leaf.getParent().getValue() == powerConst:
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
			derivative = DiffProduction.getDerivative( DiffProduction.nameMap[production], leftFunction, rightFunction )
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
		tree = DiffFunctionTree()
		while tree.getComplexity() < complexity:
			productionRule = DiffProduction.getRandomProductionRule()
			tree.applyProduction( productionRule )
		tree.assignFunctionsToLeaves()
		return tree