from anon_hkp as anon
import pandas as pd

path = "/home/f4de/uni/dpp/dpp-final/"
dataset = path+"datasets/dataBMS1_transaction.csv"
dataset_name = dataset.split("/")[7]

df = pd.read_csv(dataset)
rows =  df.shape[0]
to_remove = [i for i in df.columns if anon.sup(i)/rows < 0.1]
df.drop(df.columns[to_remove], inplace=True, axis=1)
df.to_csv(f"{path}datasets/preproc_{dataset_name}")