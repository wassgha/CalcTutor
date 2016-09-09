import numpy as np

from random import randint
from sympy.parsing.sympy_parser import parse_expr
from sympy import *

from enum import Enum

class FunctionTree:

	elemFunctions = ["e^x", "x", "sin(x)", "cos(x)"]

	def __init__( self, root ):
		self.root = root
		self.leftSubtree = None
		self.rightSubtree = None

	def applyProduction( self, production ):
		# create new root, which is an inner node holding a production rule
		newRoot = Node( NodeType.INNER_NODE, getRandomIndex(Production.functionArray) )
		# create new tree, where left subtree is the current tree and right subtree is a leaf
		newTree = FunctionTree( newRoot )
		newRightSubTree = Tree( Node( NodeType.LEAF ) )
		newTree.setLeftSubtree( self )
		newTree.setRightSubtree( newRightSubTree )
		return newTree

	def setLeftSubtree( self, tree ):
		self.leftSubtree = tree

	def setRightSubtree( self, tree ):
		self.rightSubtree = tree

	def getComplexity( self ):
		leftComp = rightComp = 0
		if self.leftSubtree is not None:
			leftComp = self.leftSubtree.getComplexity()
		if self.rightSubtree is not None:
			rightComp = self.rightSubtree.getComplexity()
		return leftComp + rightComp + self.root.getComplexity()

	class Node:
		def __init__( self, type, holder='' ):
			self.holder = holder
			self.type = type

		def getComplexity( self ):
			if self.type == NodeType.INNER_NODE:
				return Production.complexityMap[self.holder]
			else:
				return 0

	class NodeType(Enum):
		LEAF = 0
		INNER_NODE = 1


def getRandomIndex( arr ):
	return randint( 0, len(arr) )