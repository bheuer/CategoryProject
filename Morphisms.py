from collections import defaultdict 
from itertools import product
from copy import deepcopy
from Object import Object

class AbstractMorphism(object):
    def __init__(self, source, target):
        self.source = source
        self.target = target
        
        if not  self.source.diagram == self.target.diagram:
            raise ValueError
        
        self.diagram  = self.source.diagram
    
    def compose(self,g):
        if isinstance(g,Identity):
            return Morphism([self])
        return Morphism([self,g])
    
    def __mul__(self,g):
        return self.compose(g)
    
    def __lt__(self,morph):
        assert isinstance(morph,AbstractMorphism)
        return self.source==morph.target
    
    def __gt__(self,morph):
        return morph<self
    
    def __floordiv__(self,morph):
        assert isinstance(morph,AbstractMorphism)
        return self.target==morph.target and self.source==morph.source
    
class AtomicMorphism(AbstractMorphism):
    def __init__(self,source,target,name):
        super(AtomicMorphism,self).__init__(source,target)
        self.name = name
        self.diagram.addMorphi(self)
    
    def __repr__(self):
        return self.name
    
    def id(self):
        return self.name
    
    def __eq__(self,morphi):
        if not isinstance(morphi,AtomicMorphism):
            return morphi==self
        if morphi.name==self.name and morphi.target == self.target and morphi.source == self.source:
            return True
        return False
    
    def __neq__(self,morphi):
        return not self==morphi

def isWellDefined(ListOfMorphisms):
    n = len(ListOfMorphisms)
    for i in xrange(n-1):
        if not ListOfMorphisms[i]<ListOfMorphisms[i+1]:#source of i==target of i+1
            return False
    return True

def processInputMorphisms(args):
    #takes different sorts of user input and makes it into 
    #a list of morphisms that represent a (possibly composed) morphism
    if len(args)==3 and isinstance(args[0],Object) and isinstance(args[1],Object) and isinstance(args[2],str):
        args=[AtomicMorphism(*args)]
        
    if len(args)==0:
        raise ValueError
    
    morphilist = []
    for arg in args:
        if isinstance(arg,AbstractMorphism):
            morphilist.append(arg)
    
        elif isinstance(arg,list):
            morphilist+=arg
        
    if not isWellDefined(morphilist):
        msg = "List not welldefined: "+"".join(str(morphi.source)+"->"+str(morphi.target)+"  ," for morphi in morphilist)
        raise ValueError,msg
    return morphilist

class Morphism(AbstractMorphism):
    def __init__(self, *args):
        '''
        Datastructure to represent Morphisms in a Diagram
        user-friendliness: accept different sorts of input, namely:
            1) Morphism(Object 1,Object 2,Name of Morphism)
            2) Morphism([List of Morphisms])
        '''
        
        morphilist = processInputMorphisms(args)
        
        source = morphilist[-1].source
        target = morphilist[0].target
        
        super(Morphism,self).__init__(source,target)
        
        #create list of constituting user-defined Morphisms
        self.Composition = []
        for morphi in morphilist:
            if isinstance(morphi,Identity):
                pass
            elif isinstance(morphi,AtomicMorphism):
                self.Composition.append(morphi)
            elif isinstance(morphi,Morphism):
                self.Composition += morphi.Composition
            else:
                raise ValueError
                
        if self.Composition==[] and source==target:
            self.Composition=Identity(target)
        
        
    def length(self):
        return len(self.Composition)
    
    def id(self):
        return tuple([m.name for m in self.Composition])
    
    def __eq__(self,morphi):
        
        if not isinstance(morphi,Morphism):
            raise ValueError
            morphi = Morphism(morphi)
        
        #technically the same thing
        if self.id() == morphi.id():
            return True

        #known to commute
        if self.diagram.commutes(self,morphi):
            return True
    
    def __neq__(self,morphi):
        return not self==morphi
    
    def __repr__(self):
        s = "".join(c.__repr__()+"*" for c in self.Composition)
        s=s[:-1]
        s+=":"
        s+=str(self.source)
        s+="".join(" -> "+str(c.target) for c in reversed(self.Composition))
        return s

class Identity(Morphism):
    def __init__(self,o):
        super(Morphism,self).__init__(o,o)
        self.obj = o
        self.diagram = o.diagram
        self.Composition=[]
        self.name = "id_"+self.obj.name
    def id(self):
        return (self.obj.name,)
    def compose(self,g):
        assert g.target == self.obj
        return g
    def __repr__(self):
        return "id_"+self.obj.name
    
