''' All Morphisms the user deals with are defined by the Morphism class.
Internally, though, the Morphism class stores morphisms as series of so 
called AbstractMorphisms, which correspond to the arrows that you would 
draw in a diagram. For instance, the diagram

           f     g
        A --> B --> C

has two AbstractMorphisms, corresponding to f and g, but three Morphisms, namely 

f   with composition series  [Abstract(f)]
f   with composition series  [Abstract(g)]
g*f with composition series  [Abstract(g),Abstract(f)]

(and it fact three more if we count identity morphisms which all have empty
composition series) This way, concepts like associativity are already inherent
to the data structure. Also, composition is easy to perform and is exposed to
the user via the * operator. Furthermore, Morphisms are hashed according to 
their composition series.

The following operations are defined for Morphisms class objects f and g:

g*f     :form the composition of f and g  
g==f    :asks whether f and g are known to commutate (note however that this is been taken
         care of by the Diagram class.)
g!=f    :asks whether f and g are known not to commute. Also return True if undecisive
g//f    :asks whether g and f are aligned, ie have same source & target
g<f     :asks whether the source of g is the target of f
g>f     :asks whether the source of f is the target of g
'''

from Object import Object

class AbstractMorphism(object):
    def __init__(self, source, target):
        self.source = source
        self.target = target
        
        if not  self.source.diagram == self.target.diagram:
            raise ValueError
        
        self.diagram  = self.source.diagram
    
    def compose(self,g,dry = False):
        if isinstance(g,Identity):
            return self
        c = Morphism([self,g],dry=True)
        for m in self.diagram.MorphismList:
            if m==c:
                return m
        return Morphism([self,g],dry=dry)
    
    def __mul__(self,g):
        return self.compose(g)
    
    def __lt__(self,morph):
        assert isinstance(morph,AbstractMorphism)
        return self.source==morph.target
    
    def __gt__(self,morph):
        return AbstractMorphism.__lt__(morph,self)
    
    def __floordiv__(self,morph):
        assert isinstance(morph,AbstractMorphism)
        return self.target==morph.target and self.source==morph.source
    

def isWellDefined(ListOfMorphisms):
    n = len(ListOfMorphisms)
    for i in xrange(n-1):
        if not ListOfMorphisms[i]<ListOfMorphisms[i+1]:#source of i==target of i+1
            return False
    return True

def processMorphilist(morphis):
    morphilist = []
    for arg in morphis:
        if isinstance(arg,Morphism):
            morphilist+=arg.Composition
        elif isinstance(arg,AtomicMorphism):
            morphilist.append(arg)
        elif isinstance(arg,list):
            morphilist+=processMorphilist(arg)
    return morphilist

def processInputMorphisms(*args,**kwargs):
    #Takes different sorts of user input and makes it into a list 
    #of morphisms that represent a (possibly composed) morphism.
    #Also makes clear that the morphism has a name which is unique
    #wrt to the diagram the morphism lives in
    if len(args)==0:
        raise ValueError,"empty input"
    elif all(i==[] for i in args):
        raise ValueError,"empty input"
    
    if "dry" in kwargs:
        dry = kwargs["dry"]
    else:
        dry = False
    
    if isinstance(args[-1],str):
        name = args[-1]
    elif "name" in kwargs:
        name = args[-1]
    else:
        name = None
    
    if name is not None and "*" in name:
        if not ("(" in name and ")" in name and name.index("*")>name.index("(") and  name.index("*")<name.index(")")):
            raise ValueError,(args,kwargs)
            raise ValueError,"name must not contain the symbol '*'. Seriously, I want to be nice to you and I just can't if you use it."
    
    if len(args)>=2 and isinstance(args[0],Object) and isinstance(args[1],Object):
        o1,o2 = args[0], args[1]
        if name is None:
            name = o1.diagram.giveName(mode = "m")
        args=[AtomicMorphism(o1,o2,name)]
    
    morphilist = processMorphilist(args)
    
    if not isWellDefined(morphilist):
        msg = "List not welldefined: "+"".join(str(morphi.source)+"->"+str(morphi.target)+"  ," for morphi in morphilist)
        raise ValueError,msg
    
    if name is None:
        name = "*".join(morphi.name for morphi in morphilist)
    
    return morphilist,name,dry

