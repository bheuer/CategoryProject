from Diagram import Diagram,Object,Morphism
from Solver.RuleMaster import RuleMaster
from Solver.Prioritiser import UltimateWeightPriotiser
from Property.Property import *
from IO.diagIO import diagBuild, latexDiag, Display, DisplayAll, DisplayMorphism, DisplayAllMorphisms
from Rule import *
from Homomorphism.HomomorphismIterator import HomomorphismIterator
from Rule.ExtensionRequest import ExtensionRequest


def test():
    '''constructs and displays all products of two objects'''
    D = Diagram()
    X = Object(D,"X")
    Y = Object(D,"Y")
    f1 = Morphism(X,Y,"f1")
    f1.name="f1"
    f1.latex=r"\phi"

    rule=ExistProduct
    homs=HomomorphismIterator(rule.CD,D)
    ers=[]
    for hom in homs:
        ers.append(ExtensionRequest(rule,hom))
    for ER in ers:
        ER.implement()
    
    
    return D

#    AxA = Object(D,"AxA")
#    f = Morphism(AxA,A,)
#    g = Morphism(AxA,A)
#    ProductProperty(f,g)
    
#    RM = RuleMaster(D,prioritiser = UltimateWeightPriotiser)
#    for i in xrange(10):
#        RM(verbose=True)
#        print D.MorphismList
#    print D.Properties
#    print D.MorphismList
#    print D.Objects
#    return D


#from cProfile import run
#run("test()")
D=test()
DisplayAll(D)
D['XxY'].gridpos=(0,0) #reassign position in grid to prevent ugliness
D['YxX'].gridpos=(0,1) #
print latexDiag(D)
