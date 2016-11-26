from ProductionRules import *
from random import choice, uniform, randint

class DiffProductionRules:
	# get a uniformly random production rule
	@classmethod
	def getRandomProductionRule( self ):
		return choice( list(self.complexityMap.keys()) )


	# get a weighted random elementary function
	@classmethod
	def getRandomElemFunction( self ):
		r = uniform(0, self.totalElemWeight)
		upto = 0.0
		for choice in self.elemFunctions.keys():
			w = self.elemFunctions[choice]
			if upto + w >= r:
				return choice
			upto += w
		assert False, "shouldn't get here"


	@classmethod
	def getDerivative(self, productionRule, func1, func2 ):
		func1D = func1.getDerivative()
		func2D = func2.getDerivative()
		if productionRule == "plus":
			return plus( func1D, func2D )
		if productionRule == "minus":
			return minus( func1D, func2D )
		if productionRule == "times":
			return plus( times(func1D, func2), times(func1, func2D) )
		if productionRule == "divide":
			return divide(
				minus( times(func1D, func2), times(func1, func2D) ),
				times( func2, func2 )
			)
		if productionRule == "compose":
			return times( compose(func1D, func2), func2D )
		if productionRule == "power":
			return times(
				power( func1, func2 ),
				plus(
					times( func2, divide( func1D, func1 ) ),
					times( compose( ln(), func1 ), func2D )
				)
			)
		if productionRule == "powerConst":
			assert func2.constant()
			return times(
				func2,
				times(
					powerConst( func1, const(int(func2.toString()) - 1) ),
					func1D
				)
			)
		assert False, "Unrecognized production rule"


	elemFunctions = {
	    const : 5.0,
	    # linear : 15.0,
	    monomial: 10.0,
	    constPower: 10.0,
	    # sqrt : 4.0,
	    # sin : 4.0,
	    # cos : 4.0,
	    # tan : 3.0,
	    # cot : .50,
	    # sec : 1.0,
	    # csc : .50,
	    # exp: 10.0,
	    # ln: 12.0,
	    # sqrt: 8.0,
	    #arcsin : 1.0,
	    #arccos : 0.5,
	    #arctan : 1.0,
	    #arccot : 0.5,
	    #arcsec : 0.25,
	    #arccsc : 0.25,
	    # sinh : 1.0/36,
	    # cosh : 1.0/36,
	    # tanh : 1.0/36,
	    # coth : 1.0/36,
	    # sech : 1.0/36,
	    # csch : 1.0/36
	}


	totalElemWeight = sum(w for c, w in elemFunctions.items())

	
	complexityMap = {
		plus : 1,
		minus : 1,
		# powerConst: 1,
		# times : 2,
		# divide : 4,
		# compose : 4,
		# power : 8
	}
