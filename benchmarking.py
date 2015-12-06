from Diagram import Diagram,Object,Morphism
from Solver.RuleMaster import RuleMaster
from Solver.Prioritiser import UltimateWeightPriotiser
from Property.Property import ProductProperty


def test():
        
    D = Diagram()
    A = Object(D,"A")
    AxA = Object(D,"AxA")
    f = Morphism(AxA,A,)
    g = Morphism(AxA,A)
    ProductProperty(f,g)
    
    RM = RuleMaster(D,prioritiser = UltimateWeightPriotiser)
    for _ in xrange(8):
        RM.rule(numberOfExtensions=10,verbose=True)
    D.printCommutativity()
    print D.Objects

test()
#from cProfile import run
#run("test()")