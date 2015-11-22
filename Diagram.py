from collections import defaultdict 
from networkx.algorithms.isolate import is_isolate
from Morphisms import Morphism
from Homomorphisms import IamTiredOfNetworkxNotHavingAnEdgeObjectGraph
        
class Diagram(object):
    def __init__(self):
        self.Objects = []
        self.Morphisms = {}
        self.Graph = IamTiredOfNetworkxNotHavingAnEdgeObjectGraph()
        
        self.InverseLookUp = {}
        self.UNIVERSE = set([])
        self.Rules = []
        
        self.CommutingComponents = {}
        
        self.MorphismList = []
        
    def addObject(self,obj):
        self.Objects.append(obj)
        self.Graph.add_node(obj,propertyTags = set())
        
        self.addName(obj.name)
        self.Morphisms[obj]=defaultdict(list)
        #self.addMorphi(obj.Identity)
    
    def addMorphi(self,morph):
        target = morph.target
        source = morph.source
        
        if morph in self.Morphisms[source][target]:
            return
        
        self.addName(morph.name)
        
        Morph = Morphism(morph)
        self.Morphisms[source][target].append(Morph)
        self.MorphismList.append(Morph)
        
        edge = self.Graph.add_edge(source,target,morphism = Morph,propertyTags = set())
        self.InverseLookUp[Morph] = edge
        
        self.CommutingComponents[morph.id()]=morph.id()
    
    def addName(self,name):
        
        if name in self.UNIVERSE:
            raise ValueError,"name {} already given".format(name)
        self.UNIVERSE.add(name)
    
    def giveName(self):
        i=0
        while "o"+str(i) in self.UNIVERSE:
            i+=1
        return "o"+str(i)
    
    def unify(self,morph1,morph2):
        '''take two Morphisms and register that they should be considered equal'''
        
        id1 = morph1.id()
        id2 = morph2.id()
        for m,id3 in self.CommutingComponents.items():
            if id3==id2:
                self.CommutingComponents[m]=id1
    
    def commutes(self,morph1,morph2):
        #treats morph1,morph2 as technically different morphisms and asks if they are known to commute
        m_id1 = morph1.id()
        m_id2 = morph2.id()
        if not self.CommutingComponents.has_key(m_id1) or not self.CommutingComponents.has_key(m_id2):
            return False
        return self.CommutingComponents[m_id1]==self.CommutingComponents[m_id2]
    
    def print_(self):
        for s in self.Objects:
            for t in self.Morphisms[s]:
                for f in self.Morphisms[s][t]:
                    print f

def isolatedNodes(diagram):
    for o in diagram.Objects:
        if is_isolate(diagram.Graph,o):
            yield o