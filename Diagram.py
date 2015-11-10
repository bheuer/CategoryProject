from collections import defaultdict 
from itertools import product
from Morphisms import *
from networkx import DiGraph
from networkx.algorithms.isomorphism  import DiGraphMatcher,generic_edge_match

class Diagram(object):
    def __init__(self):
        self.Objects = []
        self.Morphisms = {}
        self.Graph = DiGraph()
        
        self.UNIVERSE = set([])
        self.Rules = []
        
        self.CommutingComponents = {}
    
    def addObject(self,obj):
        self.Objects.append(obj)
        self.Graph.add_node(obj)
        
        self.addName(obj.name)
        self.Morphisms[obj]=defaultdict(list)
        #self.addMorphi(obj.Identity)
    
    def addMorphi(self,morph):
        target = morph.target
        source = morph.source
        
        if morph in self.Morphisms[source][target]:
            return
        
        self.addName(morph.name)
        self.Morphisms[source][target].append(morph)
        self.Graph.add_edge(source,target,object = morph)
        
        self.CommutingComponents[morph.id()]=morph.id()
    
    def addName(self,name):
        
        if name in self.UNIVERSE:
            raise ValueError,"name {} already given".format(name)
        self.UNIVERSE.add(name)
    
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
    
    def giveName(self):
        i=0
        while "o"+str(i) in self.UNIVERSE:
            i+=1
        return "o"+str(i)
    
    def morphismlist(self):
        return sum((i for i in D.Morphisms.values()),[])
    
    def iterateIsomorphicSubdiags(self,Subgraph,comp):
        #build all subgraphs of G which are isomorphic to Subgraph
        
        structure_matcher = generic_edge_match("object",None,comp) 
        M = DiGraphMatcher(self.Graph,Subgraph,edge_match = structure_matcher)
        for inverseMapping in M.subgraph_isomorphisms_iter():
            #this gives a Mapping of nodes. Now find all combinations of appropriate edges
            Mapping = dict((a,b) for b,a in inverseMapping.iteritems())
            
            def morphi_iterator(presource,pretarget,data):
                source = Mapping[presource]
                target = Mapping[pretarget]
                
                for morphi in self.Morphisms[source][target]:
                    if comp(data,morphi):
                        yield source,target,morphi
                        
            for morphis in product(*[morphi_iterator(s,t,m) for s,t,m in Subgraph.edges(data=True)]):
                H = DiGraph()
                H.add_nodes_from(imag for imag in Mapping.values())
            
                for source,target,morphi in morphis:
                    H.add_edge(source,target,object = morphi)
                yield H,Mapping
            
    
    def print_(self):
        for s in self.Objects:
            for t in self.Morphisms[s]:
                for f in self.Morphisms[s][t]:
                    if isinstance(f,Identity):
                        continue
                    print f
