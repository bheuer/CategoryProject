from Diagram import Diagram,Object,Morphism,Category
from Property.Property import ObjectProperty, MorphismsProperty

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

AbelianCategory = Category([ZeroObject],[])