class AtomicMorphism(AbstractMorphism):
    def __init__(self,source,target,name):#name is not default for atomics, a valid name must be given
        AbstractMorphism.__init__(self,source,target)
        self.name = name
           
    def __repr__(self):
        return self.name
    
    def __eq__(self,morphi):
        assert isinstance(morphi,AtomicMorphism)
        if morphi.name==self.name and morphi.target == self.target and morphi.source == self.source:
            return True
        return False
    
    def __neq__(self,morphi):
        return not self==morphi

class Morphism(AbstractMorphism):
    '''
        Datastructure to represent Morphisms in a Diagram
        
        accepts different sorts of input, namely:
            1) Morphism(Object 1,Object 2, Str Name of Morphism)
            2) Morphism(Object 1,Object 2)
            3) Morphism([Morphism 1, ...])
            4) Morphism(Morphism 1, ...)
        '''
    
    def __init__(self, *args, **kwargs):
        morphilist,name,dry = processInputMorphisms(*args,**kwargs)
        self.name = name
        source = morphilist[-1].source
        target = morphilist[0].target
        
        AbstractMorphism.__init__(self,source,target)
        
        if not dry: 
            assert name not in self.diagram.UNIVERSE,(name,self.diagram.MorphismNames)
        
        #create list of constituting user-defined Morphisms
        self.Composition = []
        for morphi in morphilist:
            if isinstance(morphi,Identity):
                pass
            elif isinstance(morphi,AtomicMorphism):
                self.Composition.append(morphi)
            else:
                raise ValueError
                
        if self.Composition==[]:
            assert source==target
        
        #this is pretty expensive, so cache value for later use in __hash__
        self.hashvalue = hash((self.source,self.target,tuple([m.name for m in self.Composition])))
        if not dry:
            self.diagram.addMorphi(self)
    
    def id(self):
        raise DeprecationWarning
        raise NotImplementedError
    
    def __hash__(self):
        return self.hashvalue
    
    def __eq__(self,morphi):
        if not isinstance(morphi,Morphism):
            raise ValueError
        
        if not self // morphi:
            return False
        
        #technically the same thing
        if len(self.Composition)==len(morphi.Composition):#this is a bit more efficient. Profilin said better optimise.
            if all(m1.name==m2.name for m1,m2 in zip(self.Composition,morphi.Composition)):
                return True

        #known to commute
        if self.diagram.commutes(self,morphi):
            return True
    
    def __ne__(self,morphi):
        return not self.__eq__(morphi)
    
    def iterComposingMorphisms(self):
        for i in self.Composition:
            yield self.diagram[i.name]
    
    def iterPartialMorphisms(self):
        #iter all constituting partitions of self into three morphisms end*partial*star
        l = len(self.Composition)
        
        for i0 in xrange(l):
            if i0==0:
                end = Identity(self.target,dry=True)
            else:
                end = Morphism(self.Composition[:i0],dry = True)
            
            yield end,Identity(end.source,dry = True),Morphism(self.Composition[i0:],dry = True)
            
            for i1 in xrange(i0+1,l+1):
                if i0==0 and i1==l:continue
                partial = Morphism(self.Composition[i0:i1],dry = True)
                
                if i1==l:
                    start = Identity(self.source,dry=True)
                else:
                    start = Morphism(self.Composition[i1:],dry = True)
                yield end,partial,start
    
    def equivalenceClass(self):
        return getImage(self,self.diagram.CommutativityQuotient)
    
    def __repr__(self):
        s = "".join(c.__repr__()+"*" for c in self.Composition)
        s=s[:-1]
        s+=":"
        s+=str(self.source)
        s+="".join(" -> "+str(c.target) for c in reversed(self.Composition))
        return s

class Identity(Morphism):
    def __init__(self,o,dry = False):
        if "*" in o.name:
            self.name = "id_("+o.name+")"
        else:
            self.name = "id_"+o.name # should be tested for safety
        self.obj = o
        Morphism.__init__(self,o,o,self.name,dry=dry)
        self.diagram = o.diagram
        self.Composition=[]
    def id(self):
        return ()
    def compose(self,g,dry=None):
        assert g.target == self.obj
        return g
    def __repr__(self):
        return "id_"+self.obj.name


def getIdentity(A):
    id_ = A.diagram["id_"+A.name]
    if id_ is None:
        A.diagram["id_("+A.name+")"]
    if id_ is None:
        return Identity(A)
    return id_

def getImage(morph,hom):
    res = hom.get_edge_image(morph)
    if res is not None:
        return res
    if isinstance(morph,Identity):
        return getIdentity(hom[morph.source])