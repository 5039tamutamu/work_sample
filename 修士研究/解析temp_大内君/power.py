import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def power(data, samplerate):
    dt = 1/samplerate
    N = data.size
    window = signal.hann(N)             # ハニング窓関数
    F = np.fft.fft(data * window)       # フーリエ変換
    freq = np.fft.fftfreq(N, d=dt)      # 周波数スケール

    # フーリエ変換の結果を正規化
    F = F / (N / 2)

    # 窓関数による振幅減少を補正する
    F = F * (N / np.sum(window))

    # 振幅スペクトル
    Amp = np.abs(F)

    Pow = Amp ** 2

    return Pow[:N//2], freq[:N//2]