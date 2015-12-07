
class Category:
    def __init__(self,SpecialObjects,Rules,name):
        self.SpecialObjects= SpecialObjects
        self.Rules = Rules
        self.name = name
    def __eq__(self,cat):
        return self.name==cat.name
    def __ne__(self,cat):
        return not self==cat

GenericCategory = Category([],[],"generic")