from Diagram import Diagram,Object,Morphism,Category
from Property import ObjectProperty, MorphismsProperty,Property


class InitialObject(ObjectProperty):
    name = "Initial"
    weight = -50

class FinalObject(ObjectProperty):
    name = "Final"
    weight = -50

class ZeroObject(Object):
    def __init__(self,diagram):
        Object.__init__(self,diagram,"0")
        InitialObject(self)
        FinalObject(self)
    def __repr__(self):
        return self.name
    def __hash__(self):
        return self.name.__hash__()

class ZeroMorphism(MorphismsProperty):
    name = "zeromorphism"
    weight = 0

class Kernel(Property):
    name = "kernel"
    weight = -15
    def buildCharDiagram(self,D):
        A = Object(D,"A",)
        B = Object(D,"B")
        K = Object(D,"kernel")
        Morphism(A,B,"f")
        Morphism(K,A,"ker_f")
        
class NonZeroMorphism:#Pseudoproperty like "Distinct"
    def __init__(self,f):
        assert isinstance(f,Morphism)
        self.morph = f
        diagram = f.diagram
        diagram.addProperty(self)

AbelianCategory = Category([ZeroObject],[])