class Grade:
    def __init__(self, rep, score):
        self.rep = rep
        self.score = score
    def __str__(self):
        return self.rep
    def __repr__(self):
        return 'Grade({},{})'.format(self.rep,self.score)



#These are the types used for describing various module attributes
class ModuleAttributes:
    def __str__(self):
        return __str_type(self)
class YearType(ModuleAttributes):
    pass
class ModuleType(ModuleAttributes):
    pass
class SuffixType(ModuleAttributes):
    pass


FOUNDATION,INTERMEDIATE,ADVANCED = YearType(),YearType(),YearType()
ELECTIVE,CORE,ENRICHMENT,HONOR = ModuleType(),ModuleType(),ModuleType(),ModuleType()
PRECLUSION,CORE_PREREQ,MT_IN_LIEU,EXTERNAL = SuffixType(),SuffixType(),SuffixType(),SuffixType()

#lists to be used for iteration if need be
YEAR_TYPES = [FOUNDATION, INTERMEDIATE, ADVANCED]
MODULE_TYPES = [ELECTIVE,CORE,ENRICHMENT,HONOR]
SUFFIX_TYPES = [PRECLUSION, CORE_PREREQ, MT_IN_LIEU, EXTERNAL]

MODULE_ATTRIBUTES = {'FOUNDATION':FOUNDATION, 'INTERMEDIATE':INTERMEDIATE, 'ADVANCED': ADVANCED,
                        'ELECTIVE':ELECTIVE, 'CORE':CORE, 'ENRICHMENT': ENRICHMENT, 'HONOR': HONOR,
                        'PRECLUSION':PRECLUSION, 'CORE_PREREQ':CORE_PREREQ, 'MT_IN_LIEU': MT_IN_LIEU,
                        'EXTERNAL':EXTERNAL}

def __str_type(cons):
    d = {FOUNDATION:'FOUNDATION',INTERMEDIATE:'INTERMEDIATE',ADVANCED:'ADVANCED',
    ELECTIVE:'ELECTIVE',CORE:'CORE',ENRICHMENT:'ENRICHMENT',HONOR:'HONOR',
    PRECLUSION:'PRECLUSION',CORE_PREREQ:'CORE_PREREQ',MT_IN_LIEU:'MT_IN_LIEU',EXTERNAL:'EXTERNAL'}
    return d[cons]



#Types used for non-numerical scores. Can be for da vinci, or for enrichment
# MERIT can be used for either da vinci or enrichment, so it subclasses both
#Using a special type for this is good practice.

#Implementation for comparison is needed for use cases such as telling whether
#one student scored better (ie a DISTINCTION is better than a MERIT in an
#enrichment module)
#this is done via special quantification functions which quantiy the constants
#quantified values can then be used for comparison
#another solution would have been to add an attribute that took an integer
#upon instantiation. May replace this with that
#Identical to the user, performance might be very slightly better
#A special solution is needed for MERIT, see the EitherGrade class

#Also, multiplication is also overriden
#This is for convenience - so you can multiple mc by score for all
#modules (for cap calculation purposes), without the davinci/enrichment modules throwing an error
#Will always return 0
class DaVinciGrade:
    def __gt__(self,other):
        return _quantify_dv_grades(self)>_quantify_dv_grades(other)
    def __lt__(self,other):
        return _quantify_dv_grades(self)<_quantify_dv_grades(other)
    def __le__(self,other):
        return _quantify_dv_grades(self)<=_quantify_dv_grades(other)
    def __ge__(self,other):
        return _quantify_dv_grades(self)>=_quantify_dv_grades(other)
    def __mul__(self,other):
        return 0
    __rmul__ = __mul__
    def __str__(self):
        return _var_to_string(self)
class EnrichmentGrade:
    def __gt__(self,other):
        return _quantify_en_grades(self)>_quantify_en_grades(other)
    def __lt__(self,other):
        return _quantify_en_grades(self)<_quantify_en_grades(other)
    def __le__(self,other):
        return _quantify_en_grades(self)<=_quantify_en_grades(other)
    def __ge__(self,other):
        return _quantify_en_grades(self)>=_quantify_en_grades(other)
    def __mul__(self,other):
        return 0
    def __str__(self):
        return _var_to_string(self)
    __rmul__ = __mul__
#MERIT can compare to either an EnrichmentGrade or a DaVinci grade
#So the function to be used for quantifying depends on the other argument
#So we short cut it by just defining each comparison function as one of the
#comparison functions of the other argument; naturally, the correct
#quantification function will be used
class EitherGrade(DaVinciGrade,EnrichmentGrade):
    def __gt__(self,other):
        return other.__lt__(self)
    def __lt__(self,other):
        return other.__gt__(self)
    def __le__(self,other):
        return other.__ge__(self)
    def __ge__(self,other):
        return other.__le__(self)


#The DV grades are EXCELLENT,MERIT, SATISFACTORY, UNSATISFACTORY
#The enrichment grades are DISTINCTION, MERIT, PASS, FAIL

EXCELLENT = DaVinciGrade()
MERIT = EitherGrade()
SATISFACTORY = DaVinciGrade()
UNSATISFACTORY = DaVinciGrade()

DISTINCTION = EnrichmentGrade()
PASS = EnrichmentGrade()
FAIL = EnrichmentGrade()

#lists for iteration
DV_GRADES = [EXCELLENT,MERIT,SATISFACTORY,UNSATISFACTORY]
ENR_GRADES =[DISTINCTION,MERIT,PASS,FAIL]

GRADES = {'A+': Grade('A+',5.0), 'A': Grade('A',5.0), 'A-': Grade('A-',4.5),
            'B+': Grade('B+',4.0), 'B': Grade('B',3.5), 'B-':Grade('B-', 3.0),
            'C+': Grade('C+',2.5), 'C': Grade('C',2.0), 'D+': Grade('D+',1.5),
            'D': Grade('D',1.0), 'F':Grade('F', 0.0),
            'EXCELLENT':EXCELLENT,'MERIT':MERIT,'SATISFACTORY':SATISFACTORY,
            'UNSATISFACTORY':UNSATISFACTORY,'DISTINCTION':DISTINCTION,'PASS':PASS,
            'FAIL':FAIL}
#Here is the quantification functions
def _quantify_dv_grades(dvgrade):
        if dvgrade == EXCELLENT:
            return 3
        elif dvgrade == MERIT:
            return 2
        elif dvgrade == SATISFACTORY:
            return 1
        elif dvgrade == UNSATISFACTORY:
            return 0
        return False
def _quantify_en_grades(engrade):
        if engrade == DISTINCTION:
            return 3
        elif engrade == MERIT:
            return 2
        elif engrade == PASS:
            return 1
        elif engrade == FAIL:
            return 0
        return False
def _var_to_string(var):
    if var == EXCELLENT:
        return 'EXCELLENT'
    elif var==MERIT:
        return 'MERIT'
    elif var==SATISFACTORY:
        return 'SATISFACTORY'
    elif var==UNSATISFACTORY:
        return 'UNSATISFACTORY'
    elif var==DISTINCTION:
        return 'DISTINCTION'
    elif var==PASS:
        return 'PASS'
    elif var==FAIL:
        return 'FAIL'
    return 'UNRECOGNIZED'

