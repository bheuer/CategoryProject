from Diagram.Commute import Commute
from collections import defaultdict


def ImObjectIndex(o,ER):
    return ER.mainDiag.Objects.index(o)
def ImMorphismIndex(f,ER):
    return ER.mainDiag.MorphismList.index(f)

def newObjectIndex(o,ER):
    #o is in the extension of the ER
    if ER.rule.partialInverse.is_defined_on_node(o):
        o_ = ER.rule.partialInverse[o]
        return ImObjectIndex(ER.hom[o_],ER)
    else:
        return len(ER.mainDiag.Objects)+ER.rule.newObjects.index(o)

def newMorphismIndex(f,ER):
    #o is in the extension of the ER
    if ER.rule.partialInverse.is_defined_on_edge(f):
        f_ = ER.rule.partialInverse.get_edge_image(f)
        return ImMorphismIndex(ER.hom[f_],ER)
    else:
        return len(ER.mainDiag.MorphismList)+ER.rule.newMorpshisms.index(f)

def newMorphismWeight(f,ER):
    return 30+0.5*(newObjectIndex(f.source,ER)+newObjectIndex(f.target, ER))
    
def newObjectWeight(ER):
    return 50+len(ER.mainDiag.Objects)
    
def newPropertyWeight(prop,ER):
    if isinstance(prop,Commute):
        return prop.weight
    hom = prop.homomorphism
    m1 = max(newMorphismWeight(hom.get_edge_image(f),ER) for f in prop.charDiagram.MorphismList)
    m2 = max(newObjectIndex  (hom.get_node_image(o),ER) for o in prop.charDiagram.Objects)
    return 0.1*(m1+m2)+prop.weight

def maxdef(iterator, default):
    max_ = default
    for i in iterator:
        max_ = max(max_,i)
    return max_

def ImMorphismWeight(ER):
    return maxdef((ImMorphismIndex(ER.hom.get_edge_image(f),ER) for f in ER.charDiag.MorphismList),0)

def ImObjectWeight(ER):
    return maxdef((ImObjectIndex(ER.hom.get_node_image(o),ER) for o in ER.charDiag.Objects),0)


Weights = defaultdict(int,{ \
                       "ProductRule":0,\
                       "ExistProduct":10,\
                       "ProductRuleUnique":-30,\
                       "ExistIdentity":-100\
                       })

def RuleWeight(ER):
    return Weights[ER.rule.name]

def UltimateWeightPriotiser(ER):
    weight = 0
    for o in ER.rule.newObjects:
        weight+=newObjectWeight(ER)
        
    for f in ER.rule.newMorphisms:
        weight+=newMorphismWeight(f,ER)
    
    for p in ER.rule.newProperties:
        weight+=newPropertyWeight(p,ER)
    
    weight+=ImMorphismWeight(ER)
    weight+=ImObjectWeight(ER)
    weight+=RuleWeight(ER)
    return weight