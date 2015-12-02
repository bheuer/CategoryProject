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
    for i in xrange(10):
        RM(verbose=True)
        print D.MorphismList
    print D.Properties
    print D.MorphismList
    print D.Objects


from cProfile import run
run("test()")