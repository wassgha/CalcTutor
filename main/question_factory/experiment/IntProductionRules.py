from ProductionRules import *
from random import choice, uniform, randint
from sympy.abc import x
from sympy.parsing.sympy_parser import parse_expr
from sympy.integrals.manualintegrate import manualintegrate

class IntProductionRules:
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
            #prfloat(w)
            if upto + w >= r:
                return choice
            upto += w
        assert False, "shouldn't get here"


    @classmethod
    def getIntegral( self, productionRuleString, func1, func2 ):
        if productionRuleString == "plus":
            return plus( func1.getIntegral(), func2.getIntegral() )

        if productionRuleString == "minus":
            return minus( func1.getIntegral(), func2.getIntegral() )

        if productionRuleString == "timesConst":
            assert func1.constant()
            return times( func1, func2.getIntegral() )

        if productionRuleString == "timesCompose":
            return compose( func1.getIntegral(), func2 )

        if productionRuleString == "partialInt":
            assert func1.getDerivative() is not None
            partial = times( func1.getDerivative(), func2 )
            partial =  parse_expr( partial.toString() )
            int = manualintegrate( partial, x )
            return minus( times(func1, func2), Function(str(int)) )

        assert False, "unrecognized production rule: " + productionRuleString


    elemFunctions = {
        const : 5.0,
        linear : 15.0,
        monomial: 15.0,
        # constPower: 15.0,
        # ln: 4.0,
        # sin : 4.0,
        # cos : 4.0,
        # secSquare: 3.0,
        # cscSquare: 3.0,
        # sectan: 5.0,
        # csccot: 5.0,
        # exp: 15.0,
        # oneOverX: 3.0,
        # divideOnePlusSquare: 2.0,
        # divideSqrtOneMinusSquare: 1.0
    }

    totalElemWeight = sum(w for c, w in elemFunctions.items())
    complexityMap = {
        plus : 1,
        minus : 1,
        # timesConst: 1,
        # timesCompose: 5,
        partialInt: 10
    }
