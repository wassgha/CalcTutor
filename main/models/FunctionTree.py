import numpy as np

from random import choice

from Production import *
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
			complexity = complexity + Production.complexityMap[self.holder]
		if self.left is not None:
			complexity = complexity + self.left.getComplexity()
		if self.right is not None:
			complexity = complexity + self.right.getComplexity()
		return complexity


	# Display the name of the function / production in this node
	def display( self ):
		if self.isLeaf():
			sys.stdout.write(self.getValue()().toString() + " ")
		else:
			sys.stdout.write( Production.nameMap[self.holder] + " " )


class FunctionTree:

	def __init__( self ):
		# initialize root as a leaf
		self.root = Node()


	def applyProduction( self, production ):
		leaf = self.getRandomLeaf()
		parent = leaf.getParent()
		# create new inner node holding a production rule
		newNode = Node( production )
		# create new leaf
		newLeaf = Node()
		newNode.setLeftChild( leaf )
		newNode.setRightChild( newLeaf )
		self.replaceNode( leaf, newNode, parent )


	# Move left / right random until arriving at a leaf
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


	# Assign an elementary function to each leaf
	def assignFunctionsToLeaves( self ):
		leaves = self.getAllLeaves( self.root )
		for leaf in leaves:
			func = choice( Production.elemFunctions )
			leaf.setValue( func )


	# Print the tree level by level
	def printTree( self ):
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


	# Evaluate the subtree rooted at node to get the output function
	def getFunctionAtSubtree( self, node ):
		if node.isLeaf():
			return node.getValue()()

		production = node.getValue()
		leftFunction = self.getFunctionAtSubtree( node.getLeftChild() )
		rightFunction = self.getFunctionAtSubtree( node.getRightChild() )
		result = production( leftFunction, rightFunction )
		if Production.simplify(result) == 0:
			comp = node.getComplexity()
			while True:
				# create a new function tree with the same complexity but does not simplify to 0
				newTree = FunctionTree.buildTreeWithMaxComplexity( comp )
				newOutputFunction = newTree.getOutputFunction()
				if Production.simplify( newOutputFunction ) != 0:
					break
			# replace the current subtree with the new tree
			self.replaceNode( node, newTree.getRoot(), node.getParent() )
			return newOutputFunction
		return result


	# Evaluate the entire tree to get the output function
	def getOutputFunction( self ):
		return self.getFunctionAtSubtree( self.root )


	def getDerivativeAtSubtree( self, node ):
		if node.isLeaf():
			return node.getValue()().getDerivative()

		production = node.getValue()
		leftFunction = self.getFunctionAtSubtree( node.getLeftChild() )
		rightFunction = self.getFunctionAtSubtree( node.getRightChild() )
		leftDerivative = self.getDerivativeAtSubtree( node.getLeftChild() )
		rightDerivative = self.getDerivativeAtSubtree( node.getRightChild() )
		result = Production.getDerivative( production, leftFunction, rightFunction, leftDerivative, rightDerivative )
		# print("***********")
		# print("current node: ")
		# node.display()
		# sys.stdout.write("left derivative:")
		# sys.stdout.write( leftDerivative.toString()  + "\n")
		# sys.stdout.write("left derivative:")
		# sys.stdout.write( rightDerivative.toString() + "\n")
		# print("Apply differential for p rule " + Production.nameMap[production])
		# print(result.toString())
		# print("***********")
		return result


	def getOutputDerivative( self ):
		return self.getDerivativeAtSubtree( self.root )


	def replaceNode( self, oldNode, newNode, parent ):
		if parent is None:
			self.root = newNode
		elif oldNode == parent.getLeftChild():
			parent.setLeftChild( newNode )
		else:
			parent.setRightChild( newNode )


	def buildTreeWithMaxComplexity( complexity ):
		# prod = Production()
		tree = FunctionTree()
		while tree.getComplexity() < complexity:
			productionRule = Production.getRandomProductionRule()
			tree.applyProduction( productionRule )
		tree.assignFunctionsToLeaves()
		return tree