import numpy as np
import pandas as pd

class Anonymization_hkp:
    def __init__(self,_data,_sensitive,_h,_k,_p):
        self.df = _data # orignial dataframe
        self.sensitive = _sensitive # list of sensitive items
        self.public = [ item for item in self.df.columns if item not in self.sensitive ] # list of public items (data-sensitive)
        self.h = _h
        self.k = _k
        self.p = _p

    """
    number of 1 in column (beta=1)
    """
    def sup1(self,beta):
        v = self.df[beta].value_counts().values
        if len(v) == 1: # if len is 1, there are no 1 :)
            return 0
        else:
            return v[1]


    """
    If a public item is a (size-1) mole, the item will
    not occur in any (h,k,p)-cohesion of D, thus, can be suppressed in
    a preprocessing step.
    """
    def suppress_size1_mole(self):
        for cmole in self.public:
            s = self.sup1(cmole)
            print(s)
            #p-breach todo
    
        
