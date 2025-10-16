import numpy as np

def mnfmdf(freq, power, slowf):
    #平均周波数を算出.
    MNF_u = 0
    MNF_l = 0
    for i in range(freq.size):
        MNF_u = MNF_u + freq[i] * power[i]
        MNF_l = MNF_l + power[i]
    MNF = MNF_u / MNF_l

    #中央周波数を算出.
    power1fs = 0
    for i in range(freq.size):
        power1fs = power1fs + power[i]
        if power1fs > MNF_l/2:
            MDF = freq[i]
            break
    
    #遅筋の割合を算出.
    slowrate = 0
    for i in range(freq.size):
        slowrate = slowrate + power[i]
        if freq[i] > slowf:
            break
    slowrate = slowrate / MNF_l

    return MNF, MDF, slowrate