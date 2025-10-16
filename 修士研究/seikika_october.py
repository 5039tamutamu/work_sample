import pandas as pd
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

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

data = pd.read_csv(file_path)

# サンプリング周波数とフィルタの設定
fs = 200  # サンプリング周波数 (Hz)
cutoff = 0.05  # カットオフ周波数 (Hz)
order = 2  # フィルタの次数

# 正規化カットオフ周波数
nyq = fs / 2  # ナイキスト周波数
normal_cutoff = cutoff / nyq

# ハイパスバターワースフィルターの設計
b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)

# 第11行目以降のデータを抽出（0-indexなので10行目以降）
filtered_data = data.iloc[10:].copy()

# 第2～4列目にフィルタを適用
for col in filtered_data.columns[1:4]:
    filtered_data[col] = signal.filtfilt(b, a, filtered_data[col])

# フィルタ適用前後のデータをプロット（例: 第2列目）
plt.figure(figsize=(10, 5))
plt.plot(data.iloc[10:, 0], data.iloc[10:, 1], label='Original Signal (2nd Column)')
plt.plot(filtered_data.iloc[:, 0], filtered_data.iloc[:, 1], label='Filtered Signal (2nd Column)', linestyle='--')
plt.title('High-pass Filtered Signal (2nd Column)')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.grid()
plt.show()

# フィルタ適用後のデータを保存（必要であれば）
output_path = "C:\work\20240423Aafter.csv"
filtered_data.to_csv(output_path, index=False)

print(f"フィルタ適用後のデータが '{output_path}' に保存されました。")
