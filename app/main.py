from distutils.command.upload import upload
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from pathlib import Path
import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras import Sequential
from keras.layers import Flatten, Activation
from keras.utils import to_categorical
from pathlib import Path
import keras.backend as K

import matplotlib.pyplot as plt
import cv2
import numpy as np
import pickle
import random
import sys
from preprocessing import grayscale
from ndvi import ndvi
import predict_desease
from color_mask import affected_region
app = Flask(__name__)

Root_path = (Path(os.getcwd()))

UPLOAD_FOLDER = 'app/static/uploads/'
global image
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 256 * 256
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

upload_img =os.path.join(Root_path/app.config['UPLOAD_FOLDER'] )

# gray_path = Path(os.getcwd()+"/app/static/preprocessing_img")
# d = os.listdir(upload_img)
# img = cv2.imread(os.path.join(upload_img,d[0]))
# new_img = os.path.join(gray_path , 'image.jpg')
# cv2.imwrite(new_img, img)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reset',methods=['POST'])
def reset():
    if request.method == "POST":
         if request.form['reset'] == 'Reset':
           
            return redirect(url_for('home'))

@app.route('/success/<leaf_status>')
def success(leaf_status,filename):
    step =2
    return render_template('index.html',leaf_status= leaf_status,step = step)

@app.route('/', methods=['POST'])
def upload_image():
  
    if 'file' not in request.files:
        print('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
   
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
       
        for i in os.listdir(upload_img):
            os.remove(upload_img+'/'+i)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # print('upload_image filename: ' + filename)
        # flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename,step = 0)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')  
        return redirect(request.url)
 


@app.route('/display/<filename>',methods = ["POST","GET"])
def display_img(filename):
    # print('111 display_image filename: ' + filename)
    return redirect(url_for('static',filename='uploads/' + filename), code=301)



@app.route('/leaf_predict/',methods=['POST','GET'])
def predict():
    leaf_status = ''
    if request.method == "POST":
        if request.form['Predict_desease'] == 'Predict':
            
            leaf_status, accuracy = predict_desease.predict(upload_img)
       
        
    # return render_template('index.html', leaf_status=leaf_status, step=2)
    return render_template('index.html',filename = 'Grayscale.jpg',step=2, leaf_status = leaf_status, accuracy =accuracy)



@app.route('/preprocessing',methods=['POST','GET'])
def preprocessing():

    if request.method == "POST":
         if request.form['Preprocess'] == 'Preprocess':
            gray_img  = grayscale(upload_img)
           
            
            img = os.path.join(upload_img , 'Grayscale.jpg')
           
            cv2.imwrite(img, gray_img)

    return render_template('index.html',filename = 'Grayscale.jpg',step=1)

@app.route('/veg_index',methods=['POST','GET'])
def veg_index():

    if request.method == "POST":
         if request.form['v_index'] == 'veg_index/NDVI':
            fig,extent =  ndvi(upload_img)
            output_name = upload_img+'/InfraBl.jpg'
            fig.savefig(output_name, dpi=600, transparent=True, bbox_inches=extent, pad_inches=0)

    return render_template('index.html',filename = 'InfraBl.jpg',step=3)

@app.route('/segmentation',methods=['POST','GET'])
def segment():
    if request.method == "POST":
         if request.form['segmentation'] == 'Segmentation':
            result,percent =  affected_region(upload_img)
            cv2.imwrite(os.path.join(upload_img ,"affected_reg.jpg"),result)

    return render_template('index.html',filename ='affected_reg.jpg',step=4,percent = percent)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)