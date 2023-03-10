import pickle
from flask import Flask,request,app,jsonify,url_for,render_template
import numpy as np
import pandas as pd

app=Flask(__name__)

## Load Model
regmodel=pickle.load(open('regmodel.pkl','rb'))
scaler=pickle.load(open('scaler.pkl','rb'))

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.json['data']
    new_data = scaler.transform(np.array(list(data.values())).reshape(1,-1))
    output = regmodel.predict(new_data)
    print(output[0])
    return jsonify(output[0])

@app.route('/predict',methods=['GET','POST'])
def predict() :
    if request.method == 'GET':
        return render_template('Home.html',prediction_text='Fill above form to predict price of the house')
    else:    
        data = [float(x) for x in request.form.values()]
        final_input = scaler.transform(np.array(data).reshape(1,-1))
        output = regmodel.predict(final_input)[0]
        return render_template('Home.html',prediction_text="The predicted house price is = {}".format(output))

if __name__ == '__main__':
    app.run(debug=True)