from Homomorphisms import Homomorphism
from networkx.classes.function import all_neighbors
from networkx.algorithms.components.weakly_connected import weakly_connected_components
from Diagram import Diagram,Morphism
from Object import Object

def doNodesMatch(node1,node2):
    return True
    return all(i in node2.properties for i in node1.properties)

def doEdgesMatch(edge1,edge2):
    return True
    return all(i in edge1.properties for i in edge2.properties)

def iterateEdges(G,node1,node2):
    dic = G[node1]
    if dic.has_key(node2):
        for K in dic[node2].values():
            yield K["object"]

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
    
    def matchComponents(self,index = 0):
        if index==len(self.componentRepresentatives):
            yield
            return
        
        node1 = self.componentRepresentatives[index]
        for node2 in self.G2.nodes():
            if doNodesMatch(node1,node2):
                self.hom.nodeMap[node1]=node2
                for _ in self.matchNode(node1):
                    for _ in self.matchComponents(index+1):
                        yield None
                
                self.hom.nodeMap[node1]=None
    
    def matchNode(self,node):
        neighbourlist = [n for n in all_neighbors(self.G1,node) if self.hom.nodeMap.get(n) is None]
        for _ in self.matchNeighbourhood(self.G1.out_edges([node],data = True),mode = "out"):
            for _ in self.matchNeighbourhood(self.G1.in_edges([node],data = True),mode = "in"):
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
        node,neighbour,morphi = edges[index]
        if mode=="in":
            node,neighbour = neighbour,node
        morphi = morphi["object"]
        
        node2 = self.hom.nodeMap[node]
        
        neighbour2 = self.hom.nodeMap.get(neighbour)
        if neighbour2 is not None: #node assigned before
            if self.hom.edgeMap.get(morphi) is None: #but edge not: find morphism that works
                if mode=="out":
                    iter_ = iterateEdges(self.G2, node2,neighbour2)
                    print self.hom.nodeMap
                elif mode=="in":
                    iter_ = iterateEdges(self.G2,neighbour2,node2)
                
                for morphi2 in iter_:
                    if doEdgesMatch(morphi, morphi2):
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
            potential_images = self.G2.in_edges([node2],data = True)
        if mode == "out":
            potential_images = self.G2.out_edges([node2],data = True)
        
        for inneighbour2,neighbour2,morphi2 in potential_images:
            morphi2 = morphi2["object"]
            self.hom.edgeMap[morphi] = morphi2
            self.hom.nodeMap[neighbour] = (neighbour2 if mode=="out" else inneighbour2)
            
            for _ in self.matchNeighbourhood(edges, index+1, mode):
                yield None
    
            self.hom.edgeMap[morphi] = None
            self.hom.nodeMap[neighbour] = None
    

if __name__ == "__main__":
    def test1():
        '''
        D1
        
           f      g
        A ---> B ---> C
                
                
        D2        
               X2 
               |  F2
               |  
           F   V  G
        X ---> Y ---> Z
         <---  |    
          G2   | id
               Y
           
        '''
        
        D1 = Diagram()
        D2 = Diagram()
        
        A = Object(D1,"A")
        B = Object(D1,"B")
        C = Object(D1,"C")
        Morphism(A,B,"f")
        Morphism(B,C,"g")
        
            
        X = Object(D2,"X")
        Y = Object(D2,"Y")
        Z = Object(D2,"Z")
        X2 = Object(D2,"X2")
        
        Morphism(X,Y,"F")
        Morphism(Y,Z,"G")
        Morphism(Y,Y,"id")
        Morphism(X2,Y,"F2")
        Morphism(Y,X,"G2")
        
        homiter = HomomorphismIterator(D1,D2)
        for hom in homiter():
            print hom
            
    def test2():
        '''
        D1
        
           f      
        A ---> B
         <\    / g
       h  \   /     
           C<-  
             
        D2        
               
           F      
        X ---> Y
         <\    / G
       H  \   /     
           Z<-
           |
           | id
           Z
             
        '''
        
        D1 = Diagram()
        D2 = Diagram()
        
        A = Object(D1,"A")
        B = Object(D1,"B")
        C = Object(D1,"C")
        Morphism(A,B,"f")
        Morphism(B,C,"g")
        Morphism(C,A,"h")
        
            
        X = Object(D2,"X")
        Y = Object(D2,"Y")
        Z = Object(D2,"Z")
        
        Morphism(X,Y,"F")
        Morphism(Y,Z,"G")
        Morphism(Z,X,"H")
        Morphism(Z,Z,"idZ")
        
        homiter = HomomorphismIterator(D1,D2)
        for hom in homiter():
            print hom
    
    print "test1"
    test1()
    print "test2"
    test2()