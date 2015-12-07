'''
*say something about how commutativity is implemented*

commutativity check should be O(1), so we do an expensive update of all commutativity results every tim
    1) a new commutativity result is added
    2) a new morphism is added

'''


from Morphisms import Morphism, AbstractMorphism,Identity
from Homomorphism import Homomorphism
import itertools
from itertools import product


def pairwise(iterable):#from http://stackoverflow.com/questions/5434891/iterate-a-list-as-pair-current-next-in-python
        a, b = itertools.tee(iterable)
        next(b, None)
        return itertools.izip(a, b)

class Commute:
    weight = -30
    name = "Commute"
    def __init__(self,*args):
        # check that all arguments are morphisms and aligned
        if not (len(args)>0 and all(isinstance(i,AbstractMorphism) for i in args)):
            raise ValueError,"input must be a list of Morphisms"
        if not pairwise(a//b for a,b in pairwise(args)):
            raise ValueError,"commuting morphisms must be aligned, ie have same source and target"
        
        self.MorphiList = []
        for m in args:
            if isinstance(m,CommutingMorphismEquivalenceClass):
                #self.MorphiList.append(m.representative)
                self.MorphiList+=list(m.Morphisms)
            else:
                self.MorphiList.append(m)
            
        #self.MorphiList = [(m.representative if isinstance(m,CommutingMorphismEquivalenceClass) else m) for m in args]
        diagram = args[0].diagram
        diagram.addProperty(self)
        morph0 = self.MorphiList[0]
        for i in xrange(1,len(self.MorphiList)):
            morph = self.MorphiList[i]
            assert morph // morph0
            diagram.unify(morph0,morph)
        self.name='commute'             #I hope this is an appropriate name
    
    def push_forward(self,hom):
        assert isinstance(hom, Homomorphism)
        #print [hom.get_edge_image(morph) for morph in self.MorphiList]
        return Commute(*(hom.get_edge_image(morph) for morph in self.MorphiList))
    
    def __repr__(self):
        str_ = "Property 'commute' for the following morphisms:\n"
        for morph in self.MorphiList:
            str_+="{}\n".format(morph)
        return str_

class CommutingMorphismEquivalenceClass(AbstractMorphism):
    def __init__(self,*morphisms):
        #check input
        if not all(isinstance(m,Morphism) for m in morphisms):
            raise ValueError,"input must be a non-empty list of morphisms, but was: {}".format(morphisms)
        if not all(m1//m2 for m1,m2 in pairwise(morphisms)):
            raise ValueError,"morphisms must be aligned"
        
        #intialize abstract morphism
        m = morphisms[0]
        AbstractMorphism.__init__(self,m.source,m.target)
        
        #store defining data: the morphism list
        self.Morphisms = set(morphisms)
        self.representative = next(iter(self.Morphisms))
        self.PropertyTags = []
        for m in morphisms:
            self.PropertyTags+=m.diagram.getPropertyTags(m)
    
    def merge_with(self,CMEC):
        #morphism classes must be aligned
        assert self//CMEC
        m = self.representative #pick any representing morphism
        
        if m in CMEC.Morphisms:
            #same component already
            #better not copy it, otherwise the PropertyTags run over
            return
         
        self.Morphisms.update(CMEC.Morphisms)
        self.PropertyTags += CMEC.PropertyTags
    
    def __iter__(self):
        for m in self.Morphisms:
            yield m
    
    def compose(self,CC):
        if isinstance(CC.representative,Identity):
            return self
        return self.diagram.CommutativityQuotient.get_edge_image(self.representative*CC.representative)
       
    def __mul__(self,CC):
        return self.compose(CC)
    
    def __eq__(self,CC):
        if self is CC:#same object in memory: shortcut, this is faster
            return True
        
        #reason we need that: sometimes we store references to Commutativity classes, for
        #instance in extension requests. Then when to things are unified, one of the EqivalenceClass objects
        #is just "deprecated", ie the respective morphism is assigned another Equivalence Class
        #however, the reference still exists and is stored somewhere. This makes sure that if then
        #equality is checked for these old references, it is checked relative to the newest known commutativity
        return (self.representative.equivalenceClass() is CC.representative.equivalenceClass())
    
    def __ne__(self,CC):
        return not self.__eq__(CC)
    
    def __repr__(self):
        return str(list(self.Morphisms))
            
class Distinct:#says that at least two of the morphisms don't commute
    def __init__(self,*args):
        assert len(args)>0 and all(isinstance(i,Morphism) for i in args)
        self.MorphiList = args
        diagram = args[0].diagram
        diagram.addProperty(self)
    
    def push_forward(self,hom):
        pass

def commutes(*args):
    if len(args)==1:
        morphiList = args[0]
    else:
        morphiList = args
    
    return all(f==g for f,g in pairwise(morphiList))
