import pandas as pd
import Anonymization_hkp as hkp

# sensitive = [0,5,9,15,30,47]
sensitive = [2,3]
h = 0.3
k = 1
p = 3

l = 4

if __name__ == "__main__":
    # import dataset
    #filename = "datasets/dataBMS1_transaction.csv"
    filename = "datasets/test.csv"
    df = pd.read_csv(filename)
    
    # add indexes
    df.columns = [ i for i in range(len(df.columns)) ] 

    print(df)
    anon = hkp.Anonymization_hkp(df,sensitive,h,k,p,l)
    # preprocessing
    anon.suppress_size1_mole()
    print(anon.df)
