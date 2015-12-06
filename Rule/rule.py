from Property import ProductProperty
from Diagram import Morphism,Object,Commute,Distinct,Identity
from base import RuleGenerator
from Homomorphism.base import Homomorphism
from Property.Property import Monomorphism

class ExistIdentityGenerator(RuleGenerator):
    RuleName = "ExistIdentity"
    def CharacteristicDiagram(self,CD):
        Object(CD,"A")
    
    def conclude(self,CD):
        Identity(CD["A"])

class ExistProductGenerator(RuleGenerator):
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

class ProductRuleGenerator(RuleGenerator):
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
        

    
        
class ProductRuleUniqueGenerator(RuleGenerator):
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


class EpimorphismRuleGenerator(RuleGenerator):
    def CharacteristicDiagram(self,CD):
        ''' 
                g1
           f   ---->
        A --> B     C
               ---->
                g2
        '''
        A = Object(CD,"A")
        B = Object(CD,"B")
        C = Object(CD,"C")
        f = Morphism(A,B,"f")
        Monomorphism(f)
        g1 = Morphism(B,C,"g1")
        g2 = Morphism(B,C,"g2")
        Distinct(g1,g2)
        Commute(g1*f,g2*f)
    
    def conclude(self,CD):
        g1 = CD["g1"]
        g2 = CD["g2"]
        Commute(g1,g2)

class MonomorphismRuleGenerator(RuleGenerator):
    def CharacteristicDiagram(self,CD):
        ''' 
           f1
          ---->
         A     B --> C
          ---->
           f2
        '''
        A = Object(CD,"A")
        B = Object(CD,"B")
        C = Object(CD,"C")
        f1 = Morphism(A,B,"f1")
        f2 = Morphism(A,B,"f2")
        g = Morphism(B,C,"g")
        Monomorphism(g)
        Distinct(f1,f2)
        Commute(g*f1,g*f2)
    
    def conclude(self,CD):
        f1 = CD["f1"]
        f2 = CD["f2"]
        Commute(f1,f2)
        
#this is just so that Ben's IDE knows what they are
#IDEs don't read execs
        
MonomorphismRule = MonomorphismRuleGenerator()()
EpimorphismRule  = EpimorphismRuleGenerator()()
ProductRule = ProductRuleGenerator()()
ExistProduct = ExistProductGenerator()()
