import pandas as pd
import Anonymization_hkp as hkp

sensitive = [0,5,9,15,17]
#sensitive = [7,8]
h = 0.3
k = 3
p = 3

l = 3

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
    print("[*] start preprocessing")
    anon.suppress_size1_mole()
    print("[!] end preprocessing")
    # find minimal moles
    print("[*] start finding minimal moles")
    Ms = anon.find_minimal_moles()
    print("[!] end finding minimal moles")
    #print("Minimal moles to suppress: ",Ms)
    anon.suppress_minimal_moles(Ms)
    #print("MM(e): ")
    #print(anon.MM)


