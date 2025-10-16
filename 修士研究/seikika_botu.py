###ボツ　Google Colab参照

import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt

# ファイルを読み込む
file_path = '20240423A_演算.csv'
# エンコーディングをShift-JISに指定して読み込み
try:
    df = pd.read_csv(file_path, encoding='shift_jis')
    
    # 列名を表示して確認
    print("Columns in first file:")
    print(df.columns)
    
    # 20行目以降のデータを表示して確認
    print("\nFirst few rows in first file from row 20 onwards:")
    print(df.iloc[19:].head())
    
except Exception as e:
    print(f"Error: {e}")

# 第11行目以降を対象とする
df_target = df.iloc[10:]

# 第2～4列目を最小-最大正規化する
cols_to_normalize = df_target.columns[1:4]
#df_target[cols_to_normalize] = (df_target[cols_to_normalize] - df_target[cols_to_normalize].min()) / (df_target[cols_to_normalize].max() - df_target[cols_to_normalize].min())

# 数値データのみを選択
df_numeric = df_target[cols_to_normalize].select_dtypes(include=[pd.np.number])

# 正規化
df_target[cols_to_normalize] = (df_numeric - df_numeric.min()) / (df_numeric.max() - df_numeric.min())

# バターワースフィルタを適用してノイズ除去
b, a = butter(3, 0.05)  # 3次バターワースフィルタ、カットオフ周波数0.05
df_target[cols_to_normalize] = filtfilt(b, a, df_target[cols_to_normalize], axis=0)

# 正規化とフィルタ適用後のデータを確認
df_target.head()
