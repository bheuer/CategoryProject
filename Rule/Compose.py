from ExtensionRequest import ExtensionRequest
from Diagram import Object,Morphism,Diagram
from Homomorphism.base import Homomorphism
from base import Rule
from Diagram.Morphisms import Identity

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

class ComposeRule(Rule):
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
        for m_f in self.FC.Morphisms:
            for m_g in self.GC.Morphisms:
                m = m_f.compose(m_g,dry = True)
                if self.mainDiag.doesDryMorphismExist(m):
                    self.useful = False
        
        self.hom = hom
        self.rule = rule
    
    def implement(self):
        #print "HIER",self.f,self.g
        self.FC.representative*self.GC.representative
        
