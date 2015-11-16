from Diagram import Diagram, isolatedNodes
from Homomorphisms import Homomorphism
from Morphisms import Morphism
from Object import Object

#abstractBaseClass
class Property:
    homomorphism = None
    name = None
    def __init__(self,*args):    
        self.charDiagram = self.buildCharDiagram()
        
        if len(args)==1 and isinstance(args[0],Homomorphism):
            self.homomorphism = args[0]
            assert self.homomorphism.source.is_isomorphic(self.charDiagram)
        elif len(args)==1 and isinstance(args[0],Diagram):
            raise NotImplementedError
        elif len(args)>0:
            #try to interpret user input as homomorphism images according to signature
            #Example: Product(pi1,pi2) 
            args = list(args) # make manipulatable and removable and poppable and stuff
            diagram = args[0].diagram
            signature_edges,signature_nodes = self.initSignature()
            
            hom = Homomorphism(self.charDiagram,diagram)
            try:
                for edge in signature_edges:
                    f = args.pop(0)
                    assert isinstance(f,Morphism),"too little init Morphisms given"
                    hom.extend_edge(edge,f)
                
                for node in signature_nodes:
                    obj = args.pop(0)
                    assert isinstance(obj,Object),"too few init Nodes given"
                    hom.extend_node(node,obj)
                
                assert args==[],"too many arguments"
            except ValueError:
                raise ValueError,"incoherent init data for Property"
            except IndexError:
                raise ValueError,"too little init data for Property"
            
            self.homomorphism = hom
        else:
            raise ValueError,"keine Ahnung was das sein soll"
            
            
    def buildCharDiagram(self):
        raise NotImplementedError
    
    def initSignature(self):
        signature_edges = self.charDiagram.MorphismList
        signature_nodes = isolatedNodes(self.charDiagram)
        return signature_edges,signature_nodes
        
    def definingData(self):
        return (self.name,self.homomorphism.definingData())
    
    def __repr__(self):
        str_ = "Property {} with homomorphism:\n".format(self.name)
        str_+=str(self.homomorphism)
        return str_

class MorphismsProperty(Property):
    def buildCharDiagram(self):
        D = Diagram()
        A = Object(D,"O1")
        B = Object(D,"O2")
        self.morph = Morphism(A,B,"f")
        return D
    def __repr__(self):
        print "edgeMap",self.homomorphism.edgeMap
        
        hom1 = self.morph
        hom2 = self.homomorphism.edgeMap.keys()[0]
        str_ = "Morphism Property {} for morphism {}".format(self.name,self.homomorphism.edgeMap[self.morph])
        return str_
        
class Epimorphism(MorphismsProperty):
    name = "epimorphism"

class Product(Property):
    name = "product"
    def buildCharDiagram(self):
        D = Diagram()
        A = Object(D,"factor1",)
        B = Object(D,"factor2")
        AxB = Object(D,"product")
        Morphism(AxB,A,"pi1")
        Morphism(AxB,B,"pi2")
        return D

class ZeroObject(Property):
    name = "zero"
    def buildCharDiagram(self):
        D = Diagram()
        Object(D,"0",)
        return D

if __name__ == "__main__":
    D = Diagram()
    A = Object(D,"A")
    B = Object(D,"B")
    AxB = Object(D,"AxB")
    f = Morphism(AxB,A,"f")
    g = Morphism(AxB,B,"g") 
    
    p = Product(f,g)
    zero = ZeroObject(A)
    epi = Epimorphism(f)
    
    print p
    
    print zero
    print epi