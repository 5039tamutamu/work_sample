def calculate_final_location(n, m, edges, w, T):
    graph = [[] for _ in range(n+1)]
    
    for i in range(m):
        u, v, weight = edges[i]
        graph[u].append((v, weight))
    
    current_location = 1  # 初期地点は地点1
    time = 0
    
    while time < T:
        max_weight = -1
        next_location = current_location
        
        for neighbor, weight in graph[current_location]:
            if weight > max_weight:
                max_weight = weight
                next_location = neighbor
        
        if next_location == current_location:
            break
        
        current_location = next_location
        time += 1
    
    return current_location

# 入力
n = int(input("地点の数（n）を入力してください: "))
m = int(input("道の本数（m）を入力してください: "))

edges = []
for i in range(m):
    u, v, weight = map(int, input(f"{i+1}番目の道の情報を入力してください（u v w）: ").split())
    edges.append((u, v, weight))

T = int(input("時刻（T）を入力してください: "))

# Kさんの地点を計算
final_location = calculate_final_location(n, m, edges, int(T))
print(f"時刻{T}でのKさんの地点は {final_location} です。")
