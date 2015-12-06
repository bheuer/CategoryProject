from Property import ProductProperty, Monomorphism, Epimorphism, Projective, Injective, CoProductProperty
from Diagram import Morphism,Object,Commute,Distinct,Identity
from base import RuleGenerator
from Homomorphism.base import Homomorphism

class ExistIdentity(RuleGenerator):
    def CharacteristicDiagram(self,CD):
        Object(CD,"A")
    
    def conclude(self,CD):
        Identity(CD["A"])

class ExistProduct(RuleGenerator):
    def CharacteristicDiagram(self,CD):
        self.A = Object(CD,"A")
        self.B = Object(CD,"B")
    
    def conclude(self,CD):
        A = CD["A"]
        B = CD["B"]
        AxB = Object(CD,"AxB")
        AxB.namescheme=('{}x{}',('A','B')) #this should be a pair (format string,tuple of names in chardiag), names from main diagram will be substitued when rule is implemented
        AxB.latexscheme=('{} \\times {}',('A','B'))
        pi1 = Morphism(AxB,A,"pi1")
        pi2 = Morphism(AxB,B,"pi2")
        pi1.latexscheme=('',())                  #suppress morphism name display
        pi2.latexscheme=('',())                  #suppress morphism name display

        ProductProperty(pi1,pi2)

class ProductRule(RuleGenerator):
    def CharacteristicDiagram(self,CD):
        '''
                N
           f  / : \  g
             |  P  |
             | / \ |
              A   B
        '''
        
        A = Object(CD,"A")
        B = Object(CD,"B")    
        P = Object(CD,"P")
        pi1 = Morphism(P,A,"pi1")
        pi2 = Morphism(P,B,"pi2")
        ProductProperty(pi1,pi2)
        
        N = Object(CD,"N")
        f = Morphism(N,A,"f")
        g = Morphism(N,B,"g")
    
    def conclude(self,D):
        phi = Morphism(D["N"],D["P"],"phi")
        Commute(D["f"],D["pi1"]*phi)
        Commute(D["g"],D["pi2"]*phi)

class CoProductRule(RuleGenerator):
    def CharacteristicDiagram(self,CD):
        '''
                N
           f  / : \  g
             |  P  |
             | / \ |
              A   B
        '''
        
        A = Object(CD,"A")
        B = Object(CD,"B")    
        P = Object(CD,"P")
        i1 = Morphism(A,P,"pi1")
        i2 = Morphism(B,P,"pi2")
        CoProductProperty(i1,i2)
        
        N = Object(CD,"N")
        f = Morphism(A,N,"f")
        g = Morphism(B,N,"g")
    
    def conclude(self,D):
        phi = Morphism(D["P"],D["N"],"phi")
        phi.namescheme=("{} x {}",("f","g"))
        phi.latexscheme=("{} \\oplus {}",("f","g"))
        Commute(D["f"],phi*D["i1"])
        Commute(D["g"],phi*D["i2"])
        

class ProjectiveUP(RuleGenerator):
    def CharacteristicDiagram(self,CD):
        '''P -f-> C
            /    /|\
             \   /|\
              \   |
               !  pi
                \ |
                 \|
                  B'''
        B = Object(CD,"B")
        C = Object(CD,"C")
        P = Object(CD,"P")
        f = Morphism(P,C,"f")
        pi= Morphism(B,C,"pi")
        Epimorphism(pi)
        Projective(P)

    def conclude(self,D):
        ftilde=Morphism(D['P'],D['B'])
        ftilde.namescheme=("{}tilde",("f"))
        ftilde.latexscheme=("\\tilde\{{}\}",("f"))
        Commute(D["f"],D["pi"]*ftilde)

class InjectiveUP(RuleGenerator):
    def CharacteristicDiagram(self,CD):
        '''I <-f- A
            .-    |
            |\    |
              \   |
               !  iota
                \ |
                 \|/
                  B'''
        B = Object(CD,"B")
        A = Object(CD,"A")
        I = Object(CD,"I")
        f = Morphism(A,I,"f")
        iota= Morphism(A,B,"iota")
        Monomorphism(iota)
        Injective(I)

    def conclude(self,D):
        ftilde=Morphism(D['B'],D['I'])
        ftilde.namescheme=("{}tilde",("f"))
        ftilde.latexscheme=("\\tilde\{{}\}",("f"))
        Commute(D["f"],ftilde*D['iota'])
            
class ExplicitCompositionRule(RuleGenerator):
    def CharacteristicDiagram(self,CD):
        '''
        A --f-> B --g-> C
        \            ""/|
         \            / |
          \          /
           *--g*f---*
        '''
        A=Object(CD,'A')
        B=Object(CD,'B')
        C=Object(CD,'C')
        Morphism(A,B,'f')
        Morphism(B,C,'g')

    def conclude(self,D):
        gof=Morphism(D['A'],D['C'])
        gof.latexscheme=("{} \\circ {}",('g','f'))
        gof.namescheme=("{} o {}",('g','f'))
        Commute(D["g"]*D['f'],gof)
        
class ProductRuleUnique(RuleGenerator):
    def CharacteristicDiagram(self,CD):
        '''
                N
              /| | \  
           f | | | | g
             |  P  |
             | / \ |
              A   B
        '''
        
        A = Object(CD,"A")
        B = Object(CD,"B")    
        P = Object(CD,"P")
        pi1 = Morphism(P,A,"pi1")
        pi2 = Morphism(P,B,"pi2")
        ProductProperty(pi1,pi2)
        
        N = Object(CD,"N")
        f = Morphism(N,A,"f")
        g = Morphism(N,B,"g")
        phi1 = Morphism(N,P,"phi1")
        phi2 = Morphism(N,P,"phi2")
        
        Commute(pi1*phi1,f)
        Commute(pi1*phi2,f)
        Commute(pi2*phi1,g)
        Commute(pi2*phi2,g)
        
        
        Distinct(phi1,phi2) # makes sure the RuleMaster doesn't get excited about phi1 commuting with itself
    
    def conclude(self,D):
        Commute(D["phi2"],D["phi1"])
