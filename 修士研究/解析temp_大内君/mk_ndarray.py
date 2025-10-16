import numpy as np
import pandas as pd

def mk_ndarray(path):
    df = pd.read_csv(path, header=None, skiprows=10, usecols=[1], encoding="shift-jis")
    a_df = df.values
    #print(a_df)
    data = a_df[:,0]
    
    return data