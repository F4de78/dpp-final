import numpy as np
import pandas as pd
from itertools import combinations

class Anonymization_hkp:
    def __init__(self,_data,_sensitive,_h,_k,_p,_l):
        self.df = _data # orignial dataframe
        self.sensitive = _sensitive # list of sensitive items
        self.public = [ item for item in self.df.columns if item not in self.sensitive ] # list of public items (data-sensitive)
        self.h = _h
        self.k = _k
        self.p = _p

        self.l = _l

    """
    number of 1 in column (beta=1)
    """
    def sup(self,beta):
        print(beta)
        if len(beta) == 1:
            return self.df[beta].sum()
        sum_ = self.df[beta].sum(axis=1)  # sum_ is a list: sum all columns to check how many rows are equal to 111...
        return sum_.value_counts()[len(beta)].item()
    

    def p_breach(self, beta):  # TODO: use sup() 
        occurr = []  # for each private item the number of occurrencies
        for e in self.sensitive:
            tmp = beta.copy()
            tmp.append(e)
            sum_ = self.df[tmp].sum(axis=1)  # sum_ is a list: sum all columns to check how many rows are equal
            s = sum_.value_counts()
            if (len(tmp)) not in s:
                continue
            else:
                occurr.append(sum_.value_counts()[len(tmp)])  # save the result
            
        print(occurr)
        return np.max(occurr) / self.sup(tmp)  # take the max result and calculate probability
                


    """
    If a public item is a (size-1) mole, the item will
    not occur in any (h,k,p)-cohesion of D, thus, can be suppressed in
    a preprocessing step.
    """
    # step 1) preprocessing: eliminate all size 1 moles
    def suppress_size1_mole(self):
        for cmole in self.public:   # candidate mole
            s = self.sup([cmole])
            p_br = self.p_breach([cmole])
            if s.item() < self.k or p_br > self.h:  # check if cmole is a mole
                print("----------------------")
                self.df.drop(inplace=True,columns=cmole,axis=1)  # eliminate the mole
                self.public.remove(cmole)

    
    # step 2) find all size > 1 < p minimal moles
    def find_minimal_moles(self):
        all_M = []
        i = 1
        f = self.df.columns  # after preprocessing we have f = F1 (set)
        while i < self.p and f:  # f not empty
            temp = set.union(*f)  # union of groups of dimension i and then make new groups of dimension i+1
            c = set(combinations(temp, n)) # candidate set C_(i+1)
            temp_M = []
            temp_F = []
            for beta in c:
                if self.sup(beta) < self.k or self.p_breach(beta):  # beta is a mole
                    temp_M.append(beta)
                else:
                    temp_F.append(beta)  # beta is not a mole
            all_M.append(temp_M)
            f = temp_F  # substitute F_i with F_(i+1)
            i += 1
        return all_M

    
        
