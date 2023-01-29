import pandas as pd
import logging, sys  # print debug and info
import argparse
from itertools import combinations
import numpy as np
import mole_tree
import random


class anon_hkp:
    def __init__(self,_data,_sensitive,_h,_k,_p,_l):
        # user input
        self.df = _data # dataframe,it will be modified 
        self.start_df = _data.copy() # original dataframe kept unmodified (used for statistics)
        self.sensitive = _sensitive # list of sensitive items
        self.public = [ item for item in self.df.columns if item not in self.sensitive ]  # list of public items (data-sensitive)
        self.h = _h
        self.k = _k
        self.p = _p
        self.l = _l
        # aux structures
        self.MM = {} # for each public item numbers of minimal moles in which is contained
        self.IL = {} # sup(e)


    """
    remove moles contained in bigger moles, so it removes non minimal moles 
    all_M = list of "true" minimal moles
    c = set of candidate minimal moles(candidate because maybe contains minimal moles)
    """
    def remove_subtuple(self, all_M:list, c:set): #check if c contains subtuple in all_M
        to_remove = []
        for m_tuple in all_M:  # for all small tuples
            for c_tuple in c:  # for all big tuples
                counter = 0
                for t_item in m_tuple:  # for all element of small tuples (all_m)
                    if t_item in c_tuple:  # if element is contained in big tuple
                        counter += 1
                if len(m_tuple) == counter:
                    to_remove.append(c_tuple)
        for r in to_remove:
            if r in c:  # there may be duplicates in to_remove
                c.remove(r)


    """
    number of 1 in column (beta=1)
    number of rows of a beta-cohort (beta>1)
    """
    def sup(self,beta):
        if len(beta) == 1:
            return self.df[beta].sum().values.item()
        sum_ = self.df[beta].sum(axis=1)  # sum_ is a list: sum all columns to check how many rows are equal to 111...
        s = sum_.value_counts()
        if len(beta) not in s:
            return 0
        return s[len(beta)].item()
    

    def p_breach(self, beta):
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
                prob.append(occurr / self.sup(beta))  # save the result
        return np.max(prob)  # take the max probability


    """
    If a public item is a (size-1) mole, the item will not occur in any (h,k,p)-cohesion of D, thus, 
    can be suppressed in a preprocessing step.
    """
    # step 1) preprocessing: eliminate all size 1 moles
    def suppress_size1_mole(self):
        size1_moles = []  # needed for stat
        public_copy = self.public.copy()  # copy for iteration
        for cmole in public_copy:   # candidate mole
            s = self.sup([cmole])
            p_br = self.p_breach([cmole])
            if s < self.k or p_br > self.h:  # check if cmole is a mole
                size1_moles.append(cmole)
                self.df.drop(inplace=True,columns=cmole,axis=1)  # eliminate the mole
                self.public.remove(cmole)
        logging.debug("Size 1 moles: " + str(size1_moles))
        return size1_moles

    
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
            self.remove_subtuple(all_M,c) # element in c may not be minimal moles
            temp_F = []
            for beta in c:
                if self.sup(list(beta)) < self.k or self.p_breach(list(beta)) > self.h:  # beta is a mole
                    print("Found a mole: ", str(beta))
                    all_M.append(beta)
                else:
                    temp_F.append(beta)  # beta is not a mole
            f = set(temp_F)  # substitute F_i with F_(i+1)
            i += 1
        logging.debug("Minimal moles (Ms): "+str(all_M))
        return all_M  # M*


    """
    example:
    M* = [[(1,2),(2,3)],[(4,5,6])]]
            ^^^^^^^^^^   ^^^^^^^
            set of len(mm)=2   set of len(mm)=3 ecc...
    """
    def create_MM(self, Ms : list):
        for e in self.public:  # iterate public items e
            count = 0  # count occurence of e in M*
            for l in Ms:
                if e in l:
                    count += 1
            if count != 0 :  # if e is not on M*, we skip
                self.MM[e] = count


    def create_IL(self):
        for e in self.public: # iterate public items e 
            self.IL[e] = self.sup([e])


    # step 3)
    def suppress_minimal_moles(self, Ms : list,method,size1_mole):  # suppress with method (mm/il,mm,1/il)
        self.create_MM(Ms)
        self.create_IL()
        logging.debug("initial IL "+str(self.IL))
        logging.debug("initial MM: "+str(self.MM))
        # sorting all e in Ms with respect to MM(e)
        Ms = mole_tree.sort_tuple(Ms, self.MM)
        logging.debug("sorted Ms: "+str(Ms))
        # create mole tree
        tree = mole_tree.MoleTree(0, Ms, "null", 0, None)  # root
        tree.build_tree(self.MM)
        supp_item = tree.suppress_moles(self.MM, self.IL,method)
        logging.debug("supp_item: "+str(supp_item))
        self.df.drop(inplace=True, columns=list(supp_item), axis=1)  # eliminate the items
        return supp_item  # deleted items


    def suppress_rmall(self):
        supp_item = set(self.public)  # we suppress all public items, so supp_item == public
        self.df.drop(inplace=True, columns=list(supp_item), axis=1)  # eliminate the items
        return supp_item  # deleted items


