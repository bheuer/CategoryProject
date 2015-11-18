from Homomorphisms import Homomorphism
from networkx.classes.function import all_neighbors
from networkx.algorithms.components.weakly_connected import weakly_connected_components
from Diagram import Diagram,Morphism
from Object import Object

class HomomorphismIterator:
    def __init__(self,D1,D2):
        self.D1 = D1
        self.D2 = D2
        self.G1 = D1.Graph
        self.G2 = D2.Graph
    
    def initialize(self):
        self.hom = Homomorphism(self.D1,self.D2)
        
        #for each connected component give one arbitrary representative
        self.componentRepresentatives = []
        for G in weakly_connected_components(self.G1):
            self.componentRepresentatives.append(G.pop())
        
    def __call__(self):
        self.initialize()
        for _ in self.matchComponents():
            yield self.hom.copy()
    
    def doNodesMatch(self,node1,node2):
        P1 = self.G1.node[node1]["propertyTags"]
        P2 = self.G2.node[node2]["propertyTags"]
        return P1.issubset(P2)
            
    def doEdgesMatch(self,edge1,edge2):
        P1 = edge1["propertyTags"]
        P2 = edge2["propertyTags"]
        return P1.issubset(P2)
    
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
        neighbourlist = [n for n in all_neighbors(self.G1,node) if self.hom.nodeMap.get(n) is None]
        for _ in self.matchNeighbourhood(list(self.G1.out_edges(node)),mode = "out"):
            for _ in self.matchNeighbourhood(list(self.G1.in_edges(node)),mode = "in"):
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
        properties = edge["propertyTags"]
        
        
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
    