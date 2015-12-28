import inspect
from base import Rule,RuleGenerator
from rule import *
from abelianProperty import *
from abelianRules import *
import rule
import abelianRules
from Rule.Compose import ComposeRule

GenericRules = [ComposeRule]
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
        rule = eval(clsname)
        if rule.generic:#holds in arbitrary Categories
            GenericRules.append(rule)

AbelianRules = [ComposeRule] #don't add GenericRules
try:AbelianRules.append(ExistIdentity)
except NameError:pass

for name, cls in inspect.getmembers(abelianRules):
    if inspect.isclass(cls) and issubclass(cls, RuleGenerator):
        if cls is RuleGenerator:
            continue # AbstractBaseClass
        clsname = cls.RuleName
        if clsname is None:
            clsname = cls.__name__
            if clsname.endswith("Generator"):
                clsname = clsname[:-9]
        
        exec(clsname+"= cls()()")
        AbelianRules.append(eval(clsname))
