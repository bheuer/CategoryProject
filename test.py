from Diagram import *
from Diagram.Morphisms import AbstractMorphism
from Homomorphism import HomomorphismIterator
from Property import *
from Property.base import PropertyTag
from Solver import RuleMaster
import unittest
from Property.TestPrioritiser import CustomRuleWeight_MaxObjectPlusMaxMorphismPrioritiser
from Solver.Prioritiser import UltimateWeightPriotiser
from Rule import EpimorphismRule, MonomorphismRule, ExistIdentity,\
    ProductRuleUnique, CoProductRuleUnique, FibreProductRuleUnique, FibreProductRule, AbelianRules,\
    GenericRules
from Rule.Compose import ComposeRule
from Rule.abelianProperty import AbelianCategory, Kernel, GiveZeroMorphism,isMorphismZero,\
    Exact, reprWithoutZeros, getCokernel, getKernel, iterNonZeroMorphisms,\
    isIsomorphism
from Rule.rule import ProductRule

class CompositionTestCase(unittest.TestCase):
    def runTest(self):
        D = Diagram()
         
        '''
        
            f1
        A1 ---> A2
        |        |
        | g1 //  | g2
        V        V
        B1 ---> B2
            h1
        
        '''
        A1 = Object(D,"A1")
        A2 = Object(D,"A2")
        B1 = Object(D,"B1")
        B2 = Object(D,"B2")
        
        f1 = Morphism(A1,A2,"f1")
        g1 = Morphism(A1,B1,"g1")
        g2 = Morphism(A2,B2,"g2")
        h1 = Morphism(B1,B2,"h1")
    
        assert f1==f1
        assert f1!=g1
        id_a2 = Identity(A2)
        assert isinstance(id_a2,AbstractMorphism)
        assert g2*f1 == g2*id_a2*f1
        assert g2*f1 != h1*g1
        
class SimpleCommutativityTestCase(unittest.TestCase):
    def runTest(self):
        D = Diagram()
        
        '''
            f1
        A1 ---> A2
        |        |
        | g1 //  | g2
        V        V
        B1 ---> B2
            h1
        
        '''
        A1 = Object(D,"A1")
        A2 = Object(D,"A2")
        B1 = Object(D,"B1")
        B2 = Object(D,"B2")
        
        f1 = Morphism(A1,A2,"f1")
        g1 = Morphism(A1,B1,"g1")
        g2 = Morphism(A2,B2,"g2")
        h1 = Morphism(B1,B2,"h1")
    
    
        assert g2*f1!=h1*g1
        C1 = (g2*f1).equivalenceClass()
        C2 = (h1*g1).equivalenceClass()
        assert C1!=C2
        
        Commute(g2*f1, h1*g1)
        assert C1==C2
        
        assert g2*f1==h1*g1
        assert D.commutes(g2*f1, g2*f1)
        assert D.commutes(g2*f1, h1*g1)
    
class SecondCommutativityTestCase(unittest.TestCase):
    def runTest(self):
        D = Diagram()
        
        '''
        
            f1      f2
        A1 ---> A2 ---> A3
        |        |        |
        | g1 //  | g2 //  | g3
        V        V        |
        B1 ---> B2 ---> B3
            h1      h2
        
        '''
        
        A1 = Object(D,"A1")
        A2 = Object(D,"A2")
        A3 = Object(D,"A3")
        B1 = Object(D,"B1")
        B2 = Object(D,"B2")
        B3 = Object(D,"B3")
        
        f1 = Morphism(A1,A2,"f1")
        f2 = Morphism(A2,A3,"f2")
        g1 = Morphism(A1,B1,"g1")
        g2 = Morphism(A2,B2,"g2")
        g3 = Morphism(A3,B3,"g3")
        h1 = Morphism(B1,B2,"h1")
        h2 = Morphism(B2,B3,"h2")
        

        assert f1==f1
        assert f1!=f2
        assert f2*f1==f2*f1
        assert not f2*f1==g2*f1
    
        Commute(g2*f1,h1*g1)
        assert g2*f1==h1*g1
        
        assert g3*f2!=h2*g2
        assert g3*f2*f1!=h2*g2*f1
        
        Commute(g3*f2,h2*g2)
        assert g3*f2==h2*g2
        assert D.commutes(g3*f2,h2*g2)
        
        assert g3*f2*f1==h2*h1*g1

