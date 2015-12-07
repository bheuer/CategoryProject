from Homomorphism.HomomorphismIterator import HomomorphismIterator
from Rule.ExtensionRequest import ExtensionRequest
from Rule import *
from Solver.Prioritiser import UltimateWeightPriotiser
from RuleMaster import *
from IO.diagIO import latexDiag

class SimpleRuleMaster(RuleMaster):
    
    def __init__(self,diagram,prioritiser = None, maxMorphisms = 1):
            
        self.diagram = diagram
        #self.Rules = [ExistProduct()(),ProductRule()(),ProductRuleUnique()()]#self.diagram.category.Rules
        self.Rules = [ExistIdentity,ProductRule,ProductRuleUnique,ProjectiveUP,InjectiveUP,ComposeRule,CoProductRuleGenerator()()]#self.diagram.category.Rules
        self.ExtensionRequests = []
        self.Prioritiser = prioritiser
        self.implemented = []
        self.MaxMorphisms=maxMorphisms
        
        if prioritiser is None:
            prioritiser = UltimateWeightPriotiser
        self.Prioritiser = prioritiser
        
    def __call__(self, numberOfExtensions = 1,verbose = False, printlatex=False):
        if verbose:
            print "prepare to apply {} new rules to the diagram:".format(numberOfExtensions)
         
        for rule in self.Rules:
            CD = rule.CD
            for hom in HomomorphismIterator(CD,self.diagram):
                if rule.name=="ComposeRule":
                    ER = ComposeRequest(rule,hom)
                    if not ER.useful:
                        continue
                else:
                    ER = ExtensionRequest(rule,hom)
                if iscontainedin(ER,self.implemented):
                    continue
                if not iscontainedin(ER,self.ExtensionRequests):
                    self.ExtensionRequests.append(ER)
        if verbose:
            print "{} new extension requests generated".format(len(self.ExtensionRequests))
            print "prioritise extension requests"
        if len(self.ExtensionRequests)==0:
            return False
        
        #sortedExtensionRequests = sorted(self.ExtensionRequests,key = self.Prioritiser)
        sortedExtensionRequests = self.ExtensionRequests
        
        for ruleNumber in xrange(numberOfExtensions):
            ruleCounter=0
            #if there are no more extension requests, terminate
            if not sortedExtensionRequests:
                break

            try:            
                extensionRequest = sortedExtensionRequests[ruleNumber]
            except:
                break
            rulemasterapproves=False
            for morph in extensionRequest.rule.newMorphisms:
                newsource=extensionRequest.hom.nodeMap[extensionRequest.hom.D1[morph.source.name]]
                newtarget=extensionRequest.hom.nodeMap[extensionRequest.hom.D1[morph.target.name]]
                if len([x for x in self.diagram.Morphisms[newsource][newtarget]])<self.MaxMorphisms:
                    rulemasterapproves=True
            if rulemasterapproves:
                if verbose:
                    print "________________\n\n apply new Rule:"
                    print extensionRequest.rule.name
                    print extensionRequest.hom
                    print "with priority value {}\n________________\n"\
                            .format(self.Prioritiser(extensionRequest))
                extensionRequest.implement()
                self.ExtensionRequests.remove(extensionRequest)
                self.implemented.append(extensionRequest)
                ruleCounter+=1
            else:
                self.implemented.append(extensionRequest) #RuleMaster refuses to reconsider
        self.ExtensionRequests = []
        if verbose:
            print "applied {} new rules".format(ruleCounter+1)
        if printlatex:
            return latexDiag(self.diagram)
        else:
            return True
