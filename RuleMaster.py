from Diagram import Diagram
from HomomorphismIterator import HomomorphismIterator
from ExtensionRequest import ExtensionRequest
from Property import *
from Rule import *

class RuleMaster:
    
    def __init__(self,diagram,prioritiser = None):
            
        self.diagram = diagram
        self.Rules = [ExistProduct()(),ProductRule()()]#self.diagram.category.Rules
        self.ExtensionRequests = set()
        self.Prioritiser = prioritiser
        self.implemented = set()
        if prioritiser is None:
            prioritiser = NoPriority
        self.Prioritiser = prioritiser
        
    def __call__(self):
        
        for rule in self.Rules:
            CD = rule.CD 
            for hom in HomomorphismIterator(CD,self.diagram):
                ER = ExtensionRequest(rule,hom)
                if ER in self.implemented:
                    continue
                self.ExtensionRequests.add(ER)
        
        er = sorted(self.ExtensionRequests,key = MaxObjectPriority)[0]
        er.implement()
        self.ExtensionRequests.remove(er)
        self.implemented.add(er)
        
NoPriority = lambda ER:0
def MaxObjectPriority(ER):
    return max(ER.hom.D2.Objects.index(image) for _,image in ER.hom.iterNodes() if image is not None)
    
    