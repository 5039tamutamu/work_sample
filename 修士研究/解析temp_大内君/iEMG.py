import numpy as np

def iEMG(data, samplerate, N):
    iEMG_size = int(data.size / N)
    # print(iEMG_size)
    iEMG = np.empty(iEMG_size)
    # print(iEMG)
    for i in range(iEMG_size):
        iEMG[i] = 0
        for j in range(N):
            iEMG[i] = iEMG[i] + abs(data[i*N+j])
        iEMG[i] = iEMG[i] / samplerate
    return iEMG

# data = np.arange(100)
# samplerate = 1
# N = 2
# S = iEMG(data, samplerate, N)
# print(S)