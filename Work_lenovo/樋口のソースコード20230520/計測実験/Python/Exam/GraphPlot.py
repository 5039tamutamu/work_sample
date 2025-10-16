from numpy.core.fromnumeric import size
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pandas as pd
import serial
import sys
import datetime

class GraphPlot: #クラス名の書き換え不可
    
    flag = False #データ保存のフラグ(StartExamからアクセスされる)
    LabelNum = 0 #ジェスチャの正解ラベル(StartExamからアクセスされる)
    Save = False

    f = 1000       #サンプリング周波数
    tmp = 5000     #グラフのデータ数(横軸)
    top = 600      #グラフの上端(縦軸)
    bot = 400     #グラフの下端(縦軸)
    str = 100      #保存するデータ長(秒)

    str = str*f
    counter = 0

    RecordData = np.zeros((str, 4))  #データ保存用配列

    app = QtGui.QApplication([]) #pyqtgraphのverが違うと"AttributeError: module 'pyqtgraph.Qt.QtGui' has no attribute 'QApplication'"のエラー発生あり。"pip install pyqtgraph==0.12.2"のコマンドで解決可能
    desktop = app.desktop()
    height = desktop.height()
    width = desktop.width()

    def __init__(self):
        self.Start()

    def Start(self):
        # プロット初期設定
        self.win = pg.GraphicsLayoutWidget(show=True, title="EMGgraph", size =(self.width/2, self.height))
        self.win.move(self.width/2, 0)

        self.p1 = self.win.addPlot(row=0, col=0)
        #self.p1.setYRange(self.bot, self.top)  # y軸の上限、下限の設定
        self.curve1 = self.p1.plot()  # プロットデータを入れる場所
        self.data1 = np.zeros(self.tmp) # プロットデータを一時保存する配列

        self.p2 = self.win.addPlot(row=1, col=0)
        #self.p2.setYRange(self.bot, self.top)  # y軸の上限、下限の設定
        self.curve2 = self.p2.plot()  # プロットデータを入れる場所
        self.data2 = np.zeros(self.tmp) # プロットデータを一時保存する配列

        self.p3 = self.win.addPlot(row=2, col=0)
        #self.p3.setYRange(self.bot, self.top)  # y軸の上限、下限の設定
        self.curve3 = self.p3.plot()  # プロットデータを入れる場所
        self.data3 = np.zeros(self.tmp) # プロットデータを一時保存する配列

        self.label = np.zeros(self.tmp)


        #v = self.win.addViewBox(row=1, col=0, colspan=2)
        # pg.setConfigOptions(antialias=True) #アンチエイリアスをオン

        #シリアルポートの設定
        self.ser = serial.Serial(port="COM3", baudrate=115200, dsrdtr=True, timeout=1)
        #self.ser = serial.Serial(port="COM0", baudrate=115200, dsrdtr=True, timeout=1)
        #受信バッファクリア
        self.ser.reset_input_buffer()

        # アップデート時間設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)  # 10msごとにupdateを呼び出し

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def update(self):
        self.Serial_Receive()
        self.curve1.setData(self.data1)
        self.curve2.setData(self.data2)
        self.curve3.setData(self.data3)

    def Serial_Receive(self):
        #バッファ内のデータ数取得
        Receivesize = self.ser.in_waiting 
        datasize = int(Receivesize/7)
        #print(datasize)

        #古いデータの削除
        self.data1 = np.delete(self.data1, range(datasize))
        self.data2 = np.delete(self.data2, range(datasize))
        self.data3 = np.delete(self.data3, range(datasize))

        for i in range(datasize):
            head = self.ser.read(1)
            if head == b'\x80': #ヘッダ受信
                d = self.ser.read(6)#データ受信
                #データ整形
                A = ((d[0]<<7)+d[1])-495
                B = ((d[2]<<7)+d[3])-495
                C = ((d[4]<<7)+d[5])-495

                #グラフ用配列に保存(一時保存)
                self.data1 = np.append(self.data1, A)
                self.data2 = np.append(self.data2, B)
                self.data3 = np.append(self.data3, C)

                if GraphPlot.flag == True:  #保存フラグが立っていた場合、データ保存
                    self.RecordData[self.counter]=[self.LabelNum, A, B, C]
                    self.counter += 1
                    if GraphPlot.Save == True: #保存時間を過ぎた場合
                        GraphPlot.flag = False
                        self.SaveCSV()

    def SaveCSV(self):
        now = datetime.datetime.now()
        filename = '02_' + now.strftime('%Y%m%d_%H%M%S') + '.csv'
        df = pd.DataFrame(data = self.RecordData[:self.counter, :])
        df.to_csv(filename, header=['label','1ch','2ch','3ch'], index=False)
        
        #初期化
        self.RecordData = np.zeros((self.str, 4))
        GraphPlot.Save = False
        self.counter = 0

#'''単独で動かすとき用
if __name__ == "__main__":
    plotwin = GraphPlot()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
#'''
