from Homomorphism.HomomorphismIterator import HomomorphismIterator
from ExtensionRequest import ExtensionRequest
from Rule import ProductRule,ExistProduct,ProductRuleUnique,ExistIdentity

class RuleMaster:
    
    def __init__(self,diagram,prioritiser = None):
            
        self.diagram = diagram
        #self.Rules = [ExistProduct()(),ProductRule()(),ProductRuleUnique()()]#self.diagram.category.Rules
        self.Rules = [ExistIdentity()(),ProductRule()(),ProductRuleUnique()()]#self.diagram.category.Rules
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
    Max = -1
    for _,image in ER.hom.iterNodes():
        if image is not None:
            Max = max(Max,ER.hom.D2.Objects.index(image))
    return Max
    
    
def MaxMorphismPriority(ER):
    Max = -1
    for _,image in ER.hom.iterEdges():
        if image is not None:
            Max = max(Max,ER.hom.D2.MorphiList.index(image))
    return Max
    
def MaxObjectPlusMaxMorphismPriority(ER):
    return MaxMorphismPriority(ER)+MaxObjectPriority(ER)
    
Weights = {"ProductRule":1,"ExistProduct":2,"ProductRuleUnique":0,"ExistIdentity":1}
def CustomRuleWeight_MaxObjectPrioritiser(ER,weights = Weights): #careful with default value, I know, but this should work
    return (MaxObjectPriority(ER),Weights[ER.rule.name])
    
def CustomRuleWeight_MaxObjectPlusMaxMorphismPrioritiser(ER,weights = Weights): #careful with default value, I know, but this should work
    return (MaxObjectPlusMaxMorphismPriority(ER),Weights[ER.rule.name])
    