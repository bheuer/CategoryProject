from base import Property
from Diagram import Diagram,Object,Morphism

class MorphismsProperty(Property):
    def buildCharDiagram(self,D):
        A = Object(D,"O1")
        B = Object(D,"O2")
        self.morph = Morphism(A,B,"f")
    def __repr__(self):
        str_ = "Morphism Property '{}' for morphism {}".format(self.name,self.homomorphism.edgeMap[self.morph])
        return str_
        
class Epimorphism(MorphismsProperty):
    name = "epimorphism"
    weight = -20
    
class Monomorphism(MorphismsProperty):
    name = "epimorphism"

class ProductProperty(Property):
    name = "product"
    weight = -15
    def buildCharDiagram(self,D):
        A = Object(D,"factor1",)
        B = Object(D,"factor2")
        AxB = Object(D,"product")
        Morphism(AxB,A,"pi1")
        Morphism(AxB,B,"pi2")

class ZeroObject(Property):
    name = "zero"
    def buildCharDiagram(self,D):
        Object(D,"0",)

if __name__ == "__main__":
    D = Diagram()
    A = Object(D,"A")
    B = Object(D,"B")
    AxB = Object(D,"AxB")
    f = Morphism(AxB,A,"f")
    g = Morphism(AxB,B,"g") 
    
    p = ProductProperty(f,g)
    zero = ZeroObject(A)
    epi = Epimorphism(f)
    
    print p
    print zero
    print epi