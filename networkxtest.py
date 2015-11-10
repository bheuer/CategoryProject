from networkx import *
import networkx
from Objects import Object
from Diagram import *

D = Diagram()
A1 = Object(D,"A1")
A2 = Object(D,"A2")
B1 = Object(D,"B1")
B2 = Object(D,"B2")

f1 = Morphism(A1,A2,"f1")
g1 = Morphism(A1,B1,"g1")
g2 = Morphism(A2,B2,"g2")
h1 = Morphism(B1,B2,"h1")

f1.epim = False
g1.epim = False
g2.epim = True
h1.epim = False

G = D.Graph
print G.nodes()
print G.edges()

D_ = Diagram()
C1 = Object(D_,"C1")
C2 = Object(D_,"C2")
C3 = Object(D_,"C3")

m = Morphism(C1,C2,"m")
m.epim = False

l = Morphism(C2,C3,"l")
l.epim = True

H = D_.Graph
H.add_edge(C1,C2,object = m)
H.add_edge(C2,C3,object = l)
print H.edges(data=True)

#print GM = iso.GraphMatcher(B,A,node_match=iso.categorical_node_match(['material', 'size'],['metal',1]))

print G.nodes()
def g(x,y):
    return True
    return (x.epim==y.epim)

for J,D in D.iterateIsomorphicSubdiags(H,g):
    print D
    print J.nodes()
    print J.edges(data=True)