from collections import defaultdict 
from networkx.algorithms.isolate import is_isolate
from Morphisms import Morphism, AbstractMorphism, AtomicMorphism
from Homomorphisms import IamTiredOfNetworkxNotHavingAnEdgeObjectGraph,Homomorphism

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
    
    def __getitem__(self,item):
        for i in self.Objects:
            if i.name == item:
                return i
        for i in self.MorphismList:
            if len(i.id())==1 and i.id()[0]==item:
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

class Commute:
    def __init__(self,*args):
        assert len(args)>0 and all(isinstance(i,Morphism) for i in args)
        self.MorphiList = args
        diagram = args[0].diagram
        diagram.addProperty(self)
        morph0 = self.MorphiList[0]
        for i in xrange(1,len(self.MorphiList)):
            morph = self.MorphiList[i]
            assert morph // morph0
            diagram.unify(morph0,morph)
    
    def push_forward(self,hom):
        assert isinstance(hom, Homomorphism)
        return Commute(*(hom.get_edge_image(morph) for morph in self.MorphiList))
    
    def __repr__(self):
        str_ = "Property 'commute' for the following morphisms:\n"
        for morph in self.MorphiList:
            str_+="{}\n".format(morph)
        return str_
            
        
        