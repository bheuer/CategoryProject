from Rule.rule import ProductRuleUnique, CoProductRuleUnique

class Category:
    def __init__(self,name,setOfRules,setOfDistinguishedObjects,inheritFrom = None):
        self.name = name
        self.setOfRules = setOfRules.add(inheritFrom.setOfRules)
        self.setOfDistinguishedObjects = setOfDistinguishedObjects.add(inheritFrom.setOfDistinguishedObjects)
    
Basic = Category("hasProducts",setOfRules= [ProductRuleUnique()(),CoProductRuleUnique()()])
