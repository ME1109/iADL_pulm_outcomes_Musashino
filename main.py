import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
import pickle
from model import models  # model.pyからモデルをインポート

# Streamlitのページ設定
st.set_page_config(layout="wide")
st.title("日常生活動作で入院日数や転帰を予測するアプリ")

# 入力フォームの定義
def user_input_features():
    st.sidebar.header("入力データ")
    男_1 = st.sidebar.selectbox('性別', [1, 0])
    年齢群 = st.sidebar.slider('年齢群', 0, 10, 5)
    食事 = st.sidebar.slider('食事', 0, 2, 1)
    移乗 = st.sidebar.slider('移乗', 0, 3, 1)
    整容 = st.sidebar.slider('整容', 0, 2, 1)
    トイレ動作 = st.sidebar.slider('トイレ動作', 0, 3, 1)
    入浴 = st.sidebar.slider('入浴', 0, 2, 1)
    平地歩行 = st.sidebar.slider('平地歩行', 0, 3, 1)
    階段 = st.sidebar.slider('階段', 0, 2, 1)
    更衣 = st.sidebar.slider('更衣', 0, 2, 1)
    排便管理 = st.sidebar.slider('排便管理', 0, 3, 1)
    排尿管理 = st.sidebar.slider('排尿管理', 0, 3, 1)
    認知症自立度 = st.sidebar.slider('認知症自立度', 0, 3, 1)
    介護_取得済 = st.sidebar.selectbox('介護取得済', [1, 0])
    介護_未取得 = st.sidebar.selectbox('介護未取得', [1, 0])
    介護_対象外 = st.sidebar.selectbox('介護対象外', [1, 0])
    予定外_1 = st.sidebar.selectbox('予定外', [1, 0])
    病名_喘息COPD = st.sidebar.selectbox('喘息COPD', [1, 0])
    病名_腫瘍 = st.sidebar.selectbox('腫瘍', [1, 0])
    病名_隔離感染症 = st.sidebar.selectbox('隔離感染症', [1, 0])
    病名_肺炎 = st.sidebar.selectbox('肺炎', [1, 0])
    病名_胸膜疾患 = st.sidebar.selectbox('胸膜疾患', [1, 0])
    病名_IP = st.sidebar.selectbox('IP', [1, 0])
    病名_その他 = st.sidebar.selectbox('その他', [1, 0])

    data = {
        '男_1': 男_1,
        '年齢群': 年齢群,
        '食事': 食事,
        '移乗': 移乗,
        '整容': 整容,
        'トイレ動作': トイレ動作,
        '入浴': 入浴,
        '平地歩行': 平地歩行,
        '階段': 階段,
        '更衣': 更衣,
        '排便管理': 排便管理,
        '排尿管理': 排尿管理,
        '認知症自立度': 認知症自立度,
        '介護_取得済': 介護_取得済,
        '介護_未取得': 介護_未取得,
        '介護_対象外': 介護_対象外,
        '予定外_1': 予定外_1,
        '病名_喘息COPD': 病名_喘息COPD,
        '病名_腫瘍': 病名_腫瘍,
        '病名_隔離感染症': 病名_隔離感染症,
        '病名_肺炎': 病名_肺炎,
        '病名_胸膜疾患': 病名_胸膜疾患,
        '病名_IP': 病名_IP,
        '病名_その他': 病名_その他
    }
    
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# 予測を実行するボタン
if st.sidebar.button("予測を実行"):
    input_data = input_df.values
    prediction_outcome = models['outcome_e'].predict(input_data)
    probabilities_outcome = models['outcome_e'].predict_proba(input_data)
    prediction_hospitalstay = models['hospitalstay_e'].predict(input_data)
    probabilities_hospitalstay = models['hospitalstay_e'].predict_proba(input_data)
    
    input_data_2 = input_df.drop(columns=['介護_取得済', '介護_未取得', '介護_対象外']).values
    prediction_nursingcare = models['nursingcare_e'].predict(input_data_2)
    probabilities_nursingcare = models['nursingcare_e'].predict_proba(input_data_2)

    st.subheader("予想される退院経路")
    st.write(f"死亡の確率: {probabilities_outcome[0][0] * 100:.1f}%")
    st.write(f"転院の確率: {probabilities_outcome[0][1] * 100:.1f}%")
#    st.write(f"通常退院の確率: {probabilities_outcome[0][2] * 100:.1f}%")

    st.subheader("予想される入院期間")
    st.write(f"1週間以内の確率: {probabilities_hospitalstay[0][0] * 100:.1f}%")
    st.write(f"1-2週間の確率: {probabilities_hospitalstay[0][1] * 100:.1f}%")
    st.write(f"2-3週間の確率: {probabilities_hospitalstay[0][2] * 100:.1f}%")
    st.write(f"1-3週間の確率: {(probabilities_hospitalstay[0][1] + probabilities_hospitalstay[0][2]) * 100:.1f}%")
    st.write(f"3週間以上の確率: {probabilities_hospitalstay[0][3] * 100:.1f}%")

    st.subheader("介護申請の必要性(判定1)")
    判定1 = "必要です" if (probabilities_outcome[0][1] * 100 >= 10 or (probabilities_hospitalstay[0][2] * 100 + probabilities_hospitalstay[0][3] * 100) >= 20) and (input_df['介護_未取得'].values[0] == 1) else "まだしなくて良い" if input_df['介護_未取得'].values[0] == 1 else "取得済みです(地域包括支援センターに有事相談できます)"
    st.write(f"判定1: {判定1}")

    st.subheader("介護申請の必要性(判定2)")
    st.write(f"介護申請が必要な確率: {probabilities_nursingcare[0][1] * 100:.1f}%")
    判定2 = "必要です" if probabilities_nursingcare[0][1] >= 30 else "まだしなくて良い" if input_df['介護_未取得'].values[0] == 1 else "取得済みです(地域包括支援センターに有事相談できます)"
    st.write(f"判定2: {判定2}")
