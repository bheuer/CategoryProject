from Diagram import *
from Diagram.Morphisms import AbstractMorphism,Identity
from Homomorphism import HomomorphismIterator
from Property import *
from Property.base import PropertyTag
from Rule import RuleMaster
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
        Commute(g2*f1, h1*g1)
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
        
        D.addRule(Commute(g2*f1*f0,h1*g1*f0))
        
        
        assert g2*f1*f0==h1*g1*f0
        assert g2*f1!=h1*g1
        Epimorphism(f0)
        assert g2*f1==h1*g1
        
        Monomorphism(h3)
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
        Commute(loop,A1.Identity)
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
    
        ProductProperty(pi1,pi2)
        Commute(pi2*f,pi2*g)
        
        assert f!=g
        Commute(pi1*f,pi1*g)
        assert f==g
        
if __name__ == "__main__":
    def test1():
        '''
        D1
        
           f      g
        A ---> B ---> C
                
                
        D2        
               X2 
               |  F2
               |  
           F   V  G
        X ---> Y ---> Z
         <---  |    
          G2   | id
               Y
           
        '''
        
        D1 = Diagram()
        D2 = Diagram()
        
        A = Object(D1,"A")
        B = Object(D1,"B")
        C = Object(D1,"C")
        Morphism(A,B,"f")
        Morphism(B,C,"g")
        
            
        X = Object(D2,"X")
        Y = Object(D2,"Y")
        Z = Object(D2,"Z")
        X2 = Object(D2,"X2")
        
        Morphism(X,Y,"F")
        Morphism(Y,Z,"G")
        Morphism(Y,Y,"id")
        Morphism(X2,Y,"F2")
        Morphism(Y,X,"G2")
        
        homiter = HomomorphismIterator(D1,D2)
        for hom in homiter:
            print hom
            
    def test2():
            '''
            D1
            
               f      
            A ---> B
             <\    / g
           h  \   /     
               C<-  
                 
            D2        
                   
               F      
            X ---> Y
             <\    / G
           H  \   /     
               Z<-
               |
               | id
               Z
                 
            '''
            
            D1 = Diagram()
            D2 = Diagram()
            
            A = Object(D1,"A")
            B = Object(D1,"B")
            C = Object(D1,"C")
            Morphism(A,B,"f")
            Morphism(B,C,"g")
            Morphism(C,A,"h")
            
                
            X = Object(D2,"X")
            Y = Object(D2,"Y")
            Z = Object(D2,"Z")
            
            Morphism(X,Y,"F")
            Morphism(Y,Z,"G")
            Morphism(Z,X,"H")
            Morphism(Z,Z,"idZ")
            
            homiter = HomomorphismIterator(D1,D2)
            for hom in homiter:
                print hom
        
    def test3():
            '''
            D1
            
               f      
            A ---> B
               
            
            D2        
               
               F     
            X --->Y
          G |
            V
            Z
                 
            '''
            
            D1 = Diagram()
            D2 = Diagram()
            
            A = Object(D1,"A")
            B = Object(D1,"B")
            f = Morphism(A,B,"f")
            
                
            X = Object(D2,"X")
            Y = Object(D2,"Y")
            Z = Object(D2,"Z")
            
            F = Morphism(X,Y,"F")
            G = Morphism(X,Z,"G")
            
            homiter = HomomorphismIterator(D1,D2)
            c = 0
            for hom in homiter:
                print hom
                c+=1
            assert c==2
            
            print "declare Epimorphisms"
            Epimorphism(f)
            Epimorphism(F)
            print D1.InverseLookUp[f]
            print D2.InverseLookUp[F]
            
            homiter = HomomorphismIterator(D1,D2)
            c=0
            for hom in homiter:
                print hom
                c+=1
            assert c==1
            
            #test Properties hashable and hash only checks function, not id
            p = PropertyTag(1,2,3)
            q = PropertyTag(1,2,4)
            P = set([p])
            Q = set([q])
            assert P.issubset(Q)
            
    def test4():
        
        D = Diagram()
        A = Object(D,"A")
        Object(D,"B")
        B = D["B"]
        
        RM = RuleMaster(D)
        for i in xrange(5):
            print "next implementation of a rule"
            RM()
            print D.Properties
    print test4()