# Importing the packages
from flask import Flask, jsonify, render_template, request

from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Initializing the app
app = Flask(__name__)

def img_preprocess(image):
    image = image.resize((28,28))
    im2arr = np.array(image)
    im2arr = im2arr.reshape(1,28,28,1)
    if (im2arr[0][0][0][0]>=170):
        im2arr = im2arr - 255
    return im2arr

# Routing
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/recog',methods=['GET', 'POST'])
def get_recog():
    if request.method == 'GET':
        return render_template('index6.html')
    elif request.method == 'POST':
        try:
            img = Image.open(request.files['img'].stream).convert("L")
            img = img_preprocess(img)
            model = load_model("./models/IBM_mnistCNN.h5")
            pred = model.predict(img)
            val = str(np.argmax(pred, axis=1)[0])
            data = {'num': val, 'prob': int(pred[0][int(val)]*100)}
            print(pred)
        except Exception as e:
            print(e)
            val = 'Invalid Input'
        return jsonify(data)
    else:
        return 'Unknown Request'

# Main 
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=5121, debug=True) 




