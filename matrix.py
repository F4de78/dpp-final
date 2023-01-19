from scipy.sparse import rand
import pandas as pd

# Generate a random 01 dataset
#path = "/home/chiara/Scrivania/Lezioni_ComputerScience/DP&P/dpp-final/"
path = "/home/f4de/uni/dpp/dpp-final/"

def sparse_matrix(x: int, y: int, d: float):
    data = rand(x, y, d, format='csr')
    data.data[:] = 1
    data = pd.DataFrame(data.toarray()).astype(int)
    dataset_name = "ds_x"+str(x)+"_y"+str(y)+"_d0"+str(d)[2]
    data.to_csv(path+"datasets/synthetic/1000x1000/"+dataset_name+".csv", header=False, index=False)

# create datasets
densities = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
for d in densities:
    sparse_matrix(500, 500, d)