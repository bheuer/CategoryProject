from Morphisms import Morphism
from Homomorphism import Homomorphism
import itertools

def pairwise(iterable):#from http://stackoverflow.com/questions/5434891/iterate-a-list-as-pair-current-next-in-python
        a, b = itertools.tee(iterable)
        next(b, None)
        return itertools.izip(a, b)

class Commute:
    def __init__(self,*args):
        # check that all arguments are morphisms and aligned
        if not (len(args)>0 and all(isinstance(i,Morphism) for i in args)):
            raise ValueError,"input must be a list of Morphisms"
        if not pairwise(a//b for a,b in pairwise(args)):
            raise ValueError,"commuting morphisms must be aligned, ie have same source and target"
        
        self.MorphiList = args
        diagram = args[0].diagram
        diagram.addProperty(self)
        morph0 = self.MorphiList[0]
        for i in xrange(1,len(self.MorphiList)):
            morph = self.MorphiList[i]
            assert morph // morph0
            diagram.unify(morph0,morph)
    
    def push_forward(self,hom):
        assert isinstance(hom, Homomorphism)
        print [hom.get_edge_image(morph) for morph in self.MorphiList]
        return Commute(*(hom.get_edge_image(morph) for morph in self.MorphiList))
    
    def __repr__(self):
        str_ = "Property 'commute' for the following morphisms:\n"
        for morph in self.MorphiList:
            str_+="{}\n".format(morph)
        return str_

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