def get_distorsion(anon,supp_item,size1_mole):
    supp_item.update(size1_mole)
    # anon = anon_hkp(df, sensitive, h, k, p, l)
    # we need to build stat like this because we need the original dataframe unchanged
    stat = anon_hkp(anon.start_df, anon.sensitive, anon.h, anon.k, anon.p, anon.l )
    S = sum([stat.sup([i]) for i in supp_item]) # total information loss: number of '1' in the suppressed columns
    N = sum([stat.sup([i]) for i in stat.df.columns]) # total information: number of '1' in all database
    return S/N




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--debug", help="print debug info", action='store_true')
    parser.add_argument("-H", type=float, default=0.5, help="")
    parser.add_argument("-K", type=int, default=3, help="like k-anonymity")
    parser.add_argument("-P", type=int, default=3, help="power of the attacker")
    parser.add_argument("-L", type=int, default=3, help="early stop(?)")
    parser.add_argument('-s', '--sensitive', default=[3, 4], nargs='+', help='List of sensitive items')
    parser.add_argument('--delta', type=int, help='Percentage of public items')
    parser.add_argument('--seed', type=int, default=42, help='Seed used for selecting private item')

    parser.add_argument("-rmt", help="select the removing method",type=str,choices={"rmall", "mmil","mm","1il"},default="mmil")
    parser.add_argument("-df", help="Dataset to anonymize", default="datasets/test_mole3.csv")
    parser.add_argument("-o", "--output", help="Anonymized dataset filename", default="out/test_mole3_anonymized.csv")
    parser.add_argument("--stat", help="save info for statistics", type=str)
    #utility
    parser.add_argument("--preprocess", help="create *only* the preprocessed csv", type=str)
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(format='[\x1b[31;1m%(levelname)s\033[0m] %(asctime)s.%(msecs)03d \t %(message)s',datefmt='%H:%M:%S', stream=sys.stderr, level=logging.DEBUG)
    else:
        logging.basicConfig(format='[\x1b[31;1m%(levelname)s\033[0m] %(asctime)s.%(msecs)03d \t %(message)s',datefmt='%H:%M:%S', stream=sys.stderr, level=logging.INFO)


    filename = args.df
    h = args.H
    k = args.K
    p = args.P
    l = args.L
    df = pd.read_csv(filename)

    # add indexes
    df.columns = [i for i in range(len(df.columns))]

    sensitive = [int(s) for s in args.sensitive]

    if args.delta:  # if not selected, takes from args
        # random sampling delta percent of public items
        k = (len(df.columns) * (100 - args.delta)) // 100
        random.seed(args.seed)
        sensitive = random.sample(range(len(df.columns)), int(k))
        '''
        # Select only from a subset of items: for bad distributed datasets
        temp_anon = anon_hkp(df, df.columns, h, k, p, l)
        temp = [i for i in df.columns if temp_anon.sup([i]) < 300]  # take only items with limited sup
        k = (len(df.columns) * (100 - args.delta)) // 100  # number of public items
        if len(temp) > k:
            random.seed(args.seed)
            sensitive = random.sample(temp, int(k))  # take k items from temp
        else:
            sensitive = temp  # we have enough (or less) sensitive items
        '''

    anon = anon_hkp(df, sensitive, h, k, p, l)

    if args.preprocess:  # Utility: create the preprocessed file and exit
        logging.info("Creating the preprocessed dataset")
        rows = anon.df.shape[0]
        to_remove = [i for i in anon.df.columns if anon.sup([i])/rows < 0.001]
        anon.df.drop(anon.df.columns[to_remove], inplace=True, axis=1)
        anon.df.to_csv(args.preprocess, header=False, index=False)
        logging.info("Done.")
        exit()

    logging.debug("Initial dataset:\n"+str(df))
    # suppressing size 1 moles
    logging.info("start suppressing size 1 moles")
    size1_mole = []
    if args.rmt != "rmall":  # if we are using rmall, we need to keep all item untill we compute the distorsion
        size1_mole = anon.suppress_size1_mole()
    logging.info("end suppressing size 1 moles")
    # find minimal moles
    logging.info("start finding minimal moles")
    if args.rmt != "rmall": # if we are using rmall we dont need to search moles
        Ms = anon.find_minimal_moles()
    logging.info("end finding minimal moles")
    logging.info("start suppressing moles")
    supp_item = []
    if args.rmt == "mmil":
        supp_item = anon.suppress_minimal_moles(Ms,"mmil",size1_mole)
    elif args.rmt == "mm":
        supp_item = anon.suppress_minimal_moles(Ms,"mm",size1_mole)
    elif args.rmt == "1il":
        supp_item = anon.suppress_minimal_moles(Ms,"1il",size1_mole)
    elif args.rmt == "rmall":
        supp_item = anon.suppress_rmall()
    else:
        raise ValueError('Suppressing method not recognised')

    if args.stat:  # Utility: statistics visualization
        sn = get_distorsion(anon,supp_item,size1_mole)
        f = open(args.stat, "a")
        f.write(f"{str(sn)}\n")

    logging.info("end suppressing mole")
    anon_df = anon.df
    logging.debug("Anonymized dataset:\n"+str(anon_df))
    # put anonimized df in a csv
    anon_df.to_csv(args.output)



if __name__ == '__main__':
    main()
    
        
