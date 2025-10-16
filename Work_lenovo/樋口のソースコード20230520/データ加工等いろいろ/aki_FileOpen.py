'''
11/2作成。
データセットを開くためのテストコード。
evaluate_wavelet_source_network.pyを参照。
'''
import os
import numpy as np
import pickle
import pandas as pd

number_of_classes = 7
def read_data_Evaluation(path, type):
    print("Reading Data")

    for candidate in range(16):
        for i in range(number_of_classes * 4):
            data = np.fromfile(path + '/Male' + str(candidate) + '/' + type + '/classe_%d.dat' % i, dtype=np.int16)
            data = np.array(data, dtype=np.float32)
            data = data.reshape(-1, 8)
            labels = (i % number_of_classes) + np.zeros(data.shape[0])
            data = data.T

            savedata = np.vstack([labels, data]).T

            filename = os.getcwd() +'/Myodata_Evaluation/' + str(i % number_of_classes) + '/Male' + str(candidate) + '_' + type + '_classe_%d.csv' % i
            print(filename)
            np.savetxt(filename, savedata, delimiter=',', fmt='%d')

    for candidate in range(2):
        for i in range(number_of_classes * 4):
            data = np.fromfile(path + '/Female' + str(candidate) + '/' + type + '/classe_%d.dat' % i, dtype=np.int16)
            data = np.array(data, dtype=np.float32)
            data = data.reshape(-1, 8)
            labels = (i % number_of_classes) + np.zeros(data.shape[0])
            data = data.T

            savedata = np.vstack([labels, data]).T

            filename = os.getcwd() +'/Myodata_Evaluation/' + str(i % number_of_classes) + '/Female' + str(candidate) + '_' + type + '_classe_%d.csv' % i
            print(filename)
            np.savetxt(filename, savedata, delimiter=',', fmt='%d')

def read_data_PreTraining(path, type):
    print("Reading Data")

    for candidate in range(12):
        for i in range(number_of_classes * 4):
            data = np.fromfile(path + '/Male' + str(candidate) + '/' + type + '/classe_%d.dat' % i, dtype=np.int16)
            data = np.array(data, dtype=np.float32)
            data = data.reshape(-1, 8)
            labels = (i % number_of_classes) + np.zeros(data.shape[0])
            data = data.T

            savedata = np.vstack([labels, data]).T

            filename = os.getcwd() +'/Myodata_PreTraining/' + str(i % number_of_classes) + '/Male' + str(candidate) + '_' + type + '_classe_%d.csv' % i
            print(filename)
            np.savetxt(filename, savedata, delimiter=',', fmt='%d')

    for candidate in range(10):
        for i in range(number_of_classes * 4):
            data = np.fromfile(path + '/Female' + str(candidate) + '/' + type + '/classe_%d.dat' % i, dtype=np.int16)
            data = np.array(data, dtype=np.float32)
            data = data.reshape(-1, 8)
            labels = (i % number_of_classes) + np.zeros(data.shape[0])
            data = data.T

            savedata = np.vstack([labels, data]).T

            filename = os.getcwd() +'/Myodata_PreTraining/' + str(i % number_of_classes) + '/Female' + str(candidate) + '_' + type + '_classe_%d.csv' % i
            print(filename)
            np.savetxt(filename, savedata, delimiter=',', fmt='%d')

'''
    for candidate in range(2):
        labels = []
        examples = []
        for i in range(number_of_classes * 4):
            data_read_from_file = np.fromfile(path + '/Female' + str(candidate) + '/' + type + '/classe_%d.dat' % i, dtype=np.int16)
            data_read_from_file = np.array(data_read_from_file, dtype=np.float32)
            examples.append(data_read_from_file)
            labels.append((i % number_of_classes) + np.zeros(data_read_from_file.shape[0]))
        list_dataset.append(examples)
        list_labels.append(labels)

    print ("Finished Reading Data")
    return list_dataset, list_labels

'''

read_data_PreTraining('C:/Users/naria/Documents/study/MyoArmbandDataset-master/PreTrainingDataset', type='training0')
read_data_Evaluation('C:/Users/naria/Documents/study/MyoArmbandDataset-master/EvaluationDataset', type='test0')
read_data_Evaluation('C:/Users/naria/Documents/study/MyoArmbandDataset-master/EvaluationDataset', type='test1')
#read_data_Evaluation('C:/Users/naria/Documents/study/MyoArmbandDataset-master/EvaluationDataset', type='training0')

