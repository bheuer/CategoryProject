from Diagram import Morphism,Object


class ExtensionRequest:
    '''Data structure that suggests diagram extensions without implementing them right away
        
        
        An ExtensionRequest stores the extension of the main diagram that can be 
        made as a consequence of a Rule applied to the diagram.
        It is represented by a "pushout"-Diagram of 
        
        1) the Characteristic Diagram,
        2) its extenstion as defined by the rule
        3) and a partial hom of Diagrams defined on the initial Char Diag
        
        The extension can then be implemented into the main Diagram by performing a "pushout"
        
        Example in the case of the fibered product of A,B over C
            
         extended char Diag
            
              Ax_CB                        the extension suggested 
              /  \                         is just the pushout of
             A    B                        this diagram of diagrams
              \  /                         
               C                
                      
               :               partially def
               :  rule         hom of diags
               :  
                 
             A    B                      O1----O4
              \  /       -------->        |     |
               C            hom          O2----O3---O5
                                         
         characteristic                   main Diagram
             Diagram                      
        
        An ExtensionRequest also takes care of 
            
            1) hashing the Request, in such a way that for instance the same rule isn't applied 
                again when the main Diagram is somehow manipulated, say by a different extension
    
            2) defining a Priority for this Request, which is evaluated by the RuleMaster in order
                to determine which Rule is applied on the Diagram in the next step.
        
        '''
    def __init__(self,rule,hom):
        self.rule = rule
        self.charDiag = rule.D1
        self.extension = rule.D2
        self.mainDiag = hom.D2
        self.hom=hom
        
        self.hashvalue = hash((rule.name,self.hom))
    
    def iter_new_Objects(self):
        for obj in self.rule.newObjects:
            yield obj
    
    def iter_new_Morphisms(self):
        for morphi in self.rule.newMorphisms:
            source = self.hom[morphi.source]
            target = self.hom[morphi.target]
            yield source,target
    
    def iter_new_Propertyhoms(self):
        for prop in self.rule.newProperties:
            yield prop.hom*self.hom
    
    def __hash__(self):
        return self.hashvalue
    
    def __eq__(self,ER):
        return hash(self)==hash(ER)
    
    def implement(self):
        '''carry out the pushout of the Extension Meta-Diagram'''
        #Extend hom to a lift of the extension to the main Diagram
        lift = self.hom*self.rule.partialInverse #inefficient
        for obj in self.rule.newObjects:
            newobj = Object(self.mainDiag)
            lift.set_node_image(obj,newobj)
        
        for morphi in self.rule.newMorphisms:
            source = lift[morphi.source]
            target = lift[morphi.target]
            newmorphi = Morphism(source,target)
            lift.set_edge_image(morphi,newmorphi)
       
        #compose characteristic homomorphism of property with lift to get
        #characteristic homomorphism in the extended main Diagram
        for prop in self.rule.newProperties:
            prop.push_forward(lift)
                
                
                