class MonomEpiTestCase(unittest.TestCase):
    def runTest(self):
        D = Diagram()
         
        '''
         
        f0      f1      f2
    A0 -->> A1 ---> A2 ---> A3
            |        |        |
            | g1     | g2     | g3
            V        V        |
            B1 ---> B2 ---> B3 (--->B4
                h1      h2      h3
         
        '''
         
        A0 = Object(D,"A0")
        A1 = Object(D,"A1")
        A2 = Object(D,"A2")
        A3 = Object(D,"A3")
        B1 = Object(D,"B1")
        B2 = Object(D,"B2")
        B3 = Object(D,"B3")
        B4 = Object(D,"B4")
         
        f0 = Morphism(A0,A1,"f0")
        f1 = Morphism(A1,A2,"f1")
        f2 = Morphism(A2,A3,"f2")
        g1 = Morphism(A1,B1,"g1")
        g2 = Morphism(A2,B2,"g2")
        g3 = Morphism(A3,B3,"g3")
        h1 = Morphism(B1,B2,"h1")
        h2 = Morphism(B2,B3,"h2")
        h3 = Morphism(B3,B4,"h3")
         
        RM = RuleMaster(D,prioritiser = UltimateWeightPriotiser,Rules=[EpimorphismRule,MonomorphismRule,ComposeRule])
        
        Commute(g2*f1*f0,h1*g1*f0)
        assert g2*f1*f0==h1*g1*f0
        assert g2*f1!=h1*g1
        RM.rule_exhaustively()
        assert g2*f1!=h1*g1
        
        #Epimorphism Test
        
        Epimorphism(f0)
        
        RM.rule_exhaustively()
        
        assert g2*f1==h1*g1
        
        #Monomorphism Test
        
        assert g3*f2!=h2*g2
        Commute(h3*g3*f2,h3*h2*g2)
        RM.rule_exhaustively()
        assert g3*f2!=h2*g2
        
        Monomorphism(h3)
        RM.rule_exhaustively()
        assert g3*f2==h2*g2
        assert g3*f2*f1==h2*h1*g1
     
class CycleTestCase(unittest.TestCase):
    def runTest(self):
        D = Diagram()
          
        '''
            f1
        A1 <---  A2
        |        A
        | g1 //  | g2
        V        |
        B1 ---> B2
            h1
          
        '''
        A1 = Object(D,"A1")
        A2 = Object(D,"A2")
        B1 = Object(D,"B1")
        B2 = Object(D,"B2")
          
          
        f1 = Morphism(A2,A1,"f1")
        g1 = Morphism(A1,B1,"g1")
        h1 = Morphism(B1,B2,"h1")
        g2 = Morphism(B2,A2,"g2")
        
        RM = RuleMaster(D,prioritiser = UltimateWeightPriotiser,Rules=[ExistIdentity])
        RM.rule_exhaustively()
        
        id_A1 = A1.Identity()
        loop =  f1*g2*h1*g1
        assert loop!=id_A1
        Commute(loop,id_A1)
        assert loop==id_A1
        assert loop*loop==id_A1
  
class ProductTestCase(unittest.TestCase):
    def runTest(self):
        D = Diagram()
          
        '''
            V
          f :| g
            :| 
            P         product
       pi1 / \ pi2
          /   \
         A     B
           
        '''
          
        A = Object(D,"A")
        B = Object(D,"B")
        P = Object(D,"P")
        V = Object(D,"V")
          
        pi1 = Morphism(P,A,"pi1")
        pi2 = Morphism(P,B,"pi2")
        f = Morphism(V,P,"f")
        g = Morphism(V,P,"g")
      
        ProductProperty(pi1,pi2)
        
        RM = RuleMaster(D,Rules = [ProductRuleUnique])
        
        Commute(pi2*f,pi2*g)
        RM.rule_exhaustively()
        assert f!=g
        
        Commute(pi1*f,pi1*g)
        RM.rule_exhaustively()
        assert f==g

class CoProductTestCase(unittest.TestCase):
    def runTest(self):
        D = Diagram()
          
        '''
            V
          f :| g
            :| 
            P         coproduct
       pi1 / \ pi2
          /   \
         A     B
           
        '''
          
        A = Object(D,"A")
        B = Object(D,"B")
        P = Object(D,"P")
        V = Object(D,"V")
          
        pi1 = Morphism(A,P,"pi1")
        pi2 = Morphism(B,P,"pi2")
        f = Morphism(P,V,"f")
        g = Morphism(P,V,"g")
      
        CoProductProperty(pi1,pi2)
        
        RM = RuleMaster(D,Rules = [CoProductRuleUnique])
        
        Commute(f*pi2,g*pi2)
        RM.rule_exhaustively()
        assert f!=g
        
        Commute(f*pi1,g*pi1)
        RM.rule_exhaustively()
        assert f==g

class TwoFibreProductsTestCase(unittest.TestCase):
    def runTest(self):
        CD=Diagram()
        '''
              T
          m,m2 \\  f   g
            	A -- B -- C
              h |   i|   j|
            	|    |    |
            	D -- E -- F
            	  k    l
    	'''
    	A=Object(CD,"A")
    	B=Object(CD,"B")
    	C=Object(CD,"C")
    	D=Object(CD,"D")
    	E=Object(CD,"E")
    	F=Object(CD,"F")
    	T=Object(CD,"T")
    	
    	f=Morphism(A,B,"f")
    	g=Morphism(B,C,"g")
    	h=Morphism(A,D,"h")
    	i=Morphism(B,E,"i")
    	j=Morphism(C,F,"j")
    	k=Morphism(D,E,"k")
    	l=Morphism(E,F,"l")
    	
    	Commute(k*h,i*f)
    	Commute(l*i,j*g)
    	FibreProductProperty(h,f,k,i)
    	FibreProductProperty(i,g,l,j)
    	
    	m=Morphism(T,A)
    	m2=Morphism(T,A)
    	Commute(h*m,h*m2)
    	Commute(f*m,f*m2)
    	
    	RM = RuleMaster(CD,Rules = [FibreProductRuleUnique])
            
        assert l*k*h==j*g*f
        assert m!=m2
        RM.rule_exhaustively()
        assert m==m2
        
      

