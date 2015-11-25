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