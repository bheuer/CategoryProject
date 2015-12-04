from collections import defaultdict 
from networkx.algorithms.isolate import is_isolate
from Morphisms import Morphism
from Graph import IamTiredOfNetworkxNotHavingAnEdgeObjectGraph

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
        self.Properties = []
        
    def addObject(self,obj):
        self.Objects.append(obj)
        self.Graph.add_node(obj,propertyTags = set())
        
        self.addName(obj.name)
        self.Morphisms[obj]=defaultdict(list)
        #self.addMorphi(obj.Identity)
    
    def addMorphi(self,morph):
        if not isinstance(morph, Morphism):
            raise ValueError
        
        target = morph.target
        source = morph.source
        
        if morph in self.Morphisms[source][target]:
            return
        
        self.addName(morph.name)
        
        self.Morphisms[source][target].append(morph)
        
        assert morph not in self.MorphismList # inefficient. Just to be sure
        self.MorphismList.append(morph)
        
        edge = self.Graph.add_edge(source,target,morphism = morph,propertyTags = set())
        self.InverseLookUp[morph] = edge
        
        self.CommutingComponents[morph.name]=morph.name
    
    def __getitem__(self,item):
        for i in self.Objects:
            if i.name == item:
                return i
        for i in self.MorphismList:
            if i.name == item:
                return i
        
            
    def addProperty(self,prop):
        self.Properties.append(prop)
    
    def addName(self,name):
        
        if name in self.UNIVERSE:
            raise ValueError,"name {} already given".format(name)
        self.UNIVERSE.add(name)
    
    def giveName(self,mode="o"):
        i=0
        while mode+str(i) in self.UNIVERSE:
            i+=1
        return mode+str(i)
    
    def unify(self,morph1,morph2):
        '''take two Morphisms and register that they should be considered equal'''
        id1 = morph1.name
        id2 = morph2.name
        anchor = self.CommutingComponents[id2]
        newanchor = self.CommutingComponents[id1]
        for m,id3 in self.CommutingComponents.items():
            if id3==anchor:
                self.CommutingComponents[m]=newanchor
    
    def commutes(self,morph1,morph2):
        #treats morph1,morph2 as technically different morphisms and asks if they are known to commute
        m_id1 = morph1.name
        m_id2 = morph2.name
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

    