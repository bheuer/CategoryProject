import rule
import inspect
from base import Rule,RuleGenerator

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