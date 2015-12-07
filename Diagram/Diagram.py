from collections import defaultdict 
from networkx.algorithms.isolate import is_isolate
from Morphisms import Morphism
from Graph import IamTiredOfNetworkxNotHavingAnEdgeObjectGraph
from Commute import CommutingMorphismEquivalenceClass
from Homomorphism.base import Homomorphism
from Category import Category,GenericCategory
from Morphisms import Identity, getIdentity

class Diagram(object):
    def __init__(self,category = None):
        self.Objects = []
        self.Morphisms = {}
        self.Graph = IamTiredOfNetworkxNotHavingAnEdgeObjectGraph()
        self.EquivalenceGraph = IamTiredOfNetworkxNotHavingAnEdgeObjectGraph()
        
        self.UNIVERSE = set([])
        self.Rules = []
        
        if category is None:
            category = GenericCategory
        self.category = category
        
        self.CommutativityQuotient = Homomorphism(self,self)
        self.CommutativitySection = Homomorphism(self,self)
        
        self.MorphismList = []
        self.MorphismNames = set()
        self.Properties = []
        
        
        for O in self.category.SpecialObjects:
            O(self) # initialize object
    
    def __getitem__(self,item):
        for i in self.Objects:
            if i.name == item:
                return i
        for i in self.MorphismList:
            if i.name == item:
                return i
    
    def addObject(self,obj):
        self.Objects.append(obj)
        self.Graph.add_node(obj,propertyTags = [])
        self.EquivalenceGraph.add_node(obj,propertyTags = [])
        
        self.addName(obj.name)
        self.Morphisms[obj]=defaultdict(list)
        
        self.CommutativityQuotient[obj]=obj
        self.CommutativitySection[obj]=obj        
    
    def addMorphi(self,morph):
        if not isinstance(morph, Morphism):
            raise ValueError
        
        target = morph.target
        source = morph.source
        
        if morph.name in self.MorphismNames:
            #nothing to do, Morphism is already added
            return
        
        if "0" in [o.source.name for o in morph.Composition] and len(morph.Composition)>2:
            print morph.Composition,[o.source.name for o in morph.Composition]
            assert False
        
        self.addName(morph.name)
        
        self.Morphisms[source][target].append(morph)
        self.MorphismNames.add(morph.name)
        
        self.MorphismList.append(morph)
        
        self.Graph.add_edge(source,target,morphism = morph,propertyTags = [])
        
        CMEC = CommutingMorphismEquivalenceClass(morph)
        self.EquivalenceGraph.add_edge(source,target,morphism = CMEC,propertyTags = [])
        
        self.CommutativityQuotient.set_edge_image(morph,CMEC)
        self.CommutativitySection.set_edge_image(CMEC,CMEC.representative)
        
        #see what Commutativity Class morph could be in
        
        for end,partial_m,start in morph.iterPartialMorphisms():
            if partial_m.name not in self.MorphismNames:
                continue
            if partial_m.name == morph.name:#infinite recursion and doesn't make sense
                continue
            
            for partial_m2 in partial_m.equivalenceClass():
                if partial_m2.name == partial_m.name:
                    continue
                newmorph = Morphism([end,partial_m2,start],dry = True)
                if newmorph.name in self.MorphismNames:
                    self.unify(morph,newmorph)
                #otherwise add and set equal, but be aware of infinite recursion by cycles.
                #this is not exhausstive, but it hardcodes avodiing cycles
                elif len(newmorph.Composition)<=len(morph.Composition) or not isCyclic(newmorph):
                    if isMorphismZero(partial_m2):
                        if not isMorphismZero(morph):
                            self.unify(morph,GiveZeroMorphism(source,target))
                    else:
                        
                        newmorph = Morphism([end,partial_m2,start])
                        self.unify(morph,newmorph)
                
                
    def addProperty(self,prop):
        self.Properties.append(prop)
    
    def unify(self,morph1,morph2):
        '''take two Morphisms and register that they should be considered equal'''
        #if morphisms are already known to commute, do nothing
        
        if morph1 not in self.MorphismList or morph2 not in self.MorphismList:
            return
        
        EC1 = self.CommutativityQuotient.get_edge_image(morph1)
        EC2 = self.CommutativityQuotient.get_edge_image(morph2)
        
        if EC1==EC2:
            #nothing to do
            return
        #morph1 and morph2 belong to the same Commutativity Class
        
        edge1 = self.EquivalenceGraph.InverseLookUp[EC1]
        self.EquivalenceGraph.overwrite_edge(EC2,edge1)
        
        EC1.merge_with(EC2)
        
        for m,id3 in self.CommutativityQuotient.iterEdges():
            if id3==EC2:
                self.CommutativityQuotient.set_edge_image(m,EC1)
            
        #update other morphism commutativities this causes:
        #the only new conclusions come from morphisms that
        #can be composed from morph1 and morph2
        for m in self.MorphismList:
            if m<morph1:
                self.unify(m.compose(morph1,dry=True),m.compose(morph2,dry = True))
            if morph1<m:
                self.unify(morph1.compose(m,dry = True),morph2.compose(m,dry=True))
    
    def commutes(self,morphism1,morphism2):
        #treats morph1,morph2 as technically different morphisms and asks if they are known to commute
        
        if not self.CommutativityQuotient.is_defined_on_edge(morphism1) or not self.CommutativityQuotient.is_defined_on_edge(morphism2):
            #morphisms not known => were not added by the user or by a rule => internal investigation going on
            return False
        return self.CommutativityQuotient.get_edge_image(morphism1)==self.CommutativityQuotient.get_edge_image(morphism2)
    
    def doesDryMorphismExist(self,drymorphism):
        return (drymorphism.name in self.MorphismNames)
    
    def getPropertyTags(self,morph):
        return self.Graph.InverseLookUp[morph]["propertyTags"]
    
    def appendPropertyTag(self,morph,propTag):
        self.Graph.InverseLookUp[morph]["propertyTags"].append(propTag)
        quot = morph.equivalenceClass()
        self.EquivalenceGraph.InverseLookUp[quot]["propertyTags"].append(propTag)
        
    def addName(self,name):
        if name in self.UNIVERSE:
            raise ValueError,"name {} already given".format(name)
        self.UNIVERSE.add(name)
    
    def giveName(self,mode="o"):
        i=0
        while mode+str(i) in self.UNIVERSE:
            i+=1
        return mode+str(i)
    
    def printCommutativity(self):
        printed = []
        for s in self.MorphismList:
            quot = s.equivalenceClass()
            if iscontainedin(quot, printed):
                continue
            printed.append(quot)
            print quot
    
    def __repr__(self):
        str_ = "Diagram with the following data"
        str_+= "| Objects:\n| "
        str_+="\n| ".join(str(o) for o in self.Objects)
        str_+="\n\n| Morphisms by Commutativity class:\n| "
        printed = []
        for s in self.MorphismList:
            quot = s.equivalenceClass()
            if iscontainedin(quot, printed):
                continue
            
            str_+="\n| "+str(quot)
            printed.append(quot)
        return str_
    
