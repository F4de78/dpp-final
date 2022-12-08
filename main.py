import pandas as pd
import Anonymization_hkp as hkp

sensitive = [0,5,9,15,30,47]
h = 0.3
k = 100
p = 5

if __name__ == "__main__":
    filename = "datasets/dataBMS1_transaction.csv"
    df = pd.read_csv(filename)
    df.columns = [ i for i in range(len(df.columns)) ] 

    anon = hkp.Anonymization_hkp(df,sensitive,h,k,p)
    a = anon.suppress_size1_mole()
    print(a)
