
if False:#__name__ == "__main__":
    def test1():
        '''
        D1
        
           f      g
        A ---> B ---> C
                
                
        D2        
               X2 
               |  F2
               |  
           F   V  G
        X ---> Y ---> Z
         <---  |    
          G2   | id
               Y
           
        '''
        
        D1 = Diagram()
        D2 = Diagram()
        
        A = Object(D1,"A")
        B = Object(D1,"B")
        C = Object(D1,"C")
        Morphism(A,B,"f")
        Morphism(B,C,"g")
        
            
        X = Object(D2,"X")
        Y = Object(D2,"Y")
        Z = Object(D2,"Z")
        X2 = Object(D2,"X2")
        
        Morphism(X,Y,"F")
        Morphism(Y,Z,"G")
        Morphism(Y,Y,"id")
        Morphism(X2,Y,"F2")
        Morphism(Y,X,"G2")
        
        homiter = HomomorphismIterator(D1,D2)
        for hom in homiter:
            print hom
            
    def test2():
            '''
            D1
            
               f      
            A ---> B
             <\    / g
           h  \   /     
               C<-  
                 
            D2        
                   
               F      
            X ---> Y
             <\    / G
           H  \   /     
               Z<-
               |
               | id
               Z
                 
            '''
            
            D1 = Diagram()
            D2 = Diagram()
            
            A = Object(D1,"A")
            B = Object(D1,"B")
            C = Object(D1,"C")
            Morphism(A,B,"f")
            Morphism(B,C,"g")
            Morphism(C,A,"h")
            
                
            X = Object(D2,"X")
            Y = Object(D2,"Y")
            Z = Object(D2,"Z")
            
            Morphism(X,Y,"F")
            Morphism(Y,Z,"G")
            Morphism(Z,X,"H")
            Morphism(Z,Z,"idZ")
            
            homiter = HomomorphismIterator(D1,D2)
            for hom in homiter:
                print hom
        
    def test3():
            '''
            D1
            
               f      
            A ---> B
               
            
            D2        
               
               F     
            X --->Y
          G |
            V
            Z
                 
            '''
            
            D1 = Diagram()
            D2 = Diagram()
            
            A = Object(D1,"A")
            B = Object(D1,"B")
            f = Morphism(A,B,"f")
            
                
            X = Object(D2,"X")
            Y = Object(D2,"Y")
            Z = Object(D2,"Z")
            
            F = Morphism(X,Y,"F")
            G = Morphism(X,Z,"G")
            
            homiter = HomomorphismIterator(D1,D2)
            c = 0
            for hom in homiter:
                print hom
                c+=1
            assert c==2
            
            print "declare Epimorphisms"
            Epimorphism(f)
            Epimorphism(F)
            print D1.InverseLookUp[f]
            print D2.InverseLookUp[F]
            
            homiter = HomomorphismIterator(D1,D2)
            c=0
            for hom in homiter:
                print hom
                c+=1
            assert c==1
            
            #test Properties hashable and hash only checks function, not id
            p = PropertyTag(ProductProperty(F,G),2,3)
            q = PropertyTag(ProductProperty(F,G),2,4)
            P = set([p])
            Q = set([q])
            assert P.issubset(Q)