import numpy as np
from matplotlib import pyplot as plt
from scipy import signal

#バターワースフィルタ（バンドストップ）
def bandstop(x, samplerate, fp_l, fp_u, fs_l, fs_u, gpass, gstop):
    fn = samplerate / 2                             #ナイキスト周波数
    fp = np.array([fp_l, fp_u])                     #通過域端周波数[Hz]※ベクトル
    fs = np.array([fs_l, fs_u])                     #阻止域端周波数[Hz]※ベクトル
    wp = fp / fn                                    #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn                                    #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)    #オーダーとバターワースの正規化周波数を計算
    b, a = signal.butter(N, Wn, "bandstop")         #フィルタ伝達関数の分子と分母を計算
    y = signal.filtfilt(b, a, x)                    #信号に対してフィルタをかける
    return y                                        #フィルタ後の信号を返す