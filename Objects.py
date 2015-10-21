from Rules import Rule,Commute,IntoProduct
from Morphisms import Object,Morphism
from itertools import product

class UniversalObject(Object):
    pass
    def universalProperty(self):
        raise NotImplementedError

class Product(UniversalObject):
    def __init__(self,Family,name = None):
        if not isinstance(Family,list) and not all(isinstance(member,Object) for member in Family) or len(Family)==0:
            raise ValueError
        
        self.factors = Family
        
        super(UniversalObject,self).__init__(Family[0].diagram,name=name)
        self.projections = [Morphism(self,member) for member in Family]
        
    def universalProperty(self):
        for o in self.object:
            for morphs in product(*(self.diagram.iterBySourceAndTarget(o,member) for member in self.factors)):
                
                #there exists a morphism
                m = Morphism(o,self)
                self.diagram.addMorphi(m)
                
                #such that the diagram commutes
                for morph,proj in zip(morphs,self.projections):
                    yield Commute(proj*m,morph)
                
                #and it is unique
                yield IntoProduct(o,*self.projections)