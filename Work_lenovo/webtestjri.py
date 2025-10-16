import sys

def main(lines):
    # このコードは標準入力と標準出力を用いたサンプルコードです。
    # このコードは好きなように編集・削除してもらって構いません。
    # ---
    # This is a sample code to use stdin and stdout.
    # Edit and remove this code as you like.

    def count_moving_floors(n, m, room):
        current_position = (1, 1)  # 初期位置は(1, 1)
        num_floors = 1  # 最初の床もカウントする

        while True:
            direction = room[current_position[0]-1][current_position[1]-1]

            # 移動方向に応じて次の位置を計算
            if direction == 'N':
                next_position = (current_position[0] - 1, current_position[1])
            elif direction == 'E':
                next_position = (current_position[0], current_position[1] + 1)
            elif direction == 'W':
                next_position = (current_position[0], current_position[1] - 1)
            elif direction == 'S':
                next_position = (current_position[0] + 1, current_position[1])

            # 次の位置が部屋の範囲外なら終了
            if next_position[0] < 1 or next_position[0] > n or next_position[1] < 1 or next_position[1] > m:
                break

            num_floors += 1
            current_position = next_position

        return num_floors


    # 部屋の情報を入力
    n, m = map(int, input().split())
    n, m = int(input())

    room = []
    print("各床の情報を入力してください:")
    for _ in range(n):
        row = input().strip()
        room.append(row)

    # 通過する床の数を計算
    num_moving_floors = count_moving_floors(n, m, room)
    #通過する床の数を表示
    print(num_moving_floors)


    for i, v in enumerate(lines):
        print("line[{0}]: {1}".format(i, v))

if __name__ == '__main__':
    lines = []
    for l in sys.stdin:
        lines.append(l.rstrip('\r\n'))
    main(lines)
