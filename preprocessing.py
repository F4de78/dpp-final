# tool for transaction data conversion: from tabular to sparse matrix
from mlxtend.preprocessing import TransactionEncoder
import numpy as np
import pandas as pd

path = "/home/chiara/Scrivania/Lezioni_ComputerScience/DP&P/dpp-final/"
dataset = path+"datasets/connect.dat"
dataset_name = dataset.split("/")[8].split(".")[0]


# reading .dat file
df = []
with open(dataset, 'r') as f:
    d = f.readlines()
    for i in d:
        k = i.rstrip().split(" ")
        df.append([str(i) for i in k])

df = np.array(df, dtype='O')
#df.astype(int)
print(df)

te = TransactionEncoder()
te_ary = te.fit_transform(df)
te_ary = te_ary.astype("int")
# te.columns_ # attribute to access unique column names
#print(te.columns_)
out = pd.DataFrame(te_ary)
out.to_csv(path+"datasets/"+dataset_name+".csv", header=False, index=False)