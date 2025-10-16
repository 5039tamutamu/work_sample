import pandas as pd

# ファイルのパスを指定してください
file1_path = '1010doafter.csv'
file2_path = '1019doafter.csv'

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

# 指定行(700~5000行目)の指定列(第2列)のデータを抽出
data1 = df1.iloc[800:5300][column_name1].reset_index(drop=True)
data2 = df2.iloc[1000:5500][column_name2].reset_index(drop=True)

# 数値データに変換
data1 = pd.to_numeric(data1, errors='coerce')
data2 = pd.to_numeric(data2, errors='coerce')

# t検定を実施
t_stat, p_value = ttest_ind(data1, data2, nan_policy='omit')

# 結果を表示
print(f'T-statistic: {t_stat}, P-value: {p_value}')

# do 1[1000~5500] to 2[900~5400]
# 左腕橈骨筋　T-statistic: 10.763191030703807, P-value: 7.480886471637241e-27
# 左尺側手根伸筋　T-statistic: 1.1635524466707043, P-value: 0.24463628539039378
# 左浅指屈筋　T-statistic: -3.448321139787532, P-value: 0.0005666661850683571

# do 1[1000~5500] to 3[800~5300]
# 左腕橈骨筋　T-statistic: -4.1134936340043, P-value: 3.9318625475332727e-05
# 左尺側手根伸筋　T-statistic: 7.0026396734527125, P-value: 2.6919838287271512e-12
# 左浅指屈筋　T-statistic: -0.4033513856065568, P-value: 0.6866993287060494

# do 1[1000~5500] to 4[1500~6000]
# 左腕橈骨筋　T-statistic: 2.084381752476251, P-value: 0.0371535905885164
# 左尺側手根伸筋　T-statistic: -1.1368267021994314, P-value: 0.25564101207737455
# 左浅指屈筋　T-statistic: -0.5051522410567088, P-value: 0.6134642835799844

# do 1[1000~5500] to 5[800~5300]
# 左腕橈骨筋　T-statistic: -2.471517094234609, P-value: 0.013472483942427149
# 左尺側手根伸筋　T-statistic: -0.7185559293650406, P-value: 0.47243323329604925
# 左浅指屈筋　T-statistic: -0.8526180465229383, P-value: 0.39389384509331715

# do 1[1000~5500] to 6[1000~5500]
# 左腕橈骨筋　T-statistic: -2.369835747188882, P-value: 0.017816960012448577
# 左尺側手根伸筋　T-statistic: -5.755894915965696, P-value: 8.90075502039713e-09
# 左浅指屈筋　T-statistic: 8.720543907445297, P-value: 3.2619929848202108e-18

# do 2[900~5400] to 3[800~5300]
# 左腕橈骨筋　T-statistic: -13.15416334991384, P-value: 3.696631999256886e-39
# 左尺側手根伸筋　T-statistic: 3.907160858215188, P-value: 9.40709470251258e-05
# 左浅指屈筋　T-statistic: 1.763944809374534, P-value: 0.07777520037178909

# do 2[900~5400] to 4[1500~6000]
# 左腕橈骨筋　T-statistic: -10.659143352263339, P-value: 2.2696738184888026e-26
# 左尺側手根伸筋　T-statistic: -1.3923961801800406, P-value: 0.16383686799206984
# 左浅指屈筋　T-statistic: 3.1898651645605565, P-value: 0.0014282746444627204

# do 2[900~5400] to 5[800~5300]
# 左腕橈骨筋　T-statistic: -12.145596419960686, P-value: 1.1099382494347597e-33
# 左尺側手根伸筋　T-statistic: -0.9344736676987373, P-value: 0.35008468909823576
# 左浅指屈筋　T-statistic: 2.5848910650236956, P-value: 0.009756567698437987

# do 2[900~5400] to 6[1000~5500]
# 左腕橈骨筋　T-statistic: -10.810647915093494, P-value: 4.493816130222139e-27
# 左尺側手根伸筋　T-statistic: -5.782345144716532, P-value: 7.612390994352495e-09
# 左浅指屈筋　T-statistic: 5.695790441720207, P-value: 1.2666169374646224e-08

# do 3[800~5300] to 4[1500~6000]
# 左腕橈骨筋　T-statistic: 9.728306047193277, P-value: 2.9390853904070156e-22
# 左尺側手根伸筋　T-statistic: -2.7318616022882436, P-value: 0.006310042679009336
# 左浅指屈筋　T-statistic: 0.28947384612658567, P-value: 0.7722254607640409

# do 3[800~5300] to 5[800~5300]
# 左腕橈骨筋　T-statistic: 1.3595369920412863, P-value: 0.17401055640269117
# 左尺側手根伸筋　T-statistic: -1.9872714694363671, P-value: 0.04692258954922848
# 左浅指屈筋　T-statistic: 0.03409489820671107, P-value: 0.9728022330200703

# do 3[800~5300] to 6[1000~5500]
# 左腕橈骨筋　T-statistic: -0.08167328649968568, P-value: 0.9349083382051907
# 左尺側手根伸筋　T-statistic: -7.827057497469384, P-value: 5.5591922855358e-15
# 左浅指屈筋　T-statistic: 2.2188513464491693, P-value: 0.026521693629170673

# do 4[1500~6000] to 5[800~5300]
# 左腕橈骨筋　T-statistic: -5.661323766537295, P-value: 1.5481970799710007e-08
# 左尺側手根伸筋　T-statistic: 0.13223755376383772, P-value: 0.8947993550687539
# 左浅指屈筋　T-statistic: -0.5422715717030576, P-value: 0.5876448655441388

# do 4[1500~6000] to 6[1000~5500]
# 左腕橈骨筋　T-statistic: -3.764636526909124, P-value: 0.00016785304993783878
# 左尺側手根伸筋　T-statistic: -2.177556031766473, P-value: 0.029464996289963647
# 左浅指屈筋　T-statistic: 6.62860270063726, P-value: 3.583540100545087e-11

# do 5[800~5300] to 6[1000~5500]
# 左腕橈骨筋　T-statistic: -0.8125673566431666, P-value: 0.41648765105658636
# 左尺側手根伸筋　T-statistic: -1.9549983639883115, P-value: 0.05061417960281365
# 左浅指屈筋　T-statistic: 4.673841705810543, P-value: 2.99913630001943e-06



