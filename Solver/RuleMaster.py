from Homomorphism.HomomorphismIterator import HomomorphismIterator
from Rule.ExtensionRequest import ExtensionRequest
from Rule.Rule import ProductRule,ExistProduct,ProductRuleUnique,ExistIdentity
from Solver.Prioritiser import UltimateWeightPriotiser

def iscontainedin(item,list_):
    #for unhashable items that have an equality
    for i in list_:
        if i==item:
            return True
    return False

class RuleMaster:
    
    def __init__(self,diagram,prioritiser = None):
            
        self.diagram = diagram
        #self.Rules = [ExistProduct()(),ProductRule()(),ProductRuleUnique()()]#self.diagram.category.Rules
        self.Rules = [ExistIdentity()(),ProductRule()(),ProductRuleUnique()()]#self.diagram.category.Rules
        self.ExtensionRequests = []
        self.Prioritiser = prioritiser
        self.implemented = []
        
        if prioritiser is None:
            prioritiser = UltimateWeightPriotiser
        self.Prioritiser = prioritiser
        
    def rule(self, numberOfExtensions = 1,verbose = False):
        if verbose:
            print "prepare to apply {} new rules to the diagram:".format(numberOfExtensions)
         
        for rule in self.Rules:
            CD = rule.CD 
            for hom in HomomorphismIterator(CD,self.diagram):
                ER = ExtensionRequest(rule,hom)
                if iscontainedin(ER,self.implemented):
                    continue
                if not iscontainedin(ER,self.ExtensionRequests):
                    self.ExtensionRequests.append(ER)
        if verbose:
            print "{} new extension requests generated".format(len(self.ExtensionRequests))
            print "prioritise extension requests"
        
        sortedExtensionRequests = sorted(self.ExtensionRequests,key = self.Prioritiser)
        
        ruleNumber = 0
        while ruleNumber<numberOfExtensions:
            #if there are no more extension requests, terminate
            if not sortedExtensionRequests:
                break
            
            extensionRequest = sortedExtensionRequests.pop(0)
            if extensionRequest in self.implemented:
                continue
            
            if verbose:
                print "________________\n\n apply new Rule:"
                print extensionRequest.rule.name
                print extensionRequest.hom
                print "with priority value {}\n________________\n"\
                        .format(self.Prioritiser(extensionRequest))
            
            extensionRequest.implement()
            self.implemented.append(extensionRequest)
            ruleNumber+=1
            
        self.ExtensionRequests = []
        if verbose:
            print "applied {} new rules".format(ruleNumber+1)