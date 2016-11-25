import sys

from ProductionRules import *
from DiffProductionRules import *
from IntProductionRules import *
from FunctionTree import *


class DiffFunctionTree(FunctionTree):

	def applyProduction( self, production, complexity ):
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
		newNode = Node( production, complexity )
		# create new leaf
		newLeaf = Node()
		newNode.setLeftChild( leaf )
		newNode.setRightChild( newLeaf )
		self.replaceNode( leaf, newNode, parent )
		# if an inner node has rule "powerConst", its right child must be a const
		if production == powerConst:
			newLeaf.setValue( const() )


	# Assign an elementary function to each leaf whose value has not been set
	def assignFunctionsToLeaves( self ):
		leaves = self.getAllLeaves( self.root )
		for leaf in leaves:
			if leaf.getValue() is None:
				func = DiffProductionRules.getRandomElemFunction()
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
			derivative = DiffProductionRules.getDerivative( production.__name__, leftFunction, rightFunction )
			result.setDerivative( derivative )
			return result


	# Build a function tree with the input complexity bound
	@classmethod
	def buildTreeWithMaxComplexity(self, complexity ):
		tree = DiffFunctionTree( complexity )
		while tree.getComplexity() < complexity:
			productionRule = DiffProductionRules.getRandomProductionRule()
			complexity = DiffProductionRules.complexityMap[productionRule]
			tree.applyProduction( productionRule, complexity )
		tree.assignFunctionsToLeaves()
		return tree