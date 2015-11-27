
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
    
    def __hash__(self):
        #So Dictionaries aren't hashable. We need to tuplelize them first,
        #that is, transform them in a tuple (key,value)
        #Moreover, dictionaries aren't order-safe. So we can't just iterate
        #and tuplelize whatever we find.
        #Instead, we sort the keys alphanumerically by their names
        #(that is, Object with name "A" < Object with name "B")
        #then, we can hash (ordered entries of node map, ordered entries of edge map)
        #I know this doesn't work for more general Graph Homomorphisms but I'm tired and also
        #WE ARE WRITING THIS ONLY FOR CATEGORIES, OK!?
        
        alphanumericSortingKey = lambda (a,b):a.name
        nodes = tuple(sorted(self.nodeMap.items(),key = alphanumericSortingKey))
        edges = tuple(sorted(self.edgeMap.items(),key = alphanumericSortingKey))
        return hash((nodes,edges))
    
    def __eq__(self,hom):
        return hash(self)==hash(hom)
    
    def get_edge_image(self,item):
        if self.edgeMap.has_key(item):
            return self.edgeMap[item]
        elif len(item.Composition)>1:
            iterator = item.iterComposingMorphisms()
            morphi = self.edgeMap[next(iterator)]
            for atomic in iterator: #inefficient #it just got even more inefficient
                morphi = morphi*self.edgeMap[atomic]
            return morphi
            
    
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
            
        
        
    