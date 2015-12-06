from ExtensionRequest import ExtensionRequest
from Diagram import Object,Morphism,Diagram
from Homomorphism.base import Homomorphism
from base import Rule
from Rule.abelian import ZeroObject, ZeroMorphism

CD = Diagram()
A = Object(CD,"A") 
B = Object(CD,"B") 
C = Object(CD,"C") 
F = Morphism(B,C,"F")
G = Morphism(A,B,"G")
#A -> B -> C
extension = Homomorphism(CD,CD)
extension.set_node_image(A, A)
extension.set_node_image(B, B)
extension.set_node_image(C, C)
extension.set_edge_image(F, F)
extension.set_edge_image(G, G)

class ComposeRuleClass(Rule):
    name = "ComposeRule"
    def __init__(self):
        Homomorphism.__init__(self,CD,CD)
        self.CD = CD 
        self.newMorphisms = [F.compose(G,dry = True)]
        self.newObjects = []
        self.newProperties = []
        self.extension = extension
        self.partialInverse = extension

class ComposeRequest(ExtensionRequest):
    def __init__(self,rule,hom):
        self.FC = hom.get_edge_image(F)
        self.GC = hom.get_edge_image(G)
        self.mainDiag = hom.D2
        self.charDiag = hom.D1
        
        
        self.useful = True
        if isZeroAndNotUseful(self.GC,self.FC):
            self.useful = False
        
        for m_f in self.FC.Morphisms:
            for m_g in self.GC.Morphisms:
                m = m_f.compose(m_g,dry = True)
                if self.mainDiag.doesDryMorphismExist(m):
                    self.useful = False
        
        self.hom = hom
        self.rule = rule
    
    def implement(self):
        #most important line is the following
        #here the morphism is build and then added to the diagram
        morph = self.FC.representative*self.GC.representative
        
        if isMorphiZero(self.FC) or isMorphiZero(self.GC):
            ZeroMorphism(morph)
            print "hier"


ComposeRule = ComposeRuleClass()

#methods to make Abelian Categories faster
def isZeroAndNotUseful(m1,m2):
    if not isMorphiZero(m1) and not isMorphiZero(m2):
        return False
    
    #can still be Zeromorphism
    if isinstance(m2.source,ZeroObject) and isinstance(m1.target,ZeroObject):
        for m_ in (m1,m2):
            if all(len(m.Composition)>1 for m in m_.Morphisms):
                return True
        return False
    return True

def isMorphiZero(m):
    for p in m.diagram.EquivalenceGraph.InverseLookUp[m]["propertyTags"]:
        if p.prop_name == "zeromorphism":
            return True
    return False

