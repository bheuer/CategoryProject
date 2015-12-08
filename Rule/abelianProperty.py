from Diagram import Diagram,Object,Morphism,Category
from Property import ObjectProperty, MorphismsProperty,Property
from Diagram.Commute import Commute
from Diagram.Diagram import iscontainedin,GiveZeroMorphism

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
        Morphism(K,A,"iker_f")
        
class CoKernel(Property):
    name = "cokernel"
    weight = -15
    def buildCharDiagram(self,D):
        A = Object(D,"A",)
        B = Object(D,"B")
        coker_f = Object(D,"coker_f")
        Morphism(A,B,"f")
        Morphism(B,coker_f,"pcoker_f")

class Exactness(Property):
    name = "exact"
    weight = -40
    def buildCharDiagram(self,D):
        A = Object(D,"A",)
        B = Object(D,"B")
        C = Object(D,"C")
        Morphism(A,B,"f")
        Morphism(B,C,"g")

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

def isIsomorphism(m):
    if isinstance(m,Morphism):
        m = m.equivalenceClass()
    for p in m.diagram.EquivalenceGraph.InverseLookUp[m]["propertyTags"]:
        if p.prop_name == "isomorphism":
            return True
    return False

def Exact(f,g):
    SetEqualZero(g*f)
    return Exactness(f,g)

def reprWithoutZeros(D):
    str_ = "Diagram with the following data"
    str_+= "| Objects:\n| "
    str_+="\n| ".join(str(o) for o in D.Objects)
    str_+="\n\n| Morphisms by Commutativity class:\n| "
    printed = []
    for s in D.MorphismList:
        quot = s.equivalenceClass()
        if isMorphismZero(quot):
            continue
        if iscontainedin(quot, printed):
            continue
        
        str_+="\n| "+str(quot)
        printed.append(quot)
    return str_

def getCokernel(morph):
    D = morph.diagram
    eq = morph.equivalenceClass()
    for proptag in D.EquivalenceGraph.InverseLookUp[eq]["propertyTags"]:
        if proptag.prop_name == "cokernel":
            if proptag.function=="f":
                hom = proptag.prop.homomorphism
                CD = hom.D1
                pcoker_f = CD["pcoker_f"]
                return proptag.prop.homomorphism.get_edge_image(pcoker_f)

def getKernel(morph):
    D = morph.diagram
    eq = morph.equivalenceClass()
    for proptag in D.EquivalenceGraph.InverseLookUp[eq]["propertyTags"]:
        if proptag.prop_name == "kernel":
            if proptag.function=="f":
                hom = proptag.prop.homomorphism
                CD = hom.D1
                iker_f = CD["iker_f"]
                return proptag.prop.homomorphism.get_edge_image(iker_f)

def iterNonZeroMorphisms(A,B):
    assert A.diagram==B.diagram
    D = A.diagram
    for m in D.Morphisms[A][B]:
        if not isMorphismZero(m):
            yield m

AbelianCategory = Category([ZeroObject],[],"abelian")