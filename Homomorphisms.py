from itertools import product
from copy import deepcopy 
from collections import defaultdict

class Homomorphism:
    def __init__(self,D1,D2,nodeMap={},edgeMap={}):
        self.D1 = D1
        self.D2 = D2
        self.nodeMap = nodeMap
        self.edgeMap = edgeMap
    
    def __getitem__(self,ind):
        return self.nodeMap[ind]
    def __setitem__(self,ind,val):
        self.nodeMap[ind] = val
        
    def set_node_image(self,node,image):
        self.nodeMap[node]=image
    def set_edge_image(self,edge,image):
        self.edgeMap[edge]=image
        
    def copy(self):
        return Homomorphism(self.D1,self.D2,deepcopy(self.nodeMap),deepcopy(self.edgeMap))
    
    def definingData(self):
        return (self.nodeMap,self.edgeMap)    
    
    def extend_node(self,node,image):
        if self.nodeMap.get(node) is None:
            self[node] = image
        else:
            if not self[node]==image:
                raise ValueError,"incoherent init node: node image has been assigned two different values"
    
    def extend_edge(self,edge,image):
        if self.edgeMap.get(edge) is None:
            self.extend_node(edge.source,image.source)
            self.extend_node(edge.target,image.target)
            self.set_edge_image(edge,image)
        else: 
            if not self.edgeMap[edge]==image:
                raise ValueError,"incoherent init edge: edge image has been assigned two different values"
    def __repr__(self):
        str_ = ""
        str_+= "Nodes:\n"
        for obj in self.D1.Objects:
            str_+="  {} -> {}\n".format(obj, self.nodeMap[obj])
        str_+="Edges:\n"
        for edge in self.D1.MorphismList:
            str_+= "  {} -> ({})\n".format(edge,self.edgeMap[edge])
        return str_
    
def doNodesMatch(node1,node2):
    #return all(i in node2.properties for i in node1.properties)
    for i in node1.properties:
        if i not in node2.properties:
            return False
    return True

def doEdgesMatch(edge1,edge2):
    for i in edge1.properties:
        if i not in edge2.properties:
            return False
    return True

def pairUpEdge(self,neighbour1,outedge1,imageEdgeIterator):
    for _,neighbour2,outedge2 in imageEdgeIterator:
        if doNodesMatch(neighbour1, neighbour2) and doEdgesMatch(outedge1,outedge2):
            yield neighbour1,neighbour2,outedge1,outedge2


class HomomorphismIterator:
    def __init__(self,D1,D2):
        self.D1 = D1
        self.D2 = D2
        self.G1 = D1.Graph
        self.G2 = D2.Graph
        
        raise NotImplementedError
    
    def initialize(self):
        self.hom = Homomorphism(self.D1,self.D2)
        self.nodesToDoList = self.G1.nodes()
        
    def __call__(self):
        self.initialize()
        
        self.match()
    
    def match(self):
        if self.nodesToDoList == []:
            yield self.hom.copy()
        
        #match new connected Component
        node1 = self.nodesToDoList.pop()
        for node2 in self.G2.nodes():
            if doNodesMatch(node1,node2):
                #
                self.matchNode(self,node1,node2)
                self.match()
            
    
    def imageEdgeIteratorOut(self,neighbour,outedge,image):
        for _,image2,outedge2 in self.G2.out_edges([image],data = True):
            if False:pass
    
    def imageEdgeIteratorIn(self,neighbour,outedge,image):
        for _,image2,outedge2 in self.G2.in_edges([image],data = True):
            if False:pass
     
    def neighbourhoodMatchIterator(self,node,image):
        for _,neighbour,outedge in self.G1.out_edges([node],data = True):
            imageEdgeIterator = self.imageEdgeIteratorOut()
            yield self.pairUpEdge(neighbour,outedge,imageEdgeIterator)
        for _,neighbour,outedge in self.G1.in_edges([node],data = True):
            imageEdgeIterator = self.imageEdgeIteratorIn()
            yield self.pairUpEdge(neighbour,outedge,imageEdgeIterator)
            
        
    def matchNode(self,node,image):
        
        self.nodeMap[node] = image
        
        for matchings in product(self.neighbourhoodMatchIterator(node,image)):
            for matching in matchings:
                neighbour1,neighbour2,outedge1,outedge2 = matching
                self.hom.set_node_image(neighbour1, neighbour2)
                self.hom.set_edge_image(outedge1,  outedge2)
            
            for matching in matchings:
                neighbour1,neighbour2,_,_ = matching
                self.matchNode( neighbour1,neighbour2)
        
            
        
        
    