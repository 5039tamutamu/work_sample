import pandas as pd

# ファイルのパスを指定してください
file1_path = '1010dovibafter.csv'
file2_path = '1019dovibafter.csv'

# エンコーディングをShift-JISに指定して読み込み
try:
    df1 = pd.read_csv(file1_path, encoding='utf-8')
    df2 = pd.read_csv(file2_path, encoding='utf-8')
    # df1 = pd.read_csv(file1_path, encoding='shift_jis')
    # df2 = pd.read_csv(file2_path, encoding='shift_jis')
    
    # 列名を表示して確認
    print("Columns in first file:")
    print(df1.columns)
    
    print("\nColumns in second file:")
    print(df2.columns)
    
    # 20行目以降のデータを表示して確認
    print("\nFirst few rows in first file from row 20 onwards:")
    print(df1.iloc[19:].head())
    
    print("\nFirst few rows in second file from row 20 onwards:")
    print(df2.iloc[19:].head())
    
except Exception as e:
    print(f"Error: {e}")


from scipy.stats import ttest_ind

# データフレームの列名を確認　1:左腕橈骨筋　2:左尺側手根伸筋　3:左浅指屈筋
column_name1 = df1.columns[3]
column_name2 = df2.columns[3]

# 指定行(700~5000行目)の指定列(第2列)のデータを抽出5[1000:5500]
data1 = df1.iloc[1000:5500][column_name1].reset_index(drop=True)
data2 = df2.iloc[1000:5500][column_name2].reset_index(drop=True)

# 数値データに変換
data1 = pd.to_numeric(data1, errors='coerce')
data2 = pd.to_numeric(data2, errors='coerce')

# t検定を実施
t_stat, p_value = ttest_ind(data1, data2, nan_policy='omit')

# 結果を表示
print(f'T-statistic: {t_stat}, P-value: {p_value}')

# dovib 1[500:5000] to 2[1000:5500]
# 左腕橈骨筋　T-statistic: 5.781428225464074, P-value: 7.653850824448728e-09
# 左尺側手根伸筋　T-statistic: -2.2963707643008733, P-value: 0.021677560583431715
# 左浅指屈筋　T-statistic: 4.901435014412152, P-value: 9.680124746787366e-07

# dovib 1[500:5000] to 3[800:5300]
# 左腕橈骨筋　T-statistic: -3.319239819616373, P-value: 0.000906215592155287
# 左尺側手根伸筋　T-statistic: -0.8793876385941201, P-value: 0.37921461590674344
# 左浅指屈筋　T-statistic: -3.5245523927790243, P-value: 0.0004263068432279677

# dovib 1[500:5000] to 4[1000:5500]
# 左腕橈骨筋　T-statistic: 0.2094112611574583, P-value: 0.8341319432417629
# 左尺側手根伸筋　T-statistic: -2.6178320863709326, P-value: 0.008863850302371018
# 左浅指屈筋　T-statistic: -7.712655252601383, P-value: 1.3634342115521741e-14

# dovib 1[500:5000] to 5[1000:5500]
# 左腕橈骨筋　T-statistic: -5.5692308060847955, P-value: 2.632281276605484e-08
# 左尺側手根伸筋　T-statistic: 0.4526896474069895, P-value: 0.6507831494028349
# 左浅指屈筋　T-statistic: 1.6202194568075743, P-value: 0.10522018522873226

# dovib 1[500:5000] to 6[1000:5500]
# 左腕橈骨筋　T-statistic: 0.5016868381027663, P-value: 0.6159000988020225
# 左尺側手根伸筋　T-statistic: 3.738155975654223, P-value: 0.0001865237616813674
# 左浅指屈筋　T-statistic: -2.477485329871417, P-value: 0.013249406707369881

# dovib 2[1000:5500] to 3[800:5300]
# 左腕橈骨筋　T-statistic: -8.034594367918794, P-value: 1.057308108069249e-15
# 左尺側手根伸筋　T-statistic: 3.428260240114996, P-value: 0.0006101849173343365
# 左浅指屈筋　T-statistic: -7.4850321613944475, P-value: 7.826034591824239e-14

# dovib 2[1000:5500] to 4[1000:5500]
# 左腕橈骨筋　T-statistic: -6.520955099960162, P-value: 7.362053236520794e-11
# 左尺側手根伸筋　T-statistic: -1.2577294101505079, P-value: 0.20852227171074103
# 左浅指屈筋　T-statistic: -10.46346897840263, P-value: 1.7794507765006438e-25

# dovib 2[1000:5500] to 5[1000:5500]
# 左腕橈骨筋　T-statistic: -9.946285680835325, P-value: 3.4476231984485243e-23
# 左尺側手根伸筋　T-statistic: 3.853309157144596, P-value: 0.00011734190666872366
# 左浅指屈筋　T-statistic: -2.336949434729106, P-value: 0.019463634219887897

# dovib 2[1000:5500] to 6[1000:5500]
# 左腕橈骨筋　T-statistic: -5.8387055990912415, P-value: 5.443151757699255e-09
# 左尺側手根伸筋　T-statistic: 8.240439201816978, P-value: 1.9563576098454748e-16
# 左浅指屈筋　T-statistic: -5.624949051722682, P-value: 1.9111498407045668e-08

# dovib 3[800:5300] to 4[1000:5500]
# 左腕橈骨筋　T-statistic: 4.507169388799025, P-value: 6.652832314188921e-06
# 左尺側手根伸筋　T-statistic: -2.644856073384967, P-value: 0.008186761834518377
# 左浅指屈筋　T-statistic: -5.038263032543387, P-value: 4.789094892691902e-07

# dovib 3[800:5300] to 5[1000:5500]
# 左腕橈骨筋　T-statistic: -1.0865257011274336, P-value: 0.2772755819478264
# 左尺側手根伸筋　T-statistic: 1.9278933080873064, P-value: 0.05389983161174738
# 左浅指屈筋　T-statistic: 3.977532206774399, P-value: 7.017989998262107e-05

# dovib 3[800:5300] to 6[1000:5500]
# 左腕橈骨筋　T-statistic: 4.188031243863967, P-value: 2.8406814931733903e-05
# 左尺側手根伸筋　T-statistic: 6.579220678886331, P-value: 4.9929416952195334e-11
# 左浅指屈筋　T-statistic: -0.3055748990371773, P-value: 0.7599354031945869

# dovib 4[1000:5500] to 5[1000:5500]
# 左腕橈骨筋　T-statistic: -10.69056749886265, P-value: 1.6250288317400107e-26
# 左尺側手根伸筋　T-statistic: 3.457521946727411, P-value: 0.000547689405491088
# 左浅指屈筋　T-statistic: 7.382491309619527, P-value: 1.6916981071004986e-13

# dovib 4[1000:5500] to 6[1000:5500]
# 左腕橈骨筋　T-statistic: 0.530300172866502, P-value: 0.595916912817807
# 左尺側手根伸筋　T-statistic: 6.517876436977692, P-value: 7.513982518073928e-11
# 左浅指屈筋　T-statistic: 3.443272524789362, P-value: 0.0005773374851796965

# dovib 5[1000:5500] to 6[1000:5500]
# 左腕橈骨筋　T-statistic: 7.6311792652368275, P-value: 2.5631551665612618e-14
# 左尺側手根伸筋　T-statistic: 3.9668679541311795, P-value: 7.338822633538032e-05
# 左浅指屈筋　T-statistic: -3.2620051178630547, P-value: 0.0011103932050256626