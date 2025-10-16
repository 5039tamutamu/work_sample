from cProfile import label
from tkinter import filedialog
import os
from numpy.lib.function_base import select
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

import pywt
import cv2

from scipy import signal

from aki import Graph
from aki import manageData

class dataProcessing:
    #パラメータ
    fs = 200   #サンプリング周波数
    N = 100    #基線除去の窓サイズ
    graph_num = 3
    window_size = 200    #RMSの窓サイズ
    th = 2

    def __init__(self):
        self.gp = Graph()
        self.data = manageData()

        #self.step10_FixCalData()         #キャリブレーションデータを処理

        #caldata = self.data.selectFile() #処理されたキャリブレーションデータを選択(step30で必須)
        #self.TS = pd.read_csv(caldata)

        #self.step20_FixDataset()
        #self.step25_separate()
        #self.step30_Segmentation()
        #self.step40_wavelet()
        #self.checkGraph(1000)
        #self.checkGraphs(200)
        #self.checkGraph_RMS()
        #self.Resize(100, 100)   #フォルダの画像サイズを変更する
        #plt.show()

    #キャリブレーションデータの基線除去
    def step10_FixCalData(self):
        print('Step 1 : キャリブレーションデータを選択してください')
        file = self.data.selectFile()#キャリブレーションデータの選択
        filename = os.path.splitext(os.path.basename(file))[0]

        TS = pd.read_csv(file)
        TS = self.BaselineRemove(TS, num=self.N)        #基線除去
        TS.to_csv(filename + '_fixed.csv', index=False) #基線除去したものを保存
        self.gp.Graph_row(TS.iloc[:, 0:4], filename)
        plt.show()
        print('Step 1 completed.')

    #生データの下処理
    def step20_FixDataset(self):
        #処理されたキャリブレーションデータを選択
        print('Step 2 : キャリブレーションデータを選択してください')
        caldata = self.data.selectFile() 
        TS = pd.read_csv(caldata)

        print('整形するデータの入ったフォルダを選択してください')
        filelist = self.data.selectDir() #処理するデータのフォルダを選択
        for file in filelist:
            df = pd.read_csv(file)

            df = self.BaselineRemove(df, num=self.N)     #基線除去
            df = self.Normalize(df, TS)                      #MVCによる正規化
            #df = pd.concat([df, self.RMS(df)], axis=1)   #RMSの計算列を筋電データに結合
            filename = os.path.splitext(os.path.basename(file))[0] + '_fixed' #保存するファイル名
            self.data.saveCSV(df, filename, 'fixed')              #保存するフォルダ名
        print('Step 2 completed.')

    def step25_separate(self):
        print('Step 2.5 : 分割します')
        print('1000Hzのデータの入ったフォルダを選択してください')
        filelist = self.data.selectDir() #処理するデータのフォルダを選択
        for file in filelist:
            df = pd.read_csv(file) #読み込みデータ(生データ)
            time = len(df) #dfの時間

            for i in range(5):#5つのデータ生成
                sep = pd.DataFrame(index=range(time), columns=['label','1ch','2ch','3ch'])
                k = 0
                for j in range(time):#dfの時間探索
                    if (j%5) == i:
                        sep.iloc[k] = df.iloc[j, 0:4]
                        k += 1
                filename = os.path.splitext(os.path.basename(file))[0] + '_' + str(i) #保存するファイル名
                self.data.saveCSV(sep.iloc[0:k], filename, 'datasetHM/Separated')                #保存するフォルダ名
        print('Step 2.5 completed.')

    #fixedデータをセグメンテーションする(フォルダごと)
    def step30_Segmentation(self):
        #閾値の計算
        rms = lambda d: np.sqrt((d ** 2).sum() / d.size)  #RMSの計算式
        """
        TH = np.zeros(self.graph_num)                     #閾値RMSの格納配列
        for i in range(self.graph_num):#3chループ
            TH[i] = self.th*rms(self.TS.iloc[:5000, i+1]/np.sqrt(self.TS.iloc[:, i+1]**2).max()) #閾値の計算
        print("TH : " + str(TH))
        """

        print('Step 3 : セグメンテーションするデータの入ったフォルダを選択してください')
        filelist = self.data.selectDir() #処理するデータのフォルダを選択
        for file in filelist:
            df = pd.read_csv(file)
            filename = os.path.splitext(os.path.basename(file))[0]

            #self.Seg(df, TH, filename) #セグメンテーション実行
            self.SegV2(df, filename) #セグメンテーション実行

        print('Step 3 completed.')

    #segデータをCWT変換する(フォルダごと)
    def step40_wavelet(self):
        print('Step 4 : 画像加工するデータの入ったフォルダを選択してください')
        filelist = self.data.selectDir() #処理するデータのフォルダを選択
        for file in filelist:
            df = pd.read_csv(file)

            filename = os.path.splitext(os.path.basename(file))[0]

            #スカログラムの縦軸
            scales = self.SetFreq()
            #CWT本体
            cwt1 = self.CWT(df.iloc[:, 1], scales)   #1ch->R(100x1000の2次元配列)
            cwt2 = self.CWT(df.iloc[:, 2], scales)   #2ch->G
            cwt3 = self.CWT(df.iloc[:, 3], scales)   #3ch->B

            self.RGB(cwt1, cwt2, cwt3, 'scalogram_200Hz/datasetG/6/' + filename)     #RGB画像に出力
        print('Step 4 completed.')

    def step41_spectrogram(self):#未完成(22/11/7)
        print('Step 4 : 画像加工するデータの入ったフォルダを選択してください')
        filelist = self.data.selectDir() #処理するデータのフォルダを選択
        for file in filelist:
            df = pd.read_csv(file)

            filename = os.path.splitext(os.path.basename(file))[0]

            #print(filename)
            cwt1 = self.STFT(df.iloc[:, 1])
            print('freq: ' + str(len(cwt1[0])))
            print('time: ' + str(len(cwt1[1])))
            print('dB: ' + str(len(cwt1[2])))

        print('Step 4.1 completed.')

    def STFT(self, sig):
        f, t, Sxx = signal.spectrogram(sig, self.fs)
        plt.pcolormesh(t, f, 10*np.log(Sxx)) #intensityを修正
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        cbar = plt.colorbar() #カラーバー表示のため追加
        cbar.ax.set_ylabel("Intensity [dB]") #カラーバーの名称表示のため追加
        plt.show()
        return f, t, Sxx

    #選択したファイルの筋電位グラフを全部見る
    def checkGraph(self, SF):        
        file = self.data.selectFile() #処理するデータのフォルダを選択
        df = pd.read_csv(file)
        filename = os.path.splitext(os.path.basename(file))[0]
        self.gp.Graph_pile(df.iloc[:, 1:4], filename, end = 5, top = 1, bottom = -1, sf = SF, Fig=(8, 6))

    #フォルダ内の筋電位グラフを全部見る(フォルダごと)
    def checkGraphs(self, SF):        
        filelist = self.data.selectDir() #処理するデータのフォルダを選択
        for file in filelist:
            df = pd.read_csv(file)
            filename = os.path.splitext(os.path.basename(file))[0]
            #self.gp.Graph_row(df.iloc[:, 1:4], filename, top = 40, bottom = -40)
            #self.gp.Graph_row(df.iloc[:, 1:4], filename, top = 1.2, bottom = -1.2)
            #self.gp.Graph_row(df.iloc[:, 0:4], filename, top = 1.2, bottom = -1.2)
            #self.gp.Graph_pile(df.iloc[:, 0:4], filename, top = 1.1, bottom = -1.1, sf = SF)
            self.SaveGraph(df.iloc[:, 1:4], filename)
        #plt.show()

    def SaveGraph(self, list, title, start = 0, end = 5, top = 1, bottom = -1, sf = 200, Fig = (8, 8)):#グラフを縦に3つ描画
        num = len(list) #サンプル数を取得
        timelist = np.arange(0, num, 1)/sf #時間配列を生成

        fig = plt.figure()
        plt.clf()
        plt.plot(timelist, list.iloc[:, 0], color=(1, 0, 0, 0.4))
        plt.plot(timelist, list.iloc[:, 1], color=(0, 1, 0, 0.4))
        plt.plot(timelist, list.iloc[:, 2], color=(0, 0, 1, 0.4))
        plt.ylim([bottom, top])
        plt.xlim([start, end])

        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)

        plt.tick_params(labelbottom=False, labelleft=False, 
                        labelright=False, labeltop=False, 
                        bottom=False, left=False, right=False, top=False)

        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        plt.savefig('scalogram_200Hz/datasetH/1/' + title + '.png')
        plt.close()

    def checkGraph_RMS(self):
        filelist = self.data.selectDir() #処理するデータのフォルダを選択
        for file in filelist:
            df = pd.read_csv(file)
            filename = os.path.splitext(os.path.basename(file))[0]
            self.gp.Graph_RMS(df, filename, top = 0.5, bottom = -0.5)
        #plt.show()

    #基線除去関数(df:csvデータ, num:移動平均点数)
    def BaselineRemove(self, df, num):
        b = np.ones(num)/num

        for i in range(self.graph_num):#3chループ
            B = np.convolve(df.iloc[:, i+1], b, mode='same')    #移動平均をかけた基線データ
            df.iloc[:, i+1] = df.iloc[:, i+1] - B                            #ベースラインを除去したデータ
        return df
    
    #正規化関数(df:csvデータ)
    def Normalize(self, df, TS):
        for i in range(self.graph_num):#3chループ
            df.iloc[:, i+1] = df.iloc[:, i+1]/np.sqrt((TS.iloc[:, i+1]**2).max())
        return df

    #RMSの畳み込み演算関数
    def RMS(self, df):  
        RMS = np.zeros((len(df), self.graph_num))       #RMS計算結果の格納配列
        
        rms = lambda d: np.sqrt((d ** 2).sum() / d.size)  #RMSの計算式

        for i in range(self.graph_num):#3chループ
            RMS[:, i] = df.iloc[:, i+1].rolling(window=self.window_size, min_periods=1, center=True).apply(rms) #RMSの畳み込み計算
        
        df = pd.DataFrame(data=RMS, columns=['1ch_RMS', '2ch_RMS', '3ch_RMS'])

        #print(RMS)
        #print(df)

        return df

    #セグメンテーション実行(変数TSが必須)
    def Seg(self, df, TH, filename):
        RMS = df.iloc[:, 4:7]       #RMS計算結果の格納配列
        seglist = np.zeros((5000, 4))

        j = 0    #時系列マーカー
        flag = 0 #セグメンテーション開始判定
        while j < len(df):
            if (RMS.iat[j, 0]>TH[0] or RMS.iat[j, 1]>TH[1] or RMS.iat[j, 2]>TH[2]) and flag>3000: #判定本体
                seglist = df.iloc[j:j+5000,:4]               #5秒間のセグメンテーション実行(5000,4)
                segdf = pd.DataFrame(data = seglist)         #seglistをdataframeに変換
                label = str(int(np.amax(seglist.iloc[:,0]))) #セグメンテーションした部分のジェスチャラベルを取得

                dir = os.getcwd() +'/' + label               #ジェスチャごとのフォルダのパス
                os.makedirs(dir, exist_ok=True)              #ジェスチャごとのフォルダを取得or生成

                filename2 = label +'/' + label + '_' + filename + '.csv'

                segdf.to_csv(filename2, index=False) #ジェスチャごとのCSV切り出し

                #print('    j = ' + str(j))
                #print('label = ' + label)

                j+=5000
                flag = 0
            else:
                df.iloc[j, 1:4] = 0
                j += 1
                flag += 1

        filename = filename + '_seg'               #保存するファイル名
        self.data.saveCSV(df, filename, 'seg')     #保存するフォルダ名

    def SegV2(self, df, filename):
        seglist = np.zeros((1000, 4))
        j = 0    #時系列マーカー
        label = 0
        while j < len(df):
            if(df.iat[j, 0]!=0 and df.iat[j, 0]!=label):
                label = int(df.iat[j, 0])
                seglist = df.iloc[j:j+1000,:4]               #5秒間のセグメンテーション実行(1000,4)
                segdf = pd.DataFrame(data = seglist)         #seglistをdataframeに変換

                dir = os.getcwd() +'data/segV2/' + str(label)          #ジェスチャごとのフォルダのパス
                os.makedirs(dir, exist_ok=True)              #ジェスチャごとのフォルダを取得or生成

                filename2 = 'data/segV2/' + str(label) +'/' + str(label) + '_' + filename + '.csv'
                segdf.to_csv(filename2, index=False) #ジェスチャごとのCSV切り出し
                j+=1000
            else:
                df.iloc[j, 1:4] = 0
                j+=1

        filename = filename + '_segV2'               #保存するファイル名
        self.data.saveCSV(df, filename, 'data/segV2/seg')     #保存するフォルダ名

    #CWT()の入力のひとつであるスケールを計算(いじらない)
    def SetFreq(self, freq = fs): 
        freqs = np.linspace(1, freq/2, int(freq/2)) #1~fs/2[Hz]の解析周波数リスト
        scales = freq/freqs                  #解析周波数に対応するスケールリスト(fs/2~2)
        scales = scales[::-1]
        return scales
    
    #ウェーブレット変換本体(いじらない)
    def CWT(self, sig, scales, wavelet_type = 'mexh'): 
        '''
        #マザーウェーブレットの波形確認コード
        wav = pywt.ContinuousWavelet(self.wavelet_type)
        [int_psi, x] = pywt.integrate_wavelet(wav, precision=8)
        plt.plot(x, int_psi)
        plt.show()
        '''
        cwtmatr, freqs_rate = pywt.cwt(sig, scales=scales, wavelet=wavelet_type)
        return cwtmatr

    def RGB(self, R, G, B, filename):
        #画像のサイズ設定
        img = np.zeros((R.shape[0], R.shape[1], 3), np.uint8)

        img[:, :, 2] = ((R+1)/2)*255
        img[:, :, 1] = ((G+1)/2)*255
        img[:, :, 0] = ((B+1)/2)*255
        
        img = cv2.resize(img, dsize=(100, 100))

        cv2.imwrite(filename + '.png', img)

    def Resize(self, x_size, y_size):
        filelist = self.data.selectDir() #処理するデータのフォルダを選択
        for file in filelist:
            dst1 = cv2.imread(file)
            filename = os.path.splitext(os.path.basename(file))[0]
            dst2 = cv2.resize(dst1, dsize=(x_size, y_size))
            cv2.imwrite('scalogram_200Hz/datasetI/6/' + filename + '.png', dst2)


if __name__ == "__main__":
    dataProcessing()