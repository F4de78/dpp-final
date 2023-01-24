from scipy.sparse import rand
import pandas as pd

# Generate a random 01 dataset
#path = "/home/chiara/Scrivania/Lezioni_ComputerScience/DP&P/dpp-final/"
path = "/home/f4de/uni/1lm/dpp/dpp-final/"

def sparse_matrix(x: int, y: int, d: float):
    data = rand(x, y, d, format='csr')
    data.data[:] = 1
    data = pd.DataFrame(data.toarray()).astype(int)
    dataset_name = "ds_x"+str(x)+"_y"+str(y)+"_d0"+str(d).split(".")[1]
    data.to_csv(path+"datasets/synthetic/10000x20/"+dataset_name+".csv", header=False, index=False)

# create datasets
densities = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
for d in densities:
    sparse_matrix(10_000, 20, d)