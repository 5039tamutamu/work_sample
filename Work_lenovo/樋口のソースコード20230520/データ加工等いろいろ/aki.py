from tkinter import filedialog
import os
from turtle import color
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob


class Graph:
    #グラフの範囲の設定
    graph_Start = 0
    graph_End = 65
    graph_Top = 20
    graph_Bottom = -20
    #グラフの数
    graph_num = 3

    def Graph_row(self, list, title, start = graph_Start, end = graph_End, top = graph_Top, bottom = graph_Bottom):#グラフを縦に3つ描画
        sec = len(list)
        timelist = np.arange(0, sec, 1)/1000
        major_ticks = np.arange(start,end,5) #5秒ごとの罫線リスト
        minor_ticks = np.arange(start,end,1) #１ 秒ごとの罫線リスト

        plt.rcParams['font.size'] = 20 #グラフのフォントサイズの一括指定
        fig, axes = plt.subplots(self.graph_num, 1, figsize=(16,9))

        for i in range(self.graph_num):
            axes[i].plot(timelist, list.iloc[:, i+1])
            axes[i].plot(timelist, list.iloc[:, 0]/6) #ジェスチャのラベル
            axes[i].set_xticks(major_ticks)
            axes[i].set_xticks(minor_ticks, minor=True)
            axes[i].grid(which='major', axis='x', alpha=0.6)
            axes[i].grid(which='minor', axis='x', alpha=0.3)
            #axes[i].set_xlabel('time (sec)')
            #axes[i].set_ylabel('sensor value')
            axes[i].set_ylim([bottom, top])
            axes[i].set_xlim([start, end])
            
            #axes[i].axhline(y=np.std(list.iloc[:, i+4]), color='red')
            #axes[i].axhline(y=-np.std(list.iloc[:, i]), color='red')
        plt.suptitle('file name : ' + title)
        fig.supxlabel('time (sec)')
        fig.supylabel('sensor value')
        plt.tight_layout()
        #plt.show()
        #関数の後ろで必ずplt.show()を記述

    def Graph_pile(self, list, title, start = graph_Start, end = graph_End, top = graph_Top, bottom = graph_Bottom, sf = 1000, Fig = (16, 4)):#グラフを縦に3つ描画
        num = len(list) #サンプル数を取得
        timelist = np.arange(0, num, 1)/sf #時間配列を生成
        major_ticks = np.arange(start,end,5) #5秒ごとの罫線リスト
        minor_ticks = np.arange(start,end,1) #１ 秒ごとの罫線リスト

        #plt.rcParams['font.size'] = 20 #グラフのフォントサイズの一括指定
        fig, ax = plt.subplots(figsize=Fig)
        ax2 = ax.twinx()

        ax.plot(timelist, list.iloc[:, 1], label='1ch', color=(1, 0, 0, 0.4))
        ax.plot(timelist, list.iloc[:, 2], label='2ch', color=(0, 1, 0, 0.4))
        ax.plot(timelist, list.iloc[:, 3], label='3ch', color=(0, 0, 1, 0.4))
        ax2.plot(timelist, list.iloc[:, 0], label='gesture', color='m') #ジェスチャのラベル
        ax.set_xticks(major_ticks)
        ax.set_xticks(minor_ticks, minor=True)
        ax.grid(which='major', axis='x', alpha=0.6)
        ax.grid(which='minor', axis='x', alpha=0.3)
        ax.set_ylim([bottom, top])
        ax.set_xlim([start, end])
        plt.suptitle('file name : ' + title)
        fig.supxlabel('time [sec]')
        fig.supylabel('sensor value')
        ax2.set_ylabel('gesture number')
        ax2.set_ylim([-7.2, 7.2])
        h1, l1 = ax.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax.legend(h1+h2, l1+l2 ,loc='lower right')
        plt.tight_layout()

        #plt.show()
        #関数の後ろで必ずplt.show()を記述


    def Graph_RMS(self, list, title, start = graph_Start, end = graph_End, top = graph_Top, bottom = graph_Bottom):#グラフを縦に3つ描画
        sec = len(list)
        timelist = np.arange(0, sec, 1)/1000
        major_ticks = np.arange(start,end,5) #5秒ごとの罫線リスト
        minor_ticks = np.arange(start,end,1) #１ 秒ごとの罫線リスト

        plt.rcParams['font.size'] = 20 #グラフのフォントサイズの一括指定
        fig, axes = plt.subplots(self.graph_num, 1, figsize=(16,9))

        for i in range(self.graph_num):
            axes[i].plot(timelist, list.iloc[:, i+4], label = 'EMG')
            axes[i].plot(timelist, list.iloc[:, 0]/6, label = 'gesture') #ジェスチャのラベル

            axes[i].set_xticks(major_ticks)
            axes[i].set_xticks(minor_ticks, minor=True)
            axes[i].grid(which='major', axis='x', alpha=0.6)
            axes[i].grid(which='minor', axis='x', alpha=0.3)
            #axes[i].set_xlabel('time (sec)')
            #axes[i].set_ylabel('sensor value')
            axes[i].set_ylim([bottom, top])
            axes[i].set_xlim([start, end])

            axes[i].legend() #凡例の追加
            #axes[i].axhline(y=np.std(list.iloc[:, i+4]), color='red')
            #axes[i].axhline(y=-np.std(list.iloc[:, i]), color='red')
        plt.suptitle('file name : ' + title)
        fig.supxlabel('time (sec)')
        fig.supylabel('sensor value')

        plt.tight_layout()


    def Graph_col(self, list):#グラフを横に3つ描画
        timelist = np.arange(0, 65, 0.001)
        major_ticks = np.linspace(self.graph_Start, self.graph_End, int((self.graph_End-self.graph_Start)/5)+1)
        minor_ticks = np.linspace(self.graph_Start, self.graph_End, (self.graph_End-self.graph_Start)+1)

        plt.rcParams['font.size'] = 20
        fig, axes = plt.subplots(1, self.graph_num, figsize=(16,5))

        for i in range(self.graph_num):
            axes[i].plot(timelist, list.iloc[:, i])
            #axes[i].set_ylim([self.graph_Bottom, self.graph_Top])
            #axes[i].set_xlim([self.graph_Start, self.graph_End])
            axes[i].set_xticks(major_ticks)
            axes[i].set_xticks(minor_ticks, minor=True)
            axes[i].grid(which='major', axis='x', alpha=0.6)
            axes[i].grid(which='minor', axis='x', alpha=0.3)
            axes[i].set_xlabel('time (sec)')
            axes[i].set_ylabel('sensor value')
            #axes[i].set_title('('+chr(i+97)+') '+str(i+1)+ 'ch', )

        plt.tight_layout()
        #関数の後ろで必ずplt.show()を記述

