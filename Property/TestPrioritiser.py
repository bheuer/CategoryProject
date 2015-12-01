NoPriority = lambda ER:0

def MaxObjectPriority(ER):
    Max = -1
    for _,image in ER.hom.iterNodes():
        if image is not None:
            Max = max(Max,ER.hom.D2.Objects.index(image))
    return Max    


def NewTypePriority(ER):
    ER.newObjects
    ER.newMorphisms


def MaxMorphismPriority(ER):
    Max = -1
    for _,image in ER.hom.iterEdges():
        if image is not None:
            Max = max(Max,ER.hom.D2.MorphismList.index(image))
    return Max
    
def MaxObjectPlusMaxMorphismPriority(ER):
    return MaxMorphismPriority(ER)+MaxObjectPriority(ER)
    
Weights = {"ProductRule":1,"ExistProduct":2,"ProductRuleUnique":0,"ExistIdentity":1}
def CustomRuleWeight_MaxObjectPrioritiser(ER,weights = Weights): #careful with default value, I know, but this should work
    return (MaxObjectPriority(ER),Weights[ER.rule.name])
    
def CustomRuleWeight_MaxObjectPlusMaxMorphismPrioritiser(ER,weights = Weights): #careful with default value, I know, but this should work
    return (MaxObjectPlusMaxMorphismPriority(ER),Weights[ER.rule.name])
