from Homomorphism import Homomorphism
from Diagram import Diagram

#abstract base class
class RuleGenerator:
    def __init__(self):
        self.CD = Diagram()
        self.Extension = Diagram()
        
        self.CharacteristicDiagram(self.CD)
        self.CharacteristicDiagram(self.Extension)
        
        self.conclude(self.Extension)
        
    def CharacteristicDiagram(self,CD):
        raise NotImplementedError
    def conclude(self,D):
        raise NotImplementedError  
    
    def __call__(self):
        rule = Rule(self.CD,self.Extension,name = self.__class__.__name__)
        for o in self.CD.Objects:
            rule.set_node_image(o,self.Extension[o.name])
        for e in self.CD.MorphismList:
            print e
            rule.set_edge_image(e,self.Extension[e.name])
        rule.postprocess()
        return rule

#abstract base class
class Rule(Homomorphism):
    def __init__(self,D1,D2,name):
        Homomorphism.__init__(self,D1,D2)
        self.partialInverse = Homomorphism(D2,D1)
        self.CD = D1
        self.name = name
        
    def set_node_image(self,node,image):
        self.partialInverse.set_node_image(image,node)
        Homomorphism.set_node_image(self,node,image)
        
    def set_edge_image(self,edge,image):
        self.partialInverse.set_edge_image(image,edge)
        Homomorphism.set_edge_image(self,edge,image)
    
    def postprocess(self):
        self.newObjects = []
        for o in self.D2.Objects:
            if not self.partialInverse.is_defined_on_node(o):
                self.newObjects.append(o)
        
        self.newMorphisms = []
        for e in self.D2.MorphismList:
            if not self.partialInverse.is_defined_on_edge(e):
                self.newMorphisms.append(e)
        
        self.newProperties = self.D2.Properties[len(self.D1.Properties):]
        
        
        