class manageData:
    def selectFile(self):
        #選択するCSVファイルまでのパス(このプログラムと同じディレクトリ)を取得
        idir1 = os.path.dirname(__file__)
        filetype = [('csvファイル','*.csv')]
        #GUIでファイルを選択
        file_path = filedialog.askopenfilename(filetypes = filetype, initialdir = idir1)
        return file_path
        #選択したファイルの名前
        #basename1 = os.path.basename(file_path))[0]

        #CSVファイルのデータをpandas DataFrameに格納
        #df = pd.read_csv(file_path)
        #return df

    def selectDir(self): #選択したフォルダ内のファイルリストを返す
        dir = os.path.dirname(__file__)                            #このプログラムのパスを取得
        fldPath = filedialog.askdirectory(initialdir = dir)        #フォルダを選択するGUI
        filePath = glob.glob(fldPath + '/*')                   #選択したフォルダ内のファイルリストを取得
        return filePath

    def openFile(self, path): #CSVファイルのパス -> CSVファイルの中身
        df = pd.read_csv(path)
        return df

    #CSVへの書き出し
    def saveCSV(self, df, filename, foldername):
        dir = os.getcwd() +'/' + foldername #保存先のフォルダ
        os.makedirs(dir, exist_ok=True)
        filename = foldername +'/' + filename + '.csv'
        df.to_csv(filename, index=False)
        print(filename)
