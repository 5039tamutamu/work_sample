import numpy as np
import pandas as pd

def mk_ndarray(path):
    df = pd.read_csv(path, header=None, skiprows=10, usecols=[1], encoding="shift-jis")
    a_df = df.values
    print(a_df)    #この行、後で"#"
    data = a_df[:,0]
    i = 0
    while True:
        if(abs(data[i]) > 0.3):
            data1 = data[i::1]
            break
        i = i + 1
    i = i + 1
    while True:
        if(abs(data1[-i]) > 0.3):
            data2 = data1[:-i:1]
            break
        i = i + 1
    return data2