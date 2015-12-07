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
        
        zero = GiveZeroMorphism(A,B)
        Commute(zero,image)

def GiveZeroMorphism(A,B):
    '''
    cerfully creates the zero morphism
    defines the corresponding maps A->0 and 0->B
    and A->0->B only if not defined before, otherwise
    takes those (any) that the diagram knows already
    '''
    
    assert A.diagram == B.diagram
    D = A.diagram
    zero = D["0"]
    
    if D.Morphisms[A][zero]:
        f0 = D.Morphisms[A][zero][0]
    else:
        f0 = Morphism(A,zero)
        
    if D.Morphisms[zero][B]:
        g0 = D.Morphisms[zero][B][0]
    else:
        g0 = Morphism(zero,B)
    
    return g0*f0

def SetEqualZero(f):
    zero = GiveZeroMorphism(f.source, f.target)
    Commute(f,zero)

class Kernel(Property):
    name = "kernel"
    weight = -15
    def buildCharDiagram(self,D):
        A = Object(D,"A",)
        B = Object(D,"B")
        K = Object(D,"kernel")
        Morphism(A,B,"f")
        Morphism(K,A,"ker_f")

class CoKernel(Property):
    name = "cokernel"
    weight = -15
    def buildCharDiagram(self,D):
        A = Object(D,"A",)
        B = Object(D,"B")
        C = Object(D,"cokernel")
        Morphism(A,B,"f")
        Morphism(B,C,"coker_f")

class Exact(Property):
    name = "exact"
    weight = -40
    def buildCharDiagram(self,D):
        A = Object(D,"A",)
        B = Object(D,"B")
        C = Object(D,"C")
        Morphism(A,B,"f")
        Morphism(B,C,"g")
     
class NonZeroMorphism:#Pseudoproperty like "Distinct"
    name = "nonzeromorphism"
    def __init__(self,f):
        assert isinstance(f,Morphism)
        self.morph = f
        diagram = f.diagram
        diagram.addProperty(self)
        
class NonZeroObject:
    name = "nonzeromorphism"
    def __init__(self,o):
        assert isinstance(o,Object)
        self.obj = o
        diagram = o.diagram
        diagram.addProperty(self)

def isMorphismZero(m):
    A = m.source
    B = m.target
    if isinstance(A,ZeroObject) or isinstance(B,ZeroObject):
        return True
    
    D = m.diagram
    zero = D["0"]
    
    if isinstance(m,Morphism):
        m = m.equivalenceClass()
    
    if not D.Morphisms[A][zero]:
        return False
    f0 = D.Morphisms[A][zero][0]
    
    if not D.Morphisms[zero][B]:
        return False
    g0 = D.Morphisms[zero][B][0]
    
    if (g0*f0)==m.representative:
        return True
    
    for p in m.diagram.EquivalenceGraph.InverseLookUp[m]["propertyTags"]:
        if p.prop_name == "zeromorphism":
            return True
    return False

AbelianCategory = Category([ZeroObject],[],"abelian")