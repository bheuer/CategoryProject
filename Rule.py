from Property import ProductProperty
from Morphisms import Morphism
from Diagram import Diagram
from Object import Object
from __builtin__ import NotImplementedError
from Homomorphisms import Homomorphism

class ExistProduct(RuleGenerator):
    def CharacteristicDiagram(self,CD):
        self.A = Object(CD,"A")
        self.B = Object(CD,"B")
    
    def conclusion(self):
        AxB = Object(self.CD,"AxB")
        pi1 = Morphism(self.A,AxB,"pi1")
        pi2 = Morphism(self.B,AxB,"pi2")
        ProductProperty(pi1,pi2)

class ProductRule(RuleGenerator):
    def CharacteristicDiagram(self):
        '''
                N
           f  / : \  g
             |  P  |
             | / \ |
              A   B
        '''
        
        CD = Diagram()
        A = Object(CD,"A")
        B = Object(CD,"B")    
        P = Object(CD,"P")
        pi1 = Morphism(A,P)
        pi2 = Morphism(B,P)
        ProductProperty(pi1,pi2)
        
        N = Object(CD,"N")
        Morphism(A,N,"f")
        Morphism(B,N,"g")
    
    def conclusion(self,D):
        phi = Morphism(D["P"],D["N"],"phi")
        Commute(D["f"],D["phi"]*D["pi1"])
        Commute(D["g"],phi*D["pi2"])
    

    

#Commute(D) or Commute(f,g,h)
class Commute(Request):
    def __init__(self,*args):
        if len(args)==1 and isinstance(args[0],Diagram):
            self.data = args[0]
            self.mode = "diagram"
        else:#should be list of morphisms
            self.data = args
            self.mode = "morphisms"    