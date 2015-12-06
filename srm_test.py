from Diagram import Diagram,Object,Morphism
from Solver.RuleMaster import RuleMaster
from Solver.SimpleRuleMaster import SimpleRuleMaster
from Solver.Prioritiser import UltimateWeightPriotiser
from Property.Property import *
from IO.diagIO import diagBuild, latexDiag, Display, DisplayAll, DisplayMorphism, DisplayAllMorphisms
from Rule.Rule import *
from Homomorphism.HomomorphismIterator import HomomorphismIterator
from Rule.ExtensionRequest import ExtensionRequest



def test():
    '''tests projective property'''
    D=Diagram()
    P=Object(D,'P')
    B=Object(D,'B')
    C=Object(D,'C')
    pi=Morphism(B,C)
    f=Morphism(P,C)
    Epimorphism(pi)
    pi.latex=r"\pi"
    f.latex=r"\varphi"
    Projective(P)

    f=Morphism(P,B)
    SRM = SimpleRuleMaster(D)
    for i in xrange(10):
        SRM(verbose=True)
    return D


def test2():        #fails because SimpleRuleMaster cannot do a composition yet
    D=Diagram()
    P1=Object(D,'P1')
    P1.latex='P_1'
    P2=Object(D,'P2')
    P1.latex='P_1'
    P1xP2=Object(D,'P1xP2')
    P1xP2.latex="P_1 \oplus P_2"
    pi1=Morphism(P1xP2,P1,'pi1')
    pi2=Morphism(P1xP2,P2,'pi2')
    ProductProperty(pi1,pi2)
    B=Object(D,'B')
    C=Object(D,'C')
    pi=Morphism(B,C)
    f=Morphism(P1xP2,C)
    Epimorphism(pi)
    pi.latex=r"\pi"
    f.latex=r"\varphi"
    Projective(P1)
    Projective(P2)

    SRM = SimpleRuleMaster(D,maxMorphisms=2)
    for i in xrange(30):
        SRM(verbose=True)
    return D
    
D=test()
DisplayAll(D)
DisplayAllMorphisms(D)
print latexDiag(D)
