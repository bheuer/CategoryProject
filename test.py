from Diagram import *
from Morphisms import *
from Rules import *

import unittest

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
        D.addRule(Commute(g2*f1, h1*g1))
        assert g2*f1==h1*g1
        assert D.commutes(g2*f1, g2*f1)
        assert D.commutes(g2*f1, h1*g1)
    
class SecondCommutativityTestCase(unittest.TestCase):
    def runTest(self):
        D = Diagram()
        
        '''
        
            f1        f2
        A1 ---> A2 ---> A3
        |        |        |
        | g1 //  | g2 //  | g3
        V        V        |
        B1 ---> B2 ---> B3
            h1        h2
        
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
    
        D.addRule(Commute(g2*f1,h1*g1))
        assert g2*f1==h1*g1
        
        assert g3*f2!=h2*g2
        assert g3*f2*f1!=h2*g2*f1
        
        D.addRule(Commute(g3*f2,h2*g2))
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
        
        D.addRule(Commute(g2*f1*f0,h1*g1*f0))
        
        
        assert g2*f1*f0==h1*g1*f0
        assert g2*f1!=h1*g1
        D.addRule(Epim(f0))
        assert g2*f1==h1*g1
        
        D.addRule(Mono(h3))
        assert g3*f2!=h2*g2
        D.addRule(Commute(h3*g3*f2,h3*h2*g2))
        assert g3*f2==h2*g2
        
        assert g3*f2*f1==h2*h1*g1
    
class CyclesTestCase(unittest.TestCase):
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
        
        loop =  f1*g2*h1*g1
        assert loop!=A1.Identity
        D.addRule(Commute(loop,A1.Identity))
        assert loop==A1.Identity

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
    
        D.addRule(IntoProduct(f,pi1,pi2))
        D.addRule(Commute(pi2*f,pi2*g))
        
        assert f!=g
        D.addRule(Commute(pi1*f,pi1*g))
        assert f==g

class RuleTestCase(unittest.TestCase):
    def runTest(self):
        D = Diagram()
        
        A = Object(D,"A")
        B = Object(D,"B")
        P = Object(D,"P")
        V = Object(D,"V")
        
        pi1 = Morphism(P,A,"pi1")
        pi2 = Morphism(P,B,"pi2")
        f = Morphism(V,P,"f")
        
        rule = IntoProduct(f,pi1,pi2)
        D.addRule(rule)
        assert rule.definingData()==[(pi1,pi2),f], rule.definingData()
        
