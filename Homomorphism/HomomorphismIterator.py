from Homomorphism.base import Homomorphism
from networkx.algorithms.components.weakly_connected import weakly_connected_components
from Diagram.Commute import Commute,Distinct
from Rule.abelianProperty import isMorphismZero, GiveZeroMorphism,\
    AbelianCategory, isIsomorphism, ZeroObject, ZeroMorphism
from Diagram.Morphisms import Identity
from Property.Property import getIdentity, IsNot, Isomorphism

class HomomorphismIterator:
    def __init__(self,D1,D2):
        self.D1 = D1
        self.D2 = D2
        self.G1 = D1.Graph
        self.G2 = D2.EquivalenceGraph
    
    def initializeHomomorphism(self):
        if self.D2.category == AbelianCategory:
            self.hom = AbelianHomomorphism(self.D1,self.D2)
        else:
            self.hom = BetterHomomorphism(self.D1,self.D2)
            
    
    def initialize(self):
       
        self.initializeHomomorphism()
        #for each connected component give one arbitrary representative
        self.componentRepresentatives = []
        for G in weakly_connected_components(self.G1):
            #find out which node has the least matching images
            #this should be a good node to start with and then extend homomorphism from there
            
            nodes = []
            for n in G:
                nodes.append((sum(1 for n2 in self.G2 if self.doNodesMatch(n, n2)),n))
            optimalNode = min(nodes)[1]
            
            self.componentRepresentatives.append(optimalNode)
        
    def __iter__(self):
        self.initialize()
        for _ in self.matchComponents():
            #global PropertyCheck
            if self.globalPropertyCheck():
                yield self.hom.copy()
    
    def globalPropertyCheck(self):
        for prop in self.D1.Properties:
            if isinstance(prop,Commute):
                ECs =  [self.hom.get_edge_image(morph) for morph in prop.MorphiList]
                if not all(i==ECs[0] for i in ECs):
                    return False
                
            elif isinstance(prop, Distinct):
                #check that no two morphisms of the indicated morphis are mapped to the same image
                ECs =  [self.hom.get_edge_image(morph) for morph in prop.MorphiList]
                for e in ECs:
                    if ECs.count(e)>1:
                        return False
            elif isinstance(prop, IsNot):
                continue
            else:
                #check whether the locally matched properties glue together to match to
                #a global property
                
                matched = False
                
                for prop2 in self.D2.Properties:
                    if prop2.name == prop.name:
                        if self.hom*prop.homomorphism == self.D2.CommutativityQuotient*prop2.homomorphism:
                            
                            #                     hom
                            #       (Commutat.) ------->  Commutat.
                            #       (Quotient )           Quotient
                            #            A                   A
                            #            |         //        |
                            #        topolog.             topolog.
                            #        Diagram              Diagram
                            #               A             A
                            #                \           /
                            #                 char. Diag.          
                            #                 of Property          
                            
                            matched = True
                            break
                
                if not matched:
                    return False
        return True
    
    def doNodesMatch(self,node1,node2):
        P1 = self.G1.node[node1]["propertyTags"]
        P2 = self.G2.node[node2]["propertyTags"]
        for propTag in P1:
            prop = propTag.prop
            if isinstance(prop, IsNot):
                notprop = prop.notprop
                if notprop is ZeroObject:
                    if node2.name =="0":
                        return False
                else:
                    assert False,notprop
            else:
                if propTag not in P2: # P1 subset P2
                    return False
        return True
            
    def doEdgesMatch(self,edge1,edge2):
        P1 = edge1["propertyTags"]
        P2 = edge2["propertyTags"]
        
        for propTag in P1:
            prop = propTag.prop
            if isinstance(prop, IsNot):
                notprop = prop.notprop
                morph = edge2["morphism"]
                #check that morphism is not known to be zero
                if notprop is ZeroMorphism:
                    if isMorphismZero(morph):
                        return False
                
                elif notprop is Isomorphism:
                    #check that morphism is not known to be zero
                    if isIsomorphism(morph):
                        return False
                else:
                    assert False,notprop
            else:
                if propTag not in P2: # P1 subset P2
                    return False
        return True
    
    def matchComponents(self,index = 0):
        if index==len(self.componentRepresentatives):
            yield
            return
        
        node1 = self.componentRepresentatives[index]
        for node2 in self.G2.nodes():
            if not self.doNodesMatch(node1,node2):
                continue
            self.hom.nodeMap[node1]=node2
            for _ in self.matchNode(node1):
                for _ in self.matchComponents(index+1):
                    yield None
            
            self.hom.nodeMap[node1]=None
    
    def matchNode(self,node):
        
        out_edges = [e for e in self.G1.out_edges(node) if len(e["morphism"].Composition)==1]
        in_edges = [e for e in self.G1.in_edges(node) if len(e["morphism"].Composition)==1]
        
        neighbourlist = []
        for e in out_edges:
            n = e.target
            if n not in neighbourlist and self.hom.nodeMap.get(n) is None:
                neighbourlist.append(n)
        for e in in_edges:
            n = e.source
            if n not in neighbourlist and self.hom.nodeMap.get(n) is None:
                neighbourlist.append(n)
        
        for _ in self.matchNeighbourhood(out_edges,mode = "out"):
            for _ in self.matchNeighbourhood(in_edges,mode = "in"):
                for _ in self.matchList(neighbourlist):
                    yield None
    
    def matchList(self,neighbourlist,index=0):
        if len(neighbourlist)==index:
            yield None
            return
        for _ in self.matchNode(neighbourlist[index]):
            for _ in self.matchList(neighbourlist,index+1):
                yield None
            
    
    def matchNeighbourhood(self,edges,index=0,mode="out"):
        if index==len(edges):
            yield None
            return
        
        edge = edges[index]
        node,neighbour = edge.source,edge.target
        if mode=="in":
            node,neighbour = neighbour,node
        
        node2 = self.hom.nodeMap[node]
        
        morphi = edge["morphism"]
        
        
        neighbour2 = self.hom.nodeMap.get(neighbour)
        if neighbour2 is not None: #node assigned before
            if self.hom.edgeMap.get(morphi) is None: #but edge not: find morphism that works
                if mode=="out":
                    iter_ = self.G2.iterate_edges(node2,neighbour2)
                elif mode=="in":
                    iter_ = self.G2.iterate_edges(neighbour2,node2)
                for edge2 in iter_:
                    if self.doEdgesMatch(edge, edge2):
                        morphi2 = edge2["morphism"]
                        self.hom.edgeMap[morphi] = morphi2
                        for _ in self.matchNeighbourhood(edges, index+1, mode):
                            yield None
                        self.hom.edgeMap[morphi] = None
            
            else: # edge defined already
                for _ in self.matchNeighbourhood(edges, index+1, mode):
                    yield None
            return
        
        #new edge

        if mode == "in":
            potential_images = self.G2.in_edges(node2)
        if mode == "out":
            potential_images = self.G2.out_edges(node2)
        
        for edge2 in potential_images:
            inneighbour2,outneighbour2 = edge2.source,edge2.target
            morphi2 = edge2["morphism"]
            neighbour2 = (outneighbour2 if mode=="out" else inneighbour2)
            
            if not self.doNodesMatch(neighbour, neighbour2):
                continue
            if not self.doEdgesMatch(edge, edge2):
                continue
            
            self.hom.edgeMap[morphi] = morphi2
            self.hom.nodeMap[neighbour] = neighbour2
            
            for _ in self.matchNeighbourhood(edges, index+1, mode):
                yield None
    
            self.hom.edgeMap[morphi] = None
            self.hom.nodeMap[neighbour] = None

class BetterHomomorphism(Homomorphism):
    def get_edge_image(self,item):
        res = Homomorphism.get_edge_image(self,item)
        if res is not None:
            return res
        if isinstance(item,Identity):
            return getIdentity(self.edgeMap[item.source])
                
class AbelianHomomorphism(Homomorphism):
    def get_edge_image(self,item):
        if self.edgeMap.has_key(item):
            return self.edgeMap[item]
        elif len(item.Composition)>1:
            iterator = item.iterComposingMorphisms()
            morphi = self.edgeMap[next(iterator)]
            
            if isMorphismZero(morphi):
                return  GiveZeroMorphism(self.nodeMap[item.source],self.nodeMap[item.target]).equivalenceClass()
            
            for atomic in iterator: #inefficient #it just got even more inefficient
                atomicimage = self.edgeMap[atomic]
                if isMorphismZero(atomicimage):
                    return GiveZeroMorphism(self.nodeMap[item.source],self.nodeMap[item.target]).equivalenceClass()
                
                morphi = morphi.compose(atomicimage)
            return morphi
        elif isinstance(item,Identity):
            return getIdentity(self.edgeMap[item.source])