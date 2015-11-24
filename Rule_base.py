from Homomorphisms import Homomorphism
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
    def conclude(self):
        raise NotImplementedError  
    
    def __call__(self):
        rule = Rule(self.CD,self.Extension)
        for o in self.CD.Objects:
            rule.set_node_image(o,self.Extensions[o.name])
        for e in self.CD.MorphismList:
            rule.set_edge_image(e,self.Extensions[e.name])
        return rule

#abstract base class
class Rule(Homomorphism):
    def __init__(self,D1,D2):
        Homomorphism.__init__(self,D1,D2)
        self.partialInverse = Homomorphism(D2,D1)
    
    def set_node_image(self,node,image):
        self.partialInverse.set_node_image(image,node)
        Homomorphism.set_node_image(node,image)
        
    def set_edge_image(self,edge,image):
        self.partialInverse.set_edge_image(image,edge)
        Homomorphism.set_edge_image(edge,image)
    
    def preprocess(self):
        self.newNodes = []
        for o in self.D2.Objects:
            if not self.partialInverse.is_defined_on_node(o):
                self.newNodes.append(o)
        
        self.newEdges = []
        for e in self.D2.MorphismList:
            if not self.partialInverse.is_defined_on_edge(e):
                self.newMorphisms.append(e)
        
        self.newProperties = self.D2.Properties[len(self.D1.Properties)]
        
        
        