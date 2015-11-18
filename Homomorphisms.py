from itertools import product
from copy import deepcopy 
from collections import defaultdict

class Homomorphism:
    def __init__(self,D1,D2,nodeMap=None,edgeMap=None):
        if nodeMap is None:
            nodeMap = {}
        if edgeMap is None:
            edgeMap = {}
        self.D1 = D1
        self.D2 = D2
        self.nodeMap = nodeMap
        self.edgeMap = edgeMap
        #do things on graph level, but def homomorphi on morphism (=data) level
    
    def __getitem__(self,ind):
        return self.nodeMap[ind]
    def __setitem__(self,ind,val):
        self.nodeMap[ind] = val
    
    def iterNodes(self):
        for node in self.nodeMap:
            image = self.nodeMap.get(node)
            yield node,image
    def iterEdges(self):
        for edge in self.edgeMap:
            image = self.edgeMap[edge]
            yield edge,image
    
    
    def set_node_image(self,node,image):
        self.nodeMap[node]=image
    def set_edge_image(self,edge,image):
        self.edgeMap[edge]=image
        
    def copy(self):
        return Homomorphism(self.D1,self.D2,\
                    copyDictWithoutCopyingEntries(self.nodeMap),copyDictWithoutCopyingEntries(self.edgeMap))
    
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
            str_+="  {} -> {}\n".format(obj, self.nodeMap.get(obj))
        str_+="Edges:\n"
        for edge in self.D1.MorphismList:
            str_+= "  ({}) -> ({})\n".format(edge,self.edgeMap.get(edge))
        return str_

def copyDictWithoutCopyingEntries(dic):
    return dict((key,value) for key,value in dic.items())
            
        
        
    