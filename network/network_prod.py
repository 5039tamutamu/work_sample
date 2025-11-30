import subprocess
import ipaddress
import json
import re
from pathlib import Path

# -----------------------------------
# 設定
# -----------------------------------
SUBNET = "XXX.XXX.XXX.XXX/XX"  # 自宅LANに合わせて変更
ALLOWED_FILE = "pathhogehoge\allowed_devices.json"

# -----------------------------------
# 許可済みMACアドレス一覧の読み込み
# -----------------------------------
def load_allowed_macs():
    path = Path(ALLOWED_FILE)
    if not path.exists():
        print(f"[WARN] {ALLOWED_FILE} がありません。空のホワイトリストとして扱います。")
        return {}
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    # 大文字に揃える
    return {mac.upper(): name for mac, name in data.items()}

# -----------------------------------
# サブネット内に ping を打って ARP テーブルを更新
# -----------------------------------
def ping_subnet(subnet: str):
    net = ipaddress.ip_network(subnet, strict=False)
    print(f"[INFO] Subnet {subnet} をpingでスキャン中...")
    for ip in net.hosts():
        # Windows の ping コマンド （1回だけ、出力は捨てる）
        subprocess.run(
            ["ping", "-n", "1", "-w", "100", str(ip)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

# -----------------------------------
# arp -a から MAC アドレス一覧を取得
# -----------------------------------
def get_arp_table():
    print("[INFO] ARP テーブルを取得中...")
    result = subprocess.run(
        ["arp", "-a"],
        capture_output=True,
        text=True,
        encoding="shift_jis",  # 日本語Windows想定
        errors="ignore"
    )
    output = result.stdout

    # 例:  192.168.1.5       00-11-22-33-44-55     動的
    pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F\-]{17})")
    devices = []
    for match in pattern.finditer(output):
        ip = match.group(1)
        mac = match.group(2).upper()
        devices.append((ip, mac))
    return devices

# -----------------------------------
# メイン処理
# -----------------------------------
def main():
    allowed = load_allowed_macs()
    print("[INFO] 許可済み端末:")
    for mac, name in allowed.items():
        print(f"  {mac} : {name}")

    # サブネットにping
    ping_subnet(SUBNET)

    # ARPテーブル取得
    devices = get_arp_table()

    print("\n[INFO] 現在ネットワーク上で見つかった端末:")
    for ip, mac in devices:
        name = allowed.get(mac, "UNKNOWN")
        print(f"  {ip:15} {mac:17}  ({name})")

    # 不審端末の検出
    unknowns = [(ip, mac) for ip, mac in devices if mac not in allowed]

    if unknowns:
        print("\n[ALERT] 許可していない端末が検出されました！")
        for ip, mac in unknowns:
            print(f"  {ip:15} {mac}")
        # ここでメール送信やLINE Notify, Slackなどに通知してもOK
    else:
        print("\n[OK] 不審な端末は検出されませんでした。")

if __name__ == "__main__":
    main()
