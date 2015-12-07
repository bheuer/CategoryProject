from Diagram import Diagram,Object,Morphism,Category
from Property import ObjectProperty, MorphismsProperty,Property
from Diagram.Commute import Commute


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
    def push_forward(self, hom):
        D = hom.D2
    
        m = self.definingMorphism
        image = hom.get_edge_image(m)
        
        A = image.source
        B = image.target
        
        zero = D["0"]
        if D.Morphisms[A][zero]:
            f0 = D.Morphisms[A][zero][0]
        else:
            f0 = Morphism(A,zero)
        if D.Morphisms[zero][B]:
            g0 = D.Morphisms[zero][B][0]
        else:
            g0 = Morphism(zero,B)
        Commute(g0*f0,image)
            
        
        
        
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