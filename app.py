from flask import Flask, jsonify, request, render_template
import numpy as np
import joblib
import pandas as pd

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    le_sex = joblib.load('Utils/label_encoder_sex.pkl')
    le_cpt = joblib.load('Utils/label_encoder_cpt.pkl')
    le_ecg = joblib.load('Utils/label_encoder_restecg.pkl')
    le_ea = joblib.load('Utils/label_encoder_exang.pkl')
    le_st = joblib.load('Utils/label_encoder_st_slope.pkl')
    scaler = joblib.load('Utils/scaler.pkl')
    pca = joblib.load('Utils/pca.pkl')
    model = joblib.load('Utils/model.pkl')
    d = request.json
    row = pd.DataFrame([d])
    print("------------------------------")
    print(row)
    row['Sex'] = le_sex.transform(row['Sex'])
    row['ChestPainType'] = le_cpt.transform(row['ChestPainType'])
    row['RestingECG']    = le_ecg.transform(row['RestingECG'])
    row['ExerciseAngina']= le_ea.transform(row['ExerciseAngina'])
    row['ST_Slope']      = le_st.transform(row['ST_Slope'])
    x = pca.transform(scaler.transform(row))

    score = float(model.predict_proba(x)[0][1])
    return jsonify({"score": score})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)