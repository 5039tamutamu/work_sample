import numpy as np
import pywt
from scipy.ndimage import zoom
import matplotlib.pyplot as plt

import os
from tkinter import filedialog
import glob
import pandas as pd
import time

def selectDir(): #選択したフォルダ内のファイルリストを返す
    dir = os.path.dirname(__file__)                            #このプログラムのパスを取得
    fldPath = filedialog.askdirectory(initialdir = dir)        #フォルダを選択するGUI
    print(fldPath)
    filePath = glob.glob(fldPath + '/*')                   #選択したフォルダ内のファイルリストを取得
    return filePath

def label():
    savedata = []

    filelist = selectDir() #処理するデータのフォルダを選択

    #savedir = os.path.dirname(__file__)                            #このプログラムのパスを取得
    savefldPath = 'datasetHM/label'        #フォルダを選択するGUI

    for file in filelist:
        #df = np.loadtxt(file, delimiter=',', dtype='int64') #csvデータをndarrayとして読み込み
        df = pd.read_csv(file).values
        filename = os.path.splitext(os.path.basename(file))[0]

        flag = 0 #label判定

        #ファイルごと(被験者ごと)のループ
        for i in range(len(df)):
            if df[i, 0] > 0: #labelの始まり
                flag = 1
                savedata.append(df[i, :])
            
            if flag == 1 and df[i, 0] == 0: #labelの終わり
                label = df[i-1, 0]         #保存するデータのラベル

                text = savefldPath + '/{}/' + filename + '.csv'
                savename = text.format(int(label))

                np.savetxt(savename, savedata, delimiter=',')
                savedata = []
                flag = 0

def nina_label():
    savedata = []

    filelist = selectDir() #処理するデータのフォルダを選択

    savedir = os.path.dirname(__file__)                            #このプログラムのパスを取得
    savefldPath = filedialog.askdirectory(initialdir = savedir)        #フォルダを選択するGUI

    for file in filelist:
        #df = np.loadtxt(file, delimiter=',', dtype='int64') #csvデータをndarrayとして読み込み
        df = pd.read_csv(file).values
        filename = os.path.splitext(os.path.basename(file))[0]

        flag = 0 #label判定
        count = 0 #

        #ファイルごと(被験者ごと)のループ
        for i in range(len(df)):
            if df[i, 0] > 0: #labelの始まり
                flag = 1
                savedata.append(df[i, :])
            
            if flag == 1 and df[i, 0] == 0: #labelの終わり
                label = df[i-1, 0]         #保存するデータのラベル
                count += 1                 #同一被験者、同一ジェスチャの中で何回目の計測か(1~6)

                text = savefldPath + '/{}/' + filename + '_{}.csv'
                savename = text.format(label, count)

                np.savetxt(savename, savedata, delimiter=',', fmt='%d')
                savedata = []
                flag = 0
                
#5秒間の筋電位データを8×52ごとに切り取って保存するメゾッド
def data_cut(label):
    window = [52, 9]

    #filelist = selectDir() #処理するデータのフォルダを選択
    fldPath = 'C:/Users/naria/Documents/study/datasetHM_edit/label/' + str(label)
    filelist = glob.glob(fldPath + '/*')
    print(fldPath)

    #savedir = os.path.dirname(__file__)                            #このプログラムのパスを取得
    #savefldPath = filedialog.askdirectory(initialdir = savedir)        #フォルダを選択するGUI
    savefldPath = 'C:/Users/naria/Documents/study/datasetHM_edit/seg/' + str(label)

    for file in filelist:
        i = 0

        filename = os.path.splitext(os.path.basename(file))[0]
        df = pd.read_csv(file)
        ndf = df.values
        #print('all row: '+ str(ndf.shape[0]))
        for j in range(int((ndf.shape[0]-47)/5)):
            window = ndf[i:i+52, :]
            savename = savefldPath + '/' + filename + '_%d.csv' % j
            np.savetxt(savename, window, delimiter=',')
            i += 5
        #print('final row: '+ str(i-5+52))

def cal_wavelet(label):
    #label = 2
    #filelist = selectDir() #処理するデータのフォルダを選択
    fldPath = 'C:/Users/naria/Documents/study/datasetHM_edit/seg/' + str(label)
    filelist = glob.glob(fldPath + '/*')
    print(fldPath)

    #savedir = os.path.dirname(__file__)                            #このプログラムのパスを取得
    #savefldPath = filedialog.askdirectory(initialdir = savedir)        #フォルダを選択するGUI
    savefldPath1 = 'C:/Users/naria/Documents/study/datasetHM/'
    
    canals1 = np.empty((25, 15, 3))
    counter = 0
    start = time.time()

    for file in filelist:
        counter += 1
        print('\r' + str(counter) + ' / ' + str(len(filelist)), end='')

        filename = os.path.splitext(os.path.basename(file))[0]
        #print(filename)
        df = np.loadtxt(file, delimiter=',')

        #電極番号1~8のループ
        for i in range(3):
            coefs = CWT(np.abs(df[:, i+1]), scales=np.arange(1, 33))

            coefs = zoom(coefs, .5, order=0)
            coefs = np.delete(coefs, axis=0, obj=len(coefs)-1)
            coefs = np.delete(coefs, axis=1, obj=np.shape(coefs)[1]-1)
            canals1[:, :, i] = coefs.transpose()

        savename = savefldPath1 + str(label) + '/CWT_' + filename + '.npy'
        np.save(savename, canals1)
    
    print('\ncal_wavelet: completed. time: ' + str(int(time.time() - start)))


