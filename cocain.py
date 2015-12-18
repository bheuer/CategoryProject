from Diagram import *
from Diagram.Morphisms import AbstractMorphism
from Homomorphism import HomomorphismIterator
from Property import *
from Property.base import PropertyTag
from Solver import RuleMaster
import unittest
from Property.TestPrioritiser import CustomRuleWeight_MaxObjectPlusMaxMorphismPrioritiser
from Solver.Prioritiser import UltimateWeightPriotiser
from Rule import EpimorphismRule, MonomorphismRule, ExistIdentity,\
    ProductRuleUnique, CoProductRuleUnique, FibreProductRuleUnique, FibreProductRule, AbelianRules
from Rule.Compose import ComposeRule
from Rule.abelianProperty import AbelianCategory, Kernel, GiveZeroMorphism,isMorphismZero,\
    Exact, reprWithoutZeros, getCokernel, getKernel, iterNonZeroMorphisms,\
    isIsomorphism