#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template, request

from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# In[2]:


app = Flask(__name__)


# In[3]:


@app.route('/')
def home():
    return render_template('main.html')


# In[4]:

def img_preprocess(image):
    image = image.resize((28,28))
    im2arr = np.array(image)
    im2arr = im2arr.reshape(1,28,28,1)
    if (im2arr[0][0][0][0]>=170):
        im2arr = im2arr - 255
    return im2arr

@app.route('/recog',methods=['GET', 'POST'])
def get_recog():
    if request.method == 'GET':
        return render_template('index6.html')
    elif request.method == 'POST':
        try:
            img = Image.open(request.files['img'].stream).convert("L")
            img = img_preprocess(img)
            model = load_model("./models/mnistCNN.h5")
            pred = model.predict(img)
            val = str(np.argmax(pred, axis=1)[0])
            print(pred)
            print(round(pred[0][0]))
        except :
            
            val = 'Invalid Input'
        return val
    else:
        return 'Unknown Request'


# In[ ]:


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=5121, debug=True) 


# In[ ]:




