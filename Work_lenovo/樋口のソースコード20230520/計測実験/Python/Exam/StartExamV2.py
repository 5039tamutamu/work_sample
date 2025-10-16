import os
import glob
from time import time, time_ns
from typing import Sequence
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from numpy.core.fromnumeric import size
import tkinter.font as f
import GraphPlot as GP
import random
import time
import sys

class StartExamV2: #クラス名の書き換え不可
    #時間間隔モニタ用の変数
    monitor_start = 0
    monitor_car = 0
    monitor_print = 0
    
    time_pre = 0
    time_car = 0
    time_count = 0
    timeloss = 0

    #画像フォルダのパス
    Path = os.path.dirname(__file__)
    dir_name = Path + '/HandGesture'
    #ジェスチャの画像ファイルパスを配列として取得
    img_list = glob.glob(dir_name + '/*.png')
    delta_Rest = 5000
    delta_Gesture = 5000

    def time_monitor(self): #経過時間をモニタする関数
        self.monitor_car = time.time()
        self.monitor_print = self.monitor_car - self.monitor_start
        print(str(self.monitor_print) + " : " + sys._getframe().f_back.f_code.co_name)

    def Start(self): #実験開始用のボタンを提示する画面
        #ウィンドウ設定
        self.root1 = tk.Tk()
        self.root1.geometry("500x200")
        self.Center(self.root1, 500, 200)
        self.frame1 = ttk.Frame(self.root1)
        self.frame1.pack(fill = tk.BOTH, padx=50,pady=10)

        #「訓練データを取得」ボタンの生成
        self.Button1 = tk.Button(self.frame1, text="較正データ計測(16秒)", 
        width=20, height=10, command=self.Calibration)#ボタンが押されたら遷移
        self.Button1.pack(side=tk.LEFT)

        #「テストデータを取得」ボタンの生成
        self.Button2 = tk.Button(self.frame1, text="ジェスチャ計測(65秒)", 
        width=20, height=10, command=self.Test)#ボタンが押されたら遷移
        self.Button2.pack(side=tk.RIGHT)

        self.root1.mainloop()

    def Calibration(self): #キャリブレーションフローのメイン関数
        self.RecodeingGraphic()

        self.list = [0, 1, 6, 7] #キャリブレーションで使うジェスチャ画像だけ選択
        
        self.RecodingStart()


        self.CalProccess_Rest(1)
        
    def CalProccess_Rest(self, i):
        #self.time_monitor()

        self.time_car = time.time()
        self.timeloss = int((self.time_car - self.time_pre)*1000) - self.time_count
        self.time_count += self.delta_Rest

        print(str(self.timeloss) + "ms")

        GP.GraphPlot.LabelNum = 0 
        self.Rest(self.list[i])

        if self.list[i] <= 6:
            self.root2.after(self.delta_Rest - self.timeloss, lambda:self.CalProccess_Gesture(i))
        else:
            self.root2.after(self.delta_Rest - self.timeloss, self.Reset)

        self.root2.mainloop()

    def CalProccess_Gesture(self, i):
        #self.time_monitor()

        self.time_car = time.time()
        self.timeloss = int((self.time_car - self.time_pre)*1000) - self.time_count
        self.time_count += self.delta_Gesture

        print(str(self.timeloss) + "ms")

        GP.GraphPlot.LabelNum = self.list[i]
        self.Gesture(self.list[i])

        self.root2.after(self.delta_Gesture - self.timeloss, lambda:self.CalProccess_Rest(i+1))

        self.root2.mainloop()

    def Test(self): #実験フローのメイン関数
        self.RecodeingGraphic()

        #画像の順番の指示用配列の生成
        self.sq = np.arange(1, 7)        #1~6の数列生成
        random.shuffle(self.sq)          #1~6をランダムに並べ替え
        self.sq = np.append(0, self.sq)  #先頭に0を追加(脱力ラベル)
        self.sq = np.append(self.sq, 7)  #最後に7を追加(終了ラベル)
        
        self.RecodingStart()

        self.TestProccess_Rest(1)

    def TestProccess_Rest(self, i):
        #self.time_monitor()

        self.time_car = time.time()
        self.timeloss = int((self.time_car - self.time_pre)*1000) - self.time_count
        self.time_count += self.delta_Rest

        GP.GraphPlot.LabelNum = 0 
        self.Rest(self.sq[i])
        if self.sq[i] <= 6:
            self.root2.after(self.delta_Gesture - self.timeloss, lambda:self.TestProccess_Gesture(i))
        else:
            self.root2.after(self.delta_Gesture - self.timeloss, self.Reset)

        self.root2.mainloop()

    def TestProccess_Gesture(self, i):
        #self.time_monitor()

        self.time_car = time.time()
        self.timeloss = int((self.time_car - self.time_pre)*1000) - self.time_count
        self.time_count += self.delta_Rest

        GP.GraphPlot.LabelNum = self.sq[i]
        self.Gesture(self.sq[i])
        self.root2.after(self.delta_Gesture - self.timeloss, lambda:self.TestProccess_Rest(i+1))
        self.root2.mainloop()

        
    def Rest(self, i):#i: ジェスチャの番号
        #メイン画像描画
        self.Img_R0 = tk.PhotoImage(file = self.img_list[0])
        self.canvas1.create_image(0, 0, image=self.Img_R0, anchor=tk.NW)
        #次の画像描画
        self.Img_Ri = tk.PhotoImage(file = self.img_list[i])
        self.Img_Ri = self.Img_Ri.subsample(2)  #画像の縮小(1/n)
        self.canvas2.create_image(0, 0, image=self.Img_Ri, anchor=tk.NW)


    def Gesture(self, i):#i: ジェスチャの番号
        #メイン画像描画
        self.Img_Gi = tk.PhotoImage(file = self.img_list[i])
        self.canvas1.create_image(0, 0, image=self.Img_Gi, anchor=tk.NW)
        #次の画像描画
        self.Img_G0 = tk.PhotoImage(file = self.img_list[0])
        self.Img_G0 = self.Img_G0.subsample(2)  #画像の縮小(1/n)
        self.canvas2.create_image(0, 0, image=self.Img_G0, anchor=tk.NW)

    def RecodingStart(self): #GraphPlotにアクセスしデータ保存フラグを立てる
        GP.GraphPlot.flag = True
        self.monitor_start = time.time()
        self.time_pre = time.time()
        self.time_count = 0
        

    def Reset(self):#実験中止・終了
        #self.time_monitor()

        #GP.GraphPlot.flag = False
        GP.GraphPlot.Save = True
        self.root2.destroy()
        self.Start()

    def Center(self, root, x, y):#ウィンドウの位置調整
        w = root.winfo_screenwidth()    #モニター横幅取得
        h = root.winfo_screenheight()   #モニター縦幅取得
        w = int((w/2-x)/2)              #メイン画面横幅分調整
        h = int((h-y)/2)                #メイン画面縦幅分調整
        root.geometry(str(x)+"x"+str(y)+"+"+str(w)+"+"+str(h))

    def RecodeingGraphic(self):#実験画面の共通設定
        self.root1.destroy()
        #ウィンドウ設定
        self.root2 = tk.Tk()
        self.root2.geometry("1200x800")
        self.root2.resizable(False, False)
        self.Center(self.root2, 1200, 800)

        #nextラベル設定
        self.next = tk.Label(self.root2, text="Next", font=('', 40))
        self.next.place(x=840, y=10)

        #タイマーラベル設定
        self.text = tk.StringVar()
        self.text.set('準備中...')
        self.timer = tk.Label(self.root2, text=self.text.get(), font=('', 48))
        self.timer.place(x=840, y=600)

        #実験中止用ボタン
        self.Button3 = tk.Button(self.root2, text="実験を中止", width=30, height=5, command=self.Reset)
        self.Button3.place(x=800, y=700)

        #現在のジェスチャ提示用キャンバス
        self.canvas1 = tk.Canvas(bg="black", width=600, height=800)
        self.canvas1.place(x=0, y=0)

        #次のジェスチャ提示用キャンバス
        self.canvas2 = tk.Canvas(bg="black", width=300, height=400)
        self.canvas2.place(x=750, y=100)


if __name__ == '__main__':
    test = StartExamV2()
    test.Start()
