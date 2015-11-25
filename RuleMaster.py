from Diagram import Diagram
from HomomorphismIterator import HomomorphismIterator
from ExtensionRequest import ExtensionRequest
from Property import *
from Rule import ProductRule,ExistProduct

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
        
        er = sorted(self.ExtensionRequests,key = CustomRuleWeight_MaxObjectPrioritiser)[0]
        print er.rule.name
        print er.hom
        er.implement()
        self.ExtensionRequests.remove(er)
        self.implemented.add(er)


NoPriority = lambda ER:0

def MaxObjectPriority(ER):
    return max(ER.hom.D2.Objects.index(image) for _,image in ER.hom.iterNodes() if image is not None)
    
Weights = {"ProductRule":0,"ExistProduct":1}
def CustomRuleWeight_MaxObjectPrioritiser(ER,weights = Weights): #careful with default value, I know, but this should work
    return (Weights[ER.rule.name],MaxObjectPriority(ER))
    