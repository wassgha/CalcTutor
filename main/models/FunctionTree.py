import numpy as np

from random import randint
from sympy.parsing.sympy_parser import parse_expr
from sympy import *

from enum import Enum
from Production import *
import sys

def getRandomIndex( arr ):
	return randint( 0, len(arr) - 1 )


class Node:
	def __init__( self, type, holder='' ):
		self.holder = holder
		self.type = type

	def getComplexity( self ):
		if self.type == NodeType.INNER_NODE:
			return Production.complexityMap[self.holder]
		else:
			return 0

	def display( self ):
		if self.type == NodeType.INNER_NODE:
			sys.stdout.write(Production.nameMap[self.holder] + " ")
		else:
			sys.stdout.write("elem ")

class NodeType(Enum):
	LEAF = 0
	INNER_NODE = 1


class FunctionTree:

	elemFunctions = [
		lambda x: exp(x),
		lambda x: x,
		lambda x: sin(x),
		lambda x: cos(x)
	]

	def __init__( self, root = Node(NodeType.LEAF, elemFunctions[getRandomIndex(elemFunctions)]) ):
		self.root = root
		self.leftSubtree = None
		self.rightSubtree = None

	def applyProduction( self, production ):
		# create new root, which is an inner node holding a production rule
		newRoot = Node( NodeType.INNER_NODE, production )
		# create new tree, where left subtree is the current tree and right subtree is a leaf
		newTree = FunctionTree( newRoot )
		newRightSubTree = FunctionTree( Node( NodeType.LEAF ) )
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

	def getRoot( self ):
		return self.root

	def traverse( self ):
		thisLevel = [ self ]
		while len(thisLevel) > 0:
			nextLevel = list()
			for tree in thisLevel:
				tree.getRoot().display()
				if tree.leftSubtree is not None:
					nextLevel.append( tree.leftSubtree )
				if tree.rightSubtree is not None:
					nextLevel.append( tree.rightSubtree )
			print()
			thisLevel = nextLevel
