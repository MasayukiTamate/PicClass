import os
import requests
import time

# 保存フォルダの作成
SAVE_DIR = "random_samples"
os.makedirs(SAVE_DIR, exist_ok=True)

# ダウンロードしたい枚数
COUNT = 50 
# 画像サイズ（幅, 高さ）
WIDTH, HEIGHT = 400, 300 

print(f"{COUNT}枚の画像をランダムにダウンロードします...")

for i in range(1, COUNT + 1):
    # randomパラメータを付けることで、毎回違う画像を取得できます
    url = f"https://picsum.photos/{WIDTH}/{HEIGHT}?random={i}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            filename = f"sample_{i:03d}.jpg"
            with open(os.path.join(SAVE_DIR, filename), 'wb') as f:
                f.write(response.content)
            print(f"[{i}/{COUNT}] 保存完了: {filename}")
        
        # サーバーに負荷をかけないよう、少しだけ待機（マナー）
        time.sleep(0.1)
        
    except Exception as e:
        print(f"[{i}] 失敗: {e}")

print(f"\n完了！ '{SAVE_DIR}' フォルダを確認してください。")