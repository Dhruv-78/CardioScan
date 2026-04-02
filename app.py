from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)
model_path = os.path.join(os.path.dirname(__file__), "Utils/model.pkl")
model = pickle.load(open(model_path, "rb"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    le_sex = pickle.load(open('Utils/label_encoder_sex.pkl', 'rb'))
    le_cpt = pickle.load(open('Utils/label_encoder_cpt.pkl', 'rb'))
    le_ecg = pickle.load(open('Utils/label_encoder_restecg.pkl', 'rb'))
    le_ea = pickle.load(open('Utils/label_encoder_exang.pkl', 'rb'))
    le_st = pickle.load(open('Utils/label_encoder_st_slope.pkl', 'rb'))
    scaler = pickle.load(open('Utils/scaler.pkl', 'rb'))
    pca = pickle.load(open('Utils/pca.pkl', 'rb'))
    model = pickle.load(open('Utils/model.pkl', 'rb'))
    d = request.form
    row = [x for x in d.values()]
    print("------------------------------")
    print(row)
    row['Sex'] = le_sex.transform(row['Sex'])
    row['ChestPainType'] = le_cpt.transform(row['ChestPainType'])
    row['RestingECG']    = le_ecg.transform(row['RestingECG'])
    row['ExerciseAngina']= le_ea.transform(row['ExerciseAngina'])
    row['ST_Slope']      = le_st.transform(row['ST_Slope'])
    x = pca.transform(scaler.transform(row))

    score = float(model.predict_proba(x)[0][1])
    return {"score": score}

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)