def isolatedNodes(diagram):
    for o in diagram.Objects:
        if is_isolate(diagram.Graph,o):
            yield o
            

def iscontainedin(item,list_):
    #for unhashable items that have an equality
    for i in list_:
        if i==item:
            return True
    return False

        
def GiveZeroMorphism(A,B):
    '''
    cerfully creates the zero morphism
    defines the corresponding maps A->0 and 0->B
    and A->0->B only if not defined before, otherwise
    takes those (any) that the diagram knows already
    '''
    
    assert A.diagram == B.diagram
    D = A.diagram
    zero = D["0"]
    
    if D.Morphisms[A][zero]:
        f0 = D.Morphisms[A][zero][0]
    else:
        f0 = Morphism(A,zero)
        
    if D.Morphisms[zero][B]:
        g0 = D.Morphisms[zero][B][0]
    else:
        g0 = Morphism(zero,B)
    
    return g0*f0

def isMorphismZero(m):
    A = m.source
    B = m.target
    if A.name=="0" or B.name=="0":
        return True
    
    D = m.diagram
    zero = D["0"]
    
    if isinstance(m,Morphism):
        m = m.equivalenceClass()
    
    if not D.Morphisms[A][zero]:
        return False
    f0 = D.Morphisms[A][zero][0]
    
    if not D.Morphisms[zero][B]:
        return False
    g0 = D.Morphisms[zero][B][0]
    
    if (g0*f0)==m.representative:
        return True
    
    for p in m.diagram.EquivalenceGraph.InverseLookUp[m]["propertyTags"]:
        if p.prop_name == "zeromorphism":
            return True
    return False

def isCyclic(morph):
    objs = [o.source.name for o in morph.Composition]
    objs.append( morph.target.name)
    if any(objs.count(n)>1 for n in objs):
        return True
    return False

    