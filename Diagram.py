from collections import defaultdict 
from itertools import product
from Morphisms import *

class Diagram(object):
    def __init__(self):
        self.Objects = []
        self.Graph = []
        self.UNIVERSE = set([])
        self.Rules = []
        self.UniversalObjects = []
        
        self.Morphisms = {}
        self.CommutingComponents = {}
    
    def addObject(self,obj):
        self.Objects.append(obj)
        morphs = defaultdict(list)
        
        id_obj = obj.Identity
        morphs[obj] = [id_obj]
        self.Morphisms[obj]=morphs
        self.CommutingComponents[id_obj.id()]=id_obj.id()
    
    def iterBySource(self,s):
        for t in self.Morphisms[s]:
            for m in self.Morphisms[s][t]:
                yield t,m
    
    def iterByTarget(self,t):
        for s in self.Objects:
            for m in self.Morphisms[s][t]:
                yield s,m
    
    def iterBySourceAndTarget(self,s,t,repeat=1):
        for m in product(self.Morphisms[s][t],repeat=repeat):
            yield m
    
    def iterSameTargetBySource(self,s,repeat=1):
        for o in self.Objects:
            for m in product(self.Morphisms[s][o],repeat=repeat):
                yield m
    
    def iterSameSourceByTarget(self,t,repeat=1):
        for o in self.Objects:
            for m in product(self.Morphisms[o][t],repeat=repeat):
                yield m
    
    def iterMorphisms(self):
        for s in self.Objects:
            for _,m in self.iterBySource(s):
                yield m
    
    def addMorphi(self,morph):
        target = morph.target
        source = morph.source
        name = morph.name
        if name in self.UNIVERSE:
            raise ValueError,"name {} already given".format(name)
        self.UNIVERSE.add(morph.name)
        
        for (newsource,f),(newtarget,g) in product(self.iterByTarget(source),self.iterBySource(target)):
            newmorph = g*morph*f
            self.Morphisms[newsource][newtarget].append(newmorph)
            self.CommutingComponents[newmorph.id()]=newmorph.id()
        
    def checkRule(self,rule):
        active = False
        for conclusion in rule.apply():
            print rule
            print "     ----->",conclusion
            active|=self.addRule(conclusion,checkDynamics=False)
        
        return active
        
    def addRule(self,rule,checkDynamics=True):
        rule.setDiagram(self)
        
        if not self.isRuleAdmissible(rule) or rule in self.Rules:
            return False
    
        self.Rules.append(rule)
        self.checkRule(rule)
        
        if checkDynamics:
            self.checkDynamicRules()
        return True
    
    def checkDynamicRules(self):
        active = True
        while active:
            active = False
            
            #Rules
            for r in self.Rules:
                if r.dynamic:
                    active |= self.checkRule(r)
            
            #UniversalProperties
            newrules = []
            for uo in self.UniversalObjects:
                for newrule in uo.universalProperty():
                    self.addRule(newrule, False)
                    active = True
        
    
    def isRuleAdmissible(self,rule):
        for m in rule.definingData():
            if isinstance(m, AbstractMorphism):
                if not self.isMorphismAdmissible(m):
                    return False
        return True
    
    def isMorphismAdmissible(self,morph):
        return self.CommutingComponents.has_key(morph.id())
    def check(self,predicate):
        '''Read a Rule as a predicate by checking if it follows from the previously added rules.
           Returns True if so and None otherwise.'''
        if predicate in self.Rules:
            return True
        return None
    
    def unify(self,morph1,morph2):
        '''take two Morphisms and register that they should be considered equal'''
        
        id1 = morph1.id()
        id2 = morph2.id()
        for m,id3 in self.CommutingComponents.items():
            if id3==id2:
                self.CommutingComponents[m]=id1
    
    def commutes(self,morph1,morph2):
        #treats morph1,morph2 as technically different morphisms and asks if they are known to commute
        m_id1 = morph1.id()
        m_id2 = morph2.id()
        if not self.CommutingComponents.has_key(m_id1) or not self.CommutingComponents.has_key(m_id2):
            return False
        return self.CommutingComponents[m_id1]==self.CommutingComponents[m_id2]
    
    def opposite(self):
        raise NotImplementedError
    
    def giveName(self):
        i=0
        while "o"+str(i) in self.UNIVERSE:
            i+=1
        return "o"+str(i)
        
    
    def print_(self):
        for s in self.Objects:
            for t in self.Morphisms[s]:
                for f in self.Morphisms[s][t]:
                    if isinstance(f,Identity):
                        continue
                    print f
