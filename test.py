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
    ProductRuleUnique
from Rule.Compose import ComposeRule
from Rule.abelian import AbelianCategory
from Rule.abelianRules import abelianRules

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
        
        RM = RuleMaster(D,prioritiser = UltimateWeightPriotiser)
        RM.rule_exhaustively(numberOfExtensions=2)
        
        assert D["m2*m1"]==D["id_BxA"]
        assert D["m1*m2"]==D["id_AxB"]
        
class AbelianTest(unittest.TestCase):
    def runTest(self):
        D = Diagram(category = AbelianCategory)
        A = Object(D,"A")
        B = Object(D,"B")
        
        Rules = abelianRules+[ComposeRule,ExistIdentity]
        RM = RuleMaster(D,Rules = Rules, prioritiser = UltimateWeightPriotiser)
        RM.rule_exhaustively(verbose = True)
        print D.Objects
        D.printCommutativity()
        
