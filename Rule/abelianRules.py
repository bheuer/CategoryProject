from Diagram import *
from base import RuleGenerator
from Rule.abelianProperty import ZeroMorphism, Kernel, ZeroObject,\
    SetEqualZero, CoKernel, Exactness
from Rule.abelianProperty import GiveZeroMorphism, AbelianCategory
from Property.Property import Isomorphism, SetIsomorphism, IsNot


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

class ZeroMorphismExistRuleGenerator(RuleGenerator):
    category = AbelianCategory
    def CharacteristicDiagram(self, CD):
        A = Object(CD,"A")
        B = Object(CD,"B")
        IsNot(ZeroObject,A)
        IsNot(ZeroObject,B)
    def conclude(self,CD):
        f = Morphism(CD["A"],CD["B"])
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
        IsNot(ZeroMorphism,f)
        IsNot(Isomorphism,f)
        
    def conclude(self,CD):
        K = Object(CD,"ker_f")
        K.namescheme=('ker_({})',('f'))
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
        IsNot(ZeroMorphism,g)
        
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
        IsNot(ZeroMorphism,g)
        
        phi1 = Morphism(C,K,"phi1")
        phi2 = Morphism(C,K,"phi2")
        Distinct(phi1,phi2)
        
        Commute(g,iker*phi2)
        Commute(g,iker*phi1)
    
    def conclude(self,CD):
        Commute(CD["phi1"],CD["phi2"])

class CoKernelExistRuleGenerator(RuleGenerator):
    category = AbelianCategory
    def CharacteristicDiagram(self, CD):
        
        '''
            f
        A ---> B --> coker f
        '''
        
        A = Object(CD,"A")
        B = Object(CD,"B")
        f = Morphism(A,B,"f")
        IsNot(ZeroMorphism,f)
        IsNot(Isomorphism,f)
        
    def conclude(self,CD):
        coker_f = Object(CD,"coker_f")
        coker_f.namescheme=('coker_({})',('f'))
        pcoker_f = Morphism(CD["B"],coker_f)
        pcoker_f.namescheme=('i_ker_{}',('f'))
        CoKernel(CD["f"],pcoker_f)
        ZeroMorphism(pcoker_f*CD["f"])
        
class CoKernelUniversalRuleGenerator(RuleGenerator):
    category = AbelianCategory
    def CharacteristicDiagram(self, CD):
        '''
            f
        A ---> B --> coker f
               |   ;
             g V  ;  g~ 
               C
        
        
        '''
        
        A = Object(CD,"A")
        B = Object(CD,"B")
        f = Morphism(A,B,"f")
        
        coker_f = Object(CD,"coker_f")
        pcoker_f = Morphism(B,coker_f,"pcoker_f")
        
        CoKernel(f,pcoker_f)
        
        C = Object(CD,"C")
        g = Morphism(B,C,"g")
        IsNot(ZeroMorphism,g)
        
        SetEqualZero(g*f)
    
    def conclude(self,CD):
        m = Morphism(CD["coker_f"],CD["C"])
        m.namescheme = ('m_{}~',('g'))
        
        g = CD["g"]
        pcoker_f = CD["pcoker_f"]
        Commute(g,m*pcoker_f)

class CoKernelUniqueRuleGenerator(RuleGenerator):
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
        f = Morphism(A,B,"f")
        
        coker_f = Object(CD,"coker_f")
        pcoker_f = Morphism(B,coker_f,"pcoker_f")
        CoKernel(f,pcoker_f)
        
        C = Object(CD,"C")
        g = Morphism(B,C,"g")
        
        IsNot(ZeroMorphism,g)
        
        phi1 = Morphism(coker_f,C,"phi1")
        phi2 = Morphism(coker_f,C,"phi2")
        Distinct(phi1,phi2)
        
        Commute(g,phi2*pcoker_f)
        Commute(g,phi1*pcoker_f)
    
    def conclude(self,CD):
        Commute(CD["phi1"],CD["phi2"])

class ExactnessExistsIsomorphismRuleGenerator(RuleGenerator):
    category = AbelianCategory
    def CharacteristicDiagram(self, CD):
        
        '''        
                   psi 
        ker_coker_f--> ker g
                 \    /
               f  \  /  g  
            A ---> B ---> C
                   |
                   |
                 coker f
        
        '''
        A = Object(CD,"A")
        B = Object(CD,"B")
        C = Object(CD,"C")
        
        f = Morphism(A,B,"f")
        g = Morphism(B,C,"g")
        Exactness(f,g)
        
        
        ker_g = Object(CD,"ker_g")
        iker_g = Morphism(ker_g,B,"ikerg")
        Kernel(g,iker_g)
        
        coker_f = Object(CD,"coker_f")
        pcoker_f = Morphism(B,coker_f,"pcoker_f")
        CoKernel(f,pcoker_f)
        
        ker_pcoker_f = Object(CD,"ker_pcoker_f")
        iker_pcoker_f = Morphism(ker_pcoker_f,B,"iker_pcoker_f")
        Kernel(pcoker_f,iker_pcoker_f)
        
        psi = Morphism(ker_pcoker_f,ker_g,"psi")
        
        Commute(iker_g*psi,iker_pcoker_f)
    
    def conclude(self,CD):
        SetIsomorphism(CD["psi"])

FinalExistRule = FinalExistRuleGenerator()()
InitialExistRule = InitialExistRuleGenerator()()
FinalUniqueRule = FinalUniqueRuleGenerator()()
InitialUniqueRule = InitialUniqueRuleGenerator()()
KernelExistRule = KernelExistRuleGenerator()()
KernelUniversalRule = KernelUniversalRuleGenerator()()
KernelUniqueRule = KernelUniqueRuleGenerator()()
