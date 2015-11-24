from Morphisms import Morphism
from Object import Object
from Property_base import Property
from Diagram import Diagram


class MorphismsProperty(Property):
    def buildCharDiagram(self):
        D = Diagram()
        A = Object(D,"O1")
        B = Object(D,"O2")
        self.morph = Morphism(A,B,"f")
        return D
    def __repr__(self):
        str_ = "Morphism Property '{}' for morphism {}".format(self.name,self.homomorphism.edgeMap[self.morph])
        return str_
        
class Epimorphism(MorphismsProperty):
    name = "epimorphism"

class ProductProperty(Property):
    name = "product"
    def buildCharDiagram(self):
        D = Diagram()
        A = Object(D,"factor1",)
        B = Object(D,"factor2")
        AxB = Object(D,"product")
        Morphism(AxB,A,"pi1")
        Morphism(AxB,B,"pi2")
        return D

class ZeroObject(Property):
    name = "zero"
    def buildCharDiagram(self):
        D = Diagram()
        Object(D,"0",)
        return D

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