class RuleMasterTest(unittest.TestCase):
    def runTest(self):
        
        D = Diagram()
        A = Object(D,"A")
        B = Object(D,"B")
        AxB = Object(D,"AxB")
        BxA = Object(D,"BxA")
        pi1 = Morphism(AxB,A,"pi1")
        pi2 = Morphism(AxB,B,"pi2")
        pi1_ = Morphism(BxA,A,"pi1_")
        pi2_ = Morphism(BxA,B,"pi2_")
        ProductProperty(pi1,pi2)
        ProductProperty(pi1_,pi2_)
        RM = RuleMaster(D,prioritiser = UltimateWeightPriotiser,Rules = [ExistIdentity,ProductRule,ProductRuleUnique,ComposeRule])
        
        RM.rule_exhaustively(numberOfExtensions=1)
        
        assert D["m2*m1"]==D["id_BxA"]
        assert D["m1*m2"]==D["id_AxB"]
        
class AbelianZeroObjectTest(unittest.TestCase):
    def runTest(self):
        D = Diagram(category = AbelianCategory)
        A = Object(D,"A")
        B = Object(D,"B")
        
        Rules = AbelianRules+[ComposeRule,ExistIdentity]
        RM = RuleMaster(D,Rules = Rules, prioritiser = UltimateWeightPriotiser)
        for _ in xrange(20):
            RM.rule()
        
class AbelianKernelTest(unittest.TestCase):
    def runTest(self):
        '''
                     f
        ker f --> A ---> B --> coker f
             \    |\   / |     /
              \   | \0/  |   /
               \  | /0 \ | /
                  C      Z
        
        '''
        D = Diagram(category = AbelianCategory)
        
        A = Object(D,"A")
        B = Object(D,"B")
        f = Morphism(A,B,"f")
        
        C = Object(D,"C")
        g = Morphism(C,A,"g")
        
        zerom = GiveZeroMorphism(C,B)
        Commute(f*g,zerom)
        
        Z = Object(D,"Z")
        h = Morphism(B,Z,"h")
        
        zerom = GiveZeroMorphism(A,Z)
        Commute(h*f,zerom)
        
        Rules = AbelianRules+[ComposeRule,ExistIdentity]
        RM = RuleMaster(D,Rules = Rules, prioritiser = UltimateWeightPriotiser)
        for _ in xrange(20):
            RM.rule(numberOfExtensions=1,verbose = False)
        
        #the kernel has ben created
        assert D["ker_(f)"] is not None
        ker_f = D["ker_(f)"]
        
        #and it has the property that f*iker == 0
        iker = next(m for m in D.Morphisms[ker_f][A] if not isMorphismZero(m))
        assert f*iker==GiveZeroMorphism(ker_f, B)
        
        #and there is a non-trivial morphism g_: C->ker_f
        assert any(not isMorphismZero(m) for m in D.Morphisms[C][ker_f])
        g_ = next(m for m in D.Morphisms[C][ker_f] if not isMorphismZero(m))
        
        #also the cokernel has ben created
        assert D["coker_(f)"] is not None
        coker_f = D["coker_(f)"]
        
        #and it has the property that coker*f == 0
        pcoker_f = next(m for m in D.Morphisms[B][coker_f] if not isMorphismZero(m))
        assert pcoker_f*f==GiveZeroMorphism(A,coker_f)
        
        #and there is a non-trivial morphism h_: coker_f -> Z
        assert any(not isMorphismZero(m) for m in D.Morphisms[coker_f][Z])
        h_ = next(m for m in D.Morphisms[coker_f][Z] if not isMorphismZero(m))
        
        #also, just for fun, ker->coker == 0
        assert pcoker_f*f*iker==GiveZeroMorphism(ker_f,coker_f)

class AbelianExactnessTest(unittest.TestCase):
    def runTest(self):
        D = Diagram(category=AbelianCategory)
        A = Object(D,"A")
        B = Object(D,"B")
        C = Object(D,"C")
        
        f = Morphism(A,B,"f")
        g = Morphism(B,C,"g")
        
        Exact(f,g)
        
        Rules = AbelianRules
        RM = RuleMaster(D,Rules = Rules, prioritiser = UltimateWeightPriotiser)
        for _ in xrange(40):
            RM.rule(numberOfExtensions=1,verbose = False)
        
        pcoker_f = getCokernel(f)
        iker_g = getKernel(g)
        iker_pcoker_f = getKernel(pcoker_f)
        
        ker_g = iker_g.source
        ker_coker_f = iker_pcoker_f.source
        
        psi = next(iterNonZeroMorphisms(ker_coker_f,ker_g))
        assert isIsomorphism(psi)
        #print  reprWithoutZeros(D)