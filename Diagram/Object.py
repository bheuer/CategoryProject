
class Object(object):
    def __init__(self,diagram = None,name = None):
        self.diagram = diagram
        self.name = name
        
        assert self.name not in self.diagram.UNIVERSE
        
        if name is None:
            self.name = diagram.giveName()
        self.hash_value = self.name.__hash__()
        
        self.diagram.addObject(self)
        
    def __repr__(self):
        return self.name
    def __hash__(self):
        return self.hash_value
    
    def Identity(self):
        label = "id_"+self.name
        morph = self.diagram[label]
        return morph