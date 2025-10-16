import threading
import StartExamV2 as Ex
import GraphPlot as GP

Exam = Ex.StartExamV2()

#サブスレッドでStartExamを実行
t2 = threading.Thread(target=Exam.Start)
t2.setDaemon(True)
t2.start()

#メインスレッドでGraphPlotを実行
Graph = GP.GraphPlot()