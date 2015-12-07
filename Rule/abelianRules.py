from Diagram import *
from base import RuleGenerator
from abelian import AbelianCategory
from Rule.abelian import ZeroMorphism, NonZeroMorphism, Kernel, ZeroObject,\
    SetEqualZero

class InitialExistRuleGenerator(RuleGenerator):
    category = AbelianCategory
    def CharacteristicDiagram(self, CD):
        Object(CD,"A")
    def conclude(self,CD):
        f = Morphism(CD["0"],CD["A"],"0A")
        ZeroMorphism(f)

class FinalExistRuleGenerator(RuleGenerator):
    category = AbelianCategory
    def CharacteristicDiagram(self, CD):
        Object(CD,"A")
    def conclude(self,CD):
        f = Morphism(CD["A"],CD["0"],"A0")
        ZeroMorphism(f)

class InitialUniqueRuleGenerator(RuleGenerator):
    category = AbelianCategory
    def CharacteristicDiagram(self, CD):
        A = Object(CD,"A")
        m1 = Morphism(CD["0"],A,"m1")
        m2 = Morphism(CD["0"],A,"m2")
        Distinct(m1,m2)
        
    def conclude(self,CD):
        Commute(CD["m1"],CD["m2"])

class FinalUniqueRuleGenerator(RuleGenerator):
    category = AbelianCategory
    def CharacteristicDiagram(self, CD):
        A = Object(CD,"A")
        m1 = Morphism(A,CD["0"],"m1")
        m2 = Morphism(A,CD["0"],"m2")
        Distinct(m1,m2)
        
    def conclude(self,CD):
        Commute(CD["m1"],CD["m2"])

class KernelExistRuleGenerator(RuleGenerator):
    category = AbelianCategory
    def CharacteristicDiagram(self, CD):
        A = Object(CD,"A")
        B = Object(CD,"B")
        f = Morphism(A,B,"f")
        NonZeroMorphism(f)
        
    def conclude(self,CD):
        K = Object(CD,"ker_f")
        K.namescheme=('ker_{}',('f'))
        iker = Morphism(K,CD["A"])
        iker.namescheme=('i_ker_{}',('f'))
        Kernel(CD["f"],iker)
        ZeroMorphism(CD["f"]*iker)
        
class KernelUniversalRuleGenerator(RuleGenerator):
    category = AbelianCategory
    def CharacteristicDiagram(self, CD):
        '''         f
        kerf --> A --> B
                 |   /
              g  |  / 0 
                 C /
                  
        
        '''
        
        A = Object(CD,"A")
        B = Object(CD,"B")
        K = Object(CD,"K")
        f = Morphism(A,B,"f")
        iker = Morphism(K,A,"ker_f")
        Kernel(f,iker)
        
        C = Object(CD,"C")
        g = Morphism(C,A,"g")
        NonZeroMorphism(g)
        
        SetEqualZero(f*g)
    
    def conclude(self,CD):
        m = Morphism(CD["C"],CD["K"])
        m.namescheme = ('m_{}~',('g'))
        g = CD["g"]
        iker = CD["ker_f"]
        Commute(g,iker*m)

class KernelUniqueRuleGenerator(RuleGenerator):
    category = AbelianCategory
    def CharacteristicDiagram(self, CD):
        
        '''             f
            kerf --> A --> B
                \\   |   /
       phi1,phi2 \\  |  / 0 
                  \\ C /
                  
        
        '''
        A = Object(CD,"A")
        B = Object(CD,"B")
        K = Object(CD,"K")
        f = Morphism(A,B,"f")
        iker = Morphism(K,A,"ker_f")
        Kernel(f,iker)
        
        C = Object(CD,"C")
        g = Morphism(C,A,"g")
        NonZeroMorphism(g)
        
        phi1 = Morphism(C,K,"phi1")
        phi2 = Morphism(C,K,"phi2")
        Distinct(phi1,phi2)
        
        Commute(g,iker*phi2)
        Commute(g,iker*phi1)
    
    def conclude(self,CD):
        Commute(CD["phi1"],CD["phi2"])

def isMorphismZero(m):
    A = m.source
    B = m.target
    if isinstance(A,ZeroObject) or isinstance(B,ZeroObject):
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

FinalExistRule = FinalExistRuleGenerator()()
InitialExistRule = InitialExistRuleGenerator()()
FinalUniqueRule = FinalUniqueRuleGenerator()()
InitialUniqueRule = InitialUniqueRuleGenerator()()
KernelExistRule = KernelExistRuleGenerator()()
KernelUniversalRule = KernelUniversalRuleGenerator()()
KernelUniqueRule = KernelUniqueRuleGenerator()()
abelianRules = [InitialExistRule,FinalExistRule,InitialUniqueRule,FinalUniqueRule,\
                KernelExistRule,KernelUniversalRule,KernelUniqueRule]
