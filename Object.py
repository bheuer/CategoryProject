
class Object(object):
    def __init__(self,diagram = None,name = None):
        self.diagram = diagram
        self.name = name
        
        self.name not in self.diagram.UNIVERSE
        
        if name is None:
            self.name = diagram.giveName()
        
        self.diagram.addObject(self)
        
    def __repr__(self):
        return self.name
    def __hash__(self):
        return self.name.__hash__()