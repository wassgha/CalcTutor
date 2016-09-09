import numpy as np

from random import choice
from sympy.parsing.sympy_parser import parse_expr
from sympy import *

from enum import Enum
from Production import *
import sys


class Node:
	def __init__( self, holder = None ):
		self.holder = holder
		self.left = None
		self.right = None


	def setLeftChild( self, left ):
		self.left = left


	def setRightChild( self, right ):
		self.right = right


	def getLeftChild( self ):
		return self.left


	def getRightChild( self ):
		return self.right


	def isLeaf( self ):
		return self.left is None and self.right is None


	def getComplexity( self ):
		complexity = 0
		if not self.isLeaf():
			complexity = complexity + Production.complexityMap[self.holder]
		if self.left is not None:
			complexity = complexity + self.left.getComplexity()
		if self.right is not None:
			complexity = complexity + self.right.getComplexity()
		return complexity


	def display( self ):
		if not self.isLeaf():
			sys.stdout.write(Production.nameMap[self.holder] + " ")
		else:
			sys.stdout.write("elem ")


class FunctionTree:

	elemFunctions = [
		lambda x: exp(x),
		lambda x: x,
		lambda x: sin(x),
		lambda x: cos(x)
	]

	def __init__( self ):
		# initialize root as a leaf
		self.root = Node()


	def applyProduction( self, production ):
		leafAndParent = self.getRandomLeafAndParent()
		leaf = leafAndParent[0]
		parent = leafAndParent[1]
		# create new inner node holding a production rule
		newNode = Node( production )
		# create new leaf
		newLeaf = Node()
		newNode.setLeftChild( leaf )
		newNode.setRightChild( newLeaf )

		# if current leaf has a parent, update its pointer
		if parent is not None:
			if leaf == parent.getLeftChild():
				parent.setLeftChild( newNode )
			else:
				parent.setRightChild( newNode )
		# leaf is the root, update the tree's root pointer
		else:
			self.root = newNode


	def getRandomLeafAndParent( self ):
		parent = None
		currentNode = self.root
		while not currentNode.isLeaf():
			parent = currentNode
			goLeft = choice([0, 1])
			if goLeft == 1:
				currentNode = currentNode.getLeftChild()
			else:
				currentNode = currentNode.getRightChild()
		return [currentNode, parent]


	def getComplexity( self ):
		return self.root.getComplexity()


	def getRoot( self ):
		return self.root


	def traverse( self ):
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