#8×52の筋電位データから8枚のスカログラムを書き出すメゾッド
def cal_wavelet_Nina(label):
    #label = 2
    #filelist = selectDir() #処理するデータのフォルダを選択
    fldPath = 'C:/Users/naria/Documents/study/ninapro/DB5_ExB_seg/' + str(label)
    filelist = glob.glob(fldPath + '/*')
    print(fldPath)

    #savedir = os.path.dirname(__file__)                            #このプログラムのパスを取得
    #savefldPath = filedialog.askdirectory(initialdir = savedir)        #フォルダを選択するGUI
    savefldPath1 = 'C:/Users/naria/Documents/study/datasetNina_ExB_1re/'
    savefldPath2 = 'C:/Users/naria/Documents/study/datasetNina_ExB_2re/'
    
    canals1 = np.empty((25, 15, 8))
    canals2 = np.empty((25, 15, 8))
    counter = 0
    start = time.time()

    for file in filelist:
        counter += 1
        print('\r' + str(counter) + ' / ' + str(len(filelist)), end='')

        filename = os.path.splitext(os.path.basename(file))[0]
        #print(filename)
        df = np.loadtxt(file, delimiter=',')

        #電極番号1~8のループ
        for i in range(8):
            coefs = CWT(np.abs(df[:, i+1]), scales=np.arange(1, 33))

            coefs = zoom(coefs, .5, order=0)
            coefs = np.delete(coefs, axis=0, obj=len(coefs)-1)
            coefs = np.delete(coefs, axis=1, obj=np.shape(coefs)[1]-1)
            canals1[:, :, i] = coefs.transpose()

        savename = savefldPath1 + str(label) + '/CWT_' + filename + '.npy'
        np.save(savename, canals1)

        #電極番号9~16のループ(NinaProのみ)
        for i in range(8):
            coefs = CWT(np.abs(df[:, i+8]), scales=np.arange(1, 33))

            coefs = zoom(coefs, .5, order=0)
            coefs = np.delete(coefs, axis=0, obj=len(coefs)-1)
            coefs = np.delete(coefs, axis=1, obj=np.shape(coefs)[1]-1)
            canals2[:, :, i] = coefs.transpose()

        savename = savefldPath2 + str(label) + '/CWT_' + filename + '.npy'

        np.save(savename, canals2)
    
    print('\ncal_wavelet: completed. time: ' + str(int(time.time() - start)))

def show_npy():
    idir1 = os.path.dirname(__file__)
    filetype = [('npyファイル','*.npy')]
    file_path = filedialog.askopenfilename(filetypes = filetype, initialdir = idir1)
    data = np.load(file_path)
    print(f'scores:       \n{data[0, 0, :]}\n')
    print(f'scores shape: {data.shape}')
    print(f'scores dtype: {data.dtype}')

#CWT本体
def CWT(vector, mother_wavelet='mexh', scales=np.arange(1, 32)):
    coef, freqs = pywt.cwt(vector, scales=scales, wavelet=mother_wavelet)
    return coef

#スカログラムを保存している2次元配列を画像として出力する
def show_wavelet(coef):
    print(np.shape(coef))
    #plt.rcParams.update({'font.size': 36})
    plt.matshow(coef)
    plt.ylabel('Scale')
    plt.xlabel('Samples')
    
def check_EMG():
    idir1 = os.path.dirname(__file__)
    filetype = [('csvファイル','*.csv')]
    #GUIでファイルを選択
    file = filedialog.askopenfilename(filetypes = filetype, initialdir = idir1)
    list = pd.read_csv(file)
    title = os.path.splitext(os.path.basename(file))[0]

    sf = 200
    start = 0
    end = 5
    Fig = (16, 4)

    num = len(list) #サンプル数を取得
    timelist = np.arange(0, num, 1)/sf #時間配列を生成
    #major_ticks = np.arange(start, end, 5) #5秒ごとの罫線リスト
    minor_ticks = np.arange(start, end, 1) #１ 秒ごとの罫線リスト

    #plt.rcParams['font.size'] = 20 #グラフのフォントサイズの一括指定
    fig, ax = plt.subplots(figsize=Fig)
    ax2 = ax.twinx()

    ax.plot(timelist, list.iloc[:, 1])
    #ax2.plot(timelist, list.iloc[:, 0], label='gesture', color='m') #ジェスチャのラベル
    #ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    #ax.grid(which='major', axis='x', alpha=0.6)
    ax.grid(which='minor', axis='x', alpha=0.3)
    #ax.set_ylim([bottom, top])
    ax.set_xlim([start, end])
    plt.suptitle('file name : ' + title)
    fig.supxlabel('time [sec]')
    fig.supylabel('sensor value')
    #ax2.set_ylabel('gesture number')
    #ax2.set_ylim([-7.2, 7.2])
    h1, l1 = ax.get_legend_handles_labels()
    #h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1, l1 ,loc='lower right')
    plt.tight_layout()

    plt.show()

#for i in range(1, 7):
#    data_cut(i)
#    cal_wavelet(i)

show_npy()
