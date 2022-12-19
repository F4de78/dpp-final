import pandas as pd
import Anonymization_hkp as hkp

# sensitive = [0,5,9,15,30,47]
sensitive = [7,8,9]
h = 0.3
k = 4
p = 4

l = 5

if __name__ == "__main__":
    # import dataset
    filename = "datasets/dataBMS1_transaction.csv"
    #filename = "datasets/test.csv"
    df = pd.read_csv(filename)
    val1 = [i for i in range(20,df.shape[1])]
    df.drop(df.columns[val1],inplace=True,axis=1)
    
    # add indexes
    df.columns = [ i for i in range(len(df.columns)) ] 

    #print(df)
    anon = hkp.Anonymization_hkp(df,sensitive,h,k,p,l)
    # preprocessing
    anon.suppress_size1_mole()
    print("preprocessing: ended")
    Mms = anon.find_minimal_moles()
    print(Mms)
    print(anon.df)
