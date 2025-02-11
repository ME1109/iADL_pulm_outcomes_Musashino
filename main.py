import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import ipywidgets as widgets
from IPython.display import display
from model import models  # model.pyからモデルをインポート

# インスタンス化
app = FastAPI()

# 入力データの型を定義
class InputData(BaseModel):
    男_1: int
    年齢群: int
    食事: int
    移乗: int
    整容: int
    トイレ動作: int
    入浴: int
    平地歩行: int
    階段: int
    更衣: int
    排便管理: int
    排尿管理: int
    認知症自立度: int
    介護_取得済: int
    介護_未取得: int
    介護_対象外: int
    予定外_1: int
    病名_喘息COPD: int
    病名_腫瘍: int
    病名_隔離感染症: int
    病名_肺炎: int
    病名_胸膜疾患: int
    病名_IP: int
    病名_その他: int

# トップページ
@app.get('/')
async def index():
    return {"message": "日常生活動作で入院日数や転帰を予測するアプリです"}

# POSTが送信された時（入力）と予測値（出力）の定義
@app.post('/make_predictions')
async def make_predictions(data: InputData):
    input_data = np.array([[data.男_1, data.年齢群, data.食事, data.移乗, data.整容, data.トイレ動作, data.入浴, data.平地歩行, data.階段, data.更衣, data.排便管理, data.排尿管理, data.認知症自立度,
                            data.介護_取得済, data.介護_未取得, data.介護_対象外, data.予定外_1, data.病名_喘息COPD, data.病名_腫瘍, data.病名_隔離感染症, data.病名_肺炎, data.病名_胸膜疾患, data.病名_IP, data.病名_その他]])

    prediction_outcome = models['outcome_e'].predict(input_data)
    probabilities_outcome = models['outcome_e'].predict_proba(input_data)
    prediction_hospitalstay = models['hospitalstay_e'].predict(input_data)
    probabilities_hospitalstay = models['hospitalstay_e'].predict_proba(input_data)
    
    input_data_2 = np.array([[data.男_1, data.年齢群, data.食事, data.移乗, data.整容, data.トイレ動作, data.入浴, data.平地歩行, data.階段, data.更衣, data.排便管理, data.排尿管理, data.認知症自立度,
                            data.予定外_1, data.病名_喘息COPD, data.病名_腫瘍, data.病名_隔離感染症, data.病名_肺炎, data.病名_胸膜疾患, data.病名_IP, data.病名_その他]])

    prediction_nursingcare = models['nursingcare_e'].predict(input_data_2)
    probabilities_nursingcare = models['nursingcare_e'].predict_proba(input_data_2)
    
    return {
        "予想される退院経路": {
            "死亡の確率": f"{probabilities_outcome[0][0] * 100:.1f}%",
            "転院の確率": f"{probabilities_outcome[0][1] * 100:.1f}%"
#            "通常退院の確率": f"{probabilities_outcome[0][2] * 100:.1f}%"
        },
        "予想される入院期間": {
            "1週間以内の確率": f"{probabilities_hospitalstay[0][0] * 100:.1f}%",
            "1-2週間の確率": f"{probabilities_hospitalstay[0][1] * 100:.1f}%",
            "2-3週間の確率": f"{probabilities_hospitalstay[0][2] * 100:.1f}%",
            "1-3週間の確率": f"{(probabilities_hospitalstay[0][1] + probabilities_hospitalstay[0][2]) * 100:.1f}%",
            "3週間以上の確率": f"{probabilities_hospitalstay[0][3] * 100:.1f}%"
        },
        "介護申請の必要性(判定1)": {
            "判定": "必要です" if (probabilities_outcome[0][1] * 100 >= 10 or (probabilities_hospitalstay[0][2] * 100 + probabilities_hospitalstay[0][3] * 100) >= 20) and (data.介護_未取得 == 1) else "まだしなくて良い" if data.介護_未取得 == 1 else "取得済みです(地域包括支援センターに有事相談できます)"
        },
        "介護申請の必要性(判定2)": {
#            "介護申請は不要な確率": f"{probabilities_nursingcare[0][0] * 100:.1f}%",
            "介護申請が必要な確率": f"{probabilities_nursingcare[0][1] * 100:.1f}%",
#            "判定": "必要です" if (prediction_nursingcare[0] == 1) else "まだしなくて良い" if data.介護_未取得 == 1 else "取得済みです(地域包括支援センターに有事相談できます)"
            "判定": "必要です" if probabilities_nursingcare[0][1] >= 30 else "まだしなくて良い" if data.介護_未取得 == 1 else "取得済みです(地域包括支援センターに有事相談できます)"
        }
    }
 
# FastAPIを起動する
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
