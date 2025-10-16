import numpy as np

def rms(data, N):
    RMS = np.empty(0)
    M = int(data.size/N)
    data2 = data**2
    for i in range(M):
        sum = 0
        for j in range(N):
            sum = sum + data2[i*N + j]
        RMS = np.append(RMS, np.sqrt(sum/N))
    return RMS