from collections import defaultdict 
from itertools import product
from copy import deepcopy
from networkx import *
from networkx.algorithms.isomorphism.isomorph import is_isomorphic
from Morphisms import AbstractMorphism

raise ImportError

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
    
class Composition(Rule):
    def __init__(self):
        super(Composition,self).__init__()
        self.subdiag = DiGraph
        #A -> B -> C
        self.subdiag.add_edge("A","B")
        self.subdiag.add_edge("B","C")
    def apply(self):
        for D in self.diagram.isomorphicSubdiagrams(self.subdiag):
            m1,m2 = tuple(D.morphilist())
            if not m1 > m2: continue
            
    
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

class Attribute(object):
    dynamic = False
    def __init__(self,subdiag):
        self.diagram = None
        
        #check that the subdiagram is of the desired form
        T = self.DiagTemplate()
        if T is not None:
            assert is_isomorphic(T,self.subdiag.UnderlyingGraph)
        
        self.subdiag = subdiag
        
    def setDiagram(self,diagram):
        self.diagram = diagram
    
    def DiagTemplate(self):
        return None
    
    def apply(self):
        '''apply the rule and iterate conclusions'''
        raise NotImplementedError
    
    def definingData(self):
        return [val for key,val in vars(self).items() if key not in ("diagram","dynamic")]
    
    def __eq__(self,rule):
        if type(self)!=type(rule): #tested: this does compare highest level type
            return False
        if self.definingData()==rule.definingData():
            return True
        return False

class MorphismAttribute(Attribute):
    def __init__(self,morphism):
        assert isinstance(morphism,AbstractMorphism)
        D = Diagram()
        
        
        

class Epim(Attribute):
    
    def DiagTemplate():
        #Morphism
        G = DiGraph()
        G.add_edge(1,2)
        return G 
    
    def apply
    
    
    