from Diagram import Diagram,Object,Morphism
from Solver.RuleMaster import *
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

def test3():
    str_=r"""P_1 \ar{r}{i1} & P_1 \oplus P_2 \ar[bend left]{dd}{f} & P_2 \ar{l}{i2}\\
        & A \ar{d}{\pi} & \\
        & B &"""

    D=diagBuild(str_)       #construct a diagram D from this input
                            #Also, tell the program about the following assumptions:
    Projective(D['P_1'])        #the object of D named 'P_1' is projective
    Projective(D['P_2'])        #the object of D named 'P_2' is projective
    Epimorphism(D[r'\pi'])      #the morphism named '\pi' is an epimorphism
    CoProductProperty(D['i1'],D['i2']) #P_1 \oplus P_2 is a coproduct with canonical embeddings i1,i2

    SRM = SimpleRuleMaster(D,maxMorphisms=1)
    diagSequence=[]
    while(True):
        result=SRM(numberOfExtensions=10,verbose=False,printlatex=True)
        if (result==False):
            break
        diagSequence.append(result)
    print processDiagSequence(diagSequence)
    return D

def test4():
    str_=r"""T \ar[bend left]{drrr}{u} \ar[bend right]{ddr}{v} &  & & \\
& Z \times_Y (X \times_B Y) \ar{r}{f} \ar{d}{h} & Y \times_B X \ar{r}{g} \ar{d}{i} & X \ar{d}{j} \\
& Z \ar{r}{k} & Y \ar{r}{l} & B\\
"""

    D=diagBuild(str_)       #construct a diagram D from this input
                            #Also, tell the program about the following assumptions:

    Commute(D['k']*D['h'],D['i']*D['f'])
    Commute(D['l']*D['i'],D['j']*D['g'])
    FibreProductProperty(D['h'],D['f'],D['k'],D['i'])
    FibreProductProperty(D['i'],D['g'],D['l'],D['j'])
    Commute(D['l']*D['k']*D['v'],D['j']*D['u'])
    
    SRM = SimpleRuleMaster(D,maxMorphisms=1)
    diagSequence=[]
    while(True):
        result=SRM(numberOfExtensions=10,verbose=False,printlatex=True)
        if (result==False):
            break
        diagSequence.append(result)
    print processDiagSequence(diagSequence)

    return D
D=test4()

