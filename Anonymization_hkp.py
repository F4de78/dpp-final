from itertools import combinations

import numpy as np
#from treelib import Node, Tree
import mole_tree


class Anonymization_hkp:
    def __init__(self,_data,_sensitive,_h,_k,_p,_l):
        # user input
        self.df = _data # orignial dataframe
        self.sensitive = _sensitive # list of sensitive items
        self.public = [ item for item in self.df.columns if item not in self.sensitive ] # list of public items (data-sensitive)
        self.h = _h
        self.k = _k
        self.p = _p
        self.l = _l
        # aux structures
        self.MM = {} # for each public item numbers of minimal moles in which is contained
        # self.IL = {} useless(?), = sup(e)



    """
    number of 1 in column (beta=1)
    """
    def sup(self,beta):
        if len(beta) == 1:
            #print("beta ", beta, "sup ", self.df[beta].sum().values.item())
            return self.df[beta].sum().values.item()  # (senza .values dava una serie)
        #print("bet in sup: ", beta, " type: ", type(beta))
        sum_ = self.df[beta].sum(axis=1)  # sum_ is a list: sum all columns to check how many rows are equal to 111...
        #print("sum_", sum_)
        s = sum_.value_counts()
        if len(beta) not in s:
            return 0
        return s[len(beta)].item()
    

    def p_breach(self, beta):  # TODO: use sup() 
        prob = []  # for each private/sensitive item the probability in beta (# occurr/sup(temp)
        for e in self.sensitive:
            tmp = beta.copy()
            tmp.append(e)
            sum_ = self.df[tmp].sum(axis=1)  # sum_ is a list: sum all columns to check how many rows are equal
            s = sum_.value_counts()
            if (len(tmp)) not in s:
                prob.append(0)
                continue
            else:
                occurr = sum_.value_counts()[len(tmp)]
                #print("occurr ", occurr, " sup ", self.sup(beta))
                prob.append(occurr / self.sup(beta))  # save the result
                #print("prob ", occurr / self.sup(beta))
        return np.max(prob)  # take the max probability
                


    """
    If a public item is a (size-1) mole, the item will
    not occur in any (h,k,p)-cohesion of D, thus, can be suppressed in
    a preprocessing step.
    """
    # step 1) preprocessing: eliminate all size 1 moles
    def suppress_size1_mole(self):
        public_copy = self.public.copy()  # copy for iteration
        for cmole in public_copy:   # candidate mole
            s = self.sup([cmole])
            p_br = self.p_breach([cmole])
            if s < self.k or p_br > self.h:  # check if cmole is a mole
                #print("----------------------")
                self.df.drop(inplace=True,columns=cmole,axis=1)  # eliminate the mole
                self.public.remove(cmole)

    
    # step 2) find all size > 1 < p minimal moles
    def find_minimal_moles(self): # TODO da fare con hash map?
        all_M = []
        i = 1
        f = set(self.public)  # after preprocessing we have f = F1 (set)
        while i < self.l and f:  # f not empty
            if i == 1:
                temp = f
            else:
                temp = set([item for t in f for item in t])  # union of groups of dimension i and then make new groups of dimension i+1
            c = set(combinations(temp, i+1)) # candidate set C_(i+1)
            #temp_M = []  # not necessary: we do not keep lists of moles of size i
            temp_F = []
            for beta in c:
                #print("i ", i, ": ", self.sup(list(beta)))
                #print("len di beta step 2", len(beta))
                if self.sup(list(beta)) < self.k or self.p_breach(list(beta)) > self.h:  # beta is a mole
                    #temp_M.append(beta)  # beta is a tuple: you can do set of tuples but can not do set of lists because list is not hashable
                    all_M.append(beta)
                else:
                    temp_F.append(beta)  # beta is not a mole
            #all_M.append(temp_M)
            f = set(temp_F)  # substitute F_i with F_(i+1)
            i += 1
        print(all_M)
        return all_M # M*

    """
    example:
    M* = [[(1,2),(2,3)],[(4,5,6])]]
            ^^^^^^^^^^   ^^^^^^^
            set of len(mm)=2   set of len(mm)=3 ecc...
    """

    def create_MM(self, Ms : list):
        for e in self.public: # iterate public items e 
            count = 0 # count occurence of e in M*
            for l in Ms:
                if e in l:
                    count += 1
            if count != 0 : # if e is not on M*, we skip
                self.MM[e] = count


    # step 3)
    def suppress_minimal_moles(self, Ms : list):
        self.create_MM(Ms)
        print(self.MM)


    
        
