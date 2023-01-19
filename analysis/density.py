# calculate density of a matrix from csv file

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

x_filename = "../datasets/connect.csv"

x = pd.read_csv(x_filename)
x = x.to_numpy()
mat = csr_matrix(x)
density = mat.getnnz() / np.prod(mat.shape)

print(density)