def count_divisible(num, divisor):
    count = 0
    while num % divisor == 0:
        count += 1
        num //= divisor
    return count

def calculate_class_score(nums, k):
    total_score = 0
    
    for num in nums:
        count = count_divisible(num, k)
        total_score += count
    
    return total_score

# 入力
n = int(input("生徒の人数（N）を入力してください: "))
nums = []
for i in range(n):
    num = int(input(f"{i+1}番目の生徒が書いた整数（Ai）を入力してください: "))
    nums.append(num)

k = int(input("Kの値を入力してください: "))

# クラスの点数を計算
class_score = calculate_class_score(nums, k)
print(f"クラスの点数は {class_score} 点です。")
