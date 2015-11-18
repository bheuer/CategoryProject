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
        self.homomorphism = self.processPropertyInput(args)
        self.id = id(self)
        self.registerPropertyTags()
        
    def buildCharDiagram(self):
        raise NotImplementedError
    
    def initSignature(self):
        signature_edges = self.charDiagram.MorphismList
        signature_nodes = isolatedNodes(self.charDiagram)
        return signature_edges,signature_nodes
        
    def definingData(self):
        return (self.name,self.homomorphism.definingData())
    
    def __repr__(self):
        str_ = "Property '{}' with homomorphism:\n".format(self.name)
        str_+=str(self.homomorphism)
        return str_

    def registerPropertyTags(self):
        for node,image in self.homomorphism.iterNodes():
            self.homomorphism.D2.Graph.node[image]["propertyTags"].add(PropertyTag(self.name,node.name,self.id))
        #edgeTags not working because no edge objects   
        for morph,image in self.homomorphism.iterEdges():
            morphiname = morph.Composition[0].name
            self.homomorphism.D2.InverseLookUp[image]["propertyTags"].add(PropertyTag(self.name,morphiname,self.id))
            
    def processPropertyInput(self,args):
        if len(args)==1 and isinstance(args[0],Homomorphism):
            hom = args[0]
            assert hom.source.is_isomorphic(self.charDiagram)
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
        else:
            raise ValueError,"keine Ahnung was das sein soll"
        return hom

#~end of definition of class Property


class PropertyTag:
    def __init__(self,prop_name,function,property_id):
        self.prop_name = prop_name
        self.function = function
        self.property_id = property_id
    def __eq__(self,ptag2):
        #checks whether two objects have the same function
        #does not check whether they come from the same instance of a Property
        #used to check whether a topological homomorphism is also a functional homomorphism
        return (self.prop_name == ptag2.prop_name) and (self.function == ptag2.function)
    def __hash__(self):#we want to consider sets of properties
        return hash((self.prop_name,self.function))