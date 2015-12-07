from Diagram import Diagram,Object,Morphism
from Solver.RuleMaster import RuleMaster
from Solver.Prioritiser import UltimateWeightPriotiser
from Property.Property import ProductProperty
from Rule.abelian import AbelianCategory
from Rule import *
from Rule.Compose import ComposeRule

def abeliantest():
    D = Diagram(category = AbelianCategory)
    
    A = Object(D,"A")
    B = Object(D,"B")
    f = Morphism(A,B,"f")
    
    #K = Object(D,"K")
    #iker = Morphism(K,A,"ker_f")
    #Kernel(f,iker)
    
    C = Object(D,"C")
    g = Morphism(C,A,"g")
    
    SetEqualZero(f*g)

    Rules = abelianRules+[ComposeRule,ExistIdentity]
    RM = RuleMaster(D,Rules = Rules, prioritiser = UltimateWeightPriotiser)
    for _ in xrange(40):
        RM.rule(verbose=True)
    D.printCommutativity()

abeliantest()
#from cProfile import run
#run("abeliantest()")

def test():
        
    D = Diagram()
    A = Object(D,"A")
    AxA = Object(D,"AxA")
    f = Morphism(AxA,A,)
    g = Morphism(AxA,A)
    ProductProperty(f,g)
    
    RM = RuleMaster(D,prioritiser = UltimateWeightPriotiser)
    for _ in xrange(10):
        RM.rule(numberOfExtensions=3,verbose=True)
    D.printCommutativity()
    print D.Objects

#test()
#from cProfile import run
#run("test()")