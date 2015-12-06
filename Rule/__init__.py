import inspect
from base import Rule,RuleGenerator
from rule import *
from abelian import *
from abelianRules import *
import rule

for name, cls in inspect.getmembers(rule):
    if inspect.isclass(cls) and issubclass(cls, RuleGenerator):
        if cls is RuleGenerator:
            continue # AbstractBaseClass
        clsname = cls.RuleName
        if clsname is None:
            clsname = cls.__name__
            if clsname.endswith("Generator"):
                clsname = clsname[:-9]
        
        exec(clsname+"= cls()()")
        
        #print eval(clsname)