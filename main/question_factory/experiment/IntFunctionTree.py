import sys

from ProductionRules import *
from DiffProductionRules import *
from IntProductionRules import *
from FunctionTree import *
from DiffFunctionTree import *
from sympy.parsing.sympy_parser import parse_expr
from sympy.abc import x,y
from sympy.integrals.manualintegrate import manualintegrate


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
        elif production == timesCompose:
            diffTree = DiffFunctionTree.buildTreeWithMaxComplexity( self.maxComp / 5 )
            func = diffTree.getOutputFunction()
            newLeaf.setValue( func )

        # if rule "partialInt"
        # elif production == partialInt:
        # 	constructFunctionsForPartialInt( leaf, newLeaf, newNode )


    @classmethod
    def constructFunctionsForPartialInt( self, leftChild, rightChild, parent ):
        while (True):
            # construct h(x) where int h(x) is known
            h = IntFunctionTree.buildTreeWithMaxComplexity( 5 ).getOutputFunction()

            # construct v where diff v is known
            v = DiffFunctionTree.buildTreeWithMaxComplexity( 5 ).getOutputFunction()
            vDerivative = v.getDerivative()
            assert vDerivative is not None

            # construct u = int ( h / v )
            uDerivative = divide( h, v )
            u = manualintegrate( parse_expr( uDerivative.toString() ), x )

            print( h.toString() )
            print( v.toString() )
            print( uDerivative.toString() )
            print( u )

            if not IntFunctionTree.isIntegrable( u ):
                continue

            return


    @classmethod
    def isIntegrable(self, expr):
        for args in preorder_traversal(expr):
            if isinstance( args, Integral ):
                return False
        return True


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
            integral = IntProductionRules.getIntegral( production.__name__, leftFunction, rightFunction )
            result.setIntegral( integral )
            return result


    # Build a function tree with the input complexity bound
    @classmethod
    def buildTreeWithMaxComplexity(self, complexity ):
        iteration = 0
        tree = IntFunctionTree( complexity )
        while tree.getComplexity() < complexity and iteration < 20:
            productionRule = IntProductionRules.getRandomProductionRule()
            complexity = IntProductionRules.complexityMap[productionRule]
            tree.applyProduction( productionRule, complexity )
            iteration = iteration + 1

        tree.assignFunctionsToLeaves()
        return tree
