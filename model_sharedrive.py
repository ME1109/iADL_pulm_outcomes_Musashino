import pickle
import requests
import os

# Googleドライブのリンクからファイルをダウンロードする関数（大容量ファイル対応）
def download_file_from_google_drive(file_id, destination):
    session = requests.Session()
    base_url = "https://docs.google.com/uc?export=download"

    response = session.get(base_url, params={'id': file_id}, stream=True)
    
    # Google Drive は100MB超のファイルに対して確認トークンを要求することがある
    confirm_token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            confirm_token = value

    # 確認トークンが必要な場合、再度リクエストを送る
    if confirm_token:
        response = session.get(base_url, params={'id': file_id, 'confirm': confirm_token}, stream=True)

    save_response_content(response, destination)

def save_response_content(response, destination):
    CHUNK_SIZE = 32768  # 32KB のチャンクサイズで保存
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

# ファイルIDの辞書を定義
file_ids = {
    'outcome_e': '1N8kIscQhXREu7oY_kEJ2AgpJ5IvJPzxI',
    'hospitalstay_e': '1Yb-SEEll5vvq0_wLjDRFLtZ-oPucBOdr',
    'nursingcare_e': '1NN2JEFQz9u9fZdkVNteKEBVyQ2QPwvwK',
}

# 各ファイルをダウンロード
for name, file_id in file_ids.items():
    destination = f'{name}_rf_model.pkl'
    if not os.path.exists(destination) or os.path.getsize(destination) == 0:
        print(f"🔽 {destination} をダウンロードしています...")
        download_file_from_google_drive(file_id, destination)
    else:
        print(f"✅ {destination} は既に存在します。")

# 保存したモデルを読み込む
models = {}

for name in file_ids.keys():
    filename = f"{name}_rf_model.pkl"
    try:
        with open(filename, 'rb') as f:
            models[name] = pickle.load(f)
        print(f"✅ {filename} の読み込みに成功しました。")
    except Exception as e:
        print(f"❌ {filename} の読み込みに失敗しました: {e}")

# モデルの読み込み結果をチェック
if len(models) != len(file_ids):
    print("⚠️ いくつかのモデルが正しく読み込めませんでした。ファイルを確認してください。")
