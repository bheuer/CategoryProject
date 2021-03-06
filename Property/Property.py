from base import Property
from Diagram import Diagram,Object,Morphism,Commute
from Diagram.Morphisms import Identity, getIdentity
from base import PropertyTag

class MorphismsProperty(Property):
    def __init__(self,*args):
        Property.__init__(self,*args)
        self.definingMorphism = self.homomorphism.get_edge_image(self.morph)
    def buildCharDiagram(self,D):
        A = Object(D,"O1")
        B = Object(D,"O2")
        self.morph = Morphism(A,B,"f")
    def __repr__(self):
        str_ = "Morphism Property '{}' for morphism {}".format(self.name,self.homomorphism.get_edge_image(self.morph))
        return str_

class ObjectProperty(Property):
    def buildCharDiagram(self,D):
        self.X=Object(D,"X")
    def __repr__(self):
        str_ = "Property '{}' for object {}".format(self.name,self.homomorphism[self.X].name)
        return str_ 

class Epimorphism(MorphismsProperty):
    name = "epimorphism"
    weight = -20
    
class Monomorphism(MorphismsProperty):
    name = "monomorphism"
    weight = -20

class Isomorphism(MorphismsProperty):
    name = "isomorphism"
    weight = -20
        
class Projective(ObjectProperty):
    name = "ProjectiveObject"

class Injective(ObjectProperty):
    name = "InjectiveObject"

class ProductProperty(Property):
    name = "product"
    weight = -15
    def buildCharDiagram(self,D):
        A = Object(D,"factor1")
        B = Object(D,"factor2")
        AxB = Object(D,"product")
        Morphism(AxB,A,"pi1")
        Morphism(AxB,B,"pi2")

class CoProductProperty(Property):
    name = "coproduct"
    weight = -15
    def buildCharDiagram(self,D):
        A = Object(D,"factor1")
        B = Object(D,"factor2")
        AxB = Object(D,"product")
        Morphism(A,AxB,"i1")
        Morphism(B,AxB,"i2")


class FibreProductProperty(Property):
    name = "fibre product"
    weight = -15
    def buildCharDiagram(self,D):
        A = Object(D,"factor1")
        B = Object(D,"factor2")
        AxB = Object(D,"product")
        C = Object(D, "base")
        pi1 = Morphism(AxB,A,"pi_1")
        pi2 = Morphism(AxB,B,"pi_2")
        f = Morphism(A,C,"f")
        g = Morphism(B,C,"g")
        #Commute(f*pi1,g*pi2) #not necessary

class IsNot:#Pseudoproperty Generator like Non(ZeroMorphism)
    name = "isnot"
    def __init__(self,notprop,f):
        assert isinstance(f,Morphism) or isinstance(f,Object)
        self.obj = f
        self.notprop = notprop
        diagram = f.diagram
        diagram.addProperty(self)
        
        propTag = PropertyTag(self,f.name,id(self))
        if isinstance(f,Object):
            diagram.Graph.node[f]["propertyTags"].append(propTag)
            diagram.EquivalenceGraph.node[f]["propertyTags"].append(propTag)
        elif isinstance(f,Morphism):
            diagram.appendPropertyTag(f,propTag)
            
def SetIsomorphism(m):
    minverse = Morphism(m.target,m.source)
    
    Commute(minverse*m,getIdentity(m.source))
    Commute(m*minverse,getIdentity(m.target))
    Isomorphism(m)
    Epimorphism(m)
    Monomorphism(m)