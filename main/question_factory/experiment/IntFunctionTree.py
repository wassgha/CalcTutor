import sys

from ProductionRules import *
from DiffProductionRules import *
from IntProductionRules import *
from FunctionTree import *
from DiffFunctionTree import *


class IntFunctionTree(FunctionTree):

	def applyProduction( self, production, complexity ):
		leaf = self.getRandomLeaf()

		# if this leaf's value has already been set, do nothing
		if leaf.getValue() is not None:
			return

		parent = leaf.getParent()

		# replace leaf with a combo of Inner Node, Left Child, Right Child
		newNode = Node( production, complexity )
		# create new leaf
		newLeaf = Node()
		newNode.setLeftChild( leaf )
		newNode.setRightChild( newLeaf )
		self.replaceNode( leaf, newNode, parent )


		# if rule "timesConst", its left child must be a const
		if production == timesConst:
			leaf.setValue( const() )

		# if rule "timesCompose" 
		# right child must be an output of diff production rules
		if production == timesCompose:
			diffTree = DiffFunctionTree.buildTreeWithMaxComplexity( self.maxComp / 5 )
			func = diffTree.getOutputFunction()
			newLeaf.setValue( func )

		# if rule "times", both children must be outputs of diff production rules
		if production == timesDerivative:
			diffTree1 = DiffFunctionTree.buildTreeWithMaxComplexity( self.maxComp / 5 )
			diffTree2 = DiffFunctionTree.buildTreeWithMaxComplexity( self.maxComp / 5 )
			func1 = diffTree1.getOutputFunction()
			func2 = diffTree2.getOutputFunction()
			leaf.setValue( func1 )
			newLeaf.setValue( func2 )


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