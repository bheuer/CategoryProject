from Diagram import Diagram, Object, Morphism
from Diagram.Diagram import isolatedNodes
from Homomorphism import Homomorphism
from Diagram.Commute import CommutingMorphismEquivalenceClass

#abstractBaseClass
class Property:
    '''Abstract base class for implementations of Subdiagram Properties
    
    A Property is a purely syntactic object that assigns a certain FUNCTIONAL PROPERTIES
    (not "functioral" to a subdiagram. 
    
    As an example consider the below Diagram for the univseral property of product
        
        C
        |
       AxB            
    f /  \ g
     A    B
    
    where AxB denotes the product of A and B, f and g are the projection maps,
    and where C is some arbitrary object . The Graph member of the Diagram class
    can be used to represent the structure of this Diagram topologically.#
    In order to make a statement about that AxB is the product, of A and B,
    ie that AxB has the "functional meaning" to be a product, we can take a 
    CHARACTERISTIC DIAGRAM wish defines how a product looks like in general
    
        product
     pi1 /   \ pi2       CharD
    factor1  factor2
    
    we then consider the Homomorphism of Diagrams
    
    
    CharD -> D:
        product -> AxB
        factor1 -> A
        factor2 -> B
        
        pi1 -> f
        pi2 ->g
    
    This homomorphism assigns to the subdiagram induced by A,B,AxB the 
    functional meanings representing the categorial structure of the product.
    
    We can therefore represent the statement "AxB is the product of A and B"
    by the homomorphism from the characteristic diagram into D. This is 
    exactly what the Property class does.
    
    Note that this does not incorporate any MEANING of the product, ie its 
    universal property. This is dealt with by the Rules class.
    ''' 
    
    homomorphism = None
    name = None
    weight = 0
    def __init__(self,*args):
        self.charDiagram = Diagram()
        self.buildCharDiagram(self.charDiagram)
        self.homomorphism = self.processPropertyInput(args)
        
        self.id = id(self)
        self.registerPropertyTags()
        
        self.homomorphism.D2.addProperty(self)
        
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
            propTag = PropertyTag(self,node.name,self.id)
            self.homomorphism.D2.Graph.node[image]["propertyTags"].append(propTag)
            self.homomorphism.D2.EquivalenceGraph.node[image]["propertyTags"].append(propTag)
            
        #edgeTags not working because no edge objects   
        for morph,image in self.homomorphism.iterEdges():
            morphiname = morph.Composition[0].name
            propTag = PropertyTag(self,morphiname,self.id)
            self.homomorphism.D2.appendPropertyTag(image,propTag)
            
    def processPropertyInput(self,args):
        if len(args)==1 and isinstance(args[0],Homomorphism):
            hom = args[0]
            for e,image in hom.iterEdges():
                if isinstance(image, CommutingMorphismEquivalenceClass):
                    hom.set_edge_image(e, image.representative)
            
            #assert hom.D1.is_isomorphic(self.charDiagram)
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
                    
                    if isinstance(f,CommutingMorphismEquivalenceClass):
                        f = f.representative
                    
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

    def push_forward(self,hom):
        assert isinstance(hom, Homomorphism)
        assert hom.D1==self.homomorphism.D2
        return self.__class__(hom*self.homomorphism)
    
#~end of definition of class Property

class PropertyTag:
    def __init__(self,prop,function,property_id):
        self.prop = prop
        self.prop_name = prop.name
        self.function = function
        self.property_id = property_id
    def __eq__(self,ptag2):
        #checks whether two objects have the same function
        #does not check whether they come from the same instance of a Property
        #used to check whether a topological homomorphism is also a functional homomorphism
        return (self.prop_name == ptag2.prop_name) and (self.function == ptag2.function)
    def __hash__(self):#we want to consider sets of properties
        return hash((self.prop_name,self.function))
    
    def isinstanceof(self,prop):
        if prop.name == self.prop_name:
            return True
        return False
