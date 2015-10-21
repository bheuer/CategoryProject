from collections import defaultdict 
from itertools import product
from copy import deepcopy

class Rule(object):
    dynamic = False
    def __init__(self):
        self.diagram = None
        
    def setDiagram(self,diagram):
        self.diagram = diagram
    
    def iterMorphisms(self):
        for m in self.diagram.iterMorphisms():
            yield m
    
    def apply(self):
        '''apply the rule and iterate conclusions'''
        raise NotImplementedError
    
    def definingData(self):
        return [val for key,val in vars(self).items() if key not in ("diagram","dynamic")]
    
    def complexity(self):
        return sum(i.length() for i in self.definingData() if hasattr(i,"length"))            
    
    def __eq__(self,rule):
        if type(self)!=type(rule): #tested: this does compare highest level type
            return False
        if self.definingData()==rule.definingData():
            return True
        return False
            
    
class Commute(Rule):
    def __init__(self,morph1,morph2):
        super(Commute,self).__init__()
        assert morph1 // morph2
        self.morph1 = morph1
        self.morph2 = morph2
    
    def definingData(self):
        return set([self.morph1,self.morph2])
    
    def apply(self):
        target = self.morph1.target
        source = self.morph2.source
        
        self.diagram.unify(self.morph1,self.morph2)
        
        for m in self.iterMorphisms():
            if m.target == source and not self.morph1*m==self.morph2*m:
                yield Commute(self.morph1*m,self.morph2*m)
            if m.source == target and not m*self.morph1==m*self.morph2:
                yield Commute(m*self.morph1,m*self.morph2)
    def __repr__(self):
        return "Rule: {} commutes with {}.".format(self.morph1,self.morph2)

class MorphiRule(Rule):
    dynamic=True
    def __init__(self,morph):
        super(MorphiRule,self).__init__()
        self.morph = morph
    def definingData(self):
        return [self.morph]
    def __repr__(self):
        return "{} is {}".format(self.morph,self.__class__.__name__)

class Epim(MorphiRule):
    def apply(self):
        target = self.morph.target
        
        for m1,m2 in self.diagram.iterSameTargetBySource(target,repeat=2):
            if m1*self.morph==m2*self.morph:
                yield Commute(m1,m2)

class Mono(MorphiRule):
    def apply(self):
        source = self.morph.source
        
        for m1,m2 in self.diagram.iterSameSourceByTarget(source,repeat=2):
            if self.morph*m1==self.morph*m2:
                yield Commute(m1,m2)

class Isom(MorphiRule):
    def apply(self):
        source = self.morph.source
        
        for m1,m2 in self.diagram.iterSameSourceByTarget(source,repeat=2):
            if self.morph*m1==self.morph*m2:
                yield Commute(m1,m2)
 
class Unique(Rule):
    dynamic=True
    def __init__(self,morph=None):
        super(Unique,self).__init__()
        self.morph = morph
    
    def apply(self):
        for m in self.iterMorphisms():
            if not m==self.morph and self.uniqueProperty(m):
                yield Commute(m,self.morph)
    
    def uniqueProperty(self,m):
        raise NotImplementedError
    
class IntoProduct(Unique):
    def __init__(self,morph,*Family):
        super(IntoProduct,self).__init__(morph)
        self.projections = Family
    
    def uniqueProperty(self,morph2):
        morph1 = self.morph
        if morph2.target == morph1.target and morph2.source == morph1.source:
            return all(proj*morph1==proj*morph2 for proj in self.projections)
    
class FromCoproduct(Unique):
    def __init__(self,morph,*Family):
        super(FromCoproduct,self).__init__(morph)
        self.injections = Family
    
    def uniqueProperty(self,morph2):
        morph1 = self.morph
        if morph2.target == morph1.target and morph2.source == morph1.source:
            return all(morph1*inj==morph2*inj for inj in self.injections)