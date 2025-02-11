    #デフォルト
python model.py
uvicorn main:app --reload
streamlit run ui.py
    #介護st
python model.py
uvicorn main:app --host 0.0.0.0 --port 8000   
streamlit run ui.py
    #介護pulm_ver0
python model.py
uvicorn main:app --host 0.0.0.0 --port 8001
streamlit run ui.py

#Dockerイメージを作成
docker build -t my-fastapi-streamlit-app .
#Dockerコンテナを起動
docker run -p 8000:8000 -p 8501:8501 my-fastapi-streamlit-app
#docker-compose を使う場合
docker-compose up -d
#docker-compose を使って、終了する場合
docker-compose down
#コンテナ起動後、以下のURLにアクセスしてアプリが動作するか確認する
FastAPI（バックエンド）: http://localhost:8000
Streamlit（フロントエンド）: http://localhost:8501

# フォントを変える
st.markdown("<h1 style='font-size:24px; color:blue;'>推論結果</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='font-size:20px; color:blue;'>推論結果</h2>", unsafe_allow_html=True)
# 1マスずらす
st.markdown("<div style='margin-left: 20px;'>このテキストは右にずれています。</div>", unsafe_allow_html=True)
