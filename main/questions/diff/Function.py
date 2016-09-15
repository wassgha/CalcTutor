from sympy.parsing.sympy_parser import parse_expr
from sympy import *

class Function:

	# input: string representation of the function
	def __init__( self, input, isConstant = False, elementary = True ):
		self.func = input
		self.isConstant = isConstant
		self.elementary = elementary
		self.functionType = None
		self.latex = None
		self.derivative = None


	# Return the string currently held
	def getStringFunc( self ):
		return self.func


	# Return the proper representation of this function
	def toString( self ):
		return self.func.replace("x&", "x")


	def evaluate( self, number ):
		return parse_expr( self.getStringFunc() ).subs({"x&" : number})
	

	def constant( self ):
		return self.isConstant


	def isNotElementary( self ):
		return not self.elementary


	def setType( self, inputType ):
		self.functionType = inputType


	def getType( self ):
		return self.getType
		

	def setlatex( self, latex ):
		self.latex = latex


	def getlatex( self ):
		return self.latex


	def getDisplayLatex( self ):
		return self.latex.replace("x&", "x")


	def setDerivative( self, derivative ):
		self.derivative = derivative


	def getDerivative( self ):
		return self.derivative
