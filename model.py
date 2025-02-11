import pickle

# 保存したモデルを読み込む
model_outcome_e = pickle.load(open('pulmoutcome_e_rf_model.pkl', 'rb'))
model_hospitalstay_e = pickle.load(open('pulmhospitalstay_e_rf_model.pkl', 'rb'))
model_nursingcare_apply_e = pickle.load(open('pulmnursingcare_apply_e_rf_model.pkl', 'rb'))

# モデルを辞書にまとめる
models = {
    'outcome_e': model_outcome_e,
    'hospitalstay_e': model_hospitalstay_e,
    'nursingcare_e': model_nursingcare_apply_e,
}

