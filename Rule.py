from Property import ProductProperty
from Morphisms import Morphism
from Diagram import Diagram,Commute
from Object import Object
from __builtin__ import NotImplementedError
from Homomorphisms import Homomorphism
from Rule_base import RuleGenerator

class ExistProduct(RuleGenerator):
    def CharacteristicDiagram(self,CD):
        self.A = Object(CD,"A")
        self.B = Object(CD,"B")
    
    def conclude(self,CD):
        A = CD["A"]
        B = CD["B"]
        AxB = Object(CD,"AxB")
        pi1 = Morphism(AxB,A,"pi1")
        pi2 = Morphism(AxB,B,"pi2")
        ProductProperty(pi1,pi2)

class ProductRule(RuleGenerator):
    def CharacteristicDiagram(self,CD):
        '''
                N
           f  / : \  g
             |  P  |
             | / \ |
              A   B
        '''
        
        A = Object(CD,"A")
        B = Object(CD,"B")    
        P = Object(CD,"P")
        pi1 = Morphism(P,A,"pi1")
        pi2 = Morphism(P,B,"pi2")
        ProductProperty(pi1,pi2)
        
        N = Object(CD,"N")
        Morphism(N,A,"f")
        Morphism(N,B,"g")
    
    def conclude(self,D):
        phi = Morphism(D["N"],D["P"],"phi")
        Commute(D["f"],D["pi1"]*phi)
        Commute(D["g"],D["pi2"]*phi)    