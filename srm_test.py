from Diagram import Diagram,Object,Morphism
from Solver.RuleMaster import RuleMaster
from Solver.SimpleRuleMaster import SimpleRuleMaster
from Solver.Prioritiser import UltimateWeightPriotiser
from Property.Property import *
from IO.diagIO import processDiagSequence,diagBuild, latexDiag, Display, DisplayAll, DisplayMorphism, DisplayAllMorphisms
from Rule import *
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

def test2():        
    D=Diagram()
    P1=Object(D,'P1')
    P1.latex='P_1'
    P2=Object(D,'P2')
    P1.latex='P_1'

    id1=Identity(P1)
    id2=Identity(P2)
    
    P1xP2=Object(D,'P1xP2')
    P1xP2.latex="P_1 \oplus P_2"

    idprod=Identity(P1xP2)
    
    i1=Morphism(P1,P1xP2,'i1')
    i2=Morphism(P2,P1xP2,'i2')
    CoProductProperty(i1,i2)
    
    B=Object(D,'B')
    C=Object(D,'C')
    pi=Morphism(B,C)
    f=Morphism(P1xP2,C)
    Epimorphism(pi)
    pi.latex=r"\pi"
    f.latex=r"\varphi"
    Projective(P1)
    Projective(P2)

    P1.gridpos=(0,0)
    P2.gridpos=(0,2)
    P1xP2.gridpos=(0,1)
    B.gridpos=(1,1)
    C.gridpos=(2,1)
    P1.latex='P_1'
    P2.latex='P_2'
    P1xP2.latex='P_1 \oplus P_2'
    B.latex='B'
    C.latex='C'

    SRM = SimpleRuleMaster(D,maxMorphisms=1)
    diagSequence=[]
    while(True):
        result=SRM(numberOfExtensions=10,verbose=False,printlatex=True)
        if (result==False):
            break
        diagSequence.append(result)
    print processDiagSequence(diagSequence)
    return D

D=test2()

