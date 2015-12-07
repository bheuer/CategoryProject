from Diagram import Morphism,Object,Identity
from Rule.abelianProperty import GiveZeroMorphism,isMorphismZero
from Property.Property import getIdentity


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
    
    def __eq__(self,ER):
        #Homomorphisms might turn out to be the same only later when
        #it turns out that by Commutativity two morphisms are the same
        #which a priori aren't.
        #so we can't just store a hash value and compare that, but have to rely
        #on the current equality value of morphisms in the image diagram
        if self.rule.name != ER.rule.name:
            return False
        if self.hom == ER.hom:
            return True
        return False
    
    def __ne__(self,ER):
        return not self.__eq__(ER)
    
    def implement(self):
        '''carry out the pushout of the Extension Meta-Diagram'''
        #Extend hom to a lift of the extension to the main Diagram
        lift = self.hom*self.rule.partialInverse #inefficient
        for obj in self.rule.newObjects:
            try:
                names=[]
                for s in obj.namescheme[1]:
                    obj_item =  self.charDiag[s]
                    if isinstance(obj_item,Object):
                        names.append(self.hom[self.charDiag[s]].name)
                    else:#morphism
                        names.append(self.hom.get_edge_image(self.charDiag[s]).representative.name)
                
                newname=obj.namescheme[0].format(*names)
                newobj = Object(self.mainDiag,newname)   #try naming according to scheme
            except:
                try:
                    newobj=Object(self.mainDiag,self.mainDiag.giveName(mode=newname)) #append a number to name if this failed
                except:
                    newobj = Object(self.mainDiag)           #give a generic name if everything fails
            latexlist=[]
            try:
                for s in obj.latexscheme[1]:
                    try:
                        try:
                            latexlist.append(self.hom[self.charDiag[s]].latex)
                        except:
                            latexlist.append(self.hom[self.charDiag[s]].name)
                    except:
                        try:
                            latexlist.append(self.hom.edgeMap[self.charDiag.Morphisms[s]].latex)
                        except:
                            latexlist.append(self.hom.edgeMap[self.charDiag.Morphisms[s]].name)
                newobj.latex=obj.latexscheme[0].format(*latexlist)  #set LaTeX display string
            except:
                newobj.latex=newobj.name
            lift.set_node_image(obj,newobj)

        
        for morphi in self.rule.newMorphisms:
            source = lift[morphi.source]
            target = lift[morphi.target]
            if isinstance(morphi,Identity):
                newmorphi = getIdentity(source)
            elif isMorphismZero(morphi):
                newmorphi = GiveZeroMorphism(source,target)
            else:
                newmorphi = Morphism(source,target)           #do not implement nameschemes for morphisms for now
                latexlist=[]
                try:
                    for s in morphi.latexscheme[1]:
                        try:
                            try:
                                latexlist.append(self.hom[self.charDiag[s]].latex)
                            except:
                                latexlist.append(self.hom[self.charDiag[s]].name)
                        except:
                            try:
                                latexlist.append(self.hom.edgeMap[self.charDiag[s]].representative.latex)
                            except:
                                latexlist.append(self.hom.edgeMap[self.charDiag[s]].representative.name)
                    newmorphi.latex=morphi.latexscheme[0].format(*latexlist)  #set LaTeX display string
                except:
                    pass
            lift.set_edge_image(morphi,self.mainDiag.CommutativityQuotient.get_edge_image(newmorphi))
       
        #compose characteristic homomorphism of property with lift to get
        #characteristic homomorphism in the extended main Diagram
        #for commutativity classes, just choose an arbitrary section
        for prop in self.rule.newProperties:
            prop.push_forward(lift)
                
    def __repr__(self):
        str_ = "ExtensionRequest by rule {} via the following homomorphism\n".format(self.rule.name)
        return str_+str(self.hom)
                
