import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mk_ndarray as nd
import hpfilter as hp
import bsfilter as bs
import power
import rms
import iEMG
import mnfmdf as mm

def temp(filename):
    # データ読み込み. 作業ディレクトリ以下のパスとファイル名を入力.
    data1 = nd.mk_ndarray(filename)

    # サンプリング周波数を入力し, 時間軸を生成.
    # samplerate = 1000
    samplerate = 200
    time = min([data1.size])/samplerate
    timescale = np.arange(0, time, 1/samplerate)

    # 波形出力.
    # plt.plot(timescale, data1)
    # plt.xlim(0,time)
    # plt.xlabel("time[s]")
    # plt.ylabel("EMG[mV]")
    # plt.show()

    # rms振幅波形を出力. rNで細かさを指定.
    rN = 100
    data1r = rms.rms(data1, rN)
    timescaler = np.arange(0, data1r.size, 1)*rN/samplerate
    # plt.plot(timescaler, data1r)
    # plt.xlim(0,time)
    # plt.xlabel("time[s]")
    # plt.ylabel("EMG[mV]")
    # plt.show()

    # 積分筋電位を算出.
    iN = 100
    iEMG1 = iEMG.iEMG(data1, samplerate, iN)
    timescalei = np.arange(0, iEMG1.size, 1)*iN/samplerate
    # plt.plot(timescalei, iEMG1)
    # plt.xlim(0, time)
    # plt.xlabel("time[s]")
    # plt.ylabel("EMG[mV s]")
    # plt.show()

    # 筋電位の合計を算出.
    AllEMG1 = iEMG.iEMG(data1, samplerate, data1.size)
    print("AllEMG: ", AllEMG1[0], "[mV･s]")

    # パワースペクトルを表示.
    power1, freq1 = power.power(data1, samplerate)
    # plt.plot(freq1, power1)
    # plt.grid(True)
    # plt.xlabel("frequency[Hz]")
    # plt.ylabel("power")
    # plt.xlim([0, 100])
    # plt.show()

    # ハイパスフィルタをかける.
    # 引数: データ, サンプリング周波数, 通過帯, 阻止帯, 通過帯最大損失, 阻止帯最小損失
    #大内君の元のコード
    data1f = hp.highpass(data1, samplerate, 5, 3, 1, 20)

    # バンドストップフィルタをかける.
    # 引数: データ, サンプリング周波数, 通過帯下限・上限, 阻止帯下限・上限, 通過帯最大損失, 阻止帯最小損失
    # data1f = bs.bandstop(data1f, samplerate, 49, 51, 49.5, 50.5, 1, 20)
    # data1f = bs.bandstop(data1f, samplerate, 150, 300, 150.5, 299.5, 1, 20)

    # パワースペクトルを表示.
    power1f, freq1f = power.power(data1f, samplerate)
    # plt.plot(freq1f, power1f)
    # plt.grid(True)
    # plt.xlabel("frequency[Hz]")
    # plt.ylabel("power")
    # plt.xlim([0, 100])
    # plt.show()

    # 平均周波数, 中央周波数, 低周波数帯割合を算出.
    MNF, MDF, slowrate = mm.mnfmdf(freq1f, power1f, 30)
    print("MNF: ", MNF, "[Hz]")
    print("MDF: ", MDF, "[Hz]")
    print("slowrate: ", slowrate)

    return AllEMG1, MNF, MDF, slowrate