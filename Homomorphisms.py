from networkx import MultiDiGraph

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
    
    def __hash__(self,ind,val):
        return hash((tuple(self.nodeMap.items()),tuple(self.edgeMap.items())))
    
    def get_edge_image(self,item):
        return self.edgeMap[item]
    
    def is_defined_on_edge(self,edge):
        return self.edgeMap.has_key(edge)
    
    def is_defined_on_node(self,node):
        return self.nodeMap.has_key(node)
    
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
    
    def __mul__(self,hom2):
        assert isinstance(hom2,Homomorphism)
        newEdgeMap = {}
        newNodeMap = {}
        
        for node,image in hom2.iterNodes():
            newNodeMap[node] = self[image]
        
        for edge,image in hom2.iterEdges():
            newEdgeMap[edge] = self.get_edge_image(image)
        
        return Homomorphism(hom2.D1,self.D2,nodeMap = newNodeMap, edgeMap = newEdgeMap)
        
    
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
            
        
        
    