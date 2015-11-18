from collections import defaultdict 
from itertools import product
from networkx import MultiDiGraph
from networkx.algorithms.isomorphism  import DiGraphMatcher,generic_edge_match
from networkx.algorithms.isolate import is_isolate
from Morphisms import Morphism

class Edge:
    def __init__(self,node1,node2,key,data):
        self.source = node1
        self.target = node2
        self.data = data
        self.key = key
    def __getitem__(self,datakey):
        return self.data[datakey]
    def __repr__(self):
        #for debugging purposes
        str_ = "".join("{} : {}\n".format(key,value) for key,value in self.data.items())
        return "Edge {} -> {} with data sets:\n".format(self.source,self.target)+str_
    
class IamTiredOfNetworkxNotHavingAnEdgeObjectGraph(MultiDiGraph):
    def __init__(self,*args):
        super(IamTiredOfNetworkxNotHavingAnEdgeObjectGraph,self).__init__(args)
        self.keycounter = 0
    
    def add_edge(self,node1,node2,**kwargs):# inefficient but nobody cares and it's convenient
        e=Edge(node1,node2,self.keycounter,kwargs)
        MultiDiGraph.add_edge(self,node1,node2,object = e,key = self.keycounter)
        self.keycounter+=1
        return e
    
    def out_edges(self,node):
        for _,_,data in MultiDiGraph.out_edges(self,node,data=True):
            yield data["object"]
    
    def in_edges(self,node):
        for _,_,data in MultiDiGraph.in_edges(self,node,data=True):#necessary because for out we can specify data="object", for in we can't
            yield data["object"]
    
    def iterate_edges(self,node1,node2):
        dic = self[node1]
        if dic.has_key(node2):
            for K in dic[node2].values():
                yield K["object"]
        
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
                H = MultiDiGraph()
                H.add_nodes_from(imag for imag in Mapping.values())
            
                for source,target,morphi in morphis:
                    H.add_edge(source,target,object = morphi)
                yield H,Mapping
    
    def print_(self):
        for s in self.Objects:
            for t in self.Morphisms[s]:
                for f in self.Morphisms[s][t]:
                    print f

def isolatedNodes(diagram):
    for o in diagram.Objects:
        if is_isolate(diagram.Graph,o):
            yield o
    