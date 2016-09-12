from sympy.parsing.sympy_parser import parse_expr
from sympy import *

class Function:

	def __init__( self, input, isConstant = False, elementary = True ):
		self.func = input
		self.isConstant = isConstant
		self.elementary = elementary
		self.latex = None

	# Return the string currently held
	def getStringFunc( self ):
		return self.func


	# Return the proper representation of this function
	def toString( self ):
		return self.func.replace("x&", "x")


	def evaluate( self, number ):
		return parse_expr( self.toString() ).subs({'x' : number})
	

	def constant( self ):
		return self.isConstant


	def isNotElementary( self ):
		return not self.elementary

	def setlatex( self, latex ):
		self.latex = latex


	def getlatex( self ):
		return self.latex


	def getDisplayLatex( self ):
		return self.latex.replace("x&", "x")
