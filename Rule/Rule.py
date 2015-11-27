from Property import ProductProperty
from Diagram import Morphism,Object,Commute,Distinct,Identity
from base import RuleGenerator

class ExistIdentity(RuleGenerator):
    def CharacteristicDiagram(self,CD):
        A = Object(CD,"A")
    
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
        pi1 = Morphism(AxB,A,"pi1")
        pi2 = Morphism(AxB,B,"pi2")
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