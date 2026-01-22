from application import app
from flask import render_template, request, flash
from flask_cors import CORS, cross_origin
from PIL import Image, ImageOps
import re
import base64
import numpy as np
import requests


### TODO: Change this base URL to your model server URL
model_server_base_url = "https://<your render url>.onrender.com"


url = f'{model_server_base_url}/v1/models/digit_classifier:predict'


def parseImage(imgData):
    # parse canvas bytes and save as output.png
    imgstr = re.search(b'base64,(.*)', imgData).group(1)
    with open('output.png','wb') as output:
        output.write(base64.decodebytes(imgstr))
    im = Image.open('output.png').convert('RGB')
    im_invert = ImageOps.invert(im)
    im_invert.save('output.png')

def make_prediction(instances):
    data = {"signature_name": "serving_default", "instances": instances.tolist()}
    response = requests.post(url, json=data)
    print(response.status_code)
    response_dict = response.json()
    print(response_dict)
    predictions = response_dict['predictions']
    return predictions




@app.route('/') 
@app.route('/index') 
@app.route('/home') 
def index_page(): 
    return render_template('index.html')


@app.route("/predict", methods=['GET','POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def predict():
    # get data from drawing canvas and save as image
    parseImage(request.get_data())

    # Decoding and pre-processing base64 image. Can you think of a better way to do this?
    # This line can cause bugs under certain circumstances. Can you imagine when?
    # If so, how can you fix it?
    img = Image.open("output.png").convert("L").resize((28, 28))
    # Convert to NumPy array and normalize to [0, 1]
    img = np.array(img).astype('float32') / 255.0
    # reshape data to have a single channel
    img = img.reshape(1,28,28,1)

    predictions = make_prediction(img)

    ret = ""
    for i, pred in enumerate(predictions):
        ret = "{}".format(np.argmax(pred))
        response = ret
        return response
