import pandas as pd

# ファイルのパスを指定してください
file1_path = '1010Aafter.csv'
file2_path = '1019Aafter.csv'

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

# データフレームの列名を確認　1:右上腕二頭筋　2:右上腕三頭筋　3:右三角筋
column_name1 = df1.columns[3]
column_name2 = df2.columns[3]

# 指定行(700~5000行目)の指定列(第2列)のデータを抽出
data1 = df1.iloc[1500:5500][column_name1].reset_index(drop=True)
data2 = df2.iloc[1500:5500][column_name2].reset_index(drop=True)

# 数値データに変換
data1 = pd.to_numeric(data1, errors='coerce')
data2 = pd.to_numeric(data2, errors='coerce')

# t検定を実施
t_stat, p_value = ttest_ind(data1, data2, nan_policy='omit')

# 結果を表示
print(f'T-statistic: {t_stat}, P-value: {p_value}')

# A 1[3900~7900] to 2[1100~5100]
# 右上腕二頭筋　T-statistic: 2.2505609687161505, P-value: 0.024440412011613132
# 右上腕三頭筋　T-statistic: -0.8477703965707105, P-value: 0.3965912215952415
# 右三角筋　T-statistic: 0.4505413066068382, P-value: 0.6523323894762517

# A 1[3900~7900] to 3[1500~5500]
# 右上腕二頭筋　T-statistic: 4.605270432201269, P-value: 4.182964688662471e-06
# 右上腕三頭筋　T-statistic: -0.34528214813867525, P-value: 0.7298913462354639
# 右三角筋　T-statistic: -2.0300496949541182, P-value: 0.04238451846861474

# A 1[3900~7900] to 4[1500~5500]
# 右上腕二頭筋　T-statistic: -2.437626528008956, P-value: 0.014805675092074934
# 右上腕三頭筋　T-statistic: -2.8416773819581596, P-value: 0.00449904072365885
# 右三角筋　T-statistic: -10.782069514924842, P-value: 6.402986066268055e-27

# A 1[3900~7900] to 5[1500~5500]
# 右上腕二頭筋　T-statistic: -2.8477684240383407, P-value: 0.004413919315187581
# 右上腕三頭筋　T-statistic: -0.5507832854675221, P-value: 0.5817976271876047
# 右三角筋　T-statistic: 1.2242412502073639, P-value: 0.22089729209046058

# A 1[3900~7900] to 6[1500~5500]
# 右上腕二頭筋　T-statistic: -2.5481512328823785, P-value: 0.010848085639860347
# 右上腕三頭筋　T-statistic: -0.58119114454112, P-value: 0.561128012720675
# 右三角筋　T-statistic: 0.4764067532782033, P-value: 0.633797638526538

# A 2[1100~5100] to 3[1500~5500]
# 右上腕二頭筋　T-statistic: 3.788531533715553, P-value: 0.0001526519312267737
# 右上腕三頭筋　T-statistic: 0.16939456349962315, P-value: 0.8654905833857144
# 右三角筋　T-statistic: -2.205280213144791, P-value: 0.027462785075443495

# A 2[1100~5100] to 4[1500~5500]
# 右上腕二頭筋　T-statistic: -5.864750092702424, P-value: 4.676958816272526e-09
# 右上腕三頭筋　T-statistic: -2.0512772871343508, P-value: 0.040272452761584095
# 右三角筋　T-statistic: -11.919727039870274, P-value: 1.7581532516387445e-32

# A 2[1100~5100] to 5[1500~5500]
# 右上腕二頭筋　T-statistic: -6.415438237756177, P-value: 1.484035328772405e-10
# 右上腕三頭筋　T-statistic: 0.1491454470663037, P-value: 0.8814426256612989
# 右三角筋　T-statistic: 0.7746320675852426, P-value: 0.43858000191052215

# A 2[1100~5100] to 6[1500~5500]
# 右上腕二頭筋　T-statistic: -3.6109599674158064, P-value: 0.0003069335822632052
# 右上腕三頭筋　T-statistic: 0.4911229455718501, P-value: 0.6233529690650388
# 右三角筋　T-statistic: -0.040478545961532296, P-value: 0.9677126212137653

# A 3[1500~5500] to 4[1500~5500]
# 右上腕二頭筋　T-statistic: -6.458690861228494, P-value: 1.1178265146353356e-10
# 右上腕三頭筋　T-statistic: -1.4699006924476077, P-value: 0.141627986698651
# 右三角筋　T-statistic: -1.6322111101101155, P-value: 0.10267438819834185

# A 3[1500~5500] to 5[1500~5500]
# 右上腕二頭筋　T-statistic: -6.7431618862015625, P-value: 1.6574717104637963e-11
# 右上腕三頭筋　T-statistic: -0.055116694277183284, P-value: 0.9560468729300706
# 右三角筋　T-statistic: 2.472612396253944, P-value: 0.01343359166398203

# A 3[1500~5500] to 6[1500~5500]
# 右上腕二頭筋　T-statistic: -5.1886443996467895, P-value: 2.1703253943832912e-07
# 右上腕三頭筋　T-statistic: 0.07178908225507852, P-value: 0.94277155649713
# 右三角筋　T-statistic: 2.227322410163319, P-value: 0.025953454362262665

# A 4[1500~5500] to 5[1500~5500]
# 右上腕二頭筋　T-statistic: -0.4452219120154841, P-value: 0.6561714423731537
# 右上腕三頭筋　T-statistic: 1.8751167284095287, P-value: 0.0608130745332777
# 右三角筋　T-statistic: 14.33563797290144, P-value: 4.8595037290089975e-46

# A 4[1500~5500] to 6[1500~5500]
# 右上腕二頭筋　T-statistic: -1.41963536668861, P-value: 0.1557528373078917
# 右上腕三頭筋　T-statistic: 2.932029952076266, P-value: 0.003377086849687447
# 右三角筋　T-statistic: 14.145832834953346, P-value: 6.871221261495203e-45

# A 5[1500~5500] to 6[1500~5500]
# 右上腕二頭筋　T-statistic: -1.220744938181004, P-value: 0.2222185946669848
# 右上腕三頭筋　T-statistic: 0.19902562138677432, P-value: 0.842247761597861
# 右三角筋　T-statistic: -0.9849239209491, P-value: 0.32